#!/usr/bin/env python3
"""Generator for worlds/customer-experience.html (World 04, transit map).
Run: python customer-experience.py   (writes ../customer-experience.html)
Everything sits on a 2px-aligned grid: stations every 146px, jogs of 40px at 45 degrees, fillet radius 28.
"""
import math, os

INK = "#0D1321"; PAPER = "#F6F6F4"; PER = "#FF6A2A"
GA = "#646B78"   # grey line A (ink tint)
GB = "#8C919B"   # grey line B (lighter ink tint)

R = 28  # fillet radius, used everywhere

# ---------------------------------------------------------------- geometry helpers
def fillet_path(pts, r=R):
    """Polyline -> SVG path with rounded corners; also returns dense sample list [(x,y)] ."""
    d = []; samples = []
    def unit(a, b):
        dx, dy = b[0]-a[0], b[1]-a[1]; l = math.hypot(dx, dy); return dx/l, dy/l
    cur = pts[0]; d.append("M%g,%g" % cur); samples.append(cur)
    for i in range(1, len(pts)-1):
        a, v, b = pts[i-1], pts[i], pts[i+1]
        u1 = unit(a, v); u2 = unit(v, b)
        cross = u1[0]*u2[1]-u1[1]*u2[0]
        dot = max(-1, min(1, u1[0]*u2[0]+u1[1]*u2[1]))
        th = math.acos(dot)  # deflection
        t = r*math.tan(th/2)
        s = (v[0]-u1[0]*t, v[1]-u1[1]*t); e = (v[0]+u2[0]*t, v[1]+u2[1]*t)
        d.append("L%.2f,%.2f" % s)
        # sample straight part
        n = max(2, int(math.hypot(s[0]-cur[0], s[1]-cur[1])/2))
        for k in range(1, n+1):
            samples.append((cur[0]+(s[0]-cur[0])*k/n, cur[1]+(s[1]-cur[1])*k/n))
        sweep = 1 if cross > 0 else 0
        d.append("A%g,%g 0 0 %d %.2f,%.2f" % (r, r, sweep, e[0], e[1]))
        # arc samples
        c = (s[0] + (-u1[1] if cross > 0 else u1[1])*-1*0, 0)  # placeholder
        nx, ny = (-u1[1], u1[0]) if cross > 0 else (u1[1], -u1[0])  # normal towards centre
        cx, cy = s[0]+nx*r, s[1]+ny*r
        a0 = math.atan2(s[1]-cy, s[0]-cx); a1 = math.atan2(e[1]-cy, e[0]-cx)
        da = a1-a0
        while da > math.pi: da -= 2*math.pi
        while da < -math.pi: da += 2*math.pi
        for k in range(1, 13):
            aa = a0+da*k/12; samples.append((cx+r*math.cos(aa), cy+r*math.sin(aa)))
        cur = e
    last = pts[-1]
    d.append("L%g,%g" % last)
    n = max(2, int(math.hypot(last[0]-cur[0], last[1]-cur[1])/2))
    for k in range(1, n+1):
        samples.append((cur[0]+(last[0]-cur[0])*k/n, cur[1]+(last[1]-cur[1])*k/n))
    return "".join(d), samples

def cum(samples):
    c = [0.0]
    for i in range(1, len(samples)):
        c.append(c[-1]+math.hypot(samples[i][0]-samples[i-1][0], samples[i][1]-samples[i-1][1]))
    return c

def at(samples, c, s):
    s = max(0, min(c[-1], s))
    lo, hi = 0, len(c)-1
    while hi-lo > 1:
        m = (lo+hi)//2
        if c[m] <= s: lo = m
        else: hi = m
    f = (s-c[lo])/max(1e-9, c[hi]-c[lo])
    return (samples[lo][0]+(samples[hi][0]-samples[lo][0])*f, samples[lo][1]+(samples[hi][1]-samples[lo][1])*f)

