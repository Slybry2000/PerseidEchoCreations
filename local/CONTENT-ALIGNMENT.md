# Ticket #64 — point content_pipe and Zernio output at the local-search terms

**Status: DONE 2026-07-30.** Steering changed, verified end to end. What shipped is recorded at the bottom of this document; the brief above it is left as written so the reasoning stays readable.

## The problem

PEC now has thirteen pages aimed at specific searches (`/local/`, `/workflows/`). The content factory produces and posts daily through content_pipe and Zernio, and none of that production knows those pages exist.

That is a waste in both directions. The posts do not point at pages built to convert the traffic, and the pages get no topical reinforcement from a stream of content that is already being written anyway.

## What "aligned" means here — and what it does not

This is **not** a request to turn the social output into SEO filler. Social posts do not rank and stuffing keywords into them helps nothing.

Alignment means three specific things:

1. **Topic overlap.** When the factory picks a subject for PEC's own channels, it should be drawn from the same set of problems the pages cover, so the writing compounds instead of scattering.
2. **Destination.** Posts on those topics should link to the matching workflow or city page rather than the homepage, because those pages answer the question the post raised.
3. **Language match.** The pages use owner language — "the quote went out and never came back", not "quote lifecycle automation". Content on the same topic should use the same words, so a reader arriving from a post recognises the page.

## The target set

Pages that exist and want traffic:

| Page | The problem in owner language |
|---|---|
| `/workflows/quote-follow-up/` | Quotes go out and nobody chases them |
| `/workflows/field-paperwork-to-invoice/` | The job is done, then somebody retypes it at night |
| `/workflows/order-intake-from-email/` | Orders arrive as attachments and get keyed in by hand |
| `/workflows/appointment-reminders/` | A booking nobody confirms is a coin flip |
| `/workflows/client-intake-and-documents/` | The fourth email asking for the same document |
| `/local/workflow-automation-renton-wa/` | Renton: trades, Boeing supply chain, clinics |
| `/local/workflow-automation-kent-wa/` | Kent Valley: warehouse, wholesale, fabrication |
| `/local/workflow-automation-bellevue-wa/` | Bellevue: professional practices |
| `/local/workflow-automation-tukwila-wa/` | Tukwila: multi-site retail and hospitality |
| `/local/workflow-automation-auburn-wa/` | Auburn: field service |
| `/local/workflow-automation-issaquah-wa/` | Issaquah: appointment-driven owner-led businesses |

The canonical source is `local/_build/cities.json` and `local/_build/workflows.json` — read those rather than this table if they have moved on.

## Steering surfaces to change

Per the checklist established when the site was repositioned (see the `pec-content-voice-repoint` note), a repositioning is not done until every surface agrees. For this ticket the relevant ones are:

- content_pipe's PEC project steering — the topic pool and the standing-link/rotating-CTA config
- the standing link, which currently points at the homepage for everything
- Zernio's PEC channel configs, four accounts across two logins
- any reusable topic or format packs scoped to PEC

**Write through the HTTP API, not the filesystem.** Out-of-process writes to content_pipe get clobbered — this is a known failure and it has bitten before.

## Definition of done

- A PEC post on one of the eleven topics links to the matching page, not the homepage
- The topic pool for PEC's own channels is drawn from the list above
- Attribution works end to end: a click from a post reaches the page, and the page's existing tracker (`local:<slug>` / `wf:<slug>`) shows the referrer, so the loop is measurable rather than assumed
- Nothing about client content changes — this ticket is scoped to PEC's own channels only

## What to check before starting

The 90-day constraint (sell-only, ≤8 build-hours/week through Oct 4) still applies. This is steering configuration rather than a build, so it should be small — if it starts turning into a build, that is the signal to stop and re-scope.

---

## What shipped, 2026-07-30

### The topic pool is the question bank

