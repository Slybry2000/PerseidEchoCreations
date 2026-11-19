#!/usr/bin/env python3
"""Generator for worlds/automation.html (World 03, the engineer's blueprint)."""
import math, os

PAPER = '#F6F6F4'
GROUND = '#16233F'
PERS = '#FF6A2A'
INK = '#0D1321'

# ---------------------------------------------------------------- ball path
SEG = [
    ('M', [(190, 168)]),
    ('L', [(192.3, 273.7)]),
    ('L', [(452.3, 341.3)]),
    ('L', [(735, 341)]),
    ('C', [(765, 341), (785, 352), (796, 381)]),
    ('L', [(1098, 381)]),
    ('C', [(1115, 381), (1128, 388), (1136, 396)]),
    ('L', [(1306, 564)]),
    ('C', [(1312, 590), (1318, 620), (1322, 651)]),
]


def bez(p0, p1, p2, p3, t):
    u = 1 - t
    return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0],
            u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])


pts = []  # (x, y, cumulative length)
cur = SEG[0][1][0]
pts.append((cur[0], cur[1], 0.0))
L = 0.0
for kind, ps in SEG[1:]:
    if kind == 'L':
        n = 40
        for i in range(1, n + 1):
            t = i / n
            x = cur[0] + (ps[0][0] - cur[0]) * t
            y = cur[1] + (ps[0][1] - cur[1]) * t
            L += math.hypot(x - pts[-1][0], y - pts[-1][1])
            pts.append((x, y, L))
        cur = ps[0]
    else:
        n = 60
        for i in range(1, n + 1):
            x, y = bez(cur, ps[0], ps[1], ps[2], i / n)
            L += math.hypot(x - pts[-1][0], y - pts[-1][1])
            pts.append((x, y, L))
        cur = ps[2]
TOTAL = L


def frac_at_x(xt, after=0.0):
    for (x, y, l), (x2, y2, l2) in zip(pts, pts[1:]):
        if l2 / TOTAL >= after and (x - xt) * (x2 - xt) <= 0 and x != x2:
            return (l + (l2 - l) * (xt - x) / (x2 - x)) / TOTAL
    raise ValueError(xt)


T0, TD = 1.30, 1.30  # ball leaves hopper at T0, lands at T0+TD
def tt(f):
    return T0 + TD * f

fA0, fA1 = frac_at_x(500, 0.2), frac_at_x(582, 0.2)
fGate = frac_at_x(865, 0.4)
fReply = frac_at_x(1060, 0.4)

PATH_D = ''
for kind, ps in SEG:
    PATH_D += kind + ' '.join(f'{x:g},{y:g}' for x, y in ps) + ' '

# ---------------------------------------------------------------- helpers
def dly(x):
    return 0.08 + 1.05 * max(0, x - 60) / 1340


def dr(tag, x, attrs, cls='', l=None, d=None):
    dd = dly(x) if d is None else d
    ll = f'--l:{l}s;' if l else ''
    return f'<{tag} {attrs} class="dr {cls}" pathLength="1" style="--d:{dd:.2f}s;{ll}"/>'.replace('  ', ' ')


def fd(content, d, cls=''):
    return f'<g class="fd {cls}" style="--d:{d:.2f}s">{content}</g>'


def gear_path(cx, cy, n, r_root, r_tip, theta0_deg):
    p = 2 * math.pi / n
    th0 = math.radians(theta0_deg)
    out = []
    for i in range(n):
        th = th0 + i * p
        def P(a, r):
            return cx + r * math.cos(th + a * p), cy + r * math.sin(th + a * p)
        rl = P(-0.27, r_root); tl = P(-0.13, r_tip); tr = P(0.13, r_tip); rr = P(0.27, r_root)
        nl = (cx + r_root * math.cos(th + 0.73 * p), cy + r_root * math.sin(th + 0.73 * p))
        if i == 0:
            out.append(f'M{rl[0]:.2f},{rl[1]:.2f}')
        out.append(f'L{tl[0]:.2f},{tl[1]:.2f}')
        out.append(f'A{r_tip:.2f},{r_tip:.2f} 0 0 1 {tr[0]:.2f},{tr[1]:.2f}')
        out.append(f'L{rr[0]:.2f},{rr[1]:.2f}')
        out.append(f'A{r_root:.2f},{r_root:.2f} 0 0 1 {nl[0]:.2f},{nl[1]:.2f}')
    out.append('Z')
    return ' '.join(out)


