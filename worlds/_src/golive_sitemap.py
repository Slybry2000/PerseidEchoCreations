# Adds the Fit Check and the seven service pages to the sitemap and to the sitemap generator.
# Run once from site/worlds:  python _src/golive_sitemap.py
SLUGS = ['fit-check', 'cold-email', 'social', 'automation', 'customer-experience', 'design', 'video', 'playbooks']

p = '../sitemap.xml'
s = open(p, encoding='utf8').read()
assert '/fit-check/' not in s
home = '    <loc>https://perseidechocreations.com/</loc>\n    <lastmod>2026-10-15</lastmod>'
assert s.count(home) == 1
s = s.replace(home, home.replace('2026-10-15', '2026-11-19'))
new = ''.join('  <url>\n    <loc>https://perseidechocreations.com/%s/</loc>\n    <lastmod>2026-11-19</lastmod>\n'
              '    <changefreq>monthly</changefreq>\n    <priority>0.9</priority>\n  </url>\n' % x for x in SLUGS)
a = s.index('  <url>\n    <loc>https://perseidechocreations.com/partners.html</loc>')
s = s[:a] + new + s[a:]
open(p, 'w', encoding='utf8', newline='\n').write(s)

p = '../local/_build/build.js'
s = open(p, encoding='utf8').read()
a = "    { loc: `${ORIGIN}/partners.html`,"
assert s.count(a) == 1
new = ''.join("    { loc: `${ORIGIN}/%s/`, priority: '0.9', changefreq: 'monthly', lastmod: rootLastmod('%s/index.html') },\n" % (x, x) for x in SLUGS)
s = s.replace(a, new + a)
open(p, 'w', encoding='utf8', newline='\n').write(s)
print('sitemap ok', s.count('rootLastmod('))