The factory's topic pool for PEC is the customer-question bank (`data/question-bank.json`, written through `POST /pipe/api/question-bank/perseid-echo-creations`). It was rewritten: 28 questions, 27 of them mapped to one of the eleven pages, all in the pages' own owner language ("Why do the quotes I send on Tuesday quietly turn into a no by the following week?", not "quote lifecycle automation"). The five content lanes established in the voice repoint are preserved at roughly 39 / 25 / 18 / 11 / 7. The 28th question is the direct-offer one and is deliberately unmapped, so it falls back to the homepage.

Adding a topic later is a bank edit, not a code change.

### The destination now follows the topic

A bank entry may carry a `link`. When the factory draws that question for a master, the page is stamped on the article, and at every posting exit the caption ends at that page instead of the homepage. Five small edits made that work:

| File | Change |
|---|---|
| `lib/question-bank.js` | a bank entry keeps an optional `link`; new `linkForQuestion(slug, q)` |
| `server.js` | the bank save/regenerate routes carry `link` through, and an LLM regeneration keeps the destination of any question whose text it leaves unchanged |
| `codex.js` | when a drawn question names a page, stamp it on the article (only ever fills an empty `url`) |
| `db.js` | `setArticleUrl(aid, url)` |
| `lib/content-lint.js` | at the exit, an article's own destination beats the standing project link **when it is on the same host** |

That same-host guard is what keeps this PEC-only. Other projects' articles carry scraped source URLs on foreign hosts, so they are ignored and every other project behaves exactly as before. Verified: dream-travel with a foreign article URL still resolves to its own standing link.

An unmapped PEC piece still resolves to `perseidechocreations.com` with its rotating CTA, unchanged.

### Attribution was broken and is now fixed

The pages set `window.PEC_PAGE`, but the collector was silently discarding it: `lib/site-events.js` had a three-item page allowlist (`home`, `partners`, `privacy`), so every `local:<slug>` / `wf:<slug>` event was dropped on arrival, along with the `cta_fitcheck`, `cta_nearby` and `cta_email` events the service pages emit. Fixed:

- page ids matching `local:<slug>` / `wf:<slug>` are accepted by shape, so a new city or workflow page reports the day it ships with no code change
- the three missing events were added
- the stats now carry a per-page funnel keyed on the visit's **entry** page (the Fit Check lives on the homepage, so the question worth answering is which page earned the visit that finished), and `fitcheck-stats` prints it as WHICH PAGE THEY LANDED ON

### Verified end to end

One real master generated on the rotation path drew the quote follow-up question and stamped the page. Resolved at the posting exit it reads:

```
Find the first job worth taking off your plate → https://perseidechocreations.com/workflows/quote-follow-up/?utm_source=linkedin&utm_medium=social&utm_campaign=art_…&utm_content=ast_…
```

Following that exact URL in a browser and clicking through to the Fit Check produced, in one session: a `view` on `wf:quote-follow-up` carrying `src=linkedin` and the campaign id, a `cta_fitcheck`, a `view` on `home`, and a Fit Check start. `fitcheck-stats 1` credits it to `wf:quote-follow-up` — 1 visit, 1 started. The test article was trashed afterwards.

### Deliberately not done

- **`brandStructured` was not touched.** It has no API setter and requires a pm2 stop/patch/start, and the owner language now arrives through the question text, which is the dominant steer on a master anyway. Editing the audience or category sentences to say the same thing again would risk the voice for no gain.
- **Zernio needed nothing.** The link travels inside the caption; no channel config names a destination. PEC's five channels were left alone.
- **X caption length is fine.** The workflow URLs are longer than the homepage, but X counts any URL as 23 characters and `maxChars` in `config/platform-rules.json` is prompt guidance, not a post-time gate.

Backups on the VPS: `*.bak-t64-20260730` for `db.js`, `codex.js`, `lib/question-bank.js`, `lib/content-lint.js` and `fitcheck-stats`. `server.js` and `lib/site-events.js` are git-tracked in content_pipe, so their changes are revertable there.