# ---------------------------------------------------------------- geometry
AX, AY = 540, 422
PHI = 35
M = 9.14
rpA, rpB = 64, 45.7
CD = rpA + rpB
BX, BY = AX + CD * math.cos(math.radians(PHI)), AY + CD * math.sin(math.radians(PHI))
gearA = gear_path(AX, AY, 14, 54.5, 72, PHI)
gearB = gear_path(BX, BY, 10, 36.2, 53.7, PHI + 180 + 18)

parts = []
add = parts.append

# ---- defs
defs = f'''
<defs>
 <pattern id="gm" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="{PAPER}" stroke-opacity=".075" stroke-width="1"/></pattern>
 <pattern id="gM" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0H0V100" fill="none" stroke="{PAPER}" stroke-opacity=".15" stroke-width="1"/></pattern>
 <filter id="mottle" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".012 .016" numOctaves="3" seed="7" result="n"/><feColorMatrix in="n" type="matrix" values="0 0 0 0 .55  0 0 0 0 .68  0 0 0 0 1  0 0 0 .55 -.14"/></filter>
 <filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="3"/><feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 -.18"/></filter>
 <filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="5"/></filter>
 <marker id="ar" viewBox="0 0 10 6" refX="10" refY="3" markerWidth="10" markerHeight="6" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 3L0 6Z" fill="{PAPER}"/></marker>
 <marker id="ar2" viewBox="0 0 10 6" refX="10" refY="3" markerWidth="8" markerHeight="5" markerUnits="userSpaceOnUse" orient="auto-start-reverse"><path d="M0 0L10 3L0 6Z" fill="{PAPER}"/></marker>
 <mask id="pm" maskUnits="userSpaceOnUse" x="0" y="0" width="1440" height="900"><path d="{PATH_D}" fill="none" stroke="#fff" stroke-width="8" pathLength="1" class="reveal"/></mask>
 <clipPath id="dclip"><circle cx="885" cy="492" r="53"/></clipPath>
</defs>'''

# ---- sheet
sheet = f'''
<rect width="1440" height="900" fill="{GROUND}"/>
<rect width="1440" height="900" filter="url(#mottle)" opacity=".16"/>
<rect width="1440" height="900" fill="url(#gm)"/>
<rect width="1440" height="900" fill="url(#gM)"/>
'''

# ---- construction arcs cropping off top-right corner
arcs = f'''
<g fill="none" stroke="{PAPER}" stroke-width="1" stroke-opacity=".28" stroke-dasharray="14 5 2 5">
 <circle cx="1440" cy="0" r="250"/><circle cx="1440" cy="0" r="330"/><circle cx="1440" cy="0" r="372" stroke-dasharray="3 6" stroke-opacity=".4"/>
 <path d="M1190 0L1440 250M1440 0L1110 330" stroke-opacity=".18"/>
</g>'''

# ---- sheet border & zones
zones = ''
for i in range(8):
    cx = 40 + 1360 / 8 * (i + .5)
    zones += f'<text x="{cx:.0f}" y="33" text-anchor="middle">{i+1}</text><text x="{cx:.0f}" y="880" text-anchor="middle">{i+1}</text>'
    if i:
        x = 40 + 1360 / 8 * i
        zones += f'<path d="M{x:.0f} 18V40M{x:.0f} 860V882" fill="none" stroke="{PAPER}" stroke-width="1" stroke-opacity=".6"/>'
