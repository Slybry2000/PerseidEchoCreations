# Art Bible — Perseid Echo Creations (Image-First Edition)

The binding spec for every section of this site. If a section breaks any rule below, the section is wrong, not the rule.

## 1. Voice & Feel

Quiet Authority. The page of a senior operator who has earned the right to be direct. Premium through what is left out, not what is added. Confidence signaled by restraint: one accent color, one loud move per surface, more white space than content. If this page could appear in a portfolio of AI-startup landing pages without comment, the design has failed.

The hero is the brand argument. A cropped operator's hand, marking up a printed spreadsheet on a wooden desk in a navy-walled office. No face, no robotic glow, no neural-network graphic. The photograph says "operator, doing the work" without selling a face.

## 2. Palette

| Token | Hex | Usage rule | Forbidden combos |
|---|---|---|---|
| Ink | `#0D1321` | Hero scrim, About surface, ink-deeper footer, primary text on Paper | Never paired with pure `#000` |
| Ink Deeper | `#08101F` | Footer only | — |
| Ash | `#3A4152` | Body text on Paper, eyebrow labels, secondary copy | Never used as a background fill |
| Paper | `#F6F6F4` | Default light surface, primary text on Ink | Never paired with pure `#fff` as a screen background |
| Paper Dim | `#ECEAE5` | Services section only (rhythm flip) | — |
| Surface Card | `#FFFFFF` | Service-card fill only — never a screen background | — |
| Persimmon | `#FF6A2A` | The one accent. Hero rule, italic emphasis word, primary CTA, service bullets, focus ring, ::selection | Never paired with a second chromatic color |
| Persimmon Deep | `#E15517` | Primary CTA hover only | — |
| Rule Light | `rgba(13,19,33,0.10)` | Hairline rules and card borders on Paper | — |
| Rule Dark | `rgba(246,246,244,0.14)` | Hairline rules on Ink surfaces | — |

**The 10% Rule.** Persimmon may occupy no more than 10% of the visible viewport at any scroll position.
**The No-Pure Rule.** `#fff` and `#000` are forbidden except `Surface Card` as a card fill.
**The One Accent Rule.** Persimmon is the only chromatic color. State (error/success) carries through weight, icon, and copy — never hue.

## 3. Typography

- **Display:** `Poppins SemiBold (600)`. Geometric sans, operator-grade. Tight tracking at -0.025em to -0.03em for any role 22px+.
- **Body:** `Poppins Regular (400)`. Normal tracking. 16px base, 1.6 line-height.
- **Meta:** `Poppins Medium (500)` UPPERCASE at wide tracking. All eyebrows, index markers, service numbers, footer copy. 11–13px, 0.18–0.22em tracking. **Single-family rule** — no second typeface anywhere on this site.

### Scale

| Role | Spec | Where |
|---|---|---|
| Hero Display | `clamp(46px, 6.8vw, 84px)` / 600 / -0.03em / 0.98 lh | Three-line headline only |
| Section h2 | `clamp(34px, 4.6vw, 60px)` / 600 / -0.025em / 1.04 lh | Section headings |
| Quote display | `clamp(28px, 3.6vw, 48px)` / 500 / -0.02em / 1.18 lh | Pull quote |
| Approach h3 | `clamp(24px, 2.4vw, 32px)` / 600 / -0.02em | Approach row headings |
| Service title | `clamp(20px, 1.8vw, 24px)` / 600 / -0.015em | Service card title |
| Body Large | 17px / 400 / 1.7 lh | About paragraphs, contact copy |
| Body | 16px / 400 / 1.65 lh | Default paragraph |
| Body Small | 15px / 400 / 1.6 lh | Service body, about pillars |
| Eyebrow | 11px / mono 500 / 0.20em / UPPERCASE | All section eyebrows |

### Type rules

- **Single-display rule.** Poppins SemiBold for every display role. No second display family. No serif italic flourish.
- **Italic accent rule.** One italic word per surface, in Persimmon, only on section h2 or pull quote. Never in body copy.
- **Tight-display rule.** Every role ≥22px uses negative letter-spacing.
- **Eyebrow rule.** Eyebrows are always mono 500, 11px, 0.20em, UPPERCASE, Ash. No sentence-case eyebrows.

### Banned words

`transform`, `unlock`, `leverage`, `synergy`, `next-generation`, `cutting-edge`, `world-class`, `agentic` (as decoration), `in today's fast-moving landscape`. No em dashes anywhere in copy — use commas, colons, semicolons, periods, parentheses.

