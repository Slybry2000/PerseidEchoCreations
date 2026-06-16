---
name: Perseid Echo Creations
description: Modern-monochrome design system for an operator-led AI Solutions Practice. Quiet Authority as North Star.
colors:
  persimmon: "#FF6A2A"
  persimmon-deep: "#E15517"
  ink: "#0D1321"
  ash: "#3A4152"
  paper: "#F6F6F4"
  paper-dim: "#ECEAE5"
  surface-card: "#FFFFFF"
  rule-light: "#0D13211A"
  rule-dark: "#F6F6F41A"
  selection-bg: "#FF6A2A"
  selection-text: "#0D1321"
typography:
  display:
    fontFamily: "Poppins, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "clamp(44px, 7.2vw, 84px)"
    fontWeight: 600
    lineHeight: 1.02
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Poppins, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "clamp(30px, 4vw, 44px)"
    fontWeight: 600
    lineHeight: 1.15
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Poppins, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "22px"
    fontWeight: 600
    lineHeight: 1.2
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Poppins, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "16px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  body-large:
    fontFamily: "Poppins, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "17px"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  label:
    fontFamily: "Poppins, -apple-system, BlinkMacSystemFont, sans-serif"
    fontSize: "12px"
    fontWeight: 600
    lineHeight: 1.4
    letterSpacing: "0.18em"
rounded:
  sm: "8px"
  md: "10px"
  lg: "12px"
  xl: "16px"
  modal: "18px"
  portrait: "20px"
spacing:
  xs: "8px"
  sm: "16px"
  md: "24px"
  lg: "32px"
  xl: "64px"
  section: "100px"
  hero: "120px"
components:
  button-primary:
    backgroundColor: "{colors.persimmon}"
    textColor: "{colors.ink}"
    typography: "{typography.body}"
    rounded: "{rounded.md}"
    padding: "14px 26px"
  button-primary-hover:
    backgroundColor: "{colors.persimmon-deep}"
    textColor: "{colors.ink}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.paper}"
    typography: "{typography.body}"
    rounded: "{rounded.sm}"
    padding: "9px 18px"
  button-ghost-hover:
    backgroundColor: "transparent"
    textColor: "{colors.paper}"
  card-pillar:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xl}"
    padding: "32px 28px"
  card-service:
    backgroundColor: "{colors.surface-card}"
    textColor: "{colors.ink}"
    rounded: "{rounded.xl}"
    padding: "36px 32px"
  card-engagement:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.lg}"
    padding: "22px 24px"
  nav:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    height: "72px"
---

# Design System: Perseid Echo Creations

## 1. Overview

**Creative North Star: "Quiet Authority"**

The system is premium-by-omission. Confidence is signaled through what is left out, not what is added. The site of a small firm that does not need to perform, because the work performs. Closer in feel to Linear's marketing pages or Stripe's quietest product pages than to any AI-startup template. The operator behind the practice has run real operations for twenty-one years; the design earns the right to be this restrained because the substance is specific.

Bold, declarative, premium reads here as: bold by reduction (one accent, one move per section, no ornamentation), declarative through specificity (concrete claims, real names, tight copy), premium through restraint (more space, fewer elements, better materials). The system explicitly rejects gradient-blob heroes, neon-on-black, navy-and-grey corporate gloom, Awwwards scroll-jacking, and the futurist-sci-fi reflex AI sites fall into. If the page could appear in a portfolio of AI-startup landing pages without comment, the design has failed.

**Key Characteristics:**
- Modern-monochrome with one signature color (Persimmon) doing ≤10% of the work.
- Tinted neutrals only; no `#fff` or `#000` literals — every neutral pulled toward the brand hue.
- Flat by default; elevation appears only as state.
- Typography is the load-bearing element. Hierarchy through scale and weight, not chrome.
- Ample vertical rhythm (100–120px between sections) over dense layouts.
- One loud move per surface; everything else recedes.

## 2. Colors: The Persimmon Palette

A two-toned neutral system (Ink + Paper) carrying a single warm accent (Persimmon). The accent is rare on purpose; its scarcity is what makes it read as deliberate authorship rather than decoration.

### Primary
- **Persimmon** (`#FF6A2A`): The one signature color. Used on the hero CTA, the orange focus outline, the service-number eyebrows, the contact-CTA, and `::selection`. Earns its placement by being placed sparingly. Never used as a fill on more than one major element per fold.
- **Persimmon Deep** (`#E15517`): Hover state for the primary button, and only there. Not a secondary brand color.

