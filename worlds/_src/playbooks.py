# Generator for worlds/playbooks.html  (World 07, TEAM PLAYBOOKS, field manual)
# Run: python site/worlds/_src/playbooks.py
import os, random

INK = "#0D1321"
PAGE = "#F5F1E6"
GROUND = "#EFE9DC"
PERS = "#FF6A2A"

random.seed(7)
PX, PW = 660, 725           # page x, width
TOP0, PITCH = 126, 108      # first row top, row pitch
FX = 1196                   # figure frame x
TXT_X = 826
BOX_X = 778


def dr(el, attrs="", cls="dr"):
    return f'<{el} pathLength="1" class="{cls}" {attrs}/>'


def co(letter, cx, cy):
    return (f'<g class="fi"><circle cx="{cx}" cy="{cy}" r="8.5" fill="{PAGE}" stroke="{INK}" stroke-width="1.4"/>'
            f'<text x="{cx}" y="{cy+4}" class="cl" text-anchor="middle">{letter}</text></g>')


def ld(x1, y1, x2, y2):
    return dr("line", f'x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke-width="1.2"')


def ah(pts):
    return f'<polygon class="fi" points="{pts}" fill="{INK}" stroke="none"/>'


def fig1():
    s = []
    s.append(dr("rect", 'x="72" y="18" width="50" height="60" rx="4"'))
    s.append(dr("circle", 'cx="97" cy="25" r="2"'))
    s.append(dr("circle", 'cx="97" cy="71" r="2"'))
    s.append(dr("circle", 'cx="97" cy="48" r="13"'))
    s.append(dr("circle", 'cx="22" cy="48" r="11"'))
    s.append(dr("circle", 'cx="22" cy="48" r="4"'))
    s.append(dr("path", 'd="M33 45 H92 V51 H80 V55 H75 V51 H68 V57 H63 V51 H33"'))
    s.append(dr("path", 'd="M90.2 29.2 A20 20 0 0 1 115.8 41.2"'))
    s.append(ah("117.2,46.4 120,39.7 111.6,42.7"))
    s.append(ld(14.5, 29.5, 19, 37.5)); s.append(co("A", 12, 22))
    s.append(ld(58.5, 26, 86.6, 40.2)); s.append(co("B", 52, 22))
    return "".join(s)


def fig2():
    s = []
    s.append(dr("rect", 'x="44" y="14" width="44" height="64" rx="3"'))
    s.append(dr("rect", 'x="56" y="30" width="20" height="32" rx="2"'))
    s.append(dr("path", 'd="M59 33 H73 V46 H59 Z"'))
    s.append(dr("circle", 'cx="66" cy="21" r="2.2"'))
    s.append(dr("circle", 'cx="66" cy="71" r="2.2"'))
    s.append(dr("path", 'd="M108 62 V30"'))
    s.append(ah("108,23 103.5,32 112.5,32"))
    s.append(ld(23, 29, 58, 38)); s.append(co("A", 16, 24))
    s.append(ld(115.5, 46, 110, 46)); s.append(co("B", 124, 46))
    return "".join(s)


def fig3():
    s = []
    s.append(dr("path", 'd="M28 44 L38 10 H98 L108 44 Z"'))
    s.append(dr("rect", 'x="46" y="15" width="44" height="13"', ))
    for x in (50, 64, 78):
        s.append(dr("rect", f'x="{x}" y="33" width="8" height="6"', "dr thin"))
    s.append(dr("rect", 'x="22" y="44" width="92" height="14"'))
    s.append(dr("path", 'd="M14 58 H122 L128 78 H8 Z"'))
    s.append(dr("path", 'd="M38 58 L35 78 M68 58 V78 M98 58 L101 78"', "dr thin"))
    s.append(ld(22.5, 19, 46, 21)); s.append(co("A", 14, 18))
    s.append(ld(122, 48.5, 117, 62)); s.append(co("B", 124, 40))
    return "".join(s)


def fig4():
    s = []
    s.append(dr("circle", 'cx="68" cy="14" r="3"'))
    s.append(dr("path", 'd="M68 17 L44 34 M68 17 L92 34"'))
    s.append(dr("rect", 'x="24" y="34" width="88" height="38" rx="3"'))
    s.append(dr("rect", 'x="29" y="39" width="78" height="28" rx="2"', "dr thin"))
    s.append(f'<text class="fi sg" x="68" y="62" text-anchor="middle">OPEN</text>')
    s.append(dr("path", 'd="M120 36 C132 44 132 62 120 70"'))
    s.append(ah("117,71.5 123.9,71.1 120.1,65.3"))
    s.append(ld(21, 29, 26, 40)); s.append(co("A", 14, 24))
    s.append(ld(99.5, 14, 71.5, 14)); s.append(co("B", 108, 14))
    return "".join(s)


