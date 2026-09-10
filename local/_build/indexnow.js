#!/usr/bin/env node
/* ===========================================================
   IndexNow ping
   -----------------------------------------------------------
   Tells Bing, Yandex, Naver and Seznam which URLs changed, so they
   recrawl within hours instead of whenever they get round to it.
   Bing's index is what Copilot and ChatGPT search read from, so this
   is the fastest lever the site has on the AI-answer side. Google
   does not take IndexNow; it reads sitemap.xml <lastmod> instead.

   The key file at the repo root proves domain ownership; it was
   added 2026-08-10 and must stay published.

   Run from the repo root AFTER the deploy has propagated:
     node local/_build/indexnow.js              # every URL in sitemap.xml
     node local/_build/indexnow.js <url> <url>  # just these
   Exit 0 on HTTP 200/202 (accepted), 1 otherwise.
   =========================================================== */

'use strict';

const fs   = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..', '..');
const HOST = 'perseidechocreations.com';
const KEY  = 'b0ce40fac5dd48c3b1620409104466fa8fd3a38667a9471db016afd4cd50c453';

const args = process.argv.slice(2);
const sitemap = fs.readFileSync(path.join(ROOT, 'sitemap.xml'), 'utf8');
const urls = args.length
  ? args
  : [...sitemap.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m => m[1]);

(async () => {
  const body = { host: HOST, key: KEY, keyLocation: `https://${HOST}/${KEY}.txt`, urlList: urls };
  const res = await fetch('https://api.indexnow.org/IndexNow', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
    body: JSON.stringify(body)
  });
  const text = await res.text();
  const ok = res.status === 200 || res.status === 202;
  console.log(`IndexNow ${new Date().toISOString()}: HTTP ${res.status} ${ok ? 'accepted' : 'REJECTED'} for ${urls.length} URLs`);
  if (text) console.log(text);
  urls.forEach(u => console.log('  ' + u));
  process.exit(ok ? 0 : 1);
})().catch(e => { console.error('IndexNow failed:', e.message); process.exit(1); });