### Neutral
- **Ink** (`#0D1321`): The foundational dark. Hero, About, Footer surfaces and primary text on light. Tinted toward navy-violet so it is never plain black.
- **Ash** (`#3A4152`): Secondary text on light. Body paragraphs, section ledes, list items. The contrast with Ink establishes hierarchy without color shift.
- **Paper** (`#F6F6F4`): The default light surface and primary background. Warm off-white, tinted, never pure.
- **Paper Dim** (`#ECEAE5`): The Services section background. The system's only mid-tone, used to differentiate one section from the rest of the paper canvas.
- **Surface Card** (`#FFFFFF`): The only place near-white pure appears. Used as card fills against Paper or Paper Dim. Treat as a value, not a brand color; do not use as a screen background.
- **Rule Light** (`#0D13211A`, ink at 10%): Hairline rules and card borders on Paper.
- **Rule Dark** (`#F6F6F41A`, paper at 10%): Hairline rules and borders on Ink surfaces.

### Named Rules

**The 10% Rule.** Persimmon may occupy no more than 10% of the visible viewport at any scroll position. If a design move requires more, it is the wrong move.

**The No-Pure Rule.** Pure `#fff` and `#000` are forbidden in tokens and prose. Every neutral is tinted (`#F6F6F4` paper, `#0D1321` ink). The only exception is `Surface Card` (`#FFFFFF`) used strictly as a card fill, never as a screen ground.

**The One Accent Rule.** Persimmon is the only chromatic color. No teal, no green-success, no blue-info, no second brand color. Status (error / success / warning) carries through type weight, icon, and copy, not through hue.

## 3. Typography

**Display Font:** Poppins (with `-apple-system, BlinkMacSystemFont, sans-serif` as fallback)
**Body Font:** Same. Single-family system.
**Label/Mono Font:** None. No monospace use.

**Character:** Poppins is the working font of the system, chosen for its modern geometric construction at display sizes and humanist legibility at body sizes. The system leans on weight and scale contrast rather than family contrast — bold via tightness, not via mixing voices. The display sizes use a strong negative letter-spacing (-0.025em) to feel chiseled and declarative; body sizes sit at normal tracking for comfortable reading.

### Hierarchy

- **Display** (600 weight, `clamp(44px, 7.2vw, 84px)`, line-height 1.02, tracking -0.025em): Hero only. One per page. Carries the entire promise.
- **Headline** (600 weight, `clamp(30px, 4vw, 44px)`, line-height 1.15, tracking -0.015em): Section h2s. Variants per section: About (28px–40px), Contact (32px–52px) for slightly larger emphasis.
- **Title** (600 weight, 22px, line-height 1.2, tracking -0.01em): Service-card headings.
- **Body Large** (400 weight, 17px, line-height 1.6): Section ledes, About paragraphs. Reading text where the audience is engaged.
- **Body** (400 weight, 16px, line-height 1.6): Default paragraph size. Capped at 65–75ch line length where it sets in long form.
- **Body Small** (400 weight, 15px, line-height 1.55): Card-body copy (pillars, services, engagement).
- **Label** (600 weight, 12px, tracking 0.18em, UPPERCASE): Section eyebrows, footer meta. Uses `--ash` for muted weight.
- **Pillar Label** (600 weight, 16px, tracking 0.02em, UPPERCASE): Pillar headings ("01 / Audit"). Used as a quasi-numeric heading at the same scale as body for deliberate flatness.
- **Service Number** (600 weight, 13px, tracking 0.1em, UPPERCASE, persimmon): Service-card category line ("AI / AGENTS"). The single place small UPPERCASE text takes the accent color.

### Named Rules

**The Single-Family Rule.** No second typeface anywhere. Hierarchy is achieved through size, weight, and letter-spacing only. A serif display, a monospace caption, or a script flourish would all break the system.

**The Tight-Display Rule.** Every type role at 22px or larger uses negative letter-spacing (-0.01em to -0.025em, scaled to size). Body and Body Small stay at normal tracking. The contrast between tight display and open body is part of the voice.

**The Eyebrow Rule.** UPPERCASE + 12px + 0.18em tracking + Ash is the only acceptable eyebrow form. Sentence-case eyebrows or larger small-caps are not the system.

## 4. Elevation

