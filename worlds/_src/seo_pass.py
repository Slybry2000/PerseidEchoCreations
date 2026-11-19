# Search pass, 2026-11-19. Run from a site root:  python worlds/_src/seo_pass.py
#   service pages: Service schema tied to the one business node, footer links to the search pages
#   automation page: an FAQ entry linking the five workflow pages and the Map page
#   front door: a title that says what a stranger would type
import re, json

NAMES = {'cold-email': 'Done-for-you cold email', 'social': 'Done-for-you social media', 'automation': 'Business automation',
         'customer-experience': 'Customer experience design', 'design': 'Digital design', 'video': 'Video and demo films',
         'playbooks': 'Team playbooks and training'}
FOOT = '<a href="/privacy.html">Privacy</a>'
LINKS = FOOT + ' · <a href="/workflows/">Workflows</a> · <a href="/local/">Areas served</a> · <a href="/partners.html">Partners</a>'
FAQ = ('<details><summary>What kinds of jobs do you automate?</summary><p>The ones that repeat every week. Common starting points: '
       '<a href="/workflows/quote-follow-up/">quote follow-up</a>, '
       '<a href="/workflows/field-paperwork-to-invoice/">field paperwork to invoice</a>, '
       '<a href="/workflows/order-intake-from-email/">order intake from email</a>, '
       '<a href="/workflows/appointment-reminders/">appointment reminders</a> and '
       '<a href="/workflows/client-intake-and-documents/">client intake and documents</a>. '
       'Each page gives an honest read on when to buy a tool and when to build. The first paid step is the '
       '<a href="/workflow-opportunity-map/">Workflow Opportunity Map</a>.</p></details>')

for slug, name in NAMES.items():
    p = '%s/index.html' % slug
    s = open(p, encoding='utf8').read()
    if 'ld+json' in s:
        print('skip', slug); continue
    d = re.search(r'<meta name="description" content="(.*?)">', s).group(1)
    url = 'https://perseidechocreations.com/%s/' % slug
    ld = {"@context": "https://schema.org", "@type": "Service", "@id": url + "#service", "name": name, "serviceType": name,
          "description": d.replace('&amp;', '&'), "url": url,
          "provider": {"@id": "https://perseidechocreations.com/#business"},
          "areaServed": {"@type": "Country", "name": "United States"}}
    page = {"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage", "url": url,
            "name": re.search(r'<title>(.*?)</title>', s).group(1).replace('&amp;', '&'), "inLanguage": "en-US",
            "datePublished": "2026-11-19", "dateModified": "2026-11-19",
            "author": {"@id": "https://perseidechocreations.com/#bryan"},
            "publisher": {"@id": "https://perseidechocreations.com/#business"}, "about": {"@id": url + "#service"}}
    tag = ''.join('<script type="application/ld+json">%s</script>\n' % json.dumps(x, ensure_ascii=False) for x in (ld, page))
    assert s.count('</head>') == 1 and s.count(FOOT) == 1, slug
    s = s.replace('</head>', tag + '</head>').replace(FOOT, LINKS)
    if slug == 'automation':
        a = '<section class="faq"><h2>Questions owners ask</h2>'
        assert s.count(a) == 1
        s = s.replace(a, a + FAQ)
    open(p, 'w', encoding='utf8', newline='\n').write(s)
    print('ok', slug)

OLD = 'Perseid Echo Creations: seven services, done for you'
NEW = 'Cold email, social media and automation, done for you · Perseid Echo Creations'
for p in ['worlds/_src/build_index.py', 'worlds/_src/golive.py']:
    s = open(p, encoding='utf8').read()
    if OLD in s:
        open(p, 'w', encoding='utf8', newline='\n').write(s.replace(OLD, NEW))