for i, ch in enumerate('ABCD'):
    cy = 40 + 820 / 4 * (i + .5) + 4
    zones += f'<text x="29" y="{cy:.0f}" text-anchor="middle">{ch}</text><text x="1411" y="{cy:.0f}" text-anchor="middle">{ch}</text>'
    if i:
        y = 40 + 820 / 4 * i
        zones += f'<path d="M18 {y:.0f}H40M1400 {y:.0f}H1422" fill="none" stroke="{PAPER}" stroke-width="1" stroke-opacity=".6"/>'
border = f'''
<g fill="none" stroke="{PAPER}">
 {dr('rect', 40, 'x="18" y="18" width="1404" height="864" stroke-width="1" stroke-opacity=".7"', d=.06, l=.8)}
 {dr('rect', 40, 'x="40" y="40" width="1360" height="820" stroke-width="2"', d=.1, l=.8)}
</g>
<g class="fd t zn" style="--d:.5s" fill="{PAPER}" fill-opacity=".62" font-size="11">{zones}</g>
'''

# ---- machine
mach = []
m = mach.append
m(f'<g fill="none" stroke="{PAPER}" stroke-linejoin="round" stroke-linecap="butt">')

# ground datum + hatch
hatch = ''.join(f'M{x} 556l-8 10' for x in range(112, 1236, 14))
m(dr('path', 100, f'd="M92 556H1240" stroke-width="1.6"'))
m(dr('path', 100, f'd="{hatch}" stroke-width="1" stroke-opacity=".6"', l=1.4))

# hopper
m(dr('path', 100, 'd="M98 142H282V150H98Z" stroke-width="2"'))
m(dr('path', 110, 'd="M105 150L172 235V258H208V235L275 150" stroke-width="2"'))
m(dr('path', 118, 'd="M113 150L177 228V252H203V228L267 150" stroke-width="1" stroke-opacity=".7"'))
m(dr('path', 118, 'd="M130 200V556M250 150" stroke-width="1"'))
# ramp plate
m(dr('path', 150, 'd="M150 272L450 350V360L150 282Z" stroke-width="2"', l=.7))
m(dr('path', 230, 'd="M230 303V556M330 329V556" stroke-width="1"'))
# rail plates + frame posts
m(dr('path', 450, 'd="M450 350H497V360H450Z M583 350H735V360H583Z" stroke-width="2"'))
m(dr('path', 452, 'd="M452 360V556M735 360V556M440 556H750" stroke-width="1.4"'))
m(dr('path', 452, 'd="M452 360L467 352M735 360L720 352" stroke-width="1"'))
# bearings
m(dr('path', 520, f'd="M{AX-6} 494V556M{AX+6} 494V556" stroke-width="1" stroke-opacity=".8"'))

# gear A (rotating group)
m(f'<g class="gA" style="transform-origin:{AX}px {AY}px">')
m(dr('path', 500, f'd="{gearA}" stroke-width="2"', l=.8))
m(dr('circle', 510, f'cx="{AX}" cy="{AY}" r="46" stroke-width="1"'))
m(dr('circle', 510, f'cx="{AX}" cy="{AY}" r="15" stroke-width="1.4"'))
m(dr('circle', 510, f'cx="{AX}" cy="{AY}" r="7" stroke-width="1.4"'))
m(dr('path', 510, f'd="M{AX-2.5} {AY-7}V{AY-10}H{AX+2.5}V{AY-7}" stroke-width="1"'))
for k in range(5):
    a = math.radians(PHI + 36 + 72 * k)
    m(dr('circle', 520, f'cx="{AX+31*math.cos(a):.1f}" cy="{AY+31*math.sin(a):.1f}" r="8" stroke-width="1"'))
