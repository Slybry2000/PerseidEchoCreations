# Rebuilds the left side of the Fit Check: the stock photo becomes the seven lane strips,
# and the lane the answer points to opens and plays its poster. Questions, answers and the
# email form are untouched. Run once from site/worlds:  python _src/patch_fitcheck.py
import re

p = '../fit-check/index.html'
s = open(p, encoding='utf8').read()
assert 'class="photo"' in s, 'already patched?'
home = open('../index.html', encoding='utf8').read()


def rep(a, b):
    global s
    assert s.count(a) == 1, (a[:60], s.count(a))
    s = s.replace(a, b)


# the seven strips, lifted from the front door so the emblems stay identical
SLUGS = ['cold-email', 'social', 'automation', 'customer-experience', 'design', 'video', 'playbooks']
spines = re.findall(r'<iframe src="(/worlds/[^"]+)"[^>]*></iframe></div>(<div class="spine w\d">.*?</div>)</section>', home)
assert len(spines) == 7, len(spines)
stack = ''.join(
    '<div class="ln" data-lane="%s"><div class="pst"><iframe data-src="%s" scrolling="no" title="" tabindex="-1" aria-hidden="true"></iframe></div>%s</div>'
    % (slug, src, sp) for slug, (src, sp) in zip(SLUGS, spines))

# ---- markup
a = s.index('  <aside class="photo">')
b = s.index('  </aside>') + len('  </aside>')
s = s[:a] + ('  <aside class="side">\n'
             '    <a class="brand" href="/">PERSEID ECHO CREATIONS</a>\n'
             '    <div class="stack" id="stack">' + stack + '</div>\n'
             '    <p class="cap" id="cap">You do the work. <span>I take the rest.</span></p>\n'
             '  </aside>') + s[b:]
rep('<link rel="preconnect" href="https://images.unsplash.com">\n', '')

# ---- styles
a = s.index('/* left: one real photograph.')
b = s.index('/* right: the questions */')
s = s[:a] + open('_src/fitcheck-side.css', encoding='utf8').read() + '\n' + s[b:]
rep("  .photo{position:relative;height:30vh;min-height:200px}\n  .cap{display:none}\n",
    "  .side{position:relative;height:auto;display:block}\n  .cap{display:none}\n"
    "  .stack{display:none}\n  body.done .stack{display:block}\n  body.done .ln{display:none}\n"
    "  body.done .ln.on{display:block;height:var(--ph)}\n")

# ---- script
rep("var phA=document.getElementById('ph-a'),phB=document.getElementById('ph-b');\n",
    "var stack=document.getElementById('stack'),lns=[].slice.call(stack.querySelectorAll('.ln'));\n"
    "var BR={customers:'cold-email',posting:'social',busywork:'automation',service:'customer-experience',website:'design',video:'video',team:'playbooks'};\n")
a = s.index('function setPhoto(L){')
b = s.index('function ask(q,n,pick){')
s = s[:a] + open('_src/fitcheck-side.js', encoding='utf8').read() + s[b:]
rep("step=n;count.textContent=n+' of 3';setPhoto(null);",
    "step=n;count.textContent=n+' of 3';openLane(null);hot(n>1&&ans.q1?BR[ans.q1.go]:null);")
rep("  var bk=stage.querySelector('.back');if(bk)",
    "  if(n===1)[].forEach.call(stage.querySelectorAll('.opts button'),function(b){var l=BR[q.opts[+b.getAttribute('data-i')].go];"
    "b.addEventListener('mouseenter',function(){hot(l)});b.addEventListener('focus',function(){hot(l)});b.addEventListener('mouseleave',function(){hot(null)})});\n"
    "  var bk=stage.querySelector('.back');if(bk)")
rep("count.textContent='Your answer';setPhoto(L);", "count.textContent='Your answer';hot(o.no?'-':null);openLane(o.no?null:slug);")

open(p, 'w', encoding='utf8', newline='\n').write(s)
print('fit check patched', len(s))
