# sites.perseidechocreations.com Storefront — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the single-page sales storefront at `sites.perseidechocreations.com` that converts no-website local owners into "claim your site" leads and fires a build trigger.

**Architecture:** One self-contained `sites/index.html` (inline `<style>` + vanilla JS), no build step, no framework — same pattern as `index_smb.html`. Warmed-up Perseid Echo brand (persimmon/ink/warm-paper + Poppins + EB Garamond). Claim form POSTs JSON to a claim endpoint and emits a `status:"claimed"` build event; a no-backend email fallback guarantees no lost lead. Deploys as its own Cloudflare Pages project on the `sites.` subdomain.

**Tech Stack:** Static HTML5/CSS3, vanilla JS, Google Fonts (Poppins + EB Garamond) with system fallbacks, Cloudflare Pages (host) + Pages Function or form endpoint (claim).

**Source of truth:** `docs/superpowers/specs/2026-06-03-sites-storefront-design.md`

---

## Brand constants (use verbatim)

```
--persimmon:#FF6A2A; --persimmon-deep:#E15517; --ink:#0D1321; --ash:#3A4152;
--warm:#F6F1E8; --warm2:#FBF7F0; --card:#FFFFFF; --rule:#0D13211A;
Fonts: Poppins 400/500/600/700 (UI/body) · EB Garamond 600 + italic (headline)
Price: $199 to launch + $49/month · $490/year (2 months free)
CTA label: "Claim my site →"   Brand: Perseid Echo Creations   Email: Bryan@perseidechocreations.com
```

## File structure

