#!/usr/bin/env python3
"""Generator for worlds/social.html (World 02, SOCIAL MEDIA, street poster).
Run: python site/worlds/_src/social.py
"""
import math, random, os

INK = "#0D1321"; PAPER = "#F6F6F4"; PERS = "#FF6A2A"
random.seed(11)

# ---------- halftone ----------
LX, LY = 965.0, 372.0          # landing point = heart centre = lattice origin
P = 13.0                       # nearest-neighbour dot spacing (45 degree screen)
S = P / math.sqrt(2)

BX0, BY0, BX1, BY1, BR = 540.0, 172.0, 1390.0, 566.0, 118.0
TAIL = [(800, 540), (936, 540), (772, 712)]
SH = (15.0, 15.0)              # printed shadow offset
HS = 96.0                      # heart scale
HCX, HCY = LX, LY + 0.14 * HS

def in_round(x, y, x0, y0, x1, y1, r):
    if x < x0 or x > x1 or y < y0 or y > y1:
        return False
    cx = min(max(x, x0 + r), x1 - r); cy = min(max(y, y0 + r), y1 - r)
    return (x - cx) ** 2 + (y - cy) ** 2 <= r * r

def in_tri(x, y, t):
    (x1, y1), (x2, y2), (x3, y3) = t
    d = (y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3)
    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / d
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / d
    c = 1 - a - b
    return a >= 0 and b >= 0 and c >= 0

def in_body(x, y, dx=0.0, dy=0.0):
    x -= dx; y -= dy
    return in_round(x, y, BX0, BY0, BX1, BY1, BR) or in_tri(x, y, TAIL)

def in_heart(x, y):
    u = (x - HCX) / HS; v = -(y - HCY) / HS
    return (u * u + v * v - 1) ** 3 - u * u * v ** 3 <= 0

def cover(fn, x, y, n=3):
    c = 0
    for i in range(n):
        for j in range(n):
            c += fn(x + (i + .5) / n * P - P / 2, y + (j + .5) / n * P - P / 2)
    return c / (n * n)

def dots():
    ink, paper = [], []
    rng = 52
    for i in range(-rng, rng):
        for j in range(-rng, rng):
            x = LX + (i + j) * S; y = LY + (i - j) * S
            if x < 520 or x > 1425 or y < 150 or y > 705:
                continue
            if i == 0 and j == 0:
                continue
            t = ((x - BX0) / (BX1 - BX0) * .55 + (y - BY0) / (BY1 - BY0) * .45)
            t = min(max(t, 0), 1)
            ch = cover(in_heart, x, y)
            cb = cover(in_body, x, y)
            cs = cover(lambda a, b: in_body(a, b, *SH), x, y)
            d = math.hypot(x - LX, y - LY)
            if ch > 0.02:
                tone = (0.66 + 0.32 * (1 - t)) * ch
                r = min(P * math.sqrt(tone / math.pi), P * .53)
                if r > .8:
                    paper.append((x, y, r, d))
            ink_c = max(cb - ch, 0)
            if ink_c > 0.02:
                tone = (0.36 + 0.62 * t ** 1.05) * ink_c
                r = min(P * math.sqrt(tone / math.pi), P * .53)
                if r > .8:
                    ink.append((x, y, r, d))
            elif cb < .98 and cs > 0.02:
                tone = 0.36 * cs * (1 - cb)
                r = P * math.sqrt(tone / math.pi)
                if r > .8:
                    ink.append((x, y, r, d))
    return ink, paper

ink_d, paper_d = dots()
DMAX = max(d for *_, d in ink_d + paper_d)
NB = 46
def band(d): return min(int(d / DMAX * NB), NB - 1)
def delay(b): return 1.46 + 1.05 * (b / (NB - 1)) ** 0.9

def layer(items, cls):
    bands = {}
    for x, y, r, d in items:
        bands.setdefault(band(d), []).append((x, y, r))
    out = []
    for b in sorted(bands):
        cs = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.2f}"/>' for x, y, r in bands[b])
        out.append(f'<g class="{cls}" style="--dl:{delay(b):.3f}s">{cs}</g>')
    return "".join(out)

