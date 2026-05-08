# Product

## Register

brand

## Users

Primary buyer: **SMB owners and operators at 10–100 person companies.** Hands-on leaders who feel operational pain personally and sign the check. They are past "should we use AI?" and are looking for someone who can actually ship something that earns its keep — not pilots, not theater, not a Big Four pitch. They evaluate vendors by whether the person on the call sounds like they have run an operation, and by how fast they can tell whether an engagement will land.

Reading context: scanning the page late, between meetings, on a laptop. Five seconds to decide if it is worth a reply. They have seen a thousand AI-startup landing pages and a hundred consulting sites; the page must read different from both within the first scroll.

Secondary audiences (do not optimize for them, do not let them dilute the primary):
- Founder / operator peers who refer or partner.
- Mid-market leaders who occasionally arrive via search; they self-qualify or bounce based on engagement-model fit.

Explicitly **not** the audience: enterprise procurement, cheap-build shoppers, AI-curious tinkerers, agency-of-record bakeoffs.

## Product Purpose

Convert qualified SMB operators into "Start a Conversation" submissions for **Perseid Echo Creations**, Bryan Piard's AI Solutions Practice. The site exists to make the operator-led, outcomes-focused promise legible in the first scroll, then back it up with concrete services (audit / build / operate), three engagement models (Managed / Implementation / Build-Operate-Transfer), and a credible founder story (21 years in CX and digital transformation, most recently at T-Mobile).

Success metric: the right buyers self-qualify and reach out; the wrong ones self-deselect. A lower-traffic, higher-fit inbox beats a louder, noisier one.

The site is also a portfolio piece by implication. If the operator behind it cannot ship a marketing site that reads premium, the "we ship production-grade systems" claim is harder to believe.

## Brand Personality

**Bold. Declarative. Premium.**

The voice of a senior operator who has earned the right to be direct: no jargon, no hedging, no "agentic synergy." Confident enough to make claims and stand behind them. Premium meaning quietly expensive, not flashy expensive — the feel of a small firm that costs more than a big one because the work is better.

Voice rules:
- Short sentences. Concrete nouns. First person where it earns intimacy ("I read every message").
- No em dashes anywhere in copy (use commas, colons, semicolons, periods, parentheses).
- Banned words/phrases: "transform," "unlock," "leverage," "in today's fast-moving landscape," "synergy," "agentic" as decoration, "next-generation," "cutting-edge."
- Preferred verbs: build, ship, run, operate, audit, retrofit, integrate.
- Preferred nouns: operation, workflow, agent, automation, system, engagement, retainer.

## Anti-references

Hard exclusions. The site must not look or read like any of these.

- **AI-startup templates.** No gradient-blob heroes, no "Powered by GPT" badges, no hero-metric template (big number + small label + supporting stats), no neon-on-black, no generic "agentic" decoration, no abstract glowing nodes-and-edges illustrations.
- **Big-consulting sites.** No Accenture/Deloitte stock-photo grids, no jargon-heavy copy ("digital transformation journey"), no navy+grey corporate gloom, no "we partner with you on your transformation," no four-quadrant framework diagrams.
- **Creative-studio portfolios.** No Awwwards-bait, no scroll-jacked transitions, no oversized type-as-decoration, no marquee tickers, no hover gimmicks, no kinetic-text reveals as the headline. The site sells outcomes, not visual chops.
- **Crypto / web3 aesthetics.** No neon glow, no holographic gradients, no futuristic-sci-fi, no "protocol" framing. This is the second-order reflex AI sites fall into; we avoid it deliberately.

**Design lane:** modern-monochrome with one signature color. Mostly tinted neutrals (paper / navy), one decisive orange accent doing ≤10% of the work, confident type at modern scale, bold through restraint plus one loud move per surface. Vercel / Arc / Linear territory in feel, calibrated for an operator-led services practice rather than a developer tool.

## Design Principles

1. **Operator credibility before product polish.** The page must convince an SMB operator in five seconds that the person behind it has actually run operations — not as a copywriting claim, but as a felt quality (tone, restraint, what is left out, what is specific). Every design decision is checked against: does this read as someone who has run real operations, or as marketing about running operations? When in doubt, cut the marketing thing.

2. **One loud move, then quiet.** Modern-monochrome means restraint is the baseline. Earn the right to a single loud move per section (a piece of type, a composition, the orange accent placement) and let everything else recede. Loud + loud + loud reads as creative-studio portfolio, which is anti.

3. **Specific over generic.** Every word, example, and visual asset prefers the concrete over the categorical. "Twenty-one years in customer experience, most recently at T-Mobile" beats "decades of experience." "Workflow agents, API integration, observability" beats "AI solutions." The page reads less like marketing precisely because the claims are specific enough to verify.

4. **Premium = quietly expensive.** Premium does not mean ornate, animated, or showy. It means tighter type, fewer elements, more space, better materials (real photography over stock; custom marks over icon-library SVGs; a considered grid over a default container). If a competing AI-services site could ship the same component, it is not pulling its weight.

5. **Self-qualifying, not self-promoting.** The page is built to let the right buyers in and let the wrong ones bounce. Pricing signals, language ("Start a Conversation," not "Get a free quote"), the engagement-model strip (Managed / Implementation / Build-Operate-Transfer), and the operator-led framing all do qualifying work. The site is allowed to be off-putting to the wrong buyer.

## Accessibility & Inclusion

**WCAG 2.2 AA as a hard floor**, not an aspiration.

- Body text contrast ≥ 4.5:1; large text and non-text UI ≥ 3:1. Verify the slate-on-paper combos used today; tighten any that fall below.
- Full keyboard navigation for every interactive element. Visible `:focus-visible` styles on all controls (the current orange outline at 2px / 3px offset is good — keep it).
- `prefers-reduced-motion` always honored. Reveal animations, modal entrances, hero-aware nav transitions, and any future motion must gracefully degrade to no-motion.
- Contact modal: traps focus, returns focus to the trigger on close, announces status changes via `aria-live`. Already in place; do not regress.
- Color is never the sole carrier of meaning (states, errors, statuses get a text label or icon too).
- Form fields use visible labels, not placeholder-only. Explicit error text. Correct `autocomplete` attributes (already in place for the contact form).
- SVGs: decorative ones get `aria-hidden="true"`; functional ones get accessible labels.
- Buyer context includes regulated-industry SMBs (healthcare, financial services, professional services); a11y is a buying signal, not a checkbox.
