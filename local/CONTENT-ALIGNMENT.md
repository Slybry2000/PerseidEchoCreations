# Ticket #64 — point content_pipe and Zernio output at the local-search terms

**Status: brief only. No steering has been changed.** This document exists so whoever picks the ticket up does not have to re-derive the target list.

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