m('</g>')
# gear B
m(f'<g class="gB" style="transform-origin:{BX:.2f}px {BY:.2f}px">')
m(dr('path', 580, f'd="{gearB}" stroke-width="2"', l=.8))
m(dr('circle', 590, f'cx="{BX:.2f}" cy="{BY:.2f}" r="28" stroke-width="1"'))
m(dr('circle', 590, f'cx="{BX:.2f}" cy="{BY:.2f}" r="12" stroke-width="1.4"'))
m(dr('circle', 590, f'cx="{BX:.2f}" cy="{BY:.2f}" r="5.5" stroke-width="1.4"'))
for k in range(4):
    a = math.radians(PHI + 45 + 90 * k)
    m(dr('circle', 600, f'cx="{BX+20*math.cos(a):.1f}" cy="{BY+20*math.sin(a):.1f}" r="4.6" stroke-width="1"'))
m('</g>')

# gate
m(dr('path', 840, 'd="M840 306H890V314H840Z M846 314V390M852 314V390M878 314V390M884 314V390" stroke-width="1.4"'))
m(dr('circle', 860, 'cx="865" cy="314" r="4.5" stroke-width="1.4"'))
m(dr('path', 860, 'd="M865 318L871.5 366" stroke-width="3"'))
# conveyor
m(dr('path', 790, 'd="M792 390H1098A22 22 0 0 1 1098 434H792A22 22 0 0 1 792 390Z" stroke-width="2"', l=.9))
for cx in (792, 1098):
    m(dr('circle', cx, f'cx="{cx}" cy="412" r="12" stroke-width="1.4"'))
    m(dr('circle', cx, f'cx="{cx}" cy="412" r="4" stroke-width="1.4"'))
    m(dr('path', cx, f'd="M{cx-12} 412H{cx+12}M{cx} 400V424" stroke-width="1" stroke-opacity=".7"'))
for cx in (900, 995):
    m(dr('circle', cx, f'cx="{cx}" cy="413" r="7" stroke-width="1"'))
m(dr('path', 800, 'd="M792 434L780 556M1098 434L1110 556M770 556H800" stroke-width="1"'))
# tick marks on belt top
ticks = ''.join(f'M{x} 390v-5' for x in range(812, 1090, 22))
m(dr('path', 820, f'd="{ticks}" stroke-width="1" stroke-opacity=".7"', l=.9))
# chute
m(dr('path', 1130, 'd="M1130 402L1300 572M1130 414L1300 584M1130 402V414M1300 572V584" stroke-width="2"', l=.7))
m(dr('path', 1190, 'd="M1190 474V556" stroke-width="1"'))
# tray
m(dr('path', 1260, 'd="M1250 590H1270M1262 590V660H1390V590M1382 590H1402" stroke-width="2"'))
m(dr('path', 1340, 'd="M1352 660L1356 612M1372 660L1376 612" stroke-width="1.2"'))
m(dr('path', 1250, 'd="M1240 672H1412" stroke-width="1.6"'))
m(dr('path', 1250, 'd="' + ''.join(f'M{x} 672l-8 10' for x in range(1250, 1410, 14)) + '" stroke-width="1" stroke-opacity=".6"'))
m('</g>')

# centerlines (dash-dot, fade)
cl = f'''
<g fill="none" stroke="{PAPER}" stroke-width="1" stroke-dasharray="16 4 3 4" stroke-opacity=".85">
 <path d="M{AX-88} {AY}H{AX+88}M{AX} {AY-88}V{AY+88}"/>
 <path d="M{BX-66:.2f} {BY:.2f}H{BX+66:.2f}M{BX:.2f} {BY-66:.2f}V{BY+66:.2f}"/>
 <path d="M{AX-62*math.cos(math.radians(PHI)):.1f} {AY-62*math.sin(math.radians(PHI)):.1f}L{BX+66*math.cos(math.radians(PHI)):.1f} {BY+66*math.sin(math.radians(PHI)):.1f}" stroke-opacity=".6"/>
 <path d="M792 390V434M1098 390V434" stroke-opacity="0"/>
 <path d="M770 412H1120"/>
 <path d="M190 128V262" />
</g>
<g fill="none" stroke="{PAPER}" stroke-width="1" stroke-dasharray="2 4" stroke-opacity=".7">
 <circle cx="{AX}" cy="{AY}" r="{rpA}"/><circle cx="{BX:.2f}" cy="{BY:.2f}" r="{rpB}"/>
</g>'''
cl = fd(cl, 1.0)

