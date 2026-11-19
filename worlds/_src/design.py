# Generator for worlds/design.html  (World 05, Digital Design, Swiss International Style)
import os
OUT = os.path.join(os.path.dirname(__file__), '..', 'design.html')

INK = '#0D1321'
PER = '#FF6A2A'
M = 108            # module
X0 = 72            # left/right margin
CX, CY, R = 1044, 342, 162   # the one mark
COLX = [X0 + M * i for i in range(13)]
ROWY = [72 + M * j for j in range(8)]   # 72..828

NUM_X, NUM_Y, NUM_S = 548, 504, 800     # giant numeral

def f(n):
    return ('%g' % n)

p = []
a = p.append

# ---------------- grid ----------------
def grid():
    a('<g class="grid" transform="translate(.5 .5)" fill="none" stroke="%s" stroke-width="1">' % INK)
    # baselines every 27
    a('<g class="bl" stroke-opacity=".055">')
    y = 72 - 27 * 3
    k = 0
    while y <= 900:
        if (y - 72) % M != 0:
            a('<path class="gl" pathLength="1" style="--i:%d" d="M0 %d H1440"/>' % (14 + k % 6, y))
        y += 27
        k += 1
    a('</g>')
    a('<g class="rows" stroke-opacity=".2">')
    for j, y in enumerate(ROWY):
        a('<path class="gl" pathLength="1" style="--i:%d" d="M0 %d H1440"/>' % (13 + j, y))
    a('</g>')
    a('<g class="cols" stroke-opacity=".2">')
    for i, x in enumerate(COLX):
        a('<path class="gl" pathLength="1" style="--i:%d" d="M%d 0 V900"/>' % (i, x))
    a('</g>')
    a('</g>')

# ---------------- printer's apparatus ----------------
def marks():
    a('<g class="marks" fill="none" stroke="%s" stroke-width="1" transform="translate(.5 .5)">' % INK)
    # crop marks (4 corners, offset from trim at the margin box)
    for (x, y, sx, sy) in [(72, 72, -1, -1), (1368, 72, 1, -1), (72, 828, -1, 1), (1368, 828, 1, 1)]:
        a('<path d="M%d %d H%d M%d %d V%d"/>' % (x + sx * 8, y, x + sx * 40, x, y + sy * 8, y + sy * 40))
    # registration targets
    def reg(x, y):
        a('<g><circle cx="%d" cy="%d" r="8"/><circle cx="%d" cy="%d" r="3" fill="%s" stroke="none"/>'
          '<path d="M%d %d H%d M%d %d V%d"/></g>' % (x, y, x, y, INK, x - 18, y, x + 18, x, y - 18, y + 18))
    reg(720, 36)
    reg(720, 864)
    reg(36, 450)
    reg(1404, 450)
    # fold marks (tri-fold)
    for x in (480, 960):
        a('<path d="M%d 0 V12 M%d 888 V900"/>' % (x, x))
    a('</g>')

# ---------------- wireframes ----------------
def device(x, y, w, h, cols, label, n):
    g = []
    g.append('<g class="dev d%d">' % n)
    g.append('<rect x="%g" y="%g" width="%g" height="%g" fill="#fff" stroke="%s" stroke-width="1.5"/>' % (x, y, w, h, INK))
    hb = round(h * 0.12)
    g.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s"/>' % (x, y, w, hb, INK))
    # column grid inside
    for c in range(1, cols):
        cx = x + w * c / cols
        g.append('<path d="M%g %g V%g" stroke="%s" stroke-opacity=".12" stroke-width="1"/>' % (cx, y + hb, y + h, INK))
    # hero block + orange dot, same relative place
    g.append('<rect x="%g" y="%g" width="%g" height="%g" fill="%s" fill-opacity=".09"/>' % (x + w * .08, y + h * .2, w * .84, h * .38, INK))
    g.append('<circle cx="%g" cy="%g" r="%g" fill="%s"/>' % (x + w * .7, y + h * .39, w * .075, PER))
    # text lines
    for k, wf in enumerate((.6, .8, .45)):
        g.append('<rect x="%g" y="%g" width="%g" height="3" fill="%s" fill-opacity=".55"/>' % (x + w * .08, y + h * (.68 + .08 * k), w * wf * .84 + 0, INK))
    g.append('<text class="t" x="%g" y="%g">%s</text>' % (x, y + h + 22, label))
    g.append('</g>')
    return ''.join(g)