ink_svg = layer(ink_d, "bd")
paper_svg = layer(paper_d, "bd")

# ---------- bills ----------
def heart_path(cx, cy, s):
    # small heart from two arcs and a point
    return (f"M{cx:.1f},{cy + s*.95:.1f} C{cx - s*1.7:.1f},{cy - s*.1:.1f} {cx - s*.9:.1f},{cy - s*1.2:.1f} {cx:.1f},{cy - s*.35:.1f} "
            f"C{cx + s*.9:.1f},{cy - s*1.2:.1f} {cx + s*1.7:.1f},{cy - s*.1:.1f} {cx:.1f},{cy + s*.95:.1f}Z")

def bill(i):
    W, H = 118, 158
    inv = i % 4 == 1
    g = INK if inv else PAPER
    f = PAPER if inv else INK
    x = -34 + i * 128 + random.uniform(-3, 3)
    y = -22 + random.uniform(-8, 3)
    rot = random.uniform(-.9, .9)
    v = i % 4
    s = []
    torn = i == 5
    if torn:
        pts = [(0, 0), (W, 0), (W, 146)]
        x_ = W
        while x_ > 0:
            x_ -= random.uniform(5, 11)
            pts.append((max(x_, 0), 146 + random.uniform(-6, 8)))
        pts.append((0, 150))
        body = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + "Z"
        under = "M" + " L".join(f"{a:.1f},{b + 4 + random.uniform(0, 4):.1f}" for a, b in pts[2:]) + f" L0,0 L{W},0Z"
        s.append(f'<path d="{under}" fill="#E4E2DB"/>')
        s.append(f'<path d="{body}" fill="{g}"/>')
    else:
        s.append(f'<rect width="{W}" height="{H}" fill="{g}"/>')
    # header band
    s.append(f'<rect x="0" y="26" width="{W}" height="26" fill="{f}"/>')
    s.append(f'<text x="10" y="44" font-size="13" font-weight="800" letter-spacing="1.6" fill="{g}">WK {i+1:02d}</text>')
    s.append(f'<circle cx="{W-14}" cy="39" r="4.5" fill="{PERS}"/>')
    # graphic
    if v == 0:
        s.append(f'<rect x="10" y="62" width="98" height="46" rx="12" fill="{f}"/>')
        s.append(f'<path d="M26,106 L26,120 L44,106Z" fill="{f}"/>')
        s.append(f'<path d="{heart_path(59, 83, 9)}" fill="{g}"/>')
    elif v == 1:
        for a in range(8):
            for b in range(4):
                r = 1.2 + (a / 7) * 2.9 + b * .1
                s.append(f'<circle cx="{16 + a*12.2:.1f}" cy="{68 + b*13:.1f}" r="{r:.2f}" fill="{f}"/>')
    elif v == 2:
        s.append(f'<circle cx="59" cy="85" r="25" fill="{f}"/>')
        s.append(f'<circle cx="59" cy="85" r="34" fill="none" stroke="{f}" stroke-width="1.5"/>')
    else:
        s.append(f'<rect x="10" y="62" width="98" height="46" fill="{f}"/>')
        s.append(f'<path d="{heart_path(59, 84, 12)}" fill="{g}"/>')
    # text lines
    s.append(f'<text x="10" y="128" font-size="11" font-weight="800" letter-spacing="1.4" fill="{f}">OUT NOW</text>')
    s.append(f'<rect x="10" y="136" width="{72 if i%2 else 56}" height="3" fill="{f}"/>' if not torn else "")
    s.append(f'<rect x="10" y="143" width="{34 if i%3 else 46}" height="3" fill="{f}"/>' if not torn else "")
    # misregistered overprint: persimmon-dark ghost of band
    s.append(f'<rect x="2" y="28" width="{W}" height="26" fill="{INK}" opacity=".10"/>' if not inv else "")
    # wrinkle / curl / tape
    extra = []
    if i == 8:
        extra.append(f'<path d="M-4,30 L{W+4},96" stroke="{INK}" stroke-width="1.2" opacity=".28"/>'
                     f'<path d="M-4,32 L{W+4},98" stroke="{PAPER}" stroke-width="1.5" opacity=".55"/>'
                     f'<path d="M30,0 L{W-10},158" stroke="{INK}" stroke-width="1" opacity=".16"/>'
                     f'<path d="M31.5,0 L{W-8.5},158" stroke="{PAPER}" stroke-width="1" opacity=".4"/>')
    if i == 2:
        extra.append(f'<path d="M{W},{H-26} L{W-26},{H} L{W},{H}Z" fill="{PERS}"/>'
                     f'<path d="M{W},{H-26} L{W-26},{H} L{W-26},{H-26}Z" fill="#DAD8D1"/>')
    if i in (0, 5, 10):
        extra.append(f'<rect x="{W-46}" y="2" width="56" height="17" fill="{PAPER}" opacity=".62" transform="rotate(34 {W-18} 10)"/>')
    if i in (3, 7):
        extra.append(f'<rect x="-14" y="2" width="50" height="16" fill="{PAPER}" opacity=".6" transform="rotate(-32 8 10)"/>')
    return (f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.2f})"><g class="bill" style="--i:{i}">'
            f'<rect x="3" y="3" width="{W}" height="{H}" fill="{INK}" opacity=".16"/>' + "".join(s) + "".join(extra) + '</g></g>')