# ---- station labels
def station(num, cx, cy, text, tx, light, anchor='start'):
    inner = (f'<circle cx="{cx}" cy="{cy}" r="11" fill="none" stroke="{PAPER}" stroke-width="1.4"/>'
             f'<text x="{cx}" y="{cy+4.5}" text-anchor="middle" class="t" font-size="13" font-weight="700" fill="{PAPER}">{num}</text>'
             f'<text x="{tx}" y="{cy+5.5}" text-anchor="{anchor}" class="t" font-size="17" font-weight="600" letter-spacing="2.4" fill="{PAPER}">{text}</text>')
    pulse = f'<circle class="lp" style="--lt:{light:.2f}s" cx="{cx}" cy="{cy}" r="11" fill="none" stroke="{PAPER}" stroke-width="1.2"/>'
    return (f'<g class="fd" style="--d:{max(.6, dly(cx)+.3):.2f}s"><g class="lt" style="--lt:{light:.2f}s">{inner}</g>{pulse}</g>')

stations = ''.join([
    station(1, 124, 112, 'ENQUIRY ARRIVES', 144, T0 - 0.02),
    station(2, 822, 268, 'SORTED', 842, tt(fGate) - .05),
    station(3, 950, 345, 'REPLY SENT', 970, tt(fReply) - .05),
    station(4, 1290, 700, 'FILED', 1310, T0 + TD - .08),
])
# leaders for stations
leaders = f'''<g fill="none" stroke="{PAPER}" stroke-width="1" stroke-opacity=".8">
 <path d="M124 123V142"/><path d="M834 276L862 306" /><path d="M950 356V384"/><path d="M1290 689V672"/></g>'''
leaders = fd(leaders, 1.1)

# ---- dimensions
def hdim(x1, x2, y, txt, e1, e2, ty=-7):
    s = f'<path d="M{x1} {e1}V{y+6}M{x2} {e2}V{y+6}" stroke-width="1" fill="none"/>'
    s += f'<path d="M{x1} {y}H{x2}" stroke-width="1" fill="none" marker-start="url(#ar)" marker-end="url(#ar)"/>'
    s += f'<path d="M{x1-4} {y+4}L{x1+4} {y-4}M{x2-4} {y+4}L{x2+4} {y-4}" stroke-width="1.4" fill="none"/>'
    s += f'<text x="{(x1+x2)/2}" y="{y+ty}" text-anchor="middle" class="t" font-size="13" fill="{PAPER}" stroke="none" letter-spacing="1">{txt}</text>'
    return s

dims = f'<g stroke="{PAPER}" fill="none">'
dims += hdim(452, 735, 590, '283', 560, 560)
# vertical dim at left
dims += f'<path d="M94 150H66M88 556H66" stroke-width="1"/><path d="M72 150V556" stroke-width="1" marker-start="url(#ar)" marker-end="url(#ar)"/>'
dims += f'<text transform="translate(63 353) rotate(-90)" text-anchor="middle" class="t" font-size="13" fill="{PAPER}" stroke="none" letter-spacing="1">406</text>'
# angle
dims += f'<path d="M450 350H380" stroke-width="1" stroke-dasharray="4 3"/><path d="M394 350A56 56 0 0 1 395.8 335.9" stroke-width="1"/>'
dims += f'<text x="358" y="370" class="t" font-size="13" fill="{PAPER}" stroke="none" letter-spacing="1">15°</text>'
# gear leader
dims += f'<path d="M{AX-67.7:.1f} {AY-24.6:.1f}L420 420H350" stroke-width="1" marker-start="url(#ar2)"/>'
dims += (f'<text x="352" y="415" class="t" font-size="13" fill="{PAPER}" stroke="none" letter-spacing="1">Z = 14</text>'
         f'<text x="352" y="436" class="t" font-size="13" fill="{PAPER}" stroke="none" letter-spacing="1">PD 128</text>')