def fig5():
    s = []
    s.append(dr("rect", 'x="48" y="10" width="40" height="66" rx="6"'))
    s.append(dr("rect", 'x="53" y="20" width="30" height="44"', "dr thin"))
    s.append(dr("path", 'd="M62 15 H74"', "dr thin"))
    s.append(dr("circle", 'cx="68" cy="70" r="2.5"', "dr thin"))
    s.append(dr("rect", 'x="57" y="26" width="20" height="9" rx="3"', "dr thin"))
    s.append(dr("rect", 'x="59" y="40" width="20" height="9" rx="3"', "dr thin"))
    s.append(dr("path", 'd="M57 56 H79"', "dr thin"))
    s.append(dr("path", 'd="M98 32 Q106 44 98 56"'))
    s.append(dr("path", 'd="M104 26 Q116 44 104 62"'))
    s.append(ld(27.5, 31, 48, 38)); s.append(co("A", 20, 28))
    s.append(ld(117, 61.5, 108, 56)); s.append(co("B", 124, 67))
    return "".join(s)


def fig6():
    s = []
    s.append(dr("rect", 'x="22" y="14" width="58" height="64" rx="3"'))
    s.append(dr("rect", 'x="40" y="8" width="22" height="12" rx="2"'))
    for y in (30, 44, 58):
        s.append(dr("rect", f'x="30" y="{y}" width="7" height="7"', "dr thin"))
    s.append(dr("path", 'd="M31.5 33.5 L33.5 35.5 L36.5 30 M31.5 47.5 L33.5 49.5 L36.5 44"', "dr thin"))
    s.append(dr("path", 'd="M42 34 H72 M42 48 H72 M42 62 H66"', "dr thin"))
    s.append(dr("path", 'd="M98 20 H110 V58 L104 70 L98 58 Z M98 28 H110 M98 58 H110"'))
    s.append(ld(17, 30, 22.5, 37)); s.append(co("A", 10, 24))
    s.append(ld(117.5, 38, 110.5, 40)); s.append(co("B", 126, 36))
    return "".join(s)


FIGS = [fig1, fig2, fig3, fig4, fig5, fig6]
STEPS = [
    ["1. Unlock the front door", "and the till."],
    ["2. Lights on, front to back."],
    ["3. Count the float.", "Write it down."],
    ["4. Flip the sign."],
    ["5. Check messages.", "Reply before nine."],
    ["6. Sign this page."],
]


def j(v, a=1.2):
    return round(v + random.uniform(-a, a), 1)


def rows():
    out = []
    for i, lines in enumerate(STEPS):
        top = TOP0 + PITCH * i
        d0 = round(0.28 + 0.1 * i, 2)
        by = top + 33
        # hand-ruled checkbox (overshooting corners)
        x1, x2, y1, y2 = BOX_X, BOX_X + 30, by, by + 30
        box = (f"M{x1-3.5},{y1+0.6} L{x2+4},{y1-0.4} "
               f"M{x2-0.6},{y1-3.5} L{x2+0.6},{y2+3.5} "
               f"M{x2+3.5},{y2-0.4} L{x1-4},{y2+0.6} "
               f"M{x1+0.6},{y2+3.5} L{x1-0.4},{y1-3.5}")
        out.append(f'<path pathLength="1" class="dr cb" style="--d:{d0}s" d="{box}" stroke-width="2.2"/>')
        # text
        base = top + (81 if len(lines) == 1 else 54)
        ts = ""
        for k, ln in enumerate(lines):
            if k == 0:
                ts += f'<tspan x="{TXT_X}" y="{base}">{ln}</tspan>'
            else:
                ts += f'<tspan x="{TXT_X}" y="{base+27}">{ln}</tspan>'
        out.append(f'<text class="tw st" style="--d:{round(d0+0.08,2)}s" font-size="20">{ts}</text>')
        # figure
        fy = top + 11
        out.append(
            f'<g transform="translate({FX},{fy})" class="figg" style="--d:{round(d0+0.12,2)}s">'
            f'<rect x="0" y="0" width="136" height="84" fill="{PAGE}" stroke="none"/>'
            f'<g class="fg">'
            f'{dr("rect", "x=\"0\" y=\"0\" width=\"136\" height=\"84\"", "dr frm")}'
            f'{FIGS[i]()}'
            f'<rect x="7" y="-7" width="58" height="14" fill="{PAGE}" stroke="none"/>'
            f'<text class="mo fi" x="11" y="4" font-size="11">FIG. {i+1}</text>'
            f'</g></g>')
    return "".join(out)


