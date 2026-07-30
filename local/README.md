# Local service pages

Built and shipped 2026-07-30. **Live** at `perseidechocreations.com/local/`. Rollback tag: `pec-pre-local-2026-07-30`.

> **GitHub Pages runs Jekyll, and Jekyll silently refuses to serve any directory whose name starts with `_`.** The first deploy shipped the stylesheet at `/local/_assets/local.css`, which 404'd in production while working perfectly on the local server — the pages were live and completely unstyled. Assets now live at `local/assets/`. `_build/` keeps its underscore deliberately: the generator should not be served, and Jekyll excluding it is the mechanism. **Never put a runtime asset under a `_`-prefixed path in this repo, and always check a real production URL after deploying — a passing local server proves nothing about this failure mode.**

## What this is

Six city pages plus a hub, aimed at the one traffic source that arrives already wanting what PEC sells: somebody in south or east King County searching for workflow or process automation help.

```
/local/                                        the hub
/local/workflow-automation-renton-wa/          home city, priority 0.9
/local/workflow-automation-kent-wa/
/local/workflow-automation-bellevue-wa/
/local/workflow-automation-tukwila-wa/
/local/workflow-automation-auburn-wa/
/local/workflow-automation-issaquah-wa/
```

## Why six pages and not sixty

The SERP for these terms was checked on 2026-07-29 before anything was written. It is almost entirely **programmatic location-page farms** — `drive-insight.com/servicelocationpage?service=process-automation&location=renton-wa`, `pointwake.com/locations/washington/auburn`, `hummingagent.ai/locations/washington/auburn`, `codewcg.com/locations/washington/bellevue-wa/woodinville/ai-automations/`, several with out-of-state phone numbers. Nobody genuinely local holds these terms.

That is the opportunity and also the trap. The farms are beatable because they are thin and not actually local. Copying their tactic at smaller scale loses on both counts, and a pile of near-identical city pages is the textbook doorway-page pattern Google devalues.

So the rule for this directory is: **a city only gets a page if there is something true and specific to say about the businesses there.** Renton is Boeing supply chain plus owner-led trades. Kent is the warehouse valley. Bellevue is professional practices. Tukwila is multi-site retail and hospitality. Auburn is field service. Issaquah is appointment-driven owner-led businesses. Each page's "what the work looks like here" and "where I would look first" sections come out of that difference. If you cannot write those two sections honestly for a new city, do not add the city.

The shared trunk — the staircase, the control settings, the proof section, the FAQ — is deliberately identical everywhere. That is not duplication to hide; it is the offer, and it should read the same wherever a visitor lands.

## How to add or change a city

Everything lives in `_build/`:

- `_build/cities.json` — the per-city content
- `_build/build.js` — the template and the generator

```bash
node local/_build/build.js
```

Run it from the repo root. It rewrites all seven pages and regenerates `/sitemap.xml`. Do not hand-edit the generated `index.html` files or `sitemap.xml` — the next build silently discards the change.

Root pages in the sitemap (`/`, `/partners.html`, `/privacy.html`) are listed explicitly in `build.js` under `rootPages`. **When the site gains a root page, add it there**, or it disappears from the sitemap on the next build.

## Load-bearing rules

The positioning rules in `../v3/README.md` apply here in full. The ones this directory can most easily break:

1. **Range language only on price.** `$750` for the Map is exact because it is. The build is "from $2,500", "most land between $3,500 and $9,000". Never a quote.
2. **"Workflow Opportunity Map"** by that name. Not an audit, not a blueprint, not an assessment.
3. **"Do not automate this yet" stays a possible outcome** and gets said out loud on every page. It is the strongest trust signal PEC has, and on a page arriving from a cold search it is doing even more work than on the homepage.
4. **No fabricated local proof.** No client names, no "we helped a Kent manufacturer save 20 hours", no review or `aggregateRating` markup. Every page says explicitly that the systems being pointed at are Bryan's own. The moment there is a real, permissioned local result, it can replace that paragraph — and not before.
5. **No absolute data-safety promise.** The Bellevue page comes closest to this territory and answers with a specific list instead of a "yes".
6. **The Fit Check is not duplicated.** All CTAs point at `https://perseidechocreations.com/#fitcheck`. One implementation, on the homepage, already tested end to end. Do not fork it into these pages.

## Structured data

Three JSON-LD blocks per city page: `ProfessionalService`, `BreadcrumbList`, `FAQPage`. The hub carries `CollectionPage`.

`ProfessionalService` rather than `LocalBusiness`, and the address is **city and region only**. There is no published street address and no storefront, so the entity is an area-served practice. Do not add a street address to the markup unless one is also published on the page and on the Google Business Profile — mismatched addresses across those three surfaces is a real local-ranking problem.