bills = "".join(bill(i) for i in range(12))

# ---------- wall texture ----------
wrinkles = []
for (x0, y0, x1, y1, o) in [(-20, 250, 700, 190, .20), (300, 910, 1100, 430, .12), (820, -20, 1500, 520, .10),
                            (-20, 600, 420, 930, .14), (1200, 640, 1460, 560, .12)]:
    mx = (x0 + x1) / 2 + random.uniform(-40, 40); my = (y0 + y1) / 2 + random.uniform(-30, 30)
    wrinkles.append(f'<path d="M{x0},{y0} Q{mx:.0f},{my:.0f} {x1},{y1}" stroke="{INK}" stroke-width="1.4" opacity="{o}" fill="none"/>'
                    f'<path d="M{x0},{y0+2.2} Q{mx:.0f},{my+2.2:.0f} {x1},{y1+2.2}" stroke="{PAPER}" stroke-width="1.6" opacity="{o*2.2:.2f}" fill="none"/>')
streaks = []
for k in range(14):
    yy = random.uniform(20, 880); x0 = random.uniform(-200, 900); ln = random.uniform(300, 900)
    streaks.append(f'<rect x="{x0:.0f}" y="{yy:.0f}" width="{ln:.0f}" height="{random.uniform(5,16):.0f}" fill="#FF8A55" opacity="{random.uniform(.10,.22):.2f}"/>')

