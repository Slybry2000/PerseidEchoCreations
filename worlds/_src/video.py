"""Generator for worlds/video.html (06 VIDEO). Run: python _src/video.py"""
import math, random, os

random.seed(6)
INK = "#07090F"
PAPER = "#F6F6F4"
PERS = "#FF6A2A"
LX, LY = 152, 420  # lamp
SX0, SX1, SY0, SY1 = 780, 1380, 250, 588  # screen
CX, CY = 1080, 419

# ---------- film strip ----------
holes = []
for row_y in (26, 190):
    x = -8
    while x < 1450:
        holes.append(f'<rect x="{x}" y="{row_y}" width="12" height="10" rx="2"/>')
        x += 22
holes = "".join(holes)

FW, FH, FY, PITCH, FX0 = 175, 96, 60, 205, 24

def frame(i):
    fx = FX0 + PITCH * i
    t = i / 6.0
    def pos(tt):
        return 12 + tt * 150, 16 + 46 * (max(tt, 0) ** 1.6) if tt >= 0 else 10
    sx, sy = pos(t)
    px, py = pos(t - 1 / 6.0)
    if i == 0:
        px, py = -14, 6
    stars = "".join(
        f'<circle cx="{x}" cy="{y}" r="0.9" fill="{PAPER}" opacity=".5"/>'
        for x, y in [(30, 12), (74, 22), (118, 10), (146, 28), (56, 38)]
    )
    land = (
        f'<path d="M-2,72 C28,60 50,68 80,62 S132,54 178,66 V98 H-2Z" fill="#0B0E15" stroke="{PAPER}" stroke-width="1" opacity=".9"/>'
        f'<path d="M-2,82 C40,76 92,88 178,78" fill="none" stroke="{PAPER}" stroke-width="1" opacity=".45"/>'
        f'<path d="M22,66 l4,-10 l4,10 M34,67 l3,-8 l3,8 M120,58 l4,-10 l4,10 M132,59 l3,-8 l3,8" fill="none" stroke="{PAPER}" stroke-width="1" opacity=".6"/>'
    )
    if i < 6:
        spark = (
            f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{sx:.1f}" y2="{sy:.1f}" stroke="{PAPER}" stroke-width="1.4" stroke-linecap="round" opacity=".55"/>'
            f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.6" fill="{PAPER}"/>'
        )
    else:
        gx, gy = 158, 58
        spark = (
            f'<circle cx="{gx}" cy="{gy}" r="11" fill="none" stroke="{PERS}" stroke-width="1" opacity=".5"/>'
            f'<circle cx="{gx}" cy="{gy}" r="6" fill="none" stroke="{PERS}" stroke-width="1" opacity=".8"/>'
            f'<circle cx="{gx}" cy="{gy}" r="2.6" fill="{PERS}"/>'
        )
    return (
        f'<g transform="translate({fx},{FY})"><g clip-path="url(#fc)">'
        f'<rect width="{FW}" height="{FH}" fill="#04060A"/>{stars}{land}{spark}'
        f'<rect class="ex" style="--i:{i}" width="{FW}" height="{FH}" fill="#04060A"/></g>'
        f'<rect width="{FW}" height="{FH}" fill="none" stroke="{PAPER}" stroke-opacity=".55" stroke-width="1"/></g>'
        f'<text x="{fx}" y="180" class="edge">{i+1:02d}</text>'
        f'<path d="M{fx+34},172 l9,4 l-9,4z" fill="{PAPER}" opacity=".5"/>'
    )

frames = "".join(frame(i) for i in range(7))
edge_codes = "".join(
    f'<text x="{FX0 + PITCH*i}" y="52" class="edge">PEC 06 SAFETY FILM</text>' for i in (0, 2, 5)
)

# ---------- dust motes ----------
motes = []
for _ in range(44):
    x = random.uniform(215, 765)
    hw = (x - LX) / (SX0 - LX) * (SY1 - 420) - 8
    y = LY + random.uniform(-hw, hw) * 0.95
    r = random.choice([0.8, 1.0, 1.2, 1.6, 2.0])
    o = random.uniform(0.35, 0.9)
    motes.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" opacity="{o:.2f}"/>')
motes = "".join(motes)

# ---------- scratches ----------
scr = ""
for x, y0, y1, o in [(233, 40, 520, .09), (611, 210, 880, .07), (1207, 0, 380, .08), (1363, 330, 900, .06), (906, 520, 890, .05), (47, 260, 700, .06)]:
    scr += f'<line x1="{x}" y1="{y0}" x2="{x+random.choice([-1,1])*1.5}" y2="{y1}" stroke="{PAPER}" stroke-width="1" opacity="{o}"/>'

# ---------- leader ticks ----------
ticks = ""
for a in range(0, 360, 15):
    r0, r1 = (148, 162) if a % 90 == 0 else (148, 156)
    rad = math.radians(a)
    ticks += f'<line x1="{CX+r0*math.sin(rad):.1f}" y1="{CY-r0*math.cos(rad):.1f}" x2="{CX+r1*math.sin(rad):.1f}" y2="{CY-r1*math.cos(rad):.1f}"/>'

# ---------- slate stripes ----------
def stripes(y_top, y_bot, flip):
    out = ""
    x = 1040 - 80
    k = 0
    while x < 1360 + 80:
        if flip:
            pts = f"{x+24},{y_bot} {x},{y_top} {x+20},{y_top} {x+44},{y_bot}"
        else:
            pts = f"{x},{y_bot} {x+24},{y_top} {x+44},{y_top} {x+20},{y_bot}"
        out += f'<polygon points="{pts}"/>'
        x += 80
    return out

arm_stripes = stripes(642, 672, False)
stick_stripes = stripes(672, 702, True)

# ---------- reels ----------
def reel(cx, cy, r):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}"/><circle cx="{cx}" cy="{cy}" r="{r*0.22:.1f}"/>'
    for a in (90, 210, 330):
        rad = math.radians(a)
        s += f'<circle cx="{cx+r*0.58*math.cos(rad):.1f}" cy="{cy-r*0.58*math.sin(rad):.1f}" r="{r*0.2:.1f}"/>'
    return s

reels = reel(52, 336, 46) + reel(148, 330, 38)

html = open(os.path.join(os.path.dirname(__file__), "video.tpl.html"), encoding="utf-8").read()
for k, v in {
    "%%HOLES%%": holes, "%%FRAMES%%": frames, "%%EDGE%%": edge_codes, "%%MOTES%%": motes,
    "%%SCRATCH%%": scr, "%%TICKS%%": ticks, "%%ARM%%": arm_stripes, "%%STICK%%": stick_stripes,
    "%%REELS%%": reels,
}.items():
    html = html.replace(k, v)
out = os.path.join(os.path.dirname(__file__), "..", "video.html")
open(out, "w", encoding="utf-8").write(html)
print("wrote", os.path.abspath(out), len(html))