def s_of(samples, c, pt):
    best = min(range(len(samples)), key=lambda i: (samples[i][0]-pt[0])**2+(samples[i][1]-pt[1])**2)
    return c[best]

# ---------------------------------------------------------------- the main line
XS = [290 + 146*i for i in range(8)]
YS = [360, 360, 360, 400, 400, 360, 360, 400]
NAMES = ["FIRST HELLO", "QUOTE", "BOOKING", "REMINDER", "VISIT", "THANK YOU", "REVIEW", "COMES BACK"]
stations = list(zip(XS, YS))

main_pts = [(-12, 360)]
for i in range(7):
    xa, ya = XS[i], YS[i]; yb = YS[i+1]
    if ya != yb:
        sgn = 1 if yb > ya else -1
        main_pts += [(xa+53, ya), (xa+93, ya+40*sgn)]
main_pts.append((XS[7], YS[7]))
main_d, main_s = fillet_path(main_pts)
main_c = cum(main_s); MAIN_L = main_c[-1]
st_s = [s_of(main_s, main_c, p) for p in stations]
S1 = st_s[0]

# core (ridden stretch) starts at station 1
core_pts = [stations[0]] + main_pts[main_pts.index((XS[2]+53, 360)):] if False else None
# build core as the same polyline cut at station 1 (x=290 is on the first straight run)
core_pts = [(XS[0], 360)] + [p for p in main_pts[1:]]
core_d, core_s = fillet_path(core_pts)
core_c = cum(core_s); CORE_L = core_c[-1]

# ---------------------------------------------------------------- timing
T_START = 1.3      # marker lands on station 1
T_END = 2.6        # marker reaches terminus
INK_T0, INK_S1T, INK_T1 = 0.35, 1.10, 2.40
arr = [T_START + (T_END-T_START)*(st_s[i]-S1)/(MAIN_L-S1) for i in range(8)]

# ---------------------------------------------------------------- grey lines
A_pts = [(-12, 520), (356, 520), (436, 440), (436, 150), (262, 150)]
A_d, A_s = fillet_path(A_pts)
B_pts = [(728, -12), (728, 470), (798, 540), (900, 540)]
B_d, B_s = fillet_path(B_pts)

def ticks(pts, color, skip):
    out = []
    for i in range(len(pts)-1):
        a, b = pts[i], pts[i+1]
        L = math.hypot(b[0]-a[0], b[1]-a[1]); ux, uy = (b[0]-a[0])/L, (b[1]-a[1])/L
        nx, ny = -uy, ux
        d = 44
        while d < L-44:
            x, y = a[0]+ux*d, a[1]+uy*d
            if not skip(x, y) and 0 < x < 1440 and 0 < y < 900:
                out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f"/>' % (x-nx*8, y-ny*8, x+nx*8, y+ny*8))
            d += 30
    return "".join(out)

tk_A = ticks(A_pts, GA, lambda x, y: abs(y-360) < 70 and abs(x-436) < 4)
tk_B = ticks(B_pts, GB, lambda x, y: abs(y-400) < 70 and abs(x-728) < 4 or y < 70)

# ---------------------------------------------------------------- spark flight (cubic bezier)
P = [(-26, 360), (60, 205), (200, 200), (XS[0], 360)]
def bez(t):
    mt = 1-t
    return (mt**3*P[0][0]+3*mt*mt*t*P[1][0]+3*mt*t*t*P[2][0]+t**3*P[3][0],
            mt**3*P[0][1]+3*mt*mt*t*P[1][1]+3*mt*t*t*P[2][1]+t**3*P[3][1])
