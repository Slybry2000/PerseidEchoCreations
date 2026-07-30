// ─── site events (content_pipe) ──────────────────────────────────────────────
//
// Anonymous funnel measurement for perseidechocreations.com. Exists to answer
// one question the old "it posted, nothing happened" loop could never answer:
// does the organic content actually cause Fit Checks to start and finish?
//
// Why it lives HERE, of all places: Caddy already terminates TLS for
// approve.perseidechocreations.com and rewrites every path onto this app's
// /pipe/share subtree. sudo is not passwordless on the box, so a new vhost or
// a new TLS cert was not available. Riding the existing rewrite means the
// public write endpoint is:
//
//     POST https://approve.perseidechocreations.com/_e   ->  /pipe/share/_e
//
// The READ side is deliberately NOT on that path, so it is not reachable
// through the public vhost — /pipe/api/* is localhost + tailnet only.
//
// Privacy contract (this file IS the implementation of the published policy at
// perseidechocreations.com/privacy.html — change one, change the other):
//   - No IP address is ever written to disk. A transient in-memory bucket
//     hashes the address for per-minute abuse limiting and forgets it; nothing
//     derived from it is persisted.
//   - No cookies. The session id arrives from the page, is generated per visit,
//     and dies with the tab.
//   - Every field is whitelisted or clamped. Nothing free-text is stored.
//   - Do Not Track / Global Privacy Control are honoured in the PAGE, before a
//     request is made, so an opted-out visitor never reaches this file.
//
// Storage: data/_state/site-events/YYYY-MM.jsonl, one JSON object per line.
// Monthly files make the 12-month retention promise a matter of deleting old
// files rather than rewriting a database.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, "..");
const DATA_ROOT = process.env.CP_DATA_DIR ? path.resolve(process.env.CP_DATA_DIR) : path.join(ROOT, "data");
const EVENT_DIR = path.join(DATA_ROOT, "_state", "site-events");

// Only these origins may post. Anything else is dropped without a write.
const ALLOWED_ORIGINS = new Set([
  "https://perseidechocreations.com",
  "https://www.perseidechocreations.com",
]);

// The whole vocabulary. An event name outside this list is a bug or an abuse
// attempt; either way it is not worth a disk write.
const EVENTS = new Set([
  "view",             // a page was shown
  "fc_start",         // first Fit Check question answered
  "fc_step",          // a question was answered (carries q)
  "fc_back",          // went back a question
  "fc_done",          // reached a result (carries verdict + category)
  "fc_restart",       // started over
  "fc_email",         // asked for the result by email
  "cta_call",         // clicked through to the booking calendar
  "cta_cost",         // opened pricing
  "cta_partners",     // went to the partner page
  "cta_proof",        // jumped to the proof section
  // Emitted by the local/workflow service pages (local/assets/track.js). Their
  // job is the handoff to the homepage Fit Check, so cta_fitcheck is the click
  // that matters there.
  "cta_fitcheck",     // clicked through to the Fit Check
  "cta_nearby",       // clicked through to another local page
  "cta_email",        // clicked a mailto
]);

const VERDICTS = new Set(["strong", "mid", "low"]);
const CATEGORIES = new Set(["followup", "scheduling", "paperwork", "datasync", "reporting", "comms"]);
const PAGES = new Set(["home", "partners", "privacy"]);
// The service pages identify themselves as "local:<slug>" / "wf:<slug>"
// (window.PEC_PAGE). Recognised by shape rather than by list, so a new city or
// workflow page starts reporting the day it ships with no code change here.
const PAGE_KINDS = ["local", "wf"];
function isServicePage(p) {
  if (typeof p !== "string" || p.length > 70) return false;
  const i = p.indexOf(":");
  if (i < 1) return false;
  if (!PAGE_KINDS.includes(p.slice(0, i))) return false;
  const slug = p.slice(i + 1);
  return slug.length > 0 && slug.replace(/[a-z0-9-]/g, "") === "";
}
const DEVICES = new Set(["m", "d"]);

// ── abuse limiting ──────────────────────────────────────────────────────────
// Per-minute cap per hashed address, plus a global ceiling so a single bad
// actor cannot fill the disk. Both live in memory only.
const RATE_WINDOW_MS = 60_000;
const PER_CLIENT_PER_MIN = 60;
const GLOBAL_PER_MIN = 3000;
const IP_SALT = crypto.randomBytes(16).toString("hex"); // rotates on restart, by design

let windowStart = Date.now();
let globalCount = 0;
const buckets = new Map();

function rateOk(req) {
  const now = Date.now();
  if (now - windowStart > RATE_WINDOW_MS) {
    windowStart = now;
    globalCount = 0;
    buckets.clear();
  }
  if (++globalCount > GLOBAL_PER_MIN) return false;
  const raw = req.headers["x-forwarded-for"] || req.socket?.remoteAddress || "";
  // Hashed immediately and never returned, logged, or written.
  const key = crypto.createHmac("sha256", IP_SALT).update(String(raw)).digest("hex").slice(0, 16);
  const n = (buckets.get(key) || 0) + 1;
  buckets.set(key, n);
  return n <= PER_CLIENT_PER_MIN;
}

