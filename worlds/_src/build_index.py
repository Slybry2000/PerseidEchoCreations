# Rebuilds site/worlds/index.html: head + styles + lanes + footer, keeping the script block
# from the current file. Run from site/worlds:  python _src/build_index.py
import io

js = '<script>\n' + open('_src/index.js', encoding='utf8').read() + '</script>\n'
below = open('_src/below.html', encoding='utf8').read()

css = open('_src/index.css', encoding='utf8').read() + open('_src/below.css', encoding='utf8').read()


def E(p):
    return ('<svg viewBox="0 0 30 30" aria-hidden="true" fill="none" stroke-linecap="round" '
            'stroke-linejoin="round">' + p + '</svg>')


lanes = [
    ('w1', '01', 'Cold email', 'cold-email-b-anim.html', '/cold-email/', 'Cold email done for you',
     'The list, the emails, the sending and the replies. You just take the calls.',
     E('<circle cx="15" cy="15" r="11.5" stroke="#FF6A2A" stroke-width="2"/>'
       '<circle cx="15" cy="15" r="7" stroke="#FF6A2A" stroke-width="1.2"/>'
       '<path d="M2 12q3.2-3 6.5 0t6.5 0 6.5 0 6.5 0M2 18q3.2-3 6.5 0t6.5 0 6.5 0 6.5 0" stroke="#0D1321" stroke-width="1.6"/>')),
    ('w2', '02', 'Social media', 'social.html', '/social/', 'Social media that shows up for you',
     'Posts in your voice, approved by you, out on schedule every week.',
     E('<path d="M3 4h24v16H14l-6 6v-6H3z" fill="#0D1321"/>'
       '<path d="M15 16.6c-4.6-3.2-5.2-5.3-4.3-6.9 1-1.6 3.2-1.5 4.3.3 1.1-1.8 3.3-1.9 4.3-.3.9 1.6.3 3.7-4.3 6.9z" fill="#F6F6F4"/>')),
    ('w3', '03', 'Automation', 'automation.html', '/automation/', 'Business automation that gives you your week back',
     'Your tools connected, so the busywork moves on its own.',
     E('<g stroke="#F6F6F4" stroke-width="1.6"><circle cx="15" cy="15" r="7.5"/>'
       '<path d="M15 2.5v5M15 22.5v5M2.5 15h5M22.5 15h5M6.2 6.2l3.5 3.5M20.3 20.3l3.5 3.5M6.2 23.8l3.5-3.5M20.3 9.7l3.5-3.5"/></g>'
       '<circle cx="15" cy="15" r="3" fill="#FF6A2A"/>')),
    ('w4', '04', 'Customer experience', 'customer-experience.html', '/customer-experience/', 'Customer experience by design',
     'Find where your customer&#39;s path breaks, then fix what&#39;s behind it.',
     E('<circle cx="15" cy="15" r="10.5" fill="#F6F6F4" stroke="#0D1321" stroke-width="4"/>'
       '<circle cx="15" cy="15" r="4" fill="#FF6A2A"/>')),
    ('w5', '05', 'Digital design', 'design.html', '/design/', 'Digital design that does a job',
     'Websites and pages that look sharp and move people to the next step.',
     E('<path d="M3 3h10.5v10.5H3zM16.5 16.5H27V27H16.5zM3 16.5h10.5V27H3z" fill="#0D1321"/>'
       '<path d="M16.5 3H27v10.5H16.5z" fill="#FF6A2A"/>')),
    ('w6', '06', 'Video', 'video.html', '/video/', 'Video that shows the real thing',
     'Demo films and short videos of your actual product or service.',
     E('<circle cx="15" cy="15" r="11.5" stroke="#F6F6F4" stroke-width="1.8"/>'
       '<path d="M12 9.5l9 5.5-9 5.5z" fill="#FF6A2A"/>')),
    ('w7', '07', 'Team playbooks', 'playbooks.html', '/playbooks/', 'Team playbooks your people actually use',
     'How you do things, written down once and taught properly.',
     E('<path d="M4 6h18v20H4z" stroke="#0D1321" stroke-width="2"/>'
       '<path d="M8.5 15l5 5L25.5 5.5" stroke="#FF6A2A" stroke-width="3.2"/>')),
]