# hopper width
dims += hdim(105, 275, 82, '160', 140, 140)
# cutting plane C
dims += (f'<path d="M1050 366V470" stroke-width="1.4" stroke-dasharray="14 4 3 4"/><path d="M1050 458H1030" stroke-width="2" marker-end="url(#ar)"/>'
         f'<circle cx="1050" cy="492" r="11" stroke-width="1.4"/><text x="1050" y="496.5" text-anchor="middle" class="t" font-size="13" font-weight="700" fill="{PAPER}" stroke="none">C</text>')
# scale bar
sb = 1010
dims += f'<path d="M{sb} 722H{sb+200}M{sb} 716V728M{sb+100} 718V726M{sb+200} 716V728" stroke-width="1.4"/>'
dims += f'<path d="M{sb} 718H{sb+100}V722H{sb}Z" fill="{PAPER}" stroke-width="1"/>'
dims += (f'<text x="{sb}" y="709" class="t" font-size="11" fill="{PAPER}" stroke="none" letter-spacing="1.5">0</text>'
         f'<text x="{sb+100}" y="709" text-anchor="middle" class="t" font-size="11" fill="{PAPER}" stroke="none" letter-spacing="1.5">50</text>'
         f'<text x="{sb+200}" y="709" text-anchor="end" class="t" font-size="11" fill="{PAPER}" stroke="none" letter-spacing="1.5">100 MM</text>')
dims += '</g>'
dims = fd(dims, 2.45, 'dm')

# ---- detail A: dashed circle on gear B hub, leader, bubble with exploded view
dA = f'<g fill="none" stroke="{PAPER}">'
dA += f'<circle cx="{BX:.2f}" cy="{BY:.2f}" r="23" stroke-width="1.2" stroke-dasharray="5 3"/>'
dA += f'<path d="M{BX+23:.1f} {BY:.1f}L{BX+60:.0f} 500H832" stroke-width="1"/>'
dA += f'<circle cx="{BX+78:.0f}" cy="500" r="10" fill="{GROUND}" stroke-width="1.4"/>'
dA += f'<text x="{BX+78:.0f}" y="504.5" text-anchor="middle" class="t" font-size="13" font-weight="700" fill="{PAPER}" stroke="none">A</text>'
dA += f'<circle cx="885" cy="492" r="54" stroke-width="2" fill="{GROUND}" fill-opacity=".85"/>'
dA += '<g clip-path="url(#dclip)" stroke-width="1.2">'
# exploded view along y=492
dA += ('<path d="M836 492H934" stroke-dasharray="10 3 2 3" stroke-width="1" stroke-opacity=".85"/>'
       # shaft
       '<path d="M842 485H928V499H842Z" stroke-width="1.2"/><path d="M842 485V499" stroke-width="1.2"/>'
       # nut
       '<path d="M846 470L852 466H858L864 470V514L858 518H852L846 514Z" stroke-width="1.2"/>'
       # washer
       '<path d="M870 474H874V510H870Z" stroke-width="1.2"/>'
       # gear body
       '<path d="M884 462H900V522H884Z" stroke-width="1.6"/><path d="M884 470H900M884 476H900M884 508H900M884 514H900" stroke-width="1"/>'
       '<path d="M884 482H900V502H884Z" stroke-width="1" stroke-dasharray="3 2"/>'
       # spacer + bearing
       '<path d="M907 478H913V506H907Z" stroke-width="1.2"/><path d="M920 468H930V516H920Z" stroke-width="1.2"/><path d="M920 476H930M920 508H930" stroke-width="1"/>'
       # assembly lines
       '<path d="M858 458V448M874 458V448M892 456V448M910 458V448M925 458V448" stroke-width="1" stroke-dasharray="2 3"/>'
       '<path d="M858 448H925" stroke-width="1" stroke-dasharray="2 3"/>')