// ── field hygiene ───────────────────────────────────────────────────────────
const clean = (v, max) => {
  if (typeof v !== "string") return null;
  const s = v.trim().replace(/[^A-Za-z0-9._\-/ ]/g, "").slice(0, max);
  return s || null;
};

function shape(body) {
  if (!body || typeof body !== "object") return null;
  const e = typeof body.e === "string" ? body.e : "";
  if (!EVENTS.has(e)) return null;

  const out = { t: new Date().toISOString(), e };

  // session: client-generated per visit, alphanumeric, fixed length
  if (typeof body.s === "string" && /^[a-z0-9]{6,16}$/.test(body.s)) out.s = body.s;

  if (PAGES.has(body.p) || isServicePage(body.p)) out.p = body.p;
  if (DEVICES.has(body.d)) out.d = body.d;
  if (VERDICTS.has(body.v)) out.v = body.v;
  if (CATEGORIES.has(body.c)) out.c = body.c;

  const q = Number(body.q);
  if (Number.isInteger(q) && q >= 0 && q <= 10) out.q = q;

  // attribution: where the visit came from. Host only, never a full URL.
  const src = clean(body.src, 40); if (src) out.src = src;
  const cmp = clean(body.cmp, 60); if (cmp) out.cmp = cmp;
  const ref = clean(body.ref, 80); if (ref) out.ref = ref;

  // Referral code from /refer/. Kept in its own field rather than folded into
  // src, because "who introduced them" and "which channel they arrived by" are
  // different questions — a referred visit is still (direct) by source. The
  // code is an opaque token by construction; it never carries a name or email.
  const rc = clean(body.rc, 32); if (rc) out.rc = rc;

  return out;
}

function append(rec) {
  fs.mkdirSync(EVENT_DIR, { recursive: true });
  const file = path.join(EVENT_DIR, rec.t.slice(0, 7) + ".jsonl");
  fs.appendFileSync(file, JSON.stringify(rec) + "\n");
}

// ── read side ───────────────────────────────────────────────────────────────
function readSince(days) {
  const cutoff = Date.now() - days * 86400000;
  const out = [];
  let files = [];
  try { files = fs.readdirSync(EVENT_DIR).filter((f) => f.endsWith(".jsonl")).sort(); } catch { return out; }
  for (const f of files.slice(-14)) {
    let lines = [];
    try { lines = fs.readFileSync(path.join(EVENT_DIR, f), "utf8").split("\n"); } catch { continue; }
    for (const line of lines) {
      if (!line) continue;
      try {
        const r = JSON.parse(line);
        if (Date.parse(r.t) >= cutoff) out.push(r);
      } catch { /* a torn last line is not worth failing the report over */ }
    }
  }
  return out;
}