# ---------------- build ----------------
a('''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<title>05 Digital Design | Perseid Echo Creations</title>
<meta name="viewport" content="width=1440">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;800&display=swap" rel="stylesheet">
<style>
html,body{margin:0;overflow:hidden;background:#fff}
svg{display:block;width:1440px;height:900px}
text{font-family:Archivo,"Helvetica Neue",Helvetica,Arial,sans-serif;fill:#0D1321}
.t{font-size:11px;font-weight:500;letter-spacing:.14em}
.tw{fill:#fff}
:root{--out:cubic-bezier(.16,.84,.3,1);--snap:cubic-bezier(.2,.9,.25,1);--fly:cubic-bezier(.45,.05,.55,.95)}
.spark,.ring{opacity:0}
.gl,.cl{stroke-dasharray:1;stroke-dashoffset:0}
@keyframes draw{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes snap{0%{opacity:0;transform:translate(var(--dx,0px),var(--dy,0px))}35%{opacity:1}100%{opacity:1;transform:none}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes wipe{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes pop{from{transform:scale(0)}to{transform:scale(1)}}
@keyframes flyx{from{transform:translateX(0)}to{transform:translateX(1064px)}}
@keyframes trail{0%{stroke-dashoffset:1;opacity:1}70%{stroke-dashoffset:0;opacity:1}100%{stroke-dashoffset:0;opacity:0}}
@keyframes sparkx{0%{opacity:1}100%{opacity:1}}
@keyframes ring{0%{opacity:0;transform:scale(1)}6%{opacity:.8;transform:scale(1.05)}100%{opacity:0;transform:scale(2.1)}}
@keyframes bar{from{transform:scaleX(0)}to{transform:scaleX(1)}}
.play .gl{animation:draw .42s var(--out) calc(.05s + var(--i) * .034s) backwards}
.play .spark{animation:flyx 1.35s var(--fly) .05s backwards,sparkx 1.35s linear .05s backwards}
.play .trail{animation:trail 1.9s linear .05s backwards;animation-timing-function:var(--fly),linear}
.play .dot{transform-origin:__CX__px __CY__px;animation:pop .55s var(--out) 1.4s backwards}
.play .rg1{transform-origin:__CX__px __CY__px;animation:ring .95s cubic-bezier(.2,.6,.3,1) 1.4s backwards}
.play .rg2{transform-origin:__CX__px __CY__px;animation:ring .95s cubic-bezier(.2,.6,.3,1) 1.52s backwards}
.play .rg3{transform-origin:__CX__px __CY__px;animation:ring .95s cubic-bezier(.2,.6,.3,1) 1.64s backwards}
.play .inkbar{--dx:-40px;animation:snap .3s var(--snap) 1.7s backwards}
.play .numeral{--dx:40px;animation:snap .32s var(--snap) 1.8s backwards}
.play .col{--dx:24px;animation:snap .3s var(--snap) 1.92s backwards}
.play .d1{--dx:-30px;animation:snap .3s var(--snap) 2.0s backwards}
.play .d2{--dx:-30px;animation:snap .3s var(--snap) 2.1s backwards}
.play .d3{--dx:-30px;animation:snap .3s var(--snap) 2.2s backwards}
.play .cl{animation:draw .55s var(--out) calc(1.8s + var(--j) * .06s) backwards}
.play .lab{animation:fade .3s linear 2.0s backwards}
.play .h1{--dx:-34px;animation:snap .32s var(--snap) 2.05s backwards,wipe .32s linear 2.05s backwards}
.play .h2{--dx:-34px;animation:snap .32s var(--snap) 2.2s backwards,wipe .32s linear 2.2s backwards}
.play .desc{--dx:-20px;animation:snap .3s var(--snap) 2.42s backwards}
.play .tint{animation:fade .3s linear 1.95s backwards}
.play .meas{animation:fade .35s linear calc(2.55s + var(--k) * .07s) backwards}
.play .cbar rect{transform-box:fill-box;transform-origin:0 0;animation:bar .3s var(--out) calc(2.8s + var(--k) * .05s) backwards}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.spark,.ring{display:none!important}}
</style></head><body>
<svg id="sheet" viewBox="0 0 1440 900" xmlns="http://www.w3.org/2000/svg">
<rect width="1440" height="900" fill="#fff"/>
'''.replace('__CX__', str(CX)).replace('__CY__', str(CY)))

grid()
marks()

# tint blocks (module cells)
a('<g class="tint">')
a('<rect x="%d" y="72" width="108" height="108" fill="%s" fill-opacity=".08"/>' % (COLX[2], INK))
a('<rect x="%d" y="72" width="108" height="108" fill="%s" fill-opacity=".22"/>' % (COLX[3], INK))
a('</g>')

# giant numeral (cropped off top and right), behind the circle
a('<g class="numeral"><text x="%d" y="%d" font-size="%d" font-weight="800" letter-spacing="-30" style="font-weight:800">05</text></g>' % (NUM_X, NUM_Y, NUM_S))

# thick ink bar ending on the circle's vertical center line
a('<g class="inkbar"><rect x="%d" y="504" width="%d" height="24" fill="%s"/></g>' % (504, CX - 504, INK))