### Preferred verbs

`build`, `ship`, `run`, `operate`, `audit`, `retrofit`, `integrate`.

## 4. Spacing & Layout

- **Base unit:** 8px. All padding/margin in multiples of 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 / 128.
- **Container:** `--max: 1440px`, `--content-max: 1200px`.
- **Gutter:** `clamp(24px, 5vw, 72px)`.
- **Section rhythm:** `clamp(80px, 10vw, 140px)` vertical padding on every section. Don't compress.

### Composition principle (load-bearing)

**Hero content lives top-right. CTA lives bottom-right. Index marker lives bottom-left. Three separate vertical bands so nothing collides at any viewport width.** This is the photograph's compositional contract — disrupting it disrupts the brand.

Downstream sections rotate the anchor:
- Approach: centered head, left-anchored rows
- Services: left-anchored head, two-up cards
- Quote: left-anchored block
- About: portrait left, body right (ink surface)
- Contact: copy left, form right

## 5. Components

### Wordmark
- `<a class="wordmark">` with 26×26 mark + 12px Poppins SemiBold tracked at 0.20em.
- Always paper-white on Ink, never inverted onto Paper without a contrast check.

### Ghost CTA (hero)
- 1px paper at 42% opacity border, 4px radius, 11/18px padding, 13px / 600 / 0.04em.
- Hover: border opacity → 1.0, faint paper-tinted fill, translateY(-1px).
- Always placed as a composition element, never inline with the headline.

### Primary CTA (contact)
- Persimmon fill, Ink text, 8px radius, 14/24px padding, 14px / 600.
- Hover: Persimmon Deep + translateY(-1px). Used once per page.

### Service card
- White fill on Paper Dim, 14px radius, 1px Rule-Light border.
- Explicit grid: `60px minmax(0, 1fr)` cols, four rows; **no auto-flow** anywhere on the card.
- Hover: translateY(-3px), border darkens to 0.18 ink, soft 18/38 ink shadow at 6% opacity.

### Approach row
- Editorial list, NOT a 3-column card grid.
- `80px minmax(0, 1fr)` cols. Hairline top + bottom rules. Number turns Persimmon on hover.

### Pull quote
- Quote in Display 500 italic on accent word.
- Byline in mono 500, role beneath in mono Ash.

### Field input
- Underline-only. No background, no full border. Bottom-border in Rule-Light, focuses to Ink.
- Labels always visible above field in mono 11px / 0.18em / UPPERCASE / Ash.

## 6. Imagery & Motion

- **Hero crop logic:** Tight architectural crop. Hand-only, no face. Wide establishing shots read as stock — banned.
- **Color grade:** Late-golden-hour warm with deep navy plaster shadow. 4200K. No teal-orange grade.
- **Grain:** Subtle 35mm at ~6%. No film simulation that introduces a second hue.
- **Motion budget:** Reveal animation only — 14px translateY fade, 700ms ease, single-fire, threshold 12%. No parallax, no scroll-driven keyframes, no kinetic typography.
- **Optional Seedance:** If the hero gets video, motion stays under 5% of frame at any moment — pen micro-motion, light creep, grain breathing. Locked-off camera. `prefers-reduced-motion` falls back to the still.

## 7. Forbidden Patterns

1. **Gradient blob hero** with glowing nodes or neon-on-black.
2. **"Powered by GPT" badge** or any LLM-vendor chip.
3. **Hero-metric template** (big number + small label + supporting stats).
4. **Three-column SaaS feature grid** with icon-circle + title + subtitle.
5. **Trusted-by logo carousel** of fictional or generic logos.
6. **Glassmorphism** beyond the existing 10% blur on the hero nav (which is implicit, not chrome).
7. **Awwwards-style scroll-jacking, marquee tickers, kinetic-text reveals.**
8. **Stock photography of teams pointing at screens, abstract data swirls, robotic hands.**
9. **Em dashes anywhere in copy.** Use commas, colons, periods.
10. **A second brand color.** Persimmon is the only chromatic value.
11. **Pure `#fff` or `#000`** in tokens or rules. Tinted neutrals only.
12. **Borrowed display fonts** (serif display, mono-as-display, script). Single-family Poppins.
13. **Border-left side stripes** on cards or alerts to denote category. Hairline rules only.
14. **Centered hero with two CTAs.** This page only has one CTA in the hero, and it's a ghost button placed as composition.