bs = [bez(i/2000) for i in range(2001)]; bc = cum(bs); BL = bc[-1]
SPARK_D = "M%g,%g C%g,%g %g,%g %g,%g" % (P[0]+P[1]+P[2]+P[3])
SPARK_T0, SPARK_DUR = 0.1, 1.2
N = 48
def ease_fly(t): return t**1.35
spark_kf = []; tail1 = []; tail2 = []
LD1, LD2 = 0.20, 0.09
for k in range(N+1):
    tau = k/N; p = ease_fly(tau); x, y = at(bs, bc, p*BL)
    spark_kf.append("%.3f%%{transform:translate(%.1fpx,%.1fpx)}" % (tau*100, x, y))
    tail1.append("%.3f%%{stroke-dashoffset:%.4f}" % (tau*100, LD1-p))
    tail2.append("%.3f%%{stroke-dashoffset:%.4f}" % (tau*100, LD2-p))

# ---------------------------------------------------------------- marker ride
ride_kf = []
for k in range(61):
    tau = k/60; x, y = at(main_s, main_c, S1+(MAIN_L-S1)*tau)
    ride_kf.append("%.3f%%{transform:translate(%.1fpx,%.1fpx)}" % (tau*100, x, y))

# ink progress keyframes (dashoffset = 1 - fraction)
D_INK = INK_T1
ink_kf = "0%%{stroke-dashoffset:1}%.3f%%{stroke-dashoffset:1}%.3f%%{stroke-dashoffset:%.4f}100%%{stroke-dashoffset:0}" % (
    INK_T0/D_INK*100, INK_S1T/D_INK*100, 1-S1/MAIN_L)

# ---------------------------------------------------------------- svg pieces
def label_text(i):
    x, y = stations[i]
    if i == 7: return ""
    return ('<g transform="translate(%d,%d) rotate(-45)"><text class="sn lb lb%d" x="0" y="0">%s</text></g>' % (x+26, y-28, i, NAMES[i]))

st_parts = []
for i, (x, y) in enumerate(stations):
    if i == 7:
        st_parts.append(
            '<g class="stp stp7"><circle cx="%d" cy="%d" r="40" fill="%s" stroke="%s" stroke-width="10"/>'
            '<circle cx="%d" cy="%d" r="25" fill="none" stroke="%s" stroke-width="3"/></g>' % (x, y, PAPER, INK, x, y, INK))
    elif i in (1, 3):
        st_parts.append('<g class="stp stp%d"><rect x="%d" y="%d" width="38" height="78" rx="19" fill="%s" stroke="%s" stroke-width="6"/>'
                        '<circle cx="%d" cy="%d" r="9" fill="none" stroke="%s" stroke-width="3"/></g>' % (i, x-19, y-39, PAPER, INK, x, y, INK))
    else:
        st_parts.append('<g class="stp stp%d"><circle cx="%d" cy="%d" r="17" fill="%s" stroke="%s" stroke-width="6"/></g>' % (i, x, y, PAPER, INK))
STATIONS = "".join(st_parts)
LABELS = "".join(label_text(i) for i in range(7))
NUMS = "".join('<text class="nm nm%d" x="%d" y="%d">%d</text>' % (i, x+26, y+38, i+1) for i, (x, y) in enumerate(stations) if i < 7)

# grid index
GRID = []
for k in range(7):
    GRID.append('<line x1="%d" y1="0" x2="%d" y2="10" />' % (240*k, 240*k))
    GRID.append('<line x1="%d" y1="890" x2="%d" y2="900" />' % (240*k, 240*k))
for k in range(5):
    GRID.append('<line x1="0" y1="%d" x2="10" y2="%d" />' % (225*k, 225*k))
    GRID.append('<line x1="1430" y1="%d" x2="1440" y2="%d" />' % (225*k, 225*k))
for kx in range(1, 6):
    for ky in range(1, 4):
        x, y = 240*kx, 225*ky
        if not (y > 600 and x < 900): GRID.append('<path d="M%d,%dH%d M%d,%dV%d" />' % (x-7, y, x+7, x, y-7, y+7))
