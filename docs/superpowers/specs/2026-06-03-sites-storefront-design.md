# sites.perseidechocreations.com — Design Spec

**Date:** 2026-06-03
**Status:** Approved direction, ready for implementation plan
**Owner:** Bryan Piard (Perseid Echo Creations)

## Summary

A single-page sales site on the subdomain **sites.perseidechocreations.com** that sells
the done-for-you local-business website service. It is the public "storefront" for the
**pec-placeholder** pipeline (Lane D — businesses with no website): that pipeline
auto-builds a clean placeholder page for each no-website business and hosts it with an
"Is this your business? Claim it." form. This storefront is the brand home that explains
the offer, shows the product, states the price, and converts owners into claims.

The page's one job: get a local business owner to **claim their site** (capture business
name + email as a warm lead). Everything after the claim — building/polishing the real
page, taking payment, going live — happens off-page.

## Audience

Micro local-business owners with **no website today** — pool halls, auto shops, salons,
restaurants, trades. Non-technical, price-sensitive individually, but their alternative is
*nothing*, so the competition is their own inertia, not another agency. Many arrive warm:
they scanned the QR on their auto-built placeholder page or got a QR mailout.

## Relationship to pec-placeholder

- **Product (auto-built per business):** `claim.bristlecone.so/<project>/<venue-id>/` —
  dark ink hero, persimmon buttons, "claim it" card, footer "Built by Perseid Echo Creations."
- **Storefront (this spec):** `sites.perseidechocreations.com` — same brand components,
  warmed up, sells the offer. The two must read as obviously the same people.
- Note: "Bristlecone" is an internal codename only. **No Bristlecone/botanical vocabulary
  in any customer-visible copy** (per positioning decision). Footer brand is
  "Perseid Echo Creations." Retain the "you approve before it goes live" operator framing.

## Locked decisions

| Decision | Choice |
|---|---|
| Subdomain | `sites.perseidechocreations.com` |
| Primary action | Claim your site (business name + email → warm lead) |
| Pricing (headline) | **$199 to launch + $49/month**, or **$490/year** (2 months free) |
| Brand | Perseid Echo persimmon/ink/paper + Poppins, **warmed up** |
| Build shape | One self-contained `index.html`, deploys to the subdomain |

Pricing rationale lives in this session's research; in short: the **monthly is the
business**, the launch fee is low to keep cold-prospect friction down and filter flakes,
the annual option is churn insurance. (Premium $1.2k–2.5k + $99–149/mo tier exists but is
sold on a call, not shown on the page.)

## Visual design system

Reuse the product's exact palette and font so storefront and product match, then warm it:

- **Palette (from the generated placeholder):** persimmon `#FF6A2A`, persimmon-deep
  `#E15517`, ink `#0D1321`, ash `#3A4152`, warm paper `#F6F1E8`, lighter warm `#FBF7F0`,
  card `#FFFFFF`, hairline rule `#0D13211A`.
- **Type:** Poppins (400/500/600/700) for UI/body; **EB Garamond** (600, with italic) for
  the editorial headline — this serif is the main "warm-up" move and is consistent with the
  primary PEC site. Mono not needed.
- **Warm-up moves vs. the bare product:** warm paper hero instead of pure dark; serif
  headline; the claim form lifted into the hero; a live product preview beside it as proof;
  softer, reassurance-led copy.
- **Components:** persimmon primary button (ink text), ghost button, warm claim card,
  browser-chrome preview frame, trust strip, feature grid, FAQ accordion (or plain list).
- Rounded corners ~10–14px, soft shadows, generous spacing. Mobile-first responsive;
  respects `prefers-reduced-motion`.

## Page structure (top → bottom)

1. **Nav** — PEC wordmark (✦ Perseid Echo Creations) + tag "Websites for local business" +
   `Claim my site →` button.
