# Puts each service page's own poster in its hero (in place of the stock photo). Safe to re-run.
# Run from site/worlds:  python _src/patch_lanes.py
import re

PAGES = {
    'cold-email': ('cold-email-b-anim.html', 'Cold email poster'),
    'social': ('social.html', 'Social media poster'),
    'automation': ('automation.html', 'Automation poster'),
    'customer-experience': ('customer-experience.html', 'Customer experience poster'),
    'design': ('design.html', 'Digital design poster'),
    'video': ('video.html', 'Video poster'),
    'playbooks': ('playbooks.html', 'Team playbooks poster'),
}
SCRIPT = ('<script>(function(){var a=document.querySelector(".poster-art"),f=a&&a.querySelector("iframe");if(!f)return;'
          'function fit(){f.style.transform="scale("+a.clientWidth/1440+")"}'
          'fit();addEventListener("resize",fit);try{new ResizeObserver(fit).observe(a)}catch(e){}'
          'a.addEventListener("click",function(){try{f.contentWindow.play()}catch(e){}})})();</script>')
CSS = '''
/* poster hero: the service's own animated poster instead of a photo */
.hero.has-poster{grid-template-columns:.82fr 1.18fr;max-width:1360px}
.hero-art.poster-art{aspect-ratio:1440/900;max-height:none;position:relative;cursor:pointer;background:#0D1321}
.hero-art.poster-art iframe{position:absolute;left:0;top:0;width:1440px;height:900px;border:0;transform-origin:0 0;pointer-events:none}
@media(max-width:860px){.hero.has-poster{grid-template-columns:1fr}.hero-art.poster-art{aspect-ratio:1440/900}}
'''

for slug, (src, title) in PAGES.items():
    p = '../%s/index.html' % slug
    s = open(p, encoding='utf8').read()
    if 'poster-art' in s:
        print(slug, 'already done')
        continue
    s, n = re.subn(r'<div class="hero-art"><img[^>]*></div>',
                   '<div class="hero-art poster-art" title="Click to replay"><iframe src="/worlds/%s" scrolling="no" title="%s" tabindex="-1"></iframe></div>' % (src, title),
                   s, count=1)
    assert n == 1, slug
    s = s.replace('<section class="hero">', '<section class="hero has-poster">', 1)
    s = s.replace('</main>', '</main>\n' + SCRIPT, 1)
    s = s.replace('/lanes/lane.css?v=4', '/lanes/lane.css?v=5')
    open(p, 'w', encoding='utf8', newline='\n').write(s)
    print(slug, 'ok')

c = open('../lanes/lane.css', encoding='utf8').read()
if 'poster-art' not in c:
    open('../lanes/lane.css', 'w', encoding='utf8', newline='\n').write(c + CSS)
    print('css ok')