GRIDLN = "".join(GRID)
LET = "".join('<text x="%d" y="26" text-anchor="middle">%s</text>' % (120+240*k, "ABCDEF"[k]) for k in range(6))
LET += "".join('<text x="%d" y="893" text-anchor="middle">%s</text>' % (120+240*k, "ABCDEF"[k]) for k in range(2, 6))
NUMLEFT = "".join('<text x="22" y="%d" text-anchor="middle">%d</text>' % (112+225*k+4, k+1) for k in range(4))
NUMLEFT += "".join('<text x="1418" y="%d" text-anchor="middle">%d</text>' % (112+225*k+4, k+1) for k in range(4))

# river (flat tint), park (flat tint octagon)
RIVER = "M905,-12 C945,110 990,215 950,325 C918,415 930,500 990,585 C1045,665 1068,770 1034,912"
PARK = "1130,596 1330,596 1372,638 1372,778 1330,820 1130,820 1088,778 1088,638"

# zone bands
ZB = [(48, 560, "ZONE 1", 0.06), (560, 950, "ZONE 2", 0.11), (950, 1392, "ZONE 3", 0.06)]
ZONE = "".join('<rect x="%d" y="36" width="%d" height="14" fill="%s" fill-opacity="%s"/><text x="%d" y="47" class="zt">%s</text>' % (a, b-a, INK, o, a+10, t) for a, b, t, o in ZB)

# legend
LEG = """
<g class="legend" transform="translate(1142,60)">
 <rect x="0" y="0" width="250" height="198" fill="%(P)s" stroke="%(I)s" stroke-width="2"/>
 <text x="18" y="29" class="lg-h">KEY</text>
 <line x1="18" y1="40" x2="232" y2="40" stroke="%(I)s" stroke-width="1.5"/>
 <g transform="translate(0,64)"><line x1="18" y1="0" x2="70" y2="0" stroke="%(I)s" stroke-width="12"/><line x1="18" y1="0" x2="70" y2="0" stroke="%(O)s" stroke-width="4"/><text x="80" y="5" class="lg-t">Customer journey</text></g>
 <g transform="translate(0,90)"><line x1="18" y1="0" x2="62" y2="0" stroke="%(GA)s" stroke-width="8"/><line x1="66" y1="-9" x2="66" y2="9" stroke="%(GA)s" stroke-width="5"/><text x="80" y="5" class="lg-t">Where customers get lost</text></g>
 <g transform="translate(0,116)"><circle cx="44" cy="0" r="10" fill="%(P)s" stroke="%(I)s" stroke-width="4"/><text x="80" y="5" class="lg-t">Station</text></g>
 <g transform="translate(0,144)"><rect x="33" y="-13" width="22" height="26" rx="11" fill="%(P)s" stroke="%(I)s" stroke-width="4"/><text x="80" y="5" class="lg-t">Interchange</text></g>
 <g transform="translate(0,176)"></g>
</g>""" % dict(P=PAPER, I=INK, O=PER, GA=GA)
# "You are here" row is placed in a taller box; rebuild with explicit height
LEG = LEG.replace('height="190"', 'height="196"').replace('<g transform="translate(0,176)"></g>',
    '<g transform="translate(0,174)"><circle cx="44" cy="0" r="13" fill="none" stroke="%s" stroke-width="3"/><circle cx="44" cy="0" r="6" fill="%s"/><text x="80" y="5" class="lg-t">You are here</text></g>' % (PER, PER))

# ---------------------------------------------------------------- CSS animation per element
css_dyn = []
for i in range(8):
    t = arr[i]
    css_dyn.append(".play .stp%d{animation:pop .3s var(--out) %.3fs backwards}" % (i, max(0, t-0.09)))
    if i < 7:
        css_dyn.append(".play .lb%d{animation:lbin .4s var(--out) %.3fs backwards}" % (i, t-0.02))
        css_dyn.append(".play .nm%d{animation:fade .3s linear %.3fs backwards}" % (i, t+0.05))