def ticks():
    out = []
    for i in range(5):
        top = TOP0 + PITCH * i
        by = top + 33
        d = round(0.8 + 0.1 * i, 2)
        s1 = f"M{j(BOX_X+5)},{j(by+16)} L{j(BOX_X+12)},{j(by+27)}"
        s2 = f"M{j(BOX_X+12)},{j(by+27)} C{j(BOX_X+17)},{j(by+14)} {j(BOX_X+25)},{j(by+2)} {j(BOX_X+37)},{j(by-8)}"
        out.append(f'<path pathLength="1" class="dr tk a" style="--d:{d}s" d="{s1}"/>')
        out.append(f'<path pathLength="1" class="dr tk b" style="--d:{round(d+0.07,2)}s" d="{s2}"/>')
    return "".join(out)


def ground_rules():
    s = []
    y = TOP0 - 27 * 5
    while y < 900:
        s.append(f'<line x1="0" x2="{PX}" y1="{y}" y2="{y}"/>')
        y += 27
    return "".join(s)


def page_rules():
    s = []
    y = TOP0
    while y <= 830:
        s.append(f'<line x1="{PX}" x2="{PX+PW}" y1="{y}" y2="{y}"/>')
        y += 27
    return "".join(s)


def ruler():
    s = []
    for n in range(0, 45):
        x = 72 + n * 12
        h = 14 if n % 5 == 0 else 7
        s.append(f'<line x1="{x}" x2="{x}" y1="0" y2="{h}"/>')
        if n % 5 == 0 and n < 45:
            s.append(f'<text x="{x+3}" y="26" class="mo" font-size="11" stroke="none" fill="{INK}" fill-opacity=".6">{n//5}</text>')
    return "".join(s)


def tabs():
    labels = ["OPEN", "CLOSE", "REFUNDS", "NEW HIRE"]
    ys = [112, 268, 424, 580]
    out = []
    for k, (lab, y) in enumerate(zip(labels, ys)):
        fill = PAGE if k == 0 else "#E6DEC9"
        d = round(2.45 + 0.1 * k, 2)
        # tab hangs off the right edge of the page, cropping off the canvas
        out.append(
            f'<g class="tab" style="--d:{d}s">'
            f'<path d="M1380,{y} H1438 a6,6 0 0 1 6,6 V{y+144} a6,6 0 0 1 -6,6 H1380 Z" fill="{fill}" stroke="{INK}" stroke-width="1.5"/>'
            f'<text class="cn tt" transform="translate(1416,{y+75}) rotate(90)" text-anchor="middle">{lab}</text>'
            f'</g>')
    return "".join(out)


