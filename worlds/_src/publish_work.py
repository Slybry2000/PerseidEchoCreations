# 2026-11-19. Run from a site root:  python worlds/_src/publish_work.py
# 1. Page names the tracking collector accepts. It only keeps "home", "partners", "privacy" and
#    "local:<slug>" / "wf:<slug>"; anything else is stored with no page. So the new pages report as
#    wf:fit-check, wf:svc-<service>, wf:work-<case>.
# 2. Sitemap entries for the case studies.
import re

for slug in ['cold-email', 'social', 'automation', 'customer-experience', 'design', 'video', 'playbooks', 'fit-check']:
    p = '%s/index.html' % slug
    s = open(p, encoding='utf8').read()
    new = 'wf:fit-check' if slug == 'fit-check' else 'wf:svc-' + slug
    s2 = re.sub(r'window\.PEC_PAGE="[^"]*"', 'window.PEC_PAGE="%s"' % new, s)
    assert s2.count('window.PEC_PAGE="%s"' % new) == 1, slug
    open(p, 'w', encoding='utf8', newline='\n').write(s2)

WORK = ['', 'lost-inquiries-contact-form/', 'vendor-sign-ups-and-payments/', 'scoring-app-website/']
p = 'sitemap.xml'
s = open(p, encoding='utf8').read()
if '/work/' not in s:
    new = ''.join('  <url>\n    <loc>https://perseidechocreations.com/work/%s</loc>\n    <lastmod>2026-11-19</lastmod>\n'
                  '    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>\n' % x for x in WORK)
    a = s.index('  <url>\n    <loc>https://perseidechocreations.com/partners.html</loc>')
    open(p, 'w', encoding='utf8', newline='\n').write(s[:a] + new + s[a:])
p = 'local/_build/build.js'
s = open(p, encoding='utf8').read()
if '/work/' not in s:
    a = "    { loc: `${ORIGIN}/partners.html`,"
    assert s.count(a) == 1
    new = ''.join("    { loc: `${ORIGIN}/work/%s`, priority: '0.8', changefreq: 'monthly', lastmod: rootLastmod('work/%sindex.html') },\n" % (x, x) for x in WORK)
    open(p, 'w', encoding='utf8', newline='\n').write(s.replace(a, new + a))
print('ok')