- Create: `sites/index.html` — the entire storefront (markup + styles + script).
- Create: `sites/assets/og-image.jpg` — 1200×630 social image (placeholder ok; relative path).
- Optional later: `sites/functions/api/claim.js` — Pages Function (mirrors pec-placeholder's claim endpoint). Out of scope for the static build; the form must work with the email fallback first.

> Relative asset paths only (`assets/...`, never `/assets/...`) so it renders under `file://` and when served — lesson from `index_smb.html`.

---

### Task 1: Scaffold the file — head, meta, SEO, brand tokens

**Files:** Create `sites/index.html`

- [ ] **Step 1: Write the document skeleton + `<head>`**

Include: `<!DOCTYPE html>`, `lang="en"`, viewport, `<title>Get your business online — Perseid Echo Creations</title>`, meta description, canonical `https://sites.perseidechocreations.com/`, Open Graph + Twitter card (full https OG image URL `https://sites.perseidechocreations.com/assets/og-image.jpg`), `LocalBusiness`/`Service` JSON-LD, favicon, Google Fonts preconnect + Poppins/EB Garamond link.

- [ ] **Step 2: Add `:root` brand tokens + base reset in an inline `<style>`**

Use the Brand constants block above verbatim. Reset (`*{box-sizing;margin;padding}`), `body` font Poppins, warm-paper background, `::selection` persimmon, `prefers-reduced-motion` guard.

- [ ] **Step 3: Verify**

Open `sites/index.html` in a browser. Expected: blank warm-paper page, no console errors, fonts load (Poppins/EB Garamond), tab title correct. Run `view-source` / DevTools → confirm JSON-LD and OG tags present.

---

### Task 2: Nav + hero with inline claim form + live preview

**Files:** Modify `sites/index.html`

- [ ] **Step 1: Nav**

`<header>` with `✦ Perseid Echo Creations` wordmark (EB Garamond), tag "Websites for local business", and a persimmon `Claim my site →` button that anchors to `#claim`.

- [ ] **Step 2: Hero markup**

Two-column hero: left = eyebrow "Built · hosted · done for you", H1 (EB Garamond) **"We already built your website. Come <em>make it yours.</em>"**, sub "A clean, mobile-friendly page that helps customers find you — designed, built, and hosted for you. You just approve it and go live. From $199 to launch + $49/month.", then the **claim card** (see Task 6 for the form). Right = browser-chrome `live preview` of a sample product page (ink hero, "Joe's Auto Repair", persimmon call button, review line) with caption "↑ A real page we build — yours looks like this, with your info."

- [ ] **Step 3: Hero + nav styles**

Warm hero, persimmon eyebrow, clamp H1 (`clamp(30px,5vw,42px)`), primary/ghost buttons, the white claim card with soft shadow, the dark preview frame. Responsive: stack to one column under 720px.

- [ ] **Step 4: Verify**

Reload. Expected: warm hero with serif headline, claim card visible, dark preview beside it on desktop, stacked on mobile (resize to 375px). Nav button scrolls to `#claim`.

---

### Task 3: Trust strip + empathy line + how-it-works

**Files:** Modify `sites/index.html`

- [ ] **Step 1: Trust strip** — row under hero: ★★★★★ · "Live in 7 days" · "You approve before it goes live" · "Hosted & maintained" · "Cancel anytime".

- [ ] **Step 2: Empathy line** — full-width strip: *"Most customers look you up online before they ever walk in. If there's nothing to find, they move on."*

- [ ] **Step 3: How it works (3 steps)** — numbered cards: ① "Claim your page (30 seconds)" ② "We build & polish it for you — within a week (your hours, photos, reviews, map)" ③ "You approve, we take it live and host it."

- [ ] **Step 4: Verify** — reload; three sections render in order, numbered steps legible, responsive grid collapses cleanly on mobile.

---

### Task 4: What you get + "see a real one" example

**Files:** Modify `sites/index.html`

- [ ] **Step 1: Feature grid** — heading "What you get", 6–7 items with simple icons/checks: mobile-friendly · click-to-call · hours & map · photos · customer reviews · found on Google · hosted & maintained.

- [ ] **Step 2: Example section** — heading "See a real one"; a browser-chrome frame showing a full sample product page (reuse the placeholder design: ink hero + claim-style body) with caption "A live page we built for a local shop." (Sample content until Bryan supplies a real live URL — flagged open item.)

- [ ] **Step 3: Verify** — reload; feature grid wraps responsively; example frame reads as a real site preview.

---

### Task 5: Pricing + FAQ + final CTA + footer

**Files:** Modify `sites/index.html`

- [ ] **Step 1: Pricing card** — single card: **"$199 to launch + $49/month"**, subline **"or $490/year — 2 months free"**, included list (the page · hosting · updates · support · you approve before live), persimmon `Claim my site →` button → `#claim`.

- [ ] **Step 2: FAQ** — 5 items (details/summary accordion), copy from spec: no logo/photos · already have Facebook · do I own it / cancel (rent, cancel anytime, paid export) · how fast (~a week) · change it later (updates included, big changes quoted).

- [ ] **Step 3: Final claim CTA** — repeat the warm claim card with `id="claim"` anchor target and heading "Claim your site — ready this week".

- [ ] **Step 4: Footer** — "Built by Perseid Echo Creations · Bryan@perseidechocreations.com · 2026".

- [ ] **Step 5: Verify** — reload; price reads correctly everywhere; FAQ items expand/collapse; all `Claim my site` buttons scroll to the final form.

---

### Task 6: Claim form behavior — submit, trigger emit, success, honeypot

**Files:** Modify `sites/index.html`

The claim card (used in hero and final CTA — keep markup identical via the same field set):
fields **Business name** (required), **Email** (required, type=email), **Phone** (optional), a hidden honeypot `company` field, hidden `source="storefront"`, submit `Claim my site →`, and a `role="status"` line.

- [ ] **Step 1: Form markup** — real `<form>` with labelled inputs (not divs), honeypot off-screen, microcopy "You approve before anything goes live. Cancel anytime."

- [ ] **Step 2: Submit JS (vanilla, inline)** — on submit: `preventDefault`; if honeypot filled, silently drop; validate name+email present; POST JSON `{business_name,email,phone,source:"storefront"}` to `CLAIM_ENDPOINT`. Define one constant at top of script: `const CLAIM_ENDPOINT = "/api/claim";` and a `MAILTO_FALLBACK` note. On success: replace card with "Thanks — we've got it. We'll have your page ready this week and email you to take it live." On failure: show retry message, re-enable button.

- [ ] **Step 3: Trigger note in code** — comment in the JS documenting that a successful POST is the build trigger (record written `status:"claimed"`, consumed by project #2 Hermes). No extra client work needed beyond the POST.

- [ ] **Step 4: FAQ toggle JS** — if using buttons instead of native `<details>`, wire the open/close; otherwise native `<details>` needs no JS.

- [ ] **Step 5: Verify** — fill the form with a junk endpoint and confirm: empty name/email blocked with message; honeypot-filled submit silently ignored; valid submit shows "Sending…" then the failure path (no real endpoint yet) without breaking. Then point `CLAIM_ENDPOINT` at a test endpoint (or Formspree-style fallback) and confirm a real POST fires (DevTools Network).

---

### Task 7: Full verification pass

**Files:** none (review `sites/index.html`)

- [ ] **Step 1: Responsive** — check 375px, 768px, 1280px. No overflow, hero stacks, grids wrap, tap targets ≥44px.
- [ ] **Step 2: Accessibility** — keyboard-tab through nav → form → FAQ; visible focus rings; inputs have labels; persimmon-on-ink and ink-on-warm contrast pass; `prefers-reduced-motion` kills transitions.
- [ ] **Step 3: `file://` + served parity** — open by double-click AND via a local server; both render identically (relative paths hold).
- [ ] **Step 4: Brand match** — side-by-side with a generated placeholder page: same persimmon, same ink, same component feel. Confirm zero "Bristlecone"/botanical words in visible copy; footer brand correct.
- [ ] **Step 5: Commit** (when Bryan approves committing) — `git add sites/ docs/superpowers/ && git commit -m "feat: sites.perseidechocreations.com storefront"` on a branch (not main).

---

### Task 8: Deploy notes (hand-off, not a code step)

- [ ] Cloudflare Pages: new project, root = `sites/`, custom domain `sites.perseidechocreations.com`.
- [ ] Wire the real claim endpoint: either add `sites/functions/api/claim.js` (mirror pec-placeholder's KV claim function) so `/api/claim` works on-domain with no CORS, OR set `CLAIM_ENDPOINT` to a form/email service for the v1 fallback.
- [ ] Swap the example preview for a real live page; confirm `$199/$49/$490` and OG image are final.

---

## Self-Review

**Spec coverage:** Hero ✓(T2) · trust strip ✓(T3) · empathy ✓(T3) · how-it-works ✓(T3) · what-you-get ✓(T4) · see-a-real-one ✓(T4) · pricing ✓(T5) · FAQ ✓(T5) · final CTA ✓(T5) · footer ✓(T5) · claim fields + submit + email fallback ✓(T6) · **build-trigger emit** ✓(T6 Step 2–3) · SEO/meta/JSON-LD ✓(T1) · a11y/responsive/`file://` parity ✓(T7) · single self-contained file in `sites/` ✓(T1) · relative paths ✓(T1) · no payment on page ✓(scope) · Hermes pipeline excluded ✓(scope). No gaps.

**Placeholder scan:** Sample example page and final price/OG are explicitly flagged open items with defaults, not silent TODOs. No "add error handling"-style vagueness — form behavior is fully specified in T6.

**Consistency:** `CLAIM_ENDPOINT` constant, field names (`business_name`, `email`, `phone`, `source`), and the `#claim` anchor are used consistently across hero, final CTA, and JS.