CSS = """
html,body{margin:0;overflow:hidden;background:#EFE9DC}
svg{display:block;width:1440px;height:900px}
.ar{font-family:'Archivo',Arial,sans-serif;font-weight:800}
.ad{font-family:'Archivo',Arial,sans-serif;font-weight:400}
.tw{font-family:'Special Elite','Courier New',monospace}
.mo{font-family:'Courier Prime','Courier New',monospace;font-weight:700;letter-spacing:.08em}
.cn{font-family:'Barlow Condensed','Archivo Narrow',Arial,sans-serif;font-weight:700}
.sg{font-family:'Stardos Stencil','Archivo',sans-serif;font-weight:700}
.cl{font-family:'Barlow Condensed',Arial,sans-serif;font-weight:700;font-size:12px;fill:#0D1321}
.sg.fi{font-size:24px;letter-spacing:3px;fill:#0D1321;stroke:none}
.tt{font-size:16px;letter-spacing:.2em;fill:#0D1321}
.mul{mix-blend-mode:multiply}
.dr{fill:none;stroke:#0D1321;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 2}
.dr.thin{stroke-width:1.4}
.dr.frm{stroke-width:1.4}
.figg .fi{}
.ck{fill:none;stroke:#FF6A2A;stroke-width:12;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:1 2}
.tk{stroke-width:3.6}
.trail{fill:none;stroke:#FF6A2A;stroke-opacity:.3;stroke-width:1.6;stroke-linecap:round;stroke-dasharray:1 2}
.spark,.rg{display:none}
.rg{opacity:0;fill:none;stroke:#FF6A2A;stroke-width:2.6;vector-effect:non-scaling-stroke;transform-origin:815px 708px}
:root{--fly:cubic-bezier(.35,.05,.7,.75);--out:cubic-bezier(.16,.84,.3,1);--io:cubic-bezier(.5,.05,.25,1)}
.play .spark{display:inline;offset-path:path('M-30,262 C150,40 520,20 668,300 C700,380 735,610 758,716');offset-rotate:auto;animation:fly 1.4s var(--fly) .05s backwards}
.play .sparkin{animation:sparkend 1.4s linear .05s both}
.play .rg{display:inline}
.play .trail{animation:dash 1.4s var(--fly) .05s backwards}
.play .hdr1{animation:wipeX .5s steps(30,end) .15s backwards}
.play .hdr2{animation:wipeX .5s steps(30,end) .25s backwards}
.play .hdrule{transform-origin:758px 0;animation:rule .5s var(--out) .4s backwards}
.play .cb{animation:dash .26s var(--out) var(--d) backwards}
.play .st{animation:wipeX .4s steps(26,end) var(--d) backwards}
.play .figg{animation:figin .01s linear var(--d) backwards}
.play .figg .frm{animation:dash .35s var(--out) var(--d) backwards}
.play .figg .dr:not(.frm){animation:dash .6s var(--out) calc(var(--d) + .08s) backwards}
.play .figg .fi{animation:fade .3s linear calc(var(--d) + .5s) backwards}
.play .tk.a{animation:dash .08s linear var(--d) backwards}
.play .tk.b{animation:dash .11s cubic-bezier(.3,.7,.2,1) var(--d) backwards}
.play .ck{animation:dash .24s cubic-bezier(.25,.7,.2,1) 1.45s backwards}
.play .rg1{animation:ring .9s cubic-bezier(.2,.6,.3,1) 1.45s backwards}
.play .rg2{animation:ring .9s cubic-bezier(.2,.6,.3,1) 1.58s backwards}
.play .rg3{animation:ring .9s cubic-bezier(.2,.6,.3,1) 1.71s backwards}
.play .stampo{transform-origin:1274px 70px;animation:thump .36s cubic-bezier(.2,.8,.25,1) 1.78s backwards}
.play .lbl{animation:fadeUp .4s var(--out) 1.8s backwards}
.play .hw1{transform-origin:72px 700px;animation:pressin .5s var(--out) 1.85s backwards}
.play .hw2{transform-origin:72px 782px;animation:pressin .5s var(--out) 1.98s backwards}
.play .desc{animation:fadeUp .45s var(--out) 2.3s backwards}
.play .fold{animation:fadeUp .5s var(--out) 2.4s backwards}
.play .rul{animation:wipeX .7s var(--io) 2.35s backwards}
.play .tab{animation:tabin .45s var(--out) var(--d) backwards}
.play .foot{animation:wipeX .6s steps(48,end) 2.75s backwards}
.play .pgno{animation:fade .4s linear 3s backwards}
.play .clip{animation:fadeUp .5s var(--out) 2.6s backwards}
@keyframes fly{from{offset-distance:0%}to{offset-distance:100%}}
@keyframes sparkend{0%,92%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(.3)}}
@keyframes dash{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}
@keyframes wipeX{from{clip-path:inset(0 100% 0 0)}to{clip-path:inset(0 0 0 0)}}
@keyframes rule{from{transform:scaleX(0)}to{transform:scaleX(1)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes figin{from{opacity:0}to{opacity:1}}
@keyframes fadeUp{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes ring{0%{opacity:0;transform:scale(.04)}8%{opacity:1}100%{opacity:0;transform:scale(1)}}
@keyframes pressin{0%{opacity:0;transform:scale(1.14)}100%{opacity:1;transform:scale(1)}}
@keyframes thump{0%{opacity:0;transform:scale(1.5)}55%{opacity:1;transform:scale(.95)}100%{opacity:1;transform:scale(1)}}
@keyframes tabin{from{transform:translateX(-64px)}to{transform:translateX(0)}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}.spark,.rg{display:none!important}}
"""