dA += '</g>'
dA += '</g>'
dA += (f'<text x="950" y="486" class="t" font-size="13" font-weight="600" letter-spacing="2" fill="{PAPER}">DETAIL A</text><text x="950" y="504" class="t" font-size="12" letter-spacing="1.6" fill="{PAPER}" fill-opacity=".8">SCALE 2:1</text>')
dA = fd(dA, 2.0, 'dt')

# ---- title block (drafting)
tb = f'<g fill="none" stroke="{PAPER}">'
tb += dr('path', 1010, 'd="M1010 860V770H1400" stroke-width="2"', d=2.5, l=.5)
tb += dr('path', 1010, 'd="M1010 800H1400M1010 830H1400M1150 830V860M1310 830V860M1310 800V830" stroke-width="1"', d=2.6, l=.5)
tb += '</g>'
tb += '<g class="t" fill="' + PAPER + '">'
tb += f'<text x="1022" y="792" font-family="Archivo,Arial,sans-serif" font-weight="800" font-size="17" letter-spacing="2.2">PERSEID ECHO CREATIONS</text>'
tb += f'<text x="1022" y="820" font-size="13" font-weight="600" letter-spacing="1.6">GENERAL ARRANGEMENT</text>'
tb += f'<text x="1322" y="820" font-size="13" font-weight="600" letter-spacing="1.6">REV A</text>'
tb += f'<text x="1022" y="850" font-size="13" font-weight="600" letter-spacing="1.6">SHEET 03 OF 07</text>'
tb += f'<text x="1160" y="850" font-size="13" font-weight="600" letter-spacing="1.6">DRAWN BY: BRYAN</text>'
tb += f'<text x="1322" y="850" font-size="13" font-weight="600" letter-spacing="1.6">SCALE 1:1</text>'
tb += '</g>'
i0 = tb.index('<g class="t"')
tb = tb[:i0] + fd(tb[i0:], 2.75)
# the lines are drawn (dr) so wrap separately: re-split
tb_lines = ''
tb_text = ''
# (kept simple: lines inside tb get dr animation, text fades via fd)

# ---- heading block
head = f'''
<g class="lab fd" style="--d:1.75s"><text x="72" y="636" font-family="Archivo,Arial,sans-serif" font-weight="800" font-size="24" fill="{PAPER}">03</text>
<path d="M112 630H184" stroke="{PAPER}" stroke-width="1.4"/>
<text x="196" y="635" class="t" font-size="13" font-weight="600" letter-spacing="3.6" fill="{PAPER}">SERVICE THREE OF SEVEN</text></g>
<g class="hw"><text x="66" y="772" font-family="Archivo,Arial,sans-serif" font-weight="800" font-size="140" letter-spacing="-2" fill="{PAPER}" textLength="925" lengthAdjust="spacing">AUTOMATION</text></g>
<g class="desc fd" style="--d:2.3s"><text x="72" y="814" font-family="Archivo,Arial,sans-serif" font-weight="400" font-size="20" fill="{PAPER}">The busywork runs itself. You get your week back.</text></g>
'''