h = '''</head><body>
<h1 class="vh">Perseid Echo Creations: done-for-you cold email, social media, business automation, customer experience, digital design, video and team playbooks for small businesses</h1>
<div class="door" id="door">
<header class="bar"><a class="logo" href="/">PERSEID ECHO CREATIONS</a><span class="tag">You do the work. I take the rest.</span>
<nav><a class="opt far" href="#how">How it works</a><a class="opt far" href="#proof">Proof</a><a class="opt" href="#bryan">Meet Bryan</a><a class="opt" href="/fit-check/">Fit Check</a><a class="pill" href="https://calendar.app.google/XgzHeDeyYp9DyvYJ6" target="_blank" rel="noopener">Book a call</a></nav></header>
<main class="row" id="row">
'''
for i, (c, n, name, src, href, k, d, svg) in enumerate(lanes):
    h += ('  <section class="lane%s" tabindex="0" role="link" aria-label="%s" data-href="%s" data-k="%s" data-n="%s" data-d="%s">'
          '<div class="poster"><iframe src="/worlds/%s" scrolling="no" title="%s" tabindex="-1"></iframe></div>'
          '<div class="spine %s"><i>%s</i>%s<em>%s</em><b></b></div></section>\n'
          % (' on' if i == 0 else '', k, href, name, n, d, src, name, c, n, svg, name))
h += '''</main>
<footer class="foot"><div class="now"><span class="k" id="nk">01 &middot; Cold email</span><span class="d" id="nd">The list, the emails, the sending and the replies. You just take the calls.</span><a class="go" id="go" href="/cold-email/">See how it works <svg viewBox="0 0 16 10" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M1 5h14M11 1l4 4-4 4"/></svg></a></div>
<a class="fc" href="/fit-check/"><span>Not sure which one? Three questions, about a minute.</span><b>Take the Fit Check</b></a></footer>
</div>
<noscript><style>.door{display:none}.nolist a{display:block;padding:10px 20px;color:#FF6A2A}</style><div class="nolist">''' + ''.join(
    '<a href="%s">%s</a>' % (l[4], l[5]) for l in lanes) + '''</div></noscript>
<canvas id="fly" aria-hidden="true"></canvas>
'''

head = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<link rel="canonical" href="https://perseidechocreations.com/">
<script>(function(){var m={'#fitcheck':'/fit-check/','#fc-sheet':'/fit-check/','#pricing':'/automation/','#partners':'/partners.html','#about':'#bryan'},t=m[location.hash];if(!t)return;if(t.charAt(0)==='#')location.hash=t;else location.replace(t+location.search)})();</script>
<meta property="og:type" content="website"><meta property="og:site_name" content="Perseid Echo Creations">
<meta property="og:title" content="Perseid Echo Creations: seven services, done for you">
<meta property="og:description" content="Cold email, social media, automation, customer experience, digital design, video and team playbooks, done for small businesses by one person.">
<meta property="og:url" content="https://perseidechocreations.com/">
<meta property="og:image" content="https://perseidechocreations.com/art/og-seven.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "ProfessionalService", "@id": "https://perseidechocreations.com/#business", "name": "Perseid Echo", "alternateName": "Perseid Echo Creations", "legalName": "Perseid Echo LLC", "slogan": "Customer Experience & Operations", "description": "Helps businesses improve customer journeys and internal operations through workflow diagnosis, clearer ownership, practical procedures, team guidance, and tools or automation where they fit.", "url": "https://perseidechocreations.com/", "image": "https://perseidechocreations.com/art/og-seven.jpg", "founder": {"@type": "Person", "@id": "https://perseidechocreations.com/#bryan", "name": "Bryan Piard", "url": "https://perseidechocreations.com/#bryan", "image": "https://perseidechocreations.com/art/bryan.webp", "jobTitle": "Founder", "description": "More than 21 years in customer experience and operations, improving service journeys, frontline procedures, launch readiness, and cross-functional ways of working.", "worksFor": {"@id": "https://perseidechocreations.com/#business"}, "sameAs": ["https://www.linkedin.com/in/bryan-piard-70575131/"]}, "email": "bryan@perseidechocreations.com", "telephone": "+1-425-243-3473", "priceRange": "$750 - $9,000", "address": {"@type": "PostalAddress", "addressLocality": "Renton", "addressRegion": "WA", "addressCountry": "US"}, "areaServed": [{"@type": "Country", "name": "United States"}, {"@type": "City", "name": "Renton, WA"}, {"@type": "City", "name": "Kent, WA"}, {"@type": "City", "name": "Bellevue, WA"}, {"@type": "City", "name": "Tukwila, WA"}, {"@type": "City", "name": "Auburn, WA"}, {"@type": "City", "name": "Issaquah, WA"}], "serviceType": ["Customer experience and operations review", "Business process improvement", "Workflow automation", "Business process automation", "Custom internal tools", "Systems integration"], "makesOffer": [{"@type": "Offer", "name": "Workflow Opportunity Map", "description": "One customer or operational workflow. A recommended first improvement, an implementation plan, and a way to measure progress. Credited toward a build signed within 30 days.", "price": "750", "priceCurrency": "USD"}, {"@type": "Offer", "name": "Software workflow build", "description": "Mapped, built, tested, documented, handed over with training and a post-launch bug-fix window. Most builds land between $3,500 and $9,000.", "priceCurrency": "USD", "priceSpecification": {"@type": "PriceSpecification", "minPrice": "2500", "priceCurrency": "USD"}}, {"@type": "Offer", "name": "Keys", "description": "You operate the system yourself after launch. Training included.", "price": "0", "priceCurrency": "USD"}, {"@type": "Offer", "name": "Maintain", "description": "Monitoring, fixes, and tool-change adjustments. Month to month.", "priceCurrency": "USD", "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": "750", "priceCurrency": "USD", "unitCode": "MON"}}, {"@type": "Offer", "name": "Run", "description": "Day-to-day operation and exception handling. Month to month.", "priceCurrency": "USD", "priceSpecification": {"@type": "UnitPriceSpecification", "minPrice": "2000", "priceCurrency": "USD", "unitCode": "MON"}}], "sameAs": ["https://www.linkedin.com/company/perseid-echo/", "https://www.facebook.com/profile.php?id=61590842124281"]}</script>
<script type="application/ld+json">{"@context": "https://schema.org", "@type": "WebPage", "@id": "https://perseidechocreations.com/#webpage", "url": "https://perseidechocreations.com/", "name": "Perseid Echo Creations: seven services, done for you", "inLanguage": "en-US", "datePublished": "2026-01-30", "dateModified": "2026-11-19", "author": {"@id": "https://perseidechocreations.com/#bryan"}, "publisher": {"@id": "https://perseidechocreations.com/#business"}, "about": {"@id": "https://perseidechocreations.com/#business"}}</script>
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<title>Perseid Echo Creations: seven services, done for you</title>
<meta name="description" content="Cold email, social media, automation, customer experience, digital design, video and team playbooks, done for small businesses by one person.">
<link rel="icon" href="/favicon.svg">
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;600;800&display=swap" rel="stylesheet">
<style>
'''
open('../index.html', 'w', encoding='utf8', newline='\n').write(head + css + '</style>\n' + h + js + below + '</body></html>\n')
print('ok', len(head + css + h + js + below))
