# Pillar Icons — Design Brief

Three custom marks for the **Approach** section of `index.html`: **01 Audit**, **02 Build**, **03 Operate**. They sit above each pillar heading, replacing the generic Feather/Lucide outline glyphs that used to live there.

This brief is the spec. If you ship three marks that meet it, the page levels up. If they fall short of the bar below, the numerals we shipped are a strong fallback and we can revert in 30 seconds.

## Why custom marks (the strategic stake)

PRODUCT.md design-principle-4: *"custom marks over icon-library SVGs"* is named as one of the largest premium signals on the page. With every other surface restrained and intentional, three off-the-shelf icons read as the page's most visible "AI services template" residue. Replacing them is the single biggest craft signal you can make without commissioning new photography.

DESIGN.md North Star is **Quiet Authority**. The marks must feel like a senior operator's working notation, not decoration. Premium = quietly expensive: tight, considered, deliberately reductive. They should look like the kind of thing you'd find in a Pentagram identity manual or an old IDEO process map, not in a SaaS hero.

## Hard rules — non-negotiable

- **Single set.** All three marks share one stroke width, one corner-radius treatment, one geometric vocabulary. They must read as siblings on first glance.
- **Geometric primitives only.** Circles, lines, rectangles, arcs, triangles. No freeform curves, no organic shapes, no hand-drawn quality.
- **Stroke-only, no fills.** Outline marks, like architecture drawings. Allows them to inherit `currentColor` and adapt to dark/light surfaces.
- **24×24 viewBox.** Even if drawn larger and scaled down, the final SVG `viewBox="0 0 24 24"`. Render targets: 16px (zoomed-out), 24px (default), 48px+ (zoomed-in). They must legibly hold all three sizes.
- **Symmetric or deliberately asymmetric.** No accidental visual weight imbalance. If a mark is asymmetric, it's *intentionally* weighted (audit can lean toward "discovery on the right" for example).
- **Pixel grid alignment.** Lines should sit on integer or half-integer coordinates so they render crisp at 24px (no blurry sub-pixel edges).

## Hard prohibitions — match-and-reject

If any of these appear in your sketch, throw it out and start over. They are the saturated 2024–2026 vocabulary every AI-services site ships.

- ✗ Magnifier with a `+` inside (every product audit icon since 2010)
- ✗ Stacked layered cubes / pancakes (every "build" icon)
- ✗ Circular-arrow / refresh loop (every "operate" icon)
- ✗ Gear (every "settings" icon, also reads as ops cliché)
- ✗ Lightbulb (every "discovery" icon)
- ✗ Isometric perspective (Stripe-clone trap)
- ✗ Floating dots / particles / connected nodes (AI-startup decoration)
- ✗ Smiley / emotion / face hints (consumer-app voice, wrong register)
- ✗ Anything that exists verbatim in Feather, Lucide, Heroicons, Tabler, Phosphor, or Material. **Literal check:** spot-search the libraries before committing to a direction.

## Concept direction per pillar

The metaphor must connect, but it must not be literal. Aim for the abstract operator vocabulary, not the dictionary illustration.

### 01 Audit
**What it represents:** locating where the work is, where it isn't, and what's worth touching. Discovery, calibration, mapping. Not "search."

Candidate metaphor families:
- A reticle / crosshair (calibration mark)
- A surveyed point — intersecting lines locating a coordinate
- Two contour lines and a single point of interest
- A topographic mark — concentric arcs converging
- A scribed line bisecting a region (boundary-drawing)
- A measure / scale fragment

What it should *feel* like: a surveyor's notation, not a detective's magnifying glass.

### 02 Build
**What it represents:** putting the right pieces together to do real work. Construction, assembly, integration.

Candidate metaphor families:
- Two or three modules joining at a clear seam
- Joinery — interlocking shapes meeting at a flush edge
- A bracket / fixture (something that holds two things together)
- A blueprint mark — a partial structural diagram
- An assembly indicator — components in registration

What it should *feel* like: a precision joint or a structural detail, not a stack of cubes.

### 03 Operate
**What it represents:** keeping it running, watching it, adjusting. Continuity, oversight, steady-state with intervention.

Candidate metaphor families:
- A pulse line / oscillation wave / heartbeat trace
- A gauge needle in a partial arc
- An orbit — a smaller mark circling a fixed center
- A sightline / observation marker
- A pendulum / rhythm indicator
- A horizon line with a marker

What it should *feel* like: a monitoring instrument or a watch face, not a circular arrow asking for retry.

## Technical specifications

### SVG markup template

```html
<svg viewBox="0 0 24 24" width="24" height="24" fill="none"
     stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
     aria-hidden="true">
  <!-- your paths / shapes here -->
</svg>
```

- `fill="none"` — outline-only.
- `stroke="currentColor"` — inherits the parent's color so we can recolor without editing the SVG.
- `stroke-linecap="round"` and `stroke-linejoin="round"` — soft terminations, matches the curve language already in use.
- `aria-hidden="true"` — the marks are decorative; the heading carries meaning. No alt text.
- Do **not** include `width="24" height="24"` if you want CSS to size them; do include if you want intrinsic size. The current pillar slot is fine either way.

### Stroke weight

Pick **one** of these and apply to all three marks:

- `stroke-width="1.5"` — refined, Linear-marketing register, premium-quiet
- `stroke-width="2"` — confident, more declarative, slightly louder
- **NOT** `stroke-width="1"` (too fragile at 16px), **NOT** `stroke-width="2.5"+` (too clunky for the page's discipline)

Recommended: **1.75** if you want the in-between, or **2** if you want the marks to hold their own next to the 60px Persimmon numerals.

### Color and integration

The pillar block currently leads with a Persimmon numeral (`01` / `02` / `03`). Two layout options for the icons:

#### Option A — Mark above numeral, mark in Ink

```html
<div class="pillar reveal">
  <div class="pillar-mark" aria-hidden="true">
    <svg viewBox="0 0 24 24" ...>...</svg>
  </div>
  <div class="pillar-num" aria-hidden="true">01</div>
  <h3>Audit</h3>
  <p>...</p>
</div>
```

```css
.pillar-mark {
  width: 32px;
  height: 32px;
  color: var(--navy);
  margin-bottom: 18px;
}
.pillar-mark svg { width: 100%; height: 100%; }
```

Pros: numeral stays as the loud move; mark is the quiet metaphor; two distinct register elements. Premium-editorial.

#### Option B — Mark replaces numeral, mark in Persimmon

```html
<div class="pillar reveal">
  <div class="pillar-mark" aria-hidden="true">
    <svg viewBox="0 0 24 24" ...>...</svg>
  </div>
  <h3>Audit</h3>
  <p>...</p>
</div>
```

```css
.pillar-mark {
  width: 56px;
  height: 56px;
  color: var(--orange);
  margin-bottom: 22px;
}
.pillar-mark svg { width: 100%; height: 100%; }
```

Pros: simpler. The mark IS the loud move. Closer to the original page rhythm before numerals.

**Recommended:** **Option A.** The numerals already work; the marks add metaphor on top without competing for the same loud-move slot.

### Sizing across breakpoints

The marks need to read clearly at the rendered sizes:
- Desktop pillar card: ~32px (Option A) or ~56px (Option B)
- Mobile pillar card (≤640px, single-column): same — pillar cards stack but card width grows, sizes hold

Test by exporting the SVG at 16px, 24px, 32px, 48px, 64px and confirming readability and crispness at each.

## Quality bar — acceptance criteria

A mark passes when:

1. **Sibling test.** Place all three side by side at 32px. They feel like one set — same weight, same vocabulary, same level of abstraction. If one mark is detailed and another is sparse, the set is failing.
2. **Reduction test.** Render at 16px. Each mark is still legible — readable as the same shape it was at 64px. Lose-no-detail scaling.
3. **Slop test.** Search Feather, Lucide, Heroicons, Tabler, Phosphor for "audit" / "build" / "operate" / "monitor" / "settings" / "search" / "construct." Your marks must look meaningfully different from every result.
4. **Metaphor test.** Show all three marks (without labels) to a colleague. They guess "discovery, construction, monitoring" — or "looking, making, watching" — with the same general direction. If they guess literal nouns ("magnifier, blocks, refresh"), the marks fell into clichés.
5. **Discipline test.** Match against PRODUCT.md North Star. Would these marks live comfortably on a Linear marketing page or a Pentagram identity book? If they'd look more at home on a SaaS dashboard, refine.

If the marks pass 5/5, ship them. If they pass 3-4/5, iterate. If 0-2/5, revert to the numerals — they're a strong B+ baseline.

## References — aim at these

The vocabulary you want to channel, in rough order of fit:

- **Pentagram identity systems** — Penguin Books, Mastercard rebrand era. Geometric reduction, named-element marks.
- **Linear's marketing pages** — single-weight, single-color, ruthless geometric simplicity.
- **ABC Dinamo / Klim Type Foundry specimen pages** — small geometric typographic ornaments used as section markers.
- **Saul Bass / Paul Rand corporate marks** — mid-century abstraction; the IBM 8-bar logo era.
- **Late-mid-century industrial design diagrams** — Dieter Rams' Braun product diagrams; technical drawings as art direction.

Don't aim at:

- Stripe's icon library (saturated)
- Notion's icon set (saturated)
- Material Symbols (consumer)
- Phosphor / Tabler / Heroicons (icon-library default)
- Anything labeled "AI" or "automation" on Behance or Dribbble in 2024-2026

## Process suggestion

1. Sketch on paper or in any tool — get to 6-8 candidates per pillar fast.
2. Pick the strongest one per pillar based on the *sibling test* across the set. Often the first instinct is wrong; the third or fourth iteration finds the geometric vocabulary that ties them together.
3. Vectorize. Snap to the 24×24 grid. Keep stroke widths consistent across all three.
4. Export as inline SVG strings (not files; we paste them straight into the markup).
5. Drop them into the page using one of the two integration options above and view in the browser.
6. Audit against the 5 quality-bar tests.
7. Ship or iterate.

## Drop-in slot

When the marks are ready, the integration is three edits in `index.html` — one per pillar. Replace the `<div class="pillar-num" aria-hidden="true">01</div>` block with the chosen layout (numeral + mark, or mark only) per the integration spec above.

If you go with Option A, also add the `.pillar-mark` CSS rule to the `<style>` block (the current `.pillar-num` rule stays).

If anything is unclear, drop the marks into the page and we'll iterate together.

## Fallback

The current Persimmon-numeral pillars are the working baseline. If your custom marks don't pass the quality bar, the page is shippable as-is. Reverting is a 30-second swap, no data loss. Don't ship marks that don't clear the bar — three off-the-shelf icons would have done less damage than three almost-good custom ones.
