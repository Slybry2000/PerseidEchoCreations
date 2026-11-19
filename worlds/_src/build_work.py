# Case study pages. Run from site/worlds:  python _src/build_work.py   -> writes site/work/
# Published 2026-11-19 on Bryan's go.
# Every fact here is already published on the site or recorded from the real job. No measured results are claimed.
import os, html

CAL = 'https://calendar.app.google/XgzHeDeyYp9DyvYJ6'
CASES = [
 dict(slug='lost-inquiries-contact-form', service=('Digital design', '/design/'), also=('Business automation', '/automation/'),
      kick='Travel company · Website and inquiry handling',
      h1='The contact form that was losing every inquiry',
      lede='A group travel company had a "Begin a conversation" form on its site. It looked fine. It captured nothing.',
      img=('/art/work/dream-travel.jpg', 'The Dream Travel adult group travel site'),
      facts=[('Before', 'Inquiries opened the visitor\'s own mail app and were never recorded'), ('After', 'Every inquiry is saved and emailed to the team within 15 minutes'), ('Also', 'Newsletter sign-ups go straight onto the right list')],
      blocks=[
       ('The problem', ['The form on the site did not send anything. Pressing the button opened the visitor\'s email program with a blank message. Anyone on a phone without mail set up, or anyone who closed that window, was gone. Nothing was saved anywhere, so nobody knew how many people had tried.',
                        'The newsletter checkbox next to it did nothing at all.']),
       ('What I did', ['Replaced the form with one that records every inquiry the moment it is sent.',
                       'Set up a check that runs every 15 minutes and emails each new inquiry to the team. Replying to that email goes straight to the person who asked.',
                       'Connected the newsletter checkbox to the company\'s existing mailing list, kept separate from its other audiences.',
                       'Added a "Book a call" button beside the form for people who would rather talk.',
                       'Later rebuilt the front page as three panels so each kind of trip gets equal space.']),
       ('What changed', ['Inquiries now arrive in an inbox instead of disappearing, and each one can be answered by hitting reply. The owner no longer has to wonder whether the site is working.']),
       ('Work it takes off a person', ['Checking whether the form works. Copying newsletter sign-ups onto a list by hand. Chasing people who thought they had already written in.'])],
      note='Disclosure: Dream Travel is a family business. No lead counts are quoted because the old form recorded none to compare against.'),
 dict(slug='vendor-sign-ups-and-payments', service=('Business automation', '/automation/'), also=('Customer experience', '/customer-experience/'),
      kick='Trade publisher · Sign-up and payment workflow',
      h1='Vendor sign-ups and payments without the email chase',
      lede='A home care technology buyer\'s guide needed vendors to sign up, pick a listing and pay, without someone managing each one by email.',
      img=('/art/work/buyers-guide.jpg', 'The buyer\'s guide sign-up page'),
      facts=[('Scope', 'Invitation emails, sign-up tracking and payment collection'), ('Client\'s words', 'Fewer steps to send invitations'), ('Client\'s words', 'Automated payment receiving')],
      blocks=[
       ('The problem', ['Getting a vendor into the guide meant a string of manual steps: find the right contact, send an invitation, track who answered, fix bounced addresses, then arrange payment. Each vendor was a small email thread, and there were a lot of vendors.']),
       ('What I did', ['Built vendor invitation emails that go out from one place instead of one at a time.',
                       'Added sign-up tracking so it is clear who has joined, who has not, and who needs a nudge.',
                       'Set up payment collection inside the sign-up, so a vendor can join and pay in one sitting.',
                       'Kept the pages and listing categories easy to change, so the guide can grow without another build.']),
       ('What changed', ['The publisher describes it as fewer steps to send invitations, and payments that arrive on their own. Those are the client\'s own descriptions, not measured results.']),
       ('Work it takes off a person', ['Chasing updated contact emails, bouncebacks and replies by hand. Sending payment details one vendor at a time.'])],
      note='Disclosure: this is a family client, quoted with permission. Ask on the call and I will tell you what I can about the work.'),
 dict(slug='scoring-app-website', service=('Digital design', '/design/'), also=('Video', '/video/'),
      kick='My own product · Website and demo film',
      h1='A website that explains a new app in one visit',
      lede='The Green Felt Club is my own scoring app for pool players. The site had one job: let a stranger understand it and try it without a sales call.',
      img=('/art/work/green-felt-club.jpg', 'The Green Felt Club website'),
      facts=[('Built here', 'Design, writing and build'), ('Demo film', '41 seconds, made from the real product'), ('Shows', 'Joining by QR code and the venue TV screen')],
      blocks=[
       ('The problem', ['A new app has to answer three questions fast: what is it, is it for me, and what do I do next. Pool players, league organizers and venue owners each ask those differently, and none of them will read a long page to find out.']),
       ('What I did', ['Designed, wrote and built the site myself, so the words and the layout were made for each other.',
                       'Made a short demo film from the real product, showing a player joining with a QR code and the scoreboard on a venue TV.',
                       'Gave organizers and venues their own pages, so each visitor lands on the version written for them.']),
       ('What changed', ['The site does the explaining. A visitor can watch the product work before talking to anyone, which is the same job I build sites to do for clients.']),
       ('Work it takes off a person', ['Explaining the product from scratch on every call. Sending screenshots by email to show what it looks like.'])],
      note='Disclosure: this is my own product, not a client result. It is here because you can open it and judge the work yourself.',
      link=('Visit the site', 'https://www.thegreenfeltclub.com')),
]