# ---------- stencil text ----------
html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=1440">
<title>PEC World 02 Social Media</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;700;800&family=Saira+Stencil+One&display=swap" rel="stylesheet">
<style>
html,body{{margin:0;overflow:hidden;background:{PERS}}}
svg{{display:block;width:1440px;height:900px}}
text{{font-family:'Archivo',Helvetica,Arial,sans-serif}}
.sten{{font-family:'Saira Stencil One','Archivo',sans-serif;font-weight:400}}
.fb,.lg,.bill,.bd circle,.land,.rg,.hd,.hd-g,.lab,.desc,.sten-w,.mk{{transform-box:fill-box;transform-origin:center}}
.spark{{offset-path:path('M-60 318 C 220 150, 520 560, {LX:.0f} {LY:.0f}');offset-rotate:auto;offset-distance:100%;opacity:0}}
.mix{{mix-blend-mode:multiply}}
/* final state is the default. Animations run only under .play */
@keyframes fly{{from{{offset-distance:0%;opacity:1}}to{{offset-distance:100%;opacity:1}}}}
@keyframes sparkend{{0%,94%{{opacity:1}}100%{{opacity:0}}}}
@keyframes slap{{0%{{opacity:0;transform:translateY(-34px) scale(1.2)}}55%{{opacity:1}}100%{{opacity:1;transform:none}}}}
@keyframes dotin{{from{{opacity:0;transform:scale(0)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes landin{{from{{opacity:0;transform:scale(2.4)}}to{{opacity:1;transform:scale(1)}}}}
@keyframes lglow{{0%{{opacity:0;transform:scale(.3)}}14%{{opacity:.6;transform:scale(1)}}100%{{opacity:.14;transform:scale(1)}}}}
@keyframes ring{{0%{{opacity:0;transform:scale(.03)}}10%{{opacity:1}}100%{{opacity:0;transform:scale(1)}}}}
@keyframes slam{{0%{{opacity:0;transform:scale(1.09)}}30%{{opacity:1}}100%{{opacity:1;transform:scale(1)}}}}
@keyframes reg{{0%{{opacity:0;transform:translate(-14px,9px)}}100%{{opacity:.3;transform:none}}}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(10px)}}to{{opacity:1;transform:none}}}}
@keyframes rule{{from{{transform:scaleX(0)}}to{{transform:scaleX(1)}}}}
@keyframes wipeX{{from{{clip-path:inset(0 100% 0 0);opacity:.2}}to{{clip-path:inset(0 0 0 0);opacity:1}}}}
@keyframes fade{{from{{opacity:0}}to{{opacity:1}}}}
.play .spark{{animation:fly 1.08s cubic-bezier(.32,.04,.16,1) .32s both, sparkend 1.08s linear .32s both}}
.play .bill{{animation:slap .3s cubic-bezier(.2,.85,.25,1) calc(.08s + var(--i)*.068s) both}}
.play .bd circle{{animation:dotin .36s cubic-bezier(.2,.8,.25,1) var(--dl) both}}
.play .land{{animation:landin .2s cubic-bezier(.2,.9,.3,1) 1.38s both}}
.play .lg{{animation:lglow 1.7s ease-out 1.38s both}}
.play .rg{{animation:ring 1.25s cubic-bezier(.15,.6,.3,1) both}}
.play .rg.r1{{animation-delay:1.40s}}.play .rg.r2{{animation-delay:1.56s}}.play .rg.r3{{animation-delay:1.72s}}
.play .hd{{animation:slam .24s cubic-bezier(.2,.9,.2,1) 1.78s both}}
.play .hd2{{animation-delay:1.9s}}
.play .hd-g{{animation:reg .5s ease-out 1.92s both}}
.play .hd-g2{{animation-delay:2.04s}}
.play .lab{{animation:fadeUp .3s ease-out 1.72s both}}
.play .lab-r{{transform-origin:left center;animation:rule .35s cubic-bezier(.3,.6,.2,1) 1.72s both}}
.play .desc{{animation:fadeUp .4s ease-out 2.4s both}}
.play .sten-w{{animation:wipeX .5s cubic-bezier(.3,.6,.2,1) 2.62s both}}
.play .mk{{animation:fade .4s ease-out calc(2.85s + var(--k)*.08s) both}}
@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}.spark{{display:none!important}}}}
</style></head>
<body><svg id="root" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900">
<defs>
 <filter id="mott" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.0055 0.011" numOctaves="3" seed="4" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 .05  0 0 0 0 .07  0 0 0 0 .13  1.5 0 0 0 -.62"/>
 </filter>
 <filter id="mott2" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.009 0.02" numOctaves="2" seed="21" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 .97  0 0 0 0 .97  0 0 0 0 .96  0 1.6 0 0 -.74"/>
 </filter>
 <filter id="grain" x="0" y="0" width="100%" height="100%">
  <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="2" seed="9" result="n"/>
  <feColorMatrix in="n" type="matrix" values="0 0 0 0 .05  0 0 0 0 .07  0 0 0 0 .13  0 0 0 1.1 -.42"/>
 </filter>
 <filter id="rough" x="-2%" y="-10%" width="104%" height="120%">
  <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="2.2" xChannelSelector="R" yChannelSelector="G" result="d"/>
  <feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves="2" seed="17" result="s"/>
  <feColorMatrix in="s" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -5 3.6" result="m"/>
  <feComposite in="d" in2="m" operator="in"/>
 </filter>
 <filter id="inkrough" x="-1%" y="-3%" width="102%" height="106%">
  <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="2" seed="6" result="t"/>
  <feDisplacementMap in="SourceGraphic" in2="t" scale="1.6" xChannelSelector="R" yChannelSelector="G"/>
 </filter>
 <radialGradient id="glow"><stop offset="0" stop-color="{PAPER}" stop-opacity="1"/><stop offset=".3" stop-color="{PAPER}" stop-opacity=".5"/><stop offset="1" stop-color="{PAPER}" stop-opacity="0"/></radialGradient>
 <linearGradient id="tail" x1="0" x2="1"><stop offset="0" stop-color="{PAPER}" stop-opacity="0"/><stop offset="1" stop-color="{PAPER}" stop-opacity=".95"/></linearGradient>