# construction lines (draw out from the circle)
a('<g class="cons" fill="none" stroke="#fff" stroke-width="1" style="mix-blend-mode:difference" transform="translate(.5 .5)">')
cl = [
    ('M%d %d H%d' % (CX, CY, 0), '--j:0', .45, '3 4'),                 # horizontal axis to the left (the flight baseline)
    ('M%d %d V%d' % (CX, CY, 552), '--j:1', .45, '3 4'),
    ('M%d %d V%d' % (CX - R, CY, 0), '--j:2', .7, ''),                # left tangent up
    ('M%d %d V%d' % (CX - R, CY, 552), '--j:2', .7, ''),              # left tangent down
    ('M%d %d V%d' % (CX + R, CY, 0), '--j:3', .7, ''),
    ('M%d %d V%d' % (CX + R, CY, 552), '--j:3', .7, ''),
    ('M%d %d L%d %d' % (CX, CY, 1368, 180), '--j:4', .7, ''),        # 1:2 diagonal up and out
    ('M%d %d L%d %d' % (CX, CY, 720, 504), '--j:4', .7, ''),         # 1:2 diagonal down and back
]
for d, j, op, da in cl:
    a('<path class="cl" pathLength="1" style="%s" d="%s" stroke-opacity="%s"/>' % (j, d, op))
a('</g>')

# the one mark: persimmon circle, echo rings, spark
a('<circle class="ring rg1" cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="1.5"/>' % (CX, CY, R, PER))
a('<circle class="ring rg2" cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="1.5"/>' % (CX, CY, R, PER))
a('<circle class="ring rg3" cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="1.5"/>' % (CX, CY, R, PER))
a('<circle class="dot" cx="%d" cy="%d" r="%d" fill="%s"/>' % (CX, CY, R, PER))
a('<path class="trail" pathLength="1" d="M-20 %d.5 H%d" fill="none" stroke="%s" stroke-width="2" style="stroke-dasharray:1;stroke-dashoffset:1;opacity:0"/>' % (CY, CX, PER))
a('<g class="spark"><circle cx="-20" cy="%d.5" r="16" fill="%s" fill-opacity=".22"/><circle cx="-20" cy="%d.5" r="6" fill="%s"/></g>' % (CY, PER, CY, PER))

# paper-colored labels in the 0 counter / on ink are handled as .tw

# wireframes
a('<g class="wires">')
a(device(72, 252, 72, 144, 4, 'PHONE 4 COL', 1))
a(device(180, 252, 108, 144, 8, 'TABLET 8 COL', 2))
a(device(324, 284, 180, 112, 12, 'DESKTOP 12 COL', 3))
a('</g>')
a('<g class="lab"><text class="t" x="72" y="236">SAME MODULES. THREE SIZES.</text></g>')

# text column flush to the left tangent
tx = CX - R
a('<g class="col">')
for i, s in enumerate(('A page is a decision about what matters most.', 'Start with one mark.', 'Line everything else up with it.')):
    a('<text x="%d" y="%d" font-size="16" font-weight="500">%s</text>' % (tx, 585 + 27 * i, s))
a('</g>')

# title block
a('<g class="tb">')
a('<g class="lab"><text x="72" y="549" font-size="15" font-weight="800">05</text>'
  '<rect x="104" y="543" width="44" height="1.5" fill="%s"/>'
  '<text class="t" x="160" y="549">SERVICE FIVE OF SEVEN</text></g>' % INK)
a('<g class="h1"><text x="66" y="666" font-size="128" font-weight="800" letter-spacing="-5">DIGITAL</text></g>')
a('<g class="h2"><text x="66" y="774" font-size="128" font-weight="800" letter-spacing="-5">DESIGN</text></g>')
a('<g class="desc"><text x="72" y="821" font-size="20" font-weight="400">Sites and pages that look like you mean it.</text></g>')
a('</g>')

# measurement labels
a('<g class="meas-all">')
ml = [
    (72, 112, 'GRID 12 COL x 7 ROW'), (72, 130, 'MODULE 108'), (72, 148, 'BASELINE 27'), (72, 166, 'MARK DIAMETER 324'),
]
for k, (x, y, s) in enumerate(ml):
    a('<text class="t meas" style="--k:%d" x="%d" y="%d">%s</text>' % (k, x, y, s))
a('<text class="t meas" style="--k:4" x="%d" y="%d" text-anchor="end">AXIS Y 342</text>' % (CX - R - 12, CY - 8))
a('<text class="t tw meas" style="--k:5" x="%d" y="%d">TANGENT X 882</text>' % (CX - R + 8, 168))
a('<text class="t meas" style="--k:6" x="%d" y="%d">DIAGONAL 1 : 2</text>' % (1224, 272))
a('</g>')

# color bar (ink tints and the one mark)
a('<g class="cbar">')
cb = [(INK, 1), (INK, .75), (INK, .5), (INK, .25), (INK, .1), (PER, 1)]
for k, (c, o) in enumerate(cb):
    a('<rect style="--k:%d" x="%d" y="852" width="20" height="14" fill="%s" fill-opacity="%s"/>' % (k, 1368 - 20 * 6 + 20 * k, c, o))
a('</g>')
a('<g class="meas" style="--k:7"><text class="t" x="%d" y="846" text-anchor="end">INK 100 75 50 25 10 + MARK</text></g>' % 1358)

a('</svg>')
a('''<script>
window.SPARK_ENTRY = {x:0, y:342.5, t:0.16};
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
</script></body></html>''')

open(OUT, 'w', encoding='utf-8').write('\n'.join(p))
print('wrote', os.path.abspath(OUT))