HEAD = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s · Perseid Echo Creations</title>
<meta name="description" content="%(desc)s">
<link rel="canonical" href="https://perseidechocreations.com%(path)s">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<meta property="og:type" content="article"><meta property="og:site_name" content="Perseid Echo Creations">
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:url" content="https://perseidechocreations.com%(path)s">
<meta property="og:image" content="https://perseidechocreations.com/art/og-seven.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{"@context":"https://schema.org","@type":"Article","headline":"%(title)s","description":"%(desc)s","url":"https://perseidechocreations.com%(path)s","inLanguage":"en-US","datePublished":"2026-11-19","dateModified":"2026-11-19","author":{"@id":"https://perseidechocreations.com/#bryan"},"publisher":{"@id":"https://perseidechocreations.com/#business"}}</script>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/work/work.css">
</head><body>
<header class="bar"><a class="logo" href="/">PERSEID ECHO CREATIONS</a><nav><a href="/work/">Work</a><a href="/fit-check/">Fit Check</a><a class="pill" href="%(cal)s" target="_blank" rel="noopener">Book a call</a></nav></header>
'''
FOOT = '''<footer class="foot"><p><a href="/">Perseid Echo Creations</a> · <a href="/work/">All work</a> · <a href="/workflows/">Workflows</a> · <a href="/local/">Areas served</a> · <a href="/privacy.html">Privacy</a></p></footer>
<script id="vtag-ai-js" async src="https://r2.leadsy.ai/tag.js" data-pid="1xxvugkyQ7UIw1LFd" data-version="062024"></script>
<script>window.PEC_PAGE="%(pg)s";</script>
<script src="/local/assets/track.js" defer></script>
</body></html>
'''
e = html.escape


def page(c):
    path = '/work/%s/' % c['slug']
    h = HEAD % dict(title=e(c['h1']), desc=e(c['lede']), path=path, cal=CAL)
    h += '<main><section class="hero"><div class="in"><p class="kick">%s</p><h1>%s</h1><p class="lede">%s</p></div></section>\n' % (e(c['kick']), e(c['h1']), e(c['lede']))
    h += '<section class="facts"><div class="in">' + ''.join('<div><span>%s</span><b>%s</b></div>' % (e(a), e(b)) for a, b in c['facts']) + '</div></section>\n'
    h += '<section class="body"><div class="in"><figure><img src="%s" alt="%s" loading="lazy"></figure>\n' % (c['img'][0], e(c['img'][1]))
    for t, items in c['blocks']:
        h += '<h2>%s</h2>' % e(t)
        h += ('<ul>' + ''.join('<li>%s</li>' % e(x) for x in items) + '</ul>') if t == 'What I did' else ''.join('<p>%s</p>' % e(x) for x in items)
        h += '\n'
    if c.get('link'):
        h += '<p><a class="txt" href="%s" target="_blank" rel="noopener">%s →</a></p>' % (c['link'][1], e(c['link'][0]))
    h += '<p class="note">%s</p>' % e(c['note'])
    h += '<p class="rel">Related: <a href="%s">%s</a> · <a href="%s">%s</a></p></div></section>\n' % (c['service'][1], e(c['service'][0]), c['also'][1], e(c['also'][0]))
    h += ('<section class="ask"><div class="in"><h2>Got a version of this problem?</h2><p>Three questions, about a minute, and you will know which service fits or whether none does yet.</p>'
          '<div class="acts"><a class="btn" href="/fit-check/">Take the Fit Check</a><a class="btn line" href="%s" target="_blank" rel="noopener">Book a 20-minute call</a></div></div></section></main>\n' % CAL)
    return h + FOOT % dict(pg='wf:work-' + c['slug'])


os.makedirs('../work', exist_ok=True)
for c in CASES:
    os.makedirs('../work/' + c['slug'], exist_ok=True)
    open('../work/%s/index.html' % c['slug'], 'w', encoding='utf8', newline='\n').write(page(c))

h = HEAD % dict(title='Work: real jobs and what changed', desc='Real jobs, named for the problem they solved, with honest notes on what is and is not measured.', path='/work/', cal=CAL)
h += '<main><section class="hero"><div class="in"><p class="kick">Work</p><h1>Real jobs, named for the problem</h1><p class="lede">What was broken, what I did, and what it takes off a person. Where a number is not measured, the page says so.</p></div></section>\n<section class="body"><div class="in"><div class="cards">'
for c in CASES:
    h += '<a class="card" href="/work/%s/"><img src="%s" alt="" loading="lazy"><span>%s</span><b>%s</b><p>%s</p></a>' % (c['slug'], c['img'][0], e(c['kick']), e(c['h1']), e(c['lede']))
h += '</div></div></section></main>\n' + FOOT % dict(pg='wf:work')
open('../work/index.html', 'w', encoding='utf8', newline='\n').write(h)

open('../work/work.css', 'w', encoding='utf8', newline='\n').write('''
:root{--ink:#0D1321;--paper:#F6F6F4;--acc:#FF6A2A;--deep:#C2410C}
*{box-sizing:border-box}html,body{margin:0}
body{background:var(--paper);color:var(--ink);font-family:Archivo,Arial,sans-serif;font-size:18px;line-height:1.55}
a{color:inherit}
.in{max-width:860px;margin:0 auto;padding:0 20px}
.bar{background:var(--ink);color:var(--paper);display:flex;align-items:center;justify-content:space-between;gap:16px;padding:16px 20px;flex-wrap:wrap}
.bar a{text-decoration:none;font-weight:800;font-size:13px;letter-spacing:.12em;text-transform:uppercase}
.bar .logo{letter-spacing:.14em;font-size:14px}.bar nav{display:flex;align-items:center;gap:22px}
.pill{background:var(--acc);color:var(--ink);padding:10px 18px;border-radius:99px}
.hero{background:var(--ink);color:var(--paper);padding:clamp(40px,7vw,88px) 0 clamp(36px,6vw,72px)}
.kick{margin:0 0 16px;font-weight:800;font-size:13px;letter-spacing:.16em;text-transform:uppercase;color:var(--acc)}
h1{margin:0 0 20px;font-weight:800;font-size:clamp(34px,6vw,68px);line-height:.98;letter-spacing:-.02em;text-transform:uppercase;text-wrap:balance}
.lede{margin:0;max-width:32em;font-size:clamp(18px,2vw,22px);opacity:.88}
.facts{background:var(--ink);color:var(--paper);padding:0 0 clamp(36px,6vw,64px)}
.facts .in{display:grid;grid-template-columns:repeat(3,1fr);gap:0;max-width:860px}
.facts .in>div{border-top:3px solid var(--acc);padding:16px 20px 0 0;margin-right:20px}
.facts span{display:block;font-weight:800;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--acc);margin-bottom:6px}
.facts b{font-weight:600;font-size:17px;line-height:1.35}
.body{padding:clamp(36px,6vw,72px) 0}
figure{margin:0 0 40px}figure img{display:block;width:100%;height:auto;border:3px solid var(--ink)}
h2{margin:44px 0 12px;font-weight:800;font-size:clamp(22px,3vw,30px);line-height:1.05;text-transform:uppercase;letter-spacing:-.005em}
.body p{margin:0 0 16px;max-width:36em}
.body ul{margin:0 0 16px;padding:0;list-style:none;max-width:38em;border-top:3px solid var(--ink)}
.body li{padding:13px 0;border-bottom:1px solid rgba(13,19,33,.2)}
.txt{font-weight:800;color:var(--deep);text-transform:uppercase;font-size:14px;letter-spacing:.1em}
.note{margin-top:40px!important;padding:16px 18px;border-left:4px solid var(--acc);background:#fff;font-size:15px}
.rel{font-size:15px;opacity:.8}
.ask{background:var(--acc);padding:clamp(40px,6vw,72px) 0}
.ask h2{margin:0 0 10px;font-size:clamp(28px,4.4vw,48px)}.ask p{margin:0;max-width:30em}
.acts{display:flex;flex-wrap:wrap;gap:14px;margin-top:28px}
.btn{display:inline-block;background:var(--ink);color:var(--paper);font-weight:800;font-size:14px;letter-spacing:.1em;text-transform:uppercase;text-decoration:none;padding:15px 24px;border-radius:99px;border:2px solid var(--ink)}
.btn.line{background:none;color:var(--ink)}
.cards{display:grid;grid-template-columns:repeat(3,1fr);gap:28px}
.card{text-decoration:none;display:block}.card img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;border:3px solid var(--ink)}
.card span{display:block;margin:14px 0 6px;font-weight:800;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--deep)}
.card b{display:block;font-weight:800;font-size:22px;line-height:1.08;text-transform:uppercase}.card p{margin:8px 0 0;font-size:15px;opacity:.8}
.card:hover b{color:var(--deep)}
.body .in:has(.cards){max-width:1180px}
.foot{background:var(--ink);color:var(--paper);padding:28px 20px;font-size:14px;text-align:center}.foot p{margin:0;opacity:.8}
@media (max-width:760px){.facts .in,.cards{grid-template-columns:1fr}.facts .in>div{margin:0 0 18px}.bar nav{gap:14px}}
''')
print('built', len(CASES), 'case studies')