</defs>

<!-- WALL -->
<rect width="1440" height="900" fill="{PERS}"/>
<g>{"".join(streaks)}</g>
<rect x="0" y="0" width="520" height="900" fill="#F2601F" opacity=".35"/>
<rect x="520" y="0" width="2" height="900" fill="{INK}" opacity=".16"/>
<rect x="522" y="0" width="2" height="900" fill="{PAPER}" opacity=".30"/>
<rect width="1440" height="900" filter="url(#mott)" opacity=".24"/>
<rect width="1440" height="900" filter="url(#mott2)" opacity=".16"/>
<g fill="none">{"".join(wrinkles)}</g>

<!-- SMALL BILLS, row along the top -->
<g font-family="Archivo,Helvetica,Arial,sans-serif">{bills}</g>

<!-- HALFTONE (misregistered: paper plate sits 3px off the ink plate) -->
<g id="ht">
 <g fill="{INK}">{ink_svg}</g>
 <g fill="{PAPER}" transform="translate(3 -2)">{paper_svg}</g>
</g>

<!-- LANDING DOT + ECHO RINGS -->
<g>
 <circle class="lg" cx="{LX}" cy="{LY}" r="46" fill="url(#glow)"/>
 <circle class="land" cx="{LX}" cy="{LY}" r="6.9" fill="{PAPER}"/>
 <g fill="none">
  <circle class="rg r1" cx="{LX}" cy="{LY}" r="330" stroke="{PAPER}" stroke-width="7" opacity="0" style="stroke-opacity:.18"/>
  <circle class="rg r1" cx="{LX}" cy="{LY}" r="330" stroke="{PAPER}" stroke-width="1.6" vector-effect="non-scaling-stroke" opacity="0"/>
  <circle class="rg r2" cx="{LX}" cy="{LY}" r="330" stroke="{PAPER}" stroke-width="1.4" vector-effect="non-scaling-stroke" opacity="0"/>
  <circle class="rg r3" cx="{LX}" cy="{LY}" r="330" stroke="{PAPER}" stroke-width="1.2" vector-effect="non-scaling-stroke" opacity="0"/>
 </g>
</g>

<!-- SPARK -->
<g class="spark">
 <path d="M-150,0 L0,-3.6 L0,3.6Z" fill="url(#tail)"/>
 <circle r="20" fill="url(#glow)" opacity=".7"/>
 <circle r="5.6" fill="{PAPER}"/>
</g>

