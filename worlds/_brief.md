# Seven Worlds: shared brief for poster designers

You are a senior graphic designer and motion designer working in hand-written SVG, CSS and a little vanilla JavaScript. No libraries, no raster images, no stock photos, no AI-generated media, no emoji, no icon sets. Google Fonts via `<link>` are allowed.

## What this is
Perseid Echo Creations (PEC) is a one-person studio (Bryan) doing marketing and operations work for small businesses. Its front page is seven "worlds", one per service. Each world is a full poster in its OWN graphic-design tradition, so the seven look dramatically different from each other. One thing is constant: a single spark (a Perseid meteor, persimmon #FF6A2A) flies into every poster from the LEFT edge and BECOMES something native to that world. The moment it becomes that thing, two or three thin "echo" rings ripple outward. A visitor who has never heard of PEC should understand the service at a glance and think "these people can really design".

## The bar to match
World 01 (Cold Email) is finished. Before you design anything, look at it with the Read tool:
- Final poster: `C:\Projects\PEC-accordion-preview\site\worlds\shots\cold-email-b.png`
- Mid-animation frame: `C:\Projects\PEC-accordion-preview\site\worlds\shots\anim-t0.7.png`
- Source, for technique (how it animates and exposes its controls): `C:\Projects\PEC-accordion-preview\site\worlds\cold-email-b-anim.html` (large; skim the `<style>` and `<script>`, do not copy its look)

Your poster must be at least that good, and must NOT look like it: different ground, different tradition, different rhythm. What carries over is only the craft level, the palette discipline and the block described below.

## Fixed rules for every poster
- Canvas exactly 1440 x 900, `html,body{margin:0;overflow:hidden}`, one self-contained HTML file.
- Palette: ink #0D1321, paper #F6F6F4, persimmon #FF6A2A, plus the ground color named in your world brief and tints of these. No other hues.
- The poster is shown on the site at about 80% size, so nothing smaller than 11px, and hairlines no thinner than 1px.
- Title block, lower left, same structure on every poster so the set feels related: a small label `0N` followed by a short rule and `SERVICE <word> OF SEVEN` in small tracked caps; then the service name as a very large heading in Archivo 800 uppercase with tight tracking; then the one-line description given in your world brief in Archivo 400 around 20px. Keep clear space around it. Nothing may collide with it.
- Copy: use the given text exactly. American English. No em dashes anywhere. No invented statistics, prices, client names or testimonials.
- Scale contrast: one huge hero element, a few small precise details that reward a close look, a clear grid, elements cropping off the frame edges, generous empty ground. No decorative gradients, no rounded "app" cards, no glassmorphism, no drop-shadow-everything, no clip art.
- The spark and its echo rings are the only persimmon things that glow, and only slightly.

## Animation (the poster makes itself, then holds)
- One self-playing animation of about 3.2 seconds that builds the poster from its bare ground to the finished poster, then holds. The spark enters from the left edge early, travels across, and at roughly 1.3 to 1.6s becomes the world's thing with the echo rings. The big heading arrives late (about 1.7 to 2.5s), small details last. Overlap beats so it reads as one continuous motion. Confident easing, nothing bouncy or cute.
- Animate only transform, opacity, clip-path and stroke-dashoffset. Keep heavy SVG filters on static groups.
- Controls, identical on every poster:
  - CSS animations run only under a class on the root (e.g. `.play`); `window.play()` restarts from the start (remove class, force reflow, add class); `window.finish()` jumps to the final state.
  - `window.addEventListener('message', e => { if (e.data === 'play') play(); if (e.data === 'finish') finish(); })`
  - Auto-play on load.
  - `?t=<seconds>` freezes the animation at that time (pause all animations and set their currentTime), for stills.
  - `prefers-reduced-motion: reduce` shows the finished poster immediately.

## How to work
1. Design the FINAL poster first as static SVG. Screenshot it and critique it like an art director. Do at least three look-and-fix rounds before animating. Check for clipped or overlapping text, weak hierarchy, crooked alignment, anything that looks like a diagram instead of a poster.
2. Then add the animation and the controls.
3. Verify by looking. Headless Chrome is at `C:\Program Files\Google\Chrome\Application\chrome.exe`:
   `chrome.exe --headless=new --hide-scrollbars --window-size=1440,900 --virtual-time-budget=3000 --screenshot=<png path> "file:///C:/Projects/PEC-accordion-preview/site/worlds/<slug>.html?t=0.7"`
   Save frames to `C:\Projects\PEC-accordion-preview\site\worlds\shots\<slug>-t0.1.png`, `-t0.8.png`, `-t1.5.png`, `-t2.2.png` and `<slug>-final.png` (use `?t=5`). Open each with the Read tool. Confirm: the early frame is mostly bare ground; the spark is visible in flight; the hero is absent before the spark arrives and present after; echo rings show just after; the final frame is complete with no missing pieces. Also load without `?t` using `--virtual-time-budget=6000` and confirm it ends complete.
4. Shell note: on this Windows machine bash heredocs eat backslashes. Write files with the Write and Edit tools. If you use a generator script, keep it in the project at `site/worlds/_src/<slug>.py`.
5. Touch only your own files: `site/worlds/<slug>.html`, `site/worlds/_src/<slug>.*`, and `site/worlds/shots/<slug>-*.png`.

## Report back
The file path, the frame screenshots you checked, the exact time the spark becomes the world's thing, and two or three honest sentences on what is still weak.