2. **Hero** (warm) — eyebrow "Built · hosted · done for you"; headline *"We already built
   your website. Come make it yours."*; sub with the offer + price; **inline claim card**
   (business name, email, `Claim my site →`, microcopy "You approve before anything goes
   live. Cancel anytime."); **live preview** of a real example page beside it.
3. **Trust strip** — Live in 7 days · You approve before it goes live · Hosted &
   maintained · Cancel anytime.
4. **Empathy line** — *"Most customers look you up online before they ever walk in. If
   there's nothing to find, they move on."*
5. **How it works (3 steps)** — ① Claim your page (30 sec). ② We build & polish it for you
   within a week (your hours, photos, reviews, map). ③ You approve, we take it live and host
   it.
6. **What you get** — feature grid: mobile-friendly, click-to-call, hours & map, photos,
   reviews, found on Google, hosted & maintained.
7. **See a real one** — a live example page (the actual product) in a browser frame, as
   proof.
8. **Pricing** — one simple card: **$199 to launch + $49/month** (or **$490/year — 2 months
   free**). Includes: the page, hosting, updates, support, you approve before live. Single
   `Claim my site →` CTA. (Placeholder-free — these are the confirmed numbers.)
9. **FAQ** — non-technical reassurance (see below).
10. **Final claim CTA** — warm "Claim your site — ready this week" card (repeat of hero
    form).
11. **Footer** — Built by Perseid Echo Creations · Bryan@perseidechocreations.com · year.

## The claim mechanic

- **Fields:** Business name (required), Email (required), Phone (optional). Honeypot field
  for spam (same pattern as the product's claim form).
- **Submit:** POST JSON to a claim endpoint. **Default:** reuse the pec-placeholder claim
  pipeline (Cloudflare Pages Function → KV) so storefront leads land in the same store as
  warm leads, tagged `source: "storefront"`. **Fallback if that wiring isn't ready at
  launch:** a no-backend path that emails the lead to Bryan@perseidechocreations.com (e.g.
  a simple form endpoint), so no lead is ever lost.
- **Emit a build trigger (in scope for the storefront).** On a successful claim the
  endpoint must also emit a build event — the starting signal for the downstream autonomous
  build pipeline (below). Concretely: write the record with `status: "claimed"` and either
  (a) enqueue a message / call a webhook, or (b) rely on a poller. The storefront's job is
  only to *fire the signal reliably*; what consumes it is project #2.
- **Success state:** inline confirmation — "Thanks — we've got it. We'll have your page
  ready this week and email you to take it live." No redirect.
- **No payment on the page.** Claiming is lead capture only; Bryan sends a Stripe
  link/invoice off-page after the claim. (Keeps v1 simple; payment integration is out of
  scope.)

## Downstream: autonomous build pipeline ("Hermes") — separate project #2

The storefront is project #1 and ships on its own. Bryan wants a claim to kick off a
**fully hands-off** build where he is never involved. This is its own subsystem and gets its
own spec/plan; captured here so the storefront emits the right trigger and the two connect.

Flow (claim → live, no Bryan):
1. **Claim** (project #1) fires the build event.
2. **Hermes builder agent** pulls the business's *verified* info (existing Yelp footprint +
   a quick web look-up) and generates an upgraded real site in the Perseid Echo brand —
   **verified facts only, no invented claims.**
3. **Reviewer agent** critiques (renders, info correct, links work, on-brand, accessible)
   and loops back to the builder until it passes a bar. This is the automated "get feedback"
   loop.
4. **Owner approval** — the owner gets a preview link by email: approve to go live, or reply
   with changes (changes loop back to step 2).
5. **Auto-deploy + billing** on approval (reuses pec-placeholder `deploy --go`); Bryan gets
   a digest notification only.

**Human-gate principle preserved, Bryan removed:** the dot-suite contract requires a human
gate on anything that leaves the building. Here that human becomes **the customer approving
their own site**, not Bryan — so the safety rule holds while Bryan is fully hands-off. He can
still receive a digest and intervene if he ever chooses.

**Feasibility:** buildable on the existing stack — pec-placeholder already generates,
deploys, and syncs claims; add the Claude Agent SDK for the builder + reviewer, Firecrawl for
the look-up, email for the owner approval. Concrete trigger options to decide in project #2:
a Cloudflare Queue/webhook consumer, or a scheduled poller that extends the existing
`--sync-claims` to launch a build per newly-claimed venue.

**Risks to design for in project #2:** wrong/invented business info (mitigate: verified
sources only + reviewer agent), auto-publishing on a real business's behalf (mitigate: owner
approval gate), runaway loops/cost (mitigate: pass bar + max iterations + budget caps).

## FAQ content (recommended answers — Bryan to confirm policy stances)

- **"I don't have a logo or photos — can you still do it?"** Yes; we build from your public
  info and can add photos later.
- **"I already have a Facebook page — do I need this?"** A site you own shows up on Google
  and works when Facebook is down; it complements your page.
- **"Do I own it / what if I cancel?"** *Policy to confirm:* hosted-and-maintained by us
  (you rent), cancel anytime, paid export available if you leave. (Protects recurring while
  defusing "held hostage.")
- **"How fast?"** Live within about a week of claiming.
- **"Can I change it later?"** Yes — text/photo updates are included; bigger changes quoted.

## Technical / build approach

- **One self-contained `index.html`** (inline `<style>`, minimal vanilla JS for the claim
  form + FAQ toggles) — same simple single-file approach as `index_smb.html`. No build step,
  no framework.
- **Location:** new folder `c:/Projects/PECWEB/sites/` with `index.html` as the site root,
  so it deploys as its own Cloudflare Pages project mapped to the `sites.` subdomain. Assets
  (any images, OG image) live beside it with **relative paths** (lesson from the SMB site:
  absolute `/assets/...` paths break under `file://`).
- **SEO/meta:** title, description, canonical `https://sites.perseidechocreations.com/`,
  Open Graph + Twitter card with a full https OG image URL, `LocalBusiness`/`Service`
  JSON-LD. Favicon.
- **Accessibility:** semantic landmarks, labelled form inputs, visible focus rings, color
  contrast on persimmon-on-ink checked, `prefers-reduced-motion` honored.
- **Performance:** system-font fallback while Google Fonts load; lazy-load the preview/OG
  images; no heavy libraries.

## Out of scope (YAGNI for v1)

- Payment/checkout on the page (off-page Stripe link after claim).
- CMS, multi-page site, blog, user accounts/login.
- The Premium tier UI (sold on a call).
- **The autonomous build pipeline ("Hermes") itself — that is project #2** with its own
  spec/plan. The storefront only *emits the trigger*; it does not build, review, or deploy
  the real sites.

## Open items for Bryan to confirm (non-blocking; sensible defaults chosen)

1. **Example page** shown in "See a real one" — use a representative sample until a specific
   live page is chosen (default: a tasteful sample in product style).
2. **Lead routing** — wire to the existing claim pipeline vs. email-to-Bryan fallback for
   v1 (default: try pipeline, fall back to email).
3. **Ownership/cancel policy** copy in the FAQ (default stance above).

## Success criteria

- Reads as unmistakably the same brand as the auto-built placeholder pages.
- A non-technical owner understands the offer and price in under 10 seconds and can claim in
  ~30 seconds.
- Claim form captures business name + email reliably and routes the lead (pipeline or
  email) with a clear success state.
- Single static file, relative asset paths, renders correctly both opened locally
  (`file://`) and served on the subdomain.
- Mobile-first, accessible, fast.