Flat by default. Surfaces have weight from tonal contrast (Ink vs. Paper vs. Paper Dim), not from shadow. Shadows appear only as a response to **state** (hover, focus) or to **modal context** (panels lifted off the page). A scrolled section at rest has zero box-shadow on any element.

### Shadow Vocabulary

- **Card lift on hover** (`box-shadow: 0 16px 36px rgba(13, 19, 33, 0.06)`): Subtle pillar / card hover. Pairs with a `translateY(-4px)` lift and a border-color shift to `rgba(13, 19, 33, 0.20)`. Diffuse enough that the shadow reads as ambient settle, not as elevation drama.
- **Portrait depth** (`box-shadow: 0 24px 60px rgba(0, 0, 0, 0.35)`): The founder portrait on the dark About surface. The one place a stronger shadow lives, because the portrait is sitting on Ink and needs the lift to feel placed rather than collaged.
- **Modal panel** (`box-shadow: 0 30px 80px rgba(13, 19, 33, 0.35)`): Contact modal panel. Strong drop because the panel is floating over a 72%-opacity Ink backdrop with backdrop-blur.

### Named Rules

**The Flat-By-Default Rule.** Every section, card, and surface starts with `box-shadow: none`. State (hover, focus, modal) is the only justification for adding one. If a shadow is being used to "make a card pop" at rest, it is wrong.

**The Diffuse-Soft Rule.** Shadows always use Ink (or near-Ink) at low opacity with large blur. Sharp, dark, small-blur shadows ("2014 app" elevation) are forbidden. Y-offset is always at least double the X-offset of zero.

## 5. Components

### Buttons

- **Shape:** Soft rectangles. Primary uses 10px radius (`{rounded.md}`); ghost CTA uses 8px (`{rounded.sm}`).
- **Primary:** Persimmon background (`#FF6A2A`), Ink text (`#0D1321`), 14px / 26px padding, 15px / 600 weight type. Includes a small inline arrow SVG (5→19, 12 5 19 12 12 19) at 18px, gap 10px from the label. Hover shifts to Persimmon Deep with `translateY(-1px)`. The primary button is the orange's flagship surface.
- **Ghost (nav CTA / contact-close):** Transparent background, Paper text, `rgba(246, 246, 244, 0.28)` 1px border, 9px / 18px padding. Hover lifts the border opacity to 1.0. Used in the navigation when the hero scrolls out and on the contact-success acknowledgment.
- **Hero-aware behavior:** The nav ghost CTA is hidden while the hero is in viewport (opacity 0, translateY(-4px), pointer-events: none). It enters on hero exit. This is a load-bearing brand move — do not remove.

### Cards

- **Pillar Card:** White (`#FFFFFF`) on Paper. 16px (`{rounded.xl}`) radius. 1px Rule-Light border. 32px / 28px internal padding. 48px square Ink-tinted icon well at 12px radius. On hover: -4px lift, Rule-Light border darkens to 0.20 ink, soft shadow appears. **Body uses Body Small (15px / 1.55).**
- **Service Card:** White on Paper Dim. 16px radius. 1px Rule-Light border. 36px / 32px internal padding. Persimmon Service Number eyebrow (13px UPPERCASE / 0.1em), Title heading (22px). Ships with a left-edge animated stripe (`::before`, scaleY 0→1 on hover). **Note: this is on the watch-list; see Don'ts below.**
- **Engagement Card:** Transparent on Paper Dim. 12px (`{rounded.lg}`) radius. 1px Rule-Light border. 22px / 24px padding. Small Pillar Label heading (14px UPPERCASE) + Body Small. The lightest-weight card in the system.

### Inputs

- **Style:** Underline-only. No background, no full border. 1px bottom border in Rule-Light. 10px / 0 / 12px padding. 16px / 400 weight body type, Ink color.
- **Focus:** A second 1px line in Ink animates in beneath the resting hairline (left-origin scaleX 0→1 over 300ms). The native focus ring is suppressed in favor of this treatment. Browser focus-visible rules apply elsewhere with the orange 2px / 3px outline.
- **Placeholder:** Ash at 45% opacity. Lower contrast than body text on purpose.
- **Labels:** Always visible above the field, never placeholder-only. 12px UPPERCASE / 0.06em / Ash.
- **Modal field grid:** Two-column row for Name + Email on tablet+, single column below 540px.

### Navigation

