// POST /api/claim — record a storefront claim from sites.perseidechocreations.com.
//
// Cloudflare Pages Function. Deployed with the static page (lives in the deploy
// root's functions/ dir → same origin, so the page's fetch('/api/claim') has no
// CORS hop). A successful store is the build trigger for the autonomous pipeline
// (project #2, "Hermes"): the record carries status:"claimed", source:"storefront".
//
// Required binding: KV namespace `CLAIMS` (reuses the same store as dotsites
// so storefront leads and placeholder claims live together).

export async function onRequestPost({ request, env }) {
  let body;
  try {
    body = await request.json();
  } catch {
    return json({ ok: false, error: "bad json" }, 400);
  }

  // Honeypot: bots fill the hidden `company` field. Pretend success, store nothing.
  if (str(body.company)) return json({ ok: true });

  const business_name = str(body.business_name);
  const email = str(body.email);
  if (!business_name || !email || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) {
    return json({ ok: false, error: "business name and a valid email are required" }, 422);
  }
  if (!env.CLAIMS) return json({ ok: false, error: "claim store not configured" }, 500);

  const claim = {
    source: str(body.source) || "storefront",
    status: "claimed",
    business_name,
    email,
    phone: str(body.phone),
    ts: new Date().toISOString(),
    ua: (request.headers.get("user-agent") || "").slice(0, 300),
    ip: request.headers.get("cf-connecting-ip") || ""
  };

  // Slug from the business name keeps keys readable; ts preserves repeat claims.
  const slug = business_name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-+|-+$/g, "").slice(0, 60) || "claim";
  const key = `claim:storefront:${slug}:${claim.ts}`;
  // Auto-expire after 120 days so IP/UA (PII collected for abuse prevention) aren't kept forever.
  await env.CLAIMS.put(key, JSON.stringify(claim), { expirationTtl: 60 * 60 * 24 * 120 });
  return json({ ok: true });
}

export function onRequestOptions() {
  return cors(new Response(null, { status: 204 }));
}

function str(v) {
  return (v == null ? "" : String(v)).trim().slice(0, 500);
}

function json(obj, status = 200) {
  return cors(new Response(JSON.stringify(obj), {
    status,
    headers: { "content-type": "application/json" }
  }));
}

function cors(res) {
  res.headers.set("access-control-allow-origin", "*");
  res.headers.set("access-control-allow-methods", "POST,OPTIONS");
  res.headers.set("access-control-allow-headers", "content-type");
  return res;
}
