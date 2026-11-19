# Go-live prep, 2026-11-19. Run once from site/worlds:  python _src/golive.py <path-to-live-clone>
# Carries the live site's search and tracking setup onto the new pages:
#   front door: indexable, share tags, business schema, visitor pixel, old-anchor redirects
#   service pages: funnel tracking + share tags;  Fit Check: share tags
import re, json, sys

live = open(sys.argv[1] + '/index.html', encoding='utf8').read()
blocks = [json.loads(b) for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', live, re.S)]
biz, page = blocks[0], blocks[1]          # the FAQ block is dropped: those questions are not on the new page
assert biz['@type'] == 'ProfessionalService' and page['@type'] == 'WebPage'
biz['founder']['url'] = 'https://perseidechocreations.com/#bryan'
TITLE = 'Perseid Echo Creations: seven services, done for you'
DESC = 'Cold email, social media, automation, customer experience, digital design, video and team playbooks, done for small businesses by one person.'
page['name'] = TITLE
page['dateModified'] = '2026-11-19'
LD = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(b, ensure_ascii=False) for b in (biz, page))
LEADSY = '<script id="vtag-ai-js" async src="https://r2.leadsy.ai/tag.js" data-pid="1xxvugkyQ7UIw1LFd" data-version="062024"></script>'


def og(title, desc, url):
    return ('<meta property="og:type" content="website"><meta property="og:site_name" content="Perseid Echo Creations">\n'
            '<meta property="og:title" content="%s">\n<meta property="og:description" content="%s">\n'
            '<meta property="og:url" content="%s">\n'
            '<meta property="og:image" content="https://perseidechocreations.com/art/og-seven.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">\n'
            '<meta name="twitter:card" content="summary_large_image">\n' % (title, desc, url))


# old links people still have (emails, referral page, Google profile) keep working
REDIR = ("<script>(function(){var m={'#fitcheck':'/fit-check/','#fc-sheet':'/fit-check/','#pricing':'/automation/','#partners':'/partners.html','#about':'#bryan'},"
         "t=m[location.hash];if(!t)return;if(t.charAt(0)==='#')location.hash=t;else location.replace(t+location.search)})();</script>\n")

# ---- front door generator
p = '_src/build_index.py'
s = open(p, encoding='utf8').read()
assert '<meta name="robots" content="noindex">' in s, 'already live-prepped?'
s = s.replace('<meta name="robots" content="noindex">', '')
a = '<link rel="canonical" href="https://perseidechocreations.com/">\n'
assert s.count(a) == 1
s = s.replace(a, a + REDIR + og(TITLE, DESC, 'https://perseidechocreations.com/') + LD + '<link rel="apple-touch-icon" href="/apple-touch-icon.png">\n')
open(p, 'w', encoding='utf8', newline='\n').write(s)

p = '_src/below.html'
s = open(p, encoding='utf8').read()
a = '<script>window.PEC_PAGE="home";</script>'
assert s.count(a) == 1 and 'leadsy' not in s
s = s.replace(a, LEADSY + '\n' + a)
open(p, 'w', encoding='utf8', newline='\n').write(s)

# ---- service pages and Fit Check
for slug in ['cold-email', 'social', 'automation', 'customer-experience', 'design', 'video', 'playbooks', 'fit-check']:
    p = '../%s/index.html' % slug
    s = open(p, encoding='utf8').read()
    assert 'og:title' not in s, slug
    t = re.search(r'<title>(.*?)</title>', s).group(1)
    d = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
    c = re.search(r'<link rel="canonical" href="(.*?)">\n', s)
    s = s[:c.end()] + og(t, d, c.group(1)) + s[c.end():]
    if 'track.js' not in s:
        assert s.count(LEADSY) == 1, slug
        s = s.replace(LEADSY, LEADSY + '\n<script>window.PEC_PAGE="%s";</script>\n<script src="/local/assets/track.js" defer></script>' % slug)
    open(p, 'w', encoding='utf8', newline='\n').write(s)
    print('ok', slug)