- **Style:** Sticky top, full-width, 72px tall. Ink background at 92% opacity with `backdrop-filter: saturate(140%) blur(10px)`. 1px Rule-Dark bottom border.
- **Brand:** 36px logo mark + stacked wordmark (15px name + 10px sub-line at 0.18em UPPERCASE, sub-line in Paper at 55% opacity).
- **Links:** 14px / 500 weight, Paper at 75% opacity, gap 32px. Hover lifts to full Paper.
- **CTA:** Ghost button (see above). Hidden while hero is in viewport.
- **Mobile (≤640px):** Links hide. Brand and ghost CTA remain.

### Modal

- **Backdrop:** Fixed inset, Ink at 72% opacity, 6px backdrop-blur.
- **Panel:** Paper background, 18px radius, 48px / 44px internal padding, max-width 580px, modal shadow (see Elevation).
- **Lock:** Body gets `overflow: hidden` while open.
- **Close:** 36px square ghost button, 8px radius, top-right inside panel.
- **Success state:** Animated SVG check (200/60 stroke-dasharray draw over 600ms with 400ms delay on the check), Persimmon stroke. The single largest moment of orange in the system.

### Reveal Animation

- Sections and cards opacity-0 + translateY(14px) at rest, animate to opacity-1 + translateY(0) when 10% visible. 700ms ease, single-fire (IntersectionObserver unobserves on enter). No parallax, no scroll-driven keyframes.

## 6. Do's and Don'ts

### Do:
- **Do** use Persimmon (`#FF6A2A`) on no more than one major element per fold.
- **Do** keep the system to a single typeface (Poppins). Hierarchy comes from weight, size, and tracking.
- **Do** apply negative letter-spacing (-0.01em to -0.025em) to every type role 22px and up.
- **Do** start every surface with `box-shadow: none`; add elevation only on hover, focus, or modal context.
- **Do** tint every neutral toward the brand hue. `#F6F6F4` paper and `#0D1321` ink are the floor; values closer to pure neutral are not in the system.
- **Do** keep the hero-aware nav CTA behavior. The ghost button entering on hero exit is a load-bearing brand move.
- **Do** keep section vertical rhythm at 100–120px desktop, 70px mobile. Don't compress to fit content; let the page breathe.
- **Do** specify content. "Twenty-one years in customer experience, most recently at T-Mobile" not "decades of experience." Specificity is part of the visual system.
- **Do** test every reveal animation against `prefers-reduced-motion`. The system honors the user's preference.

### Don't:
- **Don't** use `#fff` or `#000` in any new code. Every neutral must be tinted (`#F6F6F4` / `#0D1321` minimum).
- **Don't** use `border-left` or `border-right` greater than 1px as a colored side-stripe accent on cards, list items, or alerts. The current `.service::before` orange stripe is the only legacy instance and is a candidate for replacement at next polish; do not propagate the pattern.
- **Don't** use gradient text (`background-clip: text` over a gradient). Persimmon is solid, always.
- **Don't** use glassmorphism as a default surface treatment. The 10% backdrop-blur on the nav and the 6% on the modal backdrop are the system's only allowed instances.
- **Don't** ship the hero-metric template (big number + small label + supporting stats). It is the AI-startup template anti-reference.
- **Don't** add a second brand color. Persimmon is the only chromatic value. State (error, success, warning) carries through icon and copy, not through hue.
- **Don't** ship Awwwards-style scroll-jacking, kinetic-text headlines, marquee tickers, or hover gimmicks. The system explicitly rejects creative-studio portfolio aesthetics. (PRODUCT.md anti-reference: *creative-studio portfolios*.)
- **Don't** use stock photography of teams pointing at screens, abstract data swirls, or hands-on-keyboards. The system explicitly rejects big-consulting visual language. (PRODUCT.md anti-reference: *big-consulting sites*.)
- **Don't** add neon glow, holographic gradients, futuristic-sci-fi panel HUDs, or "protocol" framing. The system explicitly rejects the crypto / web3 reflex. (PRODUCT.md anti-reference: *crypto / web3 aesthetics*.)
- **Don't** mix in a second typeface (serif display, monospace caption, script flourish). Single-family Poppins is the rule.
- **Don't** use `min-height` on card headings to force grid parity. The current `.service h3 { min-height: 2.4em }` is a fragile patch; replace with content discipline (cap titles at 2 lines) at next polish.
- **Don't** use em dashes (`—`) anywhere in copy. (PRODUCT.md voice rule.)