JS = """
window.SPARK_ENTRY = {x:0, y:228.2, t:0.205};
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
"""

CHECK = "M758,716 C770,728 780,742 788,756 C812,712 846,682 880,656"

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 900" width="1440" height="900">
<defs>
<filter id="fibA" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" seed="4"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="fibB" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.55" numOctaves="2" seed="11"/><feColorMatrix type="saturate" values="0"/></filter>
<filter id="rough" x="-5%" y="-10%" width="110%" height="120%">
<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="3" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  9 0 0 0 -2.3" result="m"/>
<feComposite in="SourceGraphic" in2="m" operator="in" result="s"/>
<feTurbulence type="turbulence" baseFrequency="0.06" numOctaves="2" seed="8" result="w"/>
<feDisplacementMap in="s" in2="w" scale="1.5"/></filter>
<filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="6"/></filter>
<linearGradient id="tailg" x1="0" x2="1" y1="0" y2="0"><stop offset="0" stop-color="{PERS}" stop-opacity="0"/><stop offset="1" stop-color="{PERS}" stop-opacity=".9"/></linearGradient>
</defs>

<!-- ground -->
<rect width="1440" height="900" fill="{GROUND}"/>
<g stroke="{INK}" stroke-opacity=".07" stroke-width="1">{ground_rules()}</g>

<!-- ruler along top edge -->
<g class="rul"><line x1="72" x2="612" y1="0.5" y2="0.5" stroke="{INK}" stroke-opacity=".55"/><g stroke="{INK}" stroke-opacity=".55" stroke-width="1.2">{ruler()}</g></g>

<!-- folder label -->
<g class="fold">
<rect x="72" y="46" width="248" height="58" fill="{PAGE}" stroke="{INK}" stroke-width="1.5"/>
<line x1="72" x2="320" y1="62" y2="62" stroke="{INK}" stroke-opacity=".25"/>
<text class="tw" x="86" y="60" font-size="12" fill="{INK}" fill-opacity=".7">DEPT. OF STANDING ORDERS</text>
<text class="tw" x="86" y="86" font-size="19" fill="{INK}">PEC FIELD MANUAL</text>
<text class="mo" x="86" y="99" font-size="11" fill="{INK}" fill-opacity=".7">SECTION 07</text>
</g>

<!-- tabs (behind the page) -->
{tabs()}

<!-- page -->
<rect x="{PX+8}" y="-20" width="{PW}" height="906" fill="{INK}" fill-opacity=".12"/>
<rect x="{PX}" y="-20" width="{PW}" height="900" fill="{PAGE}" stroke="{INK}" stroke-width="1.5"/>
<g stroke="{INK}" stroke-opacity=".16" stroke-width="1">{page_rules()}</g>
<line x1="764" x2="764" y1="-20" y2="880" stroke="{INK}" stroke-opacity=".4" stroke-width="1.2"/>

<!-- binder holes -->
<g>
{''.join(f'<circle cx="692" cy="{y}" r="19" fill="none" stroke="{INK}" stroke-opacity=".22" stroke-width="1"/><circle cx="692" cy="{y}" r="12.5" fill="{GROUND}" stroke="{INK}" stroke-opacity=".55" stroke-width="1.4"/><path d="M{692-12.5},{y} A12.5,12.5 0 0 1 {692+12.5},{y}" fill="none" stroke="{INK}" stroke-opacity=".35" stroke-width="3" transform="translate(0,1)"/>' for y in (176, 450, 724))}
</g>

<!-- header -->
<text class="mo hdr1" x="778" y="52" font-size="11" fill="{INK}" fill-opacity=".7">PEC FIELD MANUAL . SECTION 07</text>
<text class="cn hdr2" x="778" y="90" font-size="28" letter-spacing=".8" fill="{INK}">PROCEDURE 07: OPENING THE SHOP</text>
<g class="hdrule"><line x1="778" x2="1352" y1="104" y2="104" stroke="{INK}" stroke-width="2.5"/><line x1="778" x2="1352" y1="109" y2="109" stroke="{INK}" stroke-width="1"/></g>