CSS_DYN = "\n".join(css_dyn)

TERM_X, TERM_Y = stations[7]

html = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>Customer Experience</title>
<meta name="viewport" content="width=1440">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
html,body{margin:0;overflow:hidden;background:%(PAPER)s}
svg{display:block;width:1440px;height:900px}
text{font-family:'Archivo','Helvetica Neue',Arial,sans-serif}
.sn{font-weight:600;font-size:16px;letter-spacing:1.4px;fill:%(INK)s}
.nm{font-weight:600;font-size:11px;letter-spacing:1px;fill:%(INK)s;fill-opacity:.5}
.zt{font-weight:600;font-size:11px;letter-spacing:2px;fill:%(INK)s;fill-opacity:.7}
.idx text{font-weight:600;font-size:11px;letter-spacing:1px;fill:%(INK)s;fill-opacity:.5}
.idx line,.idx path{stroke:%(INK)s;stroke-opacity:.4;stroke-width:1;fill:none}
.fl-t{font-weight:700;font-size:13px;letter-spacing:1.2px;fill:%(INK)s}
.lg-h{font-weight:700;font-size:11px;letter-spacing:3px;fill:%(INK)s}
.lg-t{font-weight:500;font-size:13.5px;fill:%(INK)s}
.sm{font-weight:600;font-size:11px;letter-spacing:2.5px;fill:%(INK)s;fill-opacity:.6}
.tl-n{font-weight:800;font-size:19px;letter-spacing:1px;fill:%(INK)s}
.tl-s{font-weight:600;font-size:12px;letter-spacing:3.4px;fill:%(INK)s}
.h1{font-weight:800;font-size:120px;letter-spacing:-4px;fill:%(INK)s}
.ds{font-weight:400;font-size:20px;fill:%(INK)s}
.term{font-weight:800;font-size:25px;letter-spacing:1px;fill:%(INK)s}
.lnpill{font-weight:700;font-size:12px;letter-spacing:2px;fill:%(PAPER)s}
.mk,.stp,.sparkg,.rg,.lb,.nm{transform-box:fill-box;transform-origin:center}
.spark,.rg{display:none}
.play .spark,.play .rg{display:inline}