# ---- ball, path, spark, rings
SPARK_D = 'M-40,262 C 30,206 112,112 190,168'
spark = f'''
<g class="spark" style="offset-path:path('{SPARK_D}')">
 <g filter="url(#glow)" opacity=".5"><circle r="10" fill="{PERS}"/><path d="M0 -5L-60 0L0 5Z" fill="{PERS}"/></g>
 <path d="M0 -3.4L-96 -.5V.5L0 3.4Z" fill="{PERS}" opacity=".9"/>
 <path d="M-8 -1.4L-150 0L-8 1.4Z" fill="{PERS}" opacity=".35"/>
 <circle r="5.2" fill="{PERS}"/><circle r="2" fill="{PAPER}"/>
</g>'''
ball = f'''
<g class="ball" style="offset-path:path('{PATH_D.strip()}')">
 <g filter="url(#glow)" opacity=".4"><circle r="14" fill="{PERS}"/></g>
 <circle r="9" fill="{PERS}" stroke="{PAPER}" stroke-width="1.2"/>
 <path d="M-5 -2A5.6 5.6 0 0 1 1 -6" fill="none" stroke="{PAPER}" stroke-width="1.4" stroke-linecap="round"/>
</g>'''
route = f'<path class="route" d="{PATH_D.strip()}" fill="none" stroke="{PERS}" stroke-width="2" stroke-dasharray="7 6" mask="url(#pm)"/>'
rings = ''
for i, (cx, cy, r, t, c) in enumerate([
        (190, 168, 70, 1.30, 'rg1'), (190, 168, 70, 1.42, 'rg2'), (190, 168, 70, 1.54, 'rg3'),
        (1322, 651, 40, 2.60, 'rg1'), (1322, 651, 40, 2.72, 'rg2')]):
    rings += f'<circle class="rg {c}" style="--d:{t}s" cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{PERS}" stroke-width="1.4"/>'

notes = f'''<g class="t" fill="{PAPER}" font-size="12" letter-spacing="1.6" fill-opacity=".85">
<text x="470" y="96" font-size="13" font-weight="700" letter-spacing="3" fill-opacity="1">GENERAL NOTES</text>
<path d="M470 106H650" stroke="{PAPER}" stroke-width="1" fill="none"/>
<text x="470" y="128">1. ALL DIMENSIONS IN MM.</text><text x="470" y="146">2. ENQUIRIES IN AT HOPPER, REPLIES OUT AT CHUTE.</text><text x="470" y="164">3. NOTHING TO BE LIFTED BY HAND.</text></g>'''
notes = fd(notes, 2.55)
# ---- assemble
CSS = open(os.path.join(os.path.dirname(__file__), 'automation.css')).read()
CSS = (CSS.replace('%GA0%', f'{tt(fA0)-.12:.2f}s').replace('%GADUR%', f'{(tt(fA1)-tt(fA0))+.3:.2f}s')
          .replace('%GB0%', f'{tt(fA0)-.05:.2f}s').replace('%GBDUR%', f'{(tt(fA1)-tt(fA0))+.3:.2f}s')
          .replace('%TD%', f'{TD}s').replace('%T0%', f'{T0}s'))
JS = open(os.path.join(os.path.dirname(__file__), 'automation.js')).read()

html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>PEC World 03: Automation</title>
<meta name="viewport" content="width=1440">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;800&family=Barlow+Semi+Condensed:wght@500;600;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head>
<body><svg id="stage" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
{defs}
{sheet}
{arcs}
{border}
<g id="machine">
{''.join(mach)}
</g>
{cl}
{dA}
{leaders}
{stations}
{dims}
{notes}
{head}
{tb}
{route}
{rings}
{ball}
{spark}
<rect width="1440" height="900" filter="url(#grain)" opacity=".18" style="mix-blend-mode:screen"/>
</svg>
<script>{JS}</script></body></html>'''
out = os.path.join(os.path.dirname(__file__), '..', 'automation.html')
open(out, 'w', encoding='utf-8').write(html)
print('written', len(html), 'bytes; fracs', round(fA0, 3), round(fA1, 3), round(fGate, 3), round(fReply, 3), 'L', round(TOTAL))