<!-- TITLE BLOCK -->
<g font-family="Archivo,Helvetica,Arial,sans-serif">
 <g class="lab"><text x="72" y="560" font-size="19" font-weight="800" fill="{INK}">02</text></g>
 <rect class="lab-r" x="106" y="554" width="58" height="2" fill="{INK}"/>
 <g class="lab"><text x="178" y="560" font-size="12" font-weight="700" letter-spacing="3.6" fill="{INK}">SERVICE TWO OF SEVEN</text></g>
 <g filter="url(#inkrough)">
  <g class="hd-g" style="opacity:.3"><g transform="translate(-3 2)" fill="{INK}" font-size="140" font-weight="800" letter-spacing="-4.2"><text x="72" y="692">SOCIAL</text></g></g>
  <g class="hd-g hd-g2" style="opacity:.3"><g transform="translate(-3 2)" fill="{INK}" font-size="140" font-weight="800" letter-spacing="-4.2"><text x="72" y="804">MEDIA</text></g></g>
  <g class="hd hd1" fill="{INK}" font-size="140" font-weight="800" letter-spacing="-4.2"><text x="72" y="692">SOCIAL</text></g>
  <g class="hd hd2" fill="{INK}" font-size="140" font-weight="800" letter-spacing="-4.2"><text x="72" y="804">MEDIA</text></g>
 </g>
 <g class="desc"><text x="72" y="848" font-size="20" font-weight="400" fill="{INK}">Posts that sound like you, out every week.</text></g>
</g>

<!-- STENCIL: POST EVERY WEEK -->
<g class="sten-w">
 <g filter="url(#rough)" opacity=".92">
  <text class="sten" x="1390" y="838" font-size="64" text-anchor="end" letter-spacing="2" fill="{INK}">POST EVERY WEEK</text>
 </g>
</g>

<!-- PRINTER'S MARKS -->
<g fill="none" stroke="{INK}" stroke-width="1.2">
 <g class="mk" style="--k:0"><circle cx="1410" cy="640" r="7"/><path d="M1396,640H1424M1410,626V654"/></g>
 <g class="mk" style="--k:1"><circle cx="30" cy="470" r="7"/><path d="M16,470H44M30,456V484"/></g>
 <g class="mk" style="--k:2"><path d="M12,20V6H26M1428,20V6H1414M12,880V894H26M1428,880V894H1414" /></g>
</g>
<g class="mk" style="--k:3">
 <g fill="{INK}">{"".join(f'<rect x="{72+k*16}" y="868" width="14" height="9" opacity="{.12+k*.125:.2f}"/>' for k in range(8))}</g>
 <g font-family="Archivo,Helvetica,Arial,sans-serif" font-size="11" font-weight="700" letter-spacing="2.2" fill="{INK}">
  <text x="1390" y="877" text-anchor="end">PEC . 02 / 07 . TWO INKS . ONE WALL</text>
 </g>
</g>

<!-- grain over everything -->
<rect width="1440" height="900" filter="url(#grain)" class="mix" opacity=".35" pointer-events="none"/>
</svg>
<script>
window.SPARK_ENTRY = {{x:0, y:289.1, t:0.44}};
(function(){{
 var root=document.documentElement;
 var q=new URLSearchParams(location.search), T=q.get('t');
 var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
 function reflow(){{void root.getBoundingClientRect();}}
 function freeze(t){{document.getAnimations().forEach(function(a){{a.pause();a.currentTime=t*1000;}});}}
 window.play=function(){{
  root.classList.remove('play');reflow();
  if(reduce)return;
  root.classList.add('play');reflow();
  var ends=document.getAnimations().map(function(a){{return a.effect.getComputedTiming().endTime;}});
  window.DURATION=Math.max.apply(null,ends)/1000;
  if(T!==null&&T!==''&&!isNaN(parseFloat(T)))freeze(parseFloat(T));
 }};
 window.finish=function(){{root.classList.remove('play');}};
 window.addEventListener('message',function(e){{if(e.data==='play')play();else if(e.data==='finish')finish();}});
 play();
}})();
</script></body></html>
'''
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "social.html")
open(out, "w", encoding="utf-8").write(html)
print("wrote", out, len(html), "bytes", len(ink_d), "ink", len(paper_d), "paper dots")