Deliberately absent: `aggregateRating`, `review`, `telephone`. Nothing real to put in them yet. `telephone` should be added to `build.js` the moment there is a business number, because the map pack cares.

## Measurement

Each page sets `window.PEC_PAGE = "local:<slug>"` before loading `assets/track.js`, so the existing funnel at `approve.perseidechocreations.com/_e` can attribute a Fit Check start to the city page that produced it. Same privacy contract as the homepage: opt-out check runs first, no cookies, no third party.

`cta_fitcheck` is the event that matters here — it is the handoff to the homepage, and it is this directory's entire job.

Check it with `ssh bristlecone && fitcheck-stats`.

## Verified 2026-07-29

Headless Chrome, seven pages × three viewports (375 / 768 / 1440):

- No horizontal overflow anywhere
- No console errors and no failed requests, other than a site-wide missing `/favicon.ico` (pre-existing, also affects the homepage)
- Every text/background pair passes WCAG AA. Worst flat pair **4.71:1**, matching the homepage's 4.64:1 floor
- Hero text sits over photography, so it was checked against **composited pixels** rather than CSS colours: the photo is drawn at its actual `cover` position with the `brightness()` filter, both scrim gradients are painted over it, then the brightest pixel inside each text box is measured. Worst **5.68:1**
- One `<h1>` per page, titles 53–60 chars, meta descriptions 142–153 chars
- All JSON-LD parses and reports the expected `@type`
- 1,068–1,165 words per city page, 8 `<h2>` each

The verification script is not in the repo; it lives in the session scratchpad. If this needs re-checking, the measurement approach worth reproducing is the composited-pixel one — CSS `getComputedStyle` returns `oklch()` strings, and any contrast checker that parses those as RGB will report confident nonsense.

### Retuning the hero

`brightness(0.68)` on `.hero__art` and the two `.hero__scrim` gradients are tuned **together** against one specific problem: `ind-street.webp` contains lit signage reading "Perseid Echo Machine Shop" which lands directly behind the H1 at desktop widths. The horizontal veil stays at 0.90+ across the text column and only opens past 74%, over the machines. If the art changes, retune both numbers and re-run the composited-pixel check — the CSS-colour check will not catch this class of failure.

## Going live

Everything is additive except two one-line footer edits, so the blast radius is small.

New:
```
local/                        (7 pages, assets/, _build/)
sitemap.xml                   regenerated
robots.txt                    + Disallow: /local/_build/
```

Modified:
```
index.html                    footer nav + "Areas served" link
v3/index.html                 same edit, kept in sync (v3/ is untracked; local copy only)
```

The footer link is not optional. Without it `/local/` is an orphan, and orphaned pages do not get crawled or ranked.

**Do not `git add -A` in this repo.** There is a lot of untracked scratch work in here (`.superpowers/`, `boldcut-preview/`, `bristlecone-v2/`, `offline-original/`, `sites/`, and `v3/` itself) that must not be committed. Stage the paths explicitly:

```bash
cd /c/Projects/PECWEB
git tag pec-pre-local-2026-07-29
git add local index.html sitemap.xml robots.txt
git commit -m "Local service pages for six King County cities"
git push
```

`v3/index.html` is deliberately left out — `v3/` is untracked and staging the file would start tracking it. The edit is already applied to the local copy so the two do not drift.

Back out by reverting that commit; the tag marks the pre-local state.

## After deploy

1. **Google Search Console** → Sitemaps → resubmit `sitemap.xml`.
2. Request indexing on `/local/` and the Renton page first. Quota is about 10/day, so the rest can follow over two days. Do not request all seven in one burst.
3. **Google Business Profile is the bigger half of this and Bryan has to do it himself** — it needs account actions. Field values are in the reply that shipped this work. The map pack is where local click share actually is, and it is the one surface the location-page farms cannot fake.
4. Watch `cta_fitcheck` by page in `fitcheck-stats`. If a city page draws traffic but never hands off, the local read on that page is wrong — fix the content, do not add more cities.

## Known gaps

- **No favicon** anywhere on the site. Pre-existing, shows up as a 404 on every page including the homepage. Worth fixing site-wide.
- **No `telephone` in the schema or on the pages.** Needed before the map pack can do much.
- **Hub is 582 words**, thinner than the city pages. Acceptable for an index, but it is the weakest page here.
- **No industry pages yet.** The searches with real buyer intent are often problem-shaped rather than category-shaped — an owner searches "automate quote follow up", not "business process automation". Industry × problem pages are the obvious next layer, and they can carry the same trunk.