html{--fly:cubic-bezier(.35,.05,.7,.75);--out:cubic-bezier(.16,.84,.3,1);--io:cubic-bezier(.5,.05,.25,1)}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes fadeUp{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
@keyframes wipeX{from{clip-path:inset(0 100%% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes rise{from{transform:translateY(34px);clip-path:inset(0 0 100%% 0)}to{transform:none;clip-path:inset(0 0 0 0)}}
@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes pop{from{transform:scale(.25);opacity:0}60%%{opacity:1}to{transform:scale(1);opacity:1}}
@keyframes lbin{from{opacity:0;transform:translate(-8px,0)}to{opacity:1;transform:none}}
@keyframes ring{0%%{transform:scale(.35);opacity:0}2%%{opacity:.9}100%%{transform:scale(3.2);opacity:0}}
@keyframes ringT{0%%{transform:scale(.7);opacity:0}2%%{opacity:.9}100%%{transform:scale(3);opacity:0}}
@keyframes mkpop{from{transform:scale(0)}to{transform:scale(1)}}
@keyframes inkdraw{%(INKKF)s}
@keyframes flight{%(FLIGHT)s}
@keyframes tail1{%(T1)s}
@keyframes tail2{%(T2)s}
@keyframes ride{%(RIDE)s}
@keyframes sparkfade{0%%{opacity:0}6%%{opacity:1}90%%{opacity:1}100%%{opacity:0}}
@keyframes legin{from{opacity:0;transform:translate(1142px,74px)}to{opacity:1;transform:translate(1142px,60px)}}

.mark-ride{transform:translate(%(TX)d px,%(TY)d px)}
.play .gA{stroke-dasharray:1 2;animation:draw .85s var(--out) .35s backwards}
.play .gB{stroke-dasharray:1 2;animation:draw .8s var(--out) .5s backwards}
.play .river{stroke-dasharray:1 2;animation:draw 1s var(--io) .15s backwards}
.play .park{animation:fade .6s linear .5s backwards}
.play .zone{animation:fade .5s linear .3s backwards}
.play .idx{animation:fade .5s linear 0s backwards}
.play .tk{animation:fade .45s linear .95s backwards}
.play .fl{animation:fade .45s linear 1.0s backwards}
.play .stub{animation:fade .3s linear .95s backwards}
.play .ink{stroke-dasharray:1 2;animation:inkdraw %(DINK)ss linear 0s backwards}
.play .core{stroke-dasharray:1 2;animation:draw %(RIDEDUR).2fs linear %(TSTART).2fs backwards}
.play .pill{animation:fade .35s linear .6s backwards}
.play .sparkg{animation:flight %(SDUR)ss linear %(SDEL)ss backwards}
.play .sparkall{animation:sparkfade %(SDUR)ss linear %(SDEL)ss both}
.play .tl1{stroke-dasharray:%(LD1)s 5;animation:tail1 %(SDUR)ss linear %(SDEL)ss backwards}
.play .tl2{stroke-dasharray:%(LD2)s 5;animation:tail2 %(SDUR)ss linear %(SDEL)ss backwards}
.play .mkride{animation:ride %(RIDEDUR).2fs linear %(TSTART).2fs backwards}
.play .mkpop{animation:mkpop .32s var(--out) %(TSTART).2fs backwards}
.play .rg1{animation:ring .95s cubic-bezier(.2,.6,.3,1) 1.3s both}
.play .rg2{animation:ring .95s cubic-bezier(.2,.6,.3,1) 1.42s both}
.play .rg3{animation:ring .95s cubic-bezier(.2,.6,.3,1) 1.54s both}
.play .rt1{animation:ringT .9s cubic-bezier(.2,.6,.3,1) %(TEND).2fs both}
.play .rt2{animation:ringT .9s cubic-bezier(.2,.6,.3,1) %(TEND2).2fs both}
.play .rt3{animation:ringT .9s cubic-bezier(.2,.6,.3,1) %(TEND3).2fs both}
.play .termlb{animation:wipeX .45s var(--out) %(TEND).2fs backwards}
.play .tlab{animation:fadeUp .4s var(--out) 1.65s backwards}
.play .trule{transform-box:fill-box;transform-origin:0 50%%;animation:wipeX .45s var(--out) 1.7s backwards}
.play .h1a{animation:rise .6s cubic-bezier(.2,.9,.25,1) 1.75s backwards}
.play .h1b{animation:rise .6s cubic-bezier(.2,.9,.25,1) 1.92s backwards}
.play .ds{animation:fadeUp .45s var(--out) 2.4s backwards}
.play .legend{animation:legin .55s var(--out) 2.6s backwards}
.play .remnant{animation:fade .5s linear %(TEND).2fs backwards}
.play .foot{animation:fade .5s linear 2.9s backwards}
%(CSSDYN)s
@media (prefers-reduced-motion:reduce){*{animation:none!important}.spark,.rg{display:none!important}}
</style></head>
<body>
<svg viewBox="0 0 1440 900" xmlns="http://www.w3.org/2000/svg">
<rect width="1440" height="900" fill="%(PAPER)s"/>

<!-- grid index -->
<g class="idx"><g>%(GRIDLN)s</g>%(LET)s%(NUMLEFT)s</g>

<!-- flat tint shapes -->
<polygon class="park" points="%(PARK)s" fill="%(INK)s" fill-opacity=".055"/>
<text class="sm park" x="1118" y="618" style="font-size:11px">PARK</text>
<path class="river" d="%(RIVER)s" pathLength="1" fill="none" stroke="%(INK)s" stroke-opacity=".075" stroke-width="50" stroke-linejoin="round"/>

<!-- zone bands -->
<g class="zone">%(ZONE)s</g>

<!-- grey lines: ways customers get lost -->
<g fill="none" stroke-linejoin="round">
 <path class="gA" d="%(A_d)s" pathLength="1" stroke="%(GA)s" stroke-width="10"/>
 <path class="gB" d="%(B_d)s" pathLength="1" stroke="%(GB)s" stroke-width="10"/>
</g>
<g class="tk" stroke="%(GA)s" stroke-width="3">%(TKA)s</g>
<g class="tk" stroke="%(GB)s" stroke-width="3">%(TKB)s</g>
<g class="stub"><line x1="262" y1="132" x2="262" y2="168" stroke="%(GA)s" stroke-width="7"/><line x1="900" y1="522" x2="900" y2="558" stroke="%(GB)s" stroke-width="7"/></g>
<g class="fl">
 <rect x="92" y="134" width="156" height="32" rx="16" fill="%(PAPER)s" stroke="%(GA)s" stroke-width="3"/>
 <text class="fl-t" x="170" y="155" text-anchor="middle">NO REPLY LINE</text>
 <rect x="918" y="524" width="272" height="32" rx="16" fill="%(PAPER)s" stroke="%(GB)s" stroke-width="3"/>
 <text class="fl-t" x="1054" y="545" text-anchor="middle">FORGOT TO FOLLOW UP LINE</text>
</g>

<!-- main line: ink, then persimmon core where the traveler has ridden -->
<g fill="none" stroke-linejoin="round">
 <path class="ink" d="%(main_d)s" pathLength="1" stroke="%(INK)s" stroke-width="20"/>
 <path class="core" d="%(core_d)s" pathLength="1" stroke="%(PER)s" stroke-width="6"/>
</g>
<g class="pill"><rect x="26" y="340" width="168" height="40" rx="20" fill="%(INK)s"/><text class="lnpill" x="110" y="365" text-anchor="middle">CUSTOMER LINE</text></g>

<!-- stations, names -->
%(STATIONS)s
%(LABELS)s
%(NUMS)s
<g class="termlb"><text class="term" x="%(TX)d" y="%(TLY)d" text-anchor="middle">COMES BACK</text>
<text class="sm" x="%(TX)d" y="%(TLY2)d" text-anchor="middle">TERMINUS</text></g>

<!-- terminus echo remnant -->
<circle class="remnant" cx="%(TX)d" cy="%(TY)d" r="56" fill="none" stroke="%(PER)s" stroke-opacity=".55" stroke-width="1.5"/>

<!-- traveler marker (at terminus when finished) -->
<g class="mkride" style="transform:translate(%(TX)dpx,%(TY)dpx)">
 <g class="mk mkpop"><circle r="21" fill="none" stroke="%(PER)s" stroke-width="4"/><circle r="9" fill="%(PER)s"/></g>
</g>

<!-- echo rings (play only) -->
<g class="spark">
 <g transform="translate(%(S1X)d,%(S1Y)d)"><circle class="rg rg1" r="26" fill="none" stroke="%(PER)s" stroke-width="2.5"/><circle class="rg rg2" r="26" fill="none" stroke="%(PER)s" stroke-width="2"/><circle class="rg rg3" r="26" fill="none" stroke="%(PER)s" stroke-width="1.5"/></g>
 <g transform="translate(%(TX)d,%(TY)d)"><circle class="rg rt1" r="30" fill="none" stroke="%(PER)s" stroke-width="2.5"/><circle class="rg rt2" r="30" fill="none" stroke="%(PER)s" stroke-width="2"/><circle class="rg rt3" r="30" fill="none" stroke="%(PER)s" stroke-width="1.5"/></g>
 <g class="sparkall">
  <path class="tl1" d="%(SPARK_D)s" pathLength="1" fill="none" stroke="%(PER)s" stroke-width="3" stroke-linecap="round" stroke-dasharray="0 5"/>
  <path class="tl2" d="%(SPARK_D)s" pathLength="1" fill="none" stroke="%(PER)s" stroke-width="6" stroke-linecap="round" stroke-dasharray="0 5"/>
  <g class="sparkg"><circle r="15" fill="%(PER)s" fill-opacity=".16"/><circle r="9" fill="%(PER)s" fill-opacity=".3"/><circle r="5.5" fill="%(PER)s"/></g>
 </g>
</g>

<!-- title block -->
<g class="titleblock">
 <g class="tlab"><text class="tl-n" x="72" y="613">04</text><text class="tl-s" x="188" y="613">SERVICE FOUR OF SEVEN</text></g>
 <line class="trule" x1="108" y1="607" x2="172" y2="607" stroke="%(INK)s" stroke-width="2"/>
 <text class="h1 h1a" x="66" y="719">CUSTOMER</text>
 <text class="h1 h1b" x="66" y="835">EXPERIENCE</text>
 <text class="ds" x="72" y="870">Every step your customer takes, mapped and smoothed.</text>
</g>

%(LEG)s

<g class="foot"><text class="sm" x="1392" y="872" text-anchor="end">NOT TO SCALE</text></g>
</svg>
<script>
window.SPARK_ENTRY = {x:0, y:319.4, t:0.345};
(function(){
 var root=document.documentElement;
 var q=new URLSearchParams(location.search), T=q.get('t');
 var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
 function reflow(){void root.getBoundingClientRect();}
 function freeze(t){document.getAnimations().forEach(function(a){a.pause();a.currentTime=t*1000;});}
 window.play=function(){
  root.classList.remove('play');reflow();
  if(reduce)return;
  root.classList.add('play');reflow();
  var ends=document.getAnimations().map(function(a){return a.effect.getComputedTiming().endTime;});
  window.DURATION=Math.max.apply(null,ends)/1000;
  if(T!==null&&T!==''&&!isNaN(parseFloat(T)))freeze(parseFloat(T));
 };
 window.finish=function(){root.classList.remove('play');};
 window.addEventListener('message',function(e){if(e.data==='play')play();else if(e.data==='finish')finish();});
 play();
})();
</script></body></html>
""" % dict(
    PAPER=PAPER, INK=INK, PER=PER, GA=GA, GB=GB,
    INKKF=ink_kf, FLIGHT="".join(spark_kf), T1="".join(tail1), T2="".join(tail2), RIDE="".join(ride_kf),
    TX=TERM_X, TY=TERM_Y, DINK=D_INK, RIDEDUR=T_END-T_START, TSTART=T_START, TEND=T_END, TEND2=T_END+0.12, TEND3=T_END+0.24,
    SDUR=SPARK_DUR, SDEL=SPARK_T0, LD1=LD1, LD2=LD2, CSSDYN=CSS_DYN,
    GRIDLN=GRIDLN, LET=LET, NUMLEFT=NUMLEFT, PARK=PARK, RIVER=RIVER, ZONE=ZONE,
    A_d=A_d, B_d=B_d, TKA=tk_A, TKB=tk_B, main_d=main_d, core_d=core_d,
    STATIONS=STATIONS, LABELS=LABELS, NUMS=NUMS, TLY=TERM_Y+88, TLY2=TERM_Y+108,
    S1X=XS[0], S1Y=YS[0], SPARK_D=SPARK_D, LEG=LEG)

# the css rule .mark-ride is unused; strip the stray rule to keep the file clean
html = html.replace(".mark-ride{transform:translate(%d px,%d px)}\n" % (TERM_X, TERM_Y), "")
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "customer-experience.html")
with open(out, "w", encoding="utf-8") as f: f.write(html)
print("wrote", os.path.normpath(out), "main length %.0f" % MAIN_L, "arrivals", [round(a, 2) for a in arr])