function summarise(rows) {
  const sessions = new Set();
  const started = new Set();
  const finished = new Set();
  const byEvent = {};
  const verdicts = {};
  const categories = {};
  const reached = {};        // furthest question index per session
  const devices = {};
  const sessionSource = {};  // session -> where that visit came from
  const sessionEntry = {};   // session -> the page that started the visit
  const sessionRefCode = {}; // session -> the referral code that sent them
  const pageViews = {};      // raw views per page

  for (const r of rows) {
    byEvent[r.e] = (byEvent[r.e] || 0) + 1;
    if (r.s) sessions.add(r.s);
    if (r.d) devices[r.d] = (devices[r.d] || 0) + 1;
    // Attribution arrives on the view event; remember it for the whole session
    // so a completion can be credited to the content that caused the visit.
    if (r.s && (r.src || r.ref) && !sessionSource[r.s]) sessionSource[r.s] = r.src || r.ref;
    // Same trick for the referral code: it rides the first event of the visit
    // only, so hold it against the session or the completion cannot be
    // credited to the introduction that caused it.
    if (r.s && r.rc && !sessionRefCode[r.s]) sessionRefCode[r.s] = r.rc;
    if (r.p) {
      pageViews[r.p] = (pageViews[r.p] || 0) + 1;
      // Entry page, not last page: the Fit Check lives on the homepage, so the
      // question worth answering is which page EARNED the visit that finished.
      if (r.s && !sessionEntry[r.s]) sessionEntry[r.s] = r.p;
    }
    if (r.e === "fc_start" && r.s) started.add(r.s);
    if (r.e === "fc_done") {
      if (r.s) finished.add(r.s);
      if (r.v) verdicts[r.v] = (verdicts[r.v] || 0) + 1;
      if (r.c) categories[r.c] = (categories[r.c] || 0) + 1;
    }
    if (r.e === "fc_step" && r.s && typeof r.q === "number") {
      reached[r.s] = Math.max(reached[r.s] ?? -1, r.q);
    }
  }

  // Per-source funnel: the actual question, which is not "how many impressions"
  // but "which piece of content sent someone who then finished a Fit Check".
  const sources = {};
  const bump = (src, key) => {
    const s = src || "(direct)";
    sources[s] = sources[s] || { visits: 0, started: 0, completed: 0 };
    sources[s][key]++;
  };
  for (const s of sessions) bump(sessionSource[s], "visits");
  for (const s of started) bump(sessionSource[s], "started");
  for (const s of finished) bump(sessionSource[s], "completed");

  // Per-referral-code funnel. Only sessions that actually carried a code
  // appear here — there is no "(direct)" bucket, because the absence of a
  // referral is not a referrer and padding this table with it would make the
  // channel look busier than it is.
  const referrals = {};
  const bumpRef = (code, key) => {
    if (!code) return;
    referrals[code] = referrals[code] || { visits: 0, started: 0, completed: 0 };
    referrals[code][key]++;
  };
  for (const s of sessions) bumpRef(sessionRefCode[s], "visits");
  for (const s of started) bumpRef(sessionRefCode[s], "started");
  for (const s of finished) bumpRef(sessionRefCode[s], "completed");

  // How far people get before they quit. The number that tells you whether the
  // questions themselves are the problem.
  const dropoff = [0, 0, 0, 0, 0];
  for (const s of Object.keys(reached)) {
    const far = reached[s];
    for (let i = 0; i <= far && i < dropoff.length; i++) dropoff[i]++;
  }

  // Per-page funnel, same shape as sources: which page a finishing visitor
  // arrived on. A session with no page id lands under "(unknown)".
  const pages = {};
  const bumpPage = (page, key) => {
    const p = page || "(unknown)";
    pages[p] = pages[p] || { visits: 0, started: 0, completed: 0 };
    pages[p][key]++;
  };
  for (const s of sessions) bumpPage(sessionEntry[s], "visits");
  for (const s of started) bumpPage(sessionEntry[s], "started");
  for (const s of finished) bumpPage(sessionEntry[s], "completed");

  const startCount = started.size;
  const doneCount = finished.size;
  return {
    events: rows.length,
    sessions: sessions.size,
    funnel: {
      visits: byEvent.view || 0,
      fitCheckStarted: startCount,
      fitCheckCompleted: doneCount,
      completionRate: startCount ? +(doneCount / startCount * 100).toFixed(1) : null,
      startRate: byEvent.view ? +(startCount / byEvent.view * 100).toFixed(1) : null,
      emailedResult: byEvent.fc_email || 0,
      bookingClicks: byEvent.cta_call || 0,
    },
    reachedQuestion: dropoff,
    verdicts,
    categories,
    sources,
    referrals,
    pages,
    pageViews,
    devices,
    byEvent,
  };
}

export function registerSiteEventRoutes(app, express) {
  // Public write. text/plain so navigator.sendBeacon stays a CORS-simple
  // request (no preflight, and it still fires during page unload).
  const parseText = express.text({ type: ["text/plain", "application/json"], limit: "2kb" });

  app.options("/share/_e", (req, res) => {
    const origin = req.headers.origin;
    if (ALLOWED_ORIGINS.has(origin)) {
      res.set("Access-Control-Allow-Origin", origin);
      res.set("Access-Control-Allow-Headers", "Content-Type");
      res.set("Access-Control-Max-Age", "86400");
    }
    res.sendStatus(204);
  });

  app.post("/share/_e", parseText, (req, res) => {
    const origin = req.headers.origin;
    if (ALLOWED_ORIGINS.has(origin)) res.set("Access-Control-Allow-Origin", origin);

    // Answer first, work second: the page must never wait on this.
    res.sendStatus(204);

    try {
      if (!ALLOWED_ORIGINS.has(origin)) return;
      if (!rateOk(req)) return;
      let body = req.body;
      if (typeof body === "string") { try { body = JSON.parse(body); } catch { return; } }
      const rec = shape(body);
      if (rec) append(rec);
    } catch { /* measurement must never be able to take the server down */ }
  });

  // Read side. Under /api, so the public vhost's /share rewrite cannot reach it.
  app.get("/api/site-events/stats", (req, res) => {
    try {
      const days = Math.min(365, Math.max(1, parseInt(req.query.days, 10) || 30));
      res.json({ days, ...summarise(readSince(days)) });
    } catch (e) {
      res.status(500).json({ error: e.message });
    }
  });

  app.get("/api/site-events/raw", (req, res) => {
    try {
      const days = Math.min(90, Math.max(1, parseInt(req.query.days, 10) || 7));
      const rows = readSince(days);
      res.json({ days, count: rows.length, rows: rows.slice(-500) });
    } catch (e) {
      res.status(500).json({ error: e.message });
    }
  });
}

export default { registerSiteEventRoutes };