<!-- paper clip -->
<g class="clip"><g transform="translate(1100,-14) rotate(7)"><path d="M10 54 V12 A9 9 0 0 1 28 12 V58 A16 16 0 0 1 -4 58 V16 A5 5 0 0 1 6 16 V54" fill="none" stroke="{INK}" stroke-opacity=".8" stroke-width="2" stroke-linecap="round"/></g></g>

<!-- steps -->
{rows()}
{ticks()}

<!-- persimmon trail, spark landing, the check -->
<path pathLength="1" class="trail" d="M-30,262 C150,40 520,20 668,300 C700,380 735,610 758,716"/>
<path pathLength="1" class="ck" d="{CHECK}"/>

<!-- stamp -->
<g class="stampo"><g transform="translate(1270,72) rotate(-5)" style="transform-box:view-box"></g></g>
<g class="stampo" style="transform-origin:1274px 70px"><g transform="rotate(0)"></g></g>

<!-- footer -->
<line x1="778" x2="1352" y1="828" y2="828" stroke="{INK}" stroke-width="1.2" stroke-opacity=".5"/>
<text class="mo foot" x="778" y="852" font-size="11.5" fill="{INK}" style="letter-spacing:.14em">IF IT IS NOT WRITTEN DOWN, IT IS NOT A PROCEDURE.</text>
<text class="sg pgno" x="1352" y="860" font-size="30" text-anchor="end" fill="{INK}">07</text>

<!-- title block -->
<g class="lbl"><text class="ar" x="72" y="606" font-size="24" fill="{INK}">07</text>
<line x1="112" x2="170" y1="600" y2="600" stroke="{INK}" stroke-width="1.6"/>
<text class="mo" x="182" y="605" font-size="11.5" fill="{INK}" style="letter-spacing:.3em">SERVICE SEVEN OF SEVEN</text></g>
<g class="hw1"><text class="ar" x="72" y="700" font-size="88" fill="{INK}" style="letter-spacing:-.03em">TEAM</text></g>
<g class="hw2"><text class="ar" x="72" y="782" font-size="88" fill="{INK}" style="letter-spacing:-.03em">PLAYBOOKS</text></g>
<text class="ad desc" x="72" y="828" font-size="20" fill="{INK}">How your team does it, written down once.</text>

<!-- spark -->
<g class="spark"><g class="sparkin"><circle r="17" fill="{PERS}" opacity=".6" filter="url(#glow)"/><polygon points="0,-5.5 -92,0 0,5.5" fill="url(#tailg)"/><circle r="7" fill="{PERS}"/><circle r="2.6" fill="{PAGE}"/></g></g>
<circle class="rg rg1" cx="815" cy="708" r="150"/><circle class="rg rg2" cx="815" cy="708" r="150"/><circle class="rg rg3" cx="815" cy="708" r="150"/>

<!-- paper fibre -->
<rect width="1440" height="900" filter="url(#fibA)" class="mul" opacity=".22"/>
<rect width="1440" height="900" filter="url(#fibB)" class="mul" opacity=".12"/>
</svg>"""

# stamp: build properly and swap in
stamp = (f'<g class="stampo"><g transform="translate(1274,70) rotate(-5)"><g filter="url(#rough)" fill="none" stroke="{INK}">'
         f'<rect x="-98" y="-32" width="196" height="64" stroke-width="3.6"/>'
         f'<rect x="-92" y="-26" width="184" height="52" stroke-width="1.3"/>'
         f'<line x1="-92" x2="92" y1="3" y2="3" stroke-width="1.3"/>'
         f'<text class="sg" x="0" y="-7" text-anchor="middle" font-size="15" textLength="170" lengthAdjust="spacingAndGlyphs" fill="{INK}" stroke="none">STANDARD PROCEDURE</text>'
         f'<text class="sg" x="0" y="22" text-anchor="middle" font-size="19" letter-spacing="3" fill="{INK}" stroke="none">REV. 3</text>'
         f'</g></g></g>')
a = svg.index('<g class="stampo"><g transform="translate(1270,72) rotate(-5)" style')
b = svg.index('<!-- footer -->')
svg = svg[:a] + stamp + "\n\n" + svg[b:]

html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><title>PEC World 07: Team Playbooks</title>
<meta name="viewport" content="width=1440">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;800&family=Barlow+Condensed:wght@700&family=Courier+Prime:wght@700&family=Special+Elite&family=Stardos+Stencil:wght@700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>
{svg}
<script>{JS}</script></body></html>"""

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "playbooks.html")
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("wrote", os.path.normpath(out), len(html))
