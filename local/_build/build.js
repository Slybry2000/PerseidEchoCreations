#!/usr/bin/env node
/* ===========================================================
   Local service page generator
   -----------------------------------------------------------
   Reads cities.json, writes:
     local/<slug>/index.html    one page per city
     local/index.html           the hub that links them
     sitemap.xml                regenerated, root pages preserved

   Run from the repo root:  node local/_build/build.js

   Why a generator and not six hand-written files: the shared
   trunk (staircase, pricing language, proof, footer) has to say
   exactly the same thing everywhere, and the site's positioning
   rules live in PECWEB/v3/README.md. One template means one
   place to change when the pricing or the staircase moves.
   =========================================================== */

'use strict';

const fs   = require('fs');
const path = require('path');

const ROOT  = path.resolve(__dirname, '..', '..');
const LOCAL = path.join(ROOT, 'local');
const ORIGIN = 'https://perseidechocreations.com';
const TODAY  = process.env.PEC_BUILD_DATE || new Date().toISOString().slice(0, 10);

const data   = JSON.parse(fs.readFileSync(path.join(__dirname, 'cities.json'), 'utf8'));
const cities = data.cities;

const WORKDIR   = path.join(ROOT, 'workflows');
const wfData    = JSON.parse(fs.readFileSync(path.join(__dirname, 'workflows.json'), 'utf8'));
const workflows = wfData.workflows;

/* Each workflow names the cities it is most relevant to. Invert that once so
   a city page can link back to its workflows without repeating the mapping. */
const workflowsByCity = {};
for (const w of workflows) {
  for (const c of w.cities || []) {
    (workflowsByCity[c] = workflowsByCity[c] || []).push(w);
  }
}

const CAL   = 'https://calendar.app.google/XgzHeDeyYp9DyvYJ6';
const EMAIL = 'bryan@perseidechocreations.com';

/* ---------- helpers ---------- */
const esc = s => String(s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;');

/* Strip the <em> the H1 carries so the same string is safe in <title>,
   meta tags and JSON-LD. */
const plain = s => String(s).replace(/<\/?em>/g, '');

const mail = svg => `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h16v16H4z"></path><polyline points="4 7 12 13 20 7"></polyline></svg>`;

/* ---------- the shared trunk ----------
   Wording here is load-bearing and mirrors the homepage. See
   v3/README.md "Rules that are load-bearing" before editing:
   range language only, "Workflow Opportunity Map" by name,
   no absolute data-safety promise, no payment-plan invitation. */

function staircase (city) {
  return `
<section class="sec sec--band" aria-labelledby="path-${'h'}">
  <div class="wrap narrow rise">
    <p class="tag">How it goes</p>
    <h2 class="h-lg" id="path-h" style="margin-block:14px 16px;">Four steps, and you can stop after any of them.</h2>
    <p class="lede">Nobody in ${esc(city)} needs to commit to a build to find out whether one is worth doing. The first two steps are free and the third is bounded.</p>
    <div class="steps">
      <div class="step">
        <span class="step__n">Step one</span>
        <span class="step__p">Free · 60 seconds</span>
        <h3 class="h-sm">The Workflow Fit Check</h3>
        <p>Five questions on your own screen. You read the answer before I ask you for anything, and one of the possible answers is that you should not automate this yet.</p>
      </div>
      <div class="step">
        <span class="step__n">Step two</span>
        <span class="step__p">Free · 20 minutes</span>
        <h3 class="h-sm">A fit call</h3>
        <p>A conversation about whether this is a fit, not a free solution design. If it is not, you will hear that on the call.</p>
      </div>
      <div class="step">
        <span class="step__n">Step three</span>
        <span class="step__p">$750</span>
        <h3 class="h-sm">The Workflow Opportunity Map</h3>
        <p>One workflow, taken apart properly: what it costs you now, what should stay human, and what a build would actually involve. Credited toward a build signed within 30 days.</p>
      </div>
      <div class="step">
        <span class="step__n">Step four</span>
        <span class="step__p">From $2,500</span>
        <h3 class="h-sm">The build</h3>
        <p>Most land between $3,500 and $9,000 depending on how many systems have to agree. Then I hand you the keys, maintain it, or run it — your call.</p>
      </div>
    </div>
    <p class="hero__note" style="margin-top:24px;">
      ${mail()}
      I will not quote a build price off a web form. Ranges point at the Map, and the Map is where a real number comes from.
    </p>
  </div>
</section>`;
}

function control () {
  return `
<section class="sec" aria-labelledby="ctrl-h">
  <div class="wrap narrow rise">
    <p class="tag">The part most people worry about</p>
    <h2 class="h-lg" id="ctrl-h" style="margin-block:14px 16px;">Nothing gets authority by accident.</h2>
    <p class="lede">Every workflow I build has a setting for how much it is allowed to do on its own, and you pick it per workflow rather than once for the whole business.</p>
    <div class="cards">
      <article class="card">
        <span class="card__n">Setting one</span>
        <h3 class="h-sm">It drafts, you send</h3>
        <p>The system does the assembling and the remembering. A person reads it and presses the button. Where most work should start, and where a lot of it should stay.</p>
      </article>
      <article class="card">
        <span class="card__n">Setting two</span>
        <h3 class="h-sm">It runs, you get told</h3>
        <p>It acts on the rules you agreed and reports what it did. Suitable once a workflow has proven itself and the cost of a wrong move is small.</p>
      </article>
      <article class="card">
        <span class="card__n">Setting three</span>
        <h3 class="h-sm">It runs, you can stop it</h3>
        <p>Fully hands-off with a switch you own and a record of every action. Appropriate for high-volume, low-judgement work, and not much else.</p>
      </article>
    </div>
  </div>
</section>`;
}

function proof (city) {
  return `
<section class="sec sec--band" aria-labelledby="proof-h">
  <div class="wrap narrow rise">
    <p class="tag">Whether I can actually build</p>
    <h2 class="h-lg" id="proof-h" style="margin-block:14px 16px;">The systems I point at are ones I own and run.</h2>
    <p class="lede">
      I am one operator, not an agency with a case-study deck. So rather than show you somebody else's results, I will show you the machinery I built for my own business and still run daily &mdash; content production, outreach, lead handling, approvals, monitoring.
      It is the same kind of work I would build for you, and it is the honest version of proof: you can ask me how any part of it works and I will know, because I am the one who fixes it when it breaks.
    </p>
    <p class="lede" style="margin-top:14px;">
      What I will not do is show you a number from a business in ${esc(city)} that I have not worked with. If I have not done it, it does not go on the page.
    </p>
    <div class="close__acts">
      <a class="btn btn--line" href="${ORIGIN}/#proof">See what I currently operate</a>
    </div>
  </div>
</section>`;
}

function faqBlock (city, own) {
  return `
<section class="sec" aria-labelledby="faq-h">
  <div class="wrap narrow rise">
    <p class="tag">Straight answers</p>
    <h2 class="h-lg" id="faq-h" style="margin-block:14px 8px;">Questions ${esc(city)} owners actually ask</h2>
    <div class="faq">
      <details>
        <summary>${esc(own.q)}</summary>
        <div class="faq__a"><p>${own.a}</p></div>
      </details>
      <details>
        <summary>What if the answer is that we should not automate this?</summary>
        <div class="faq__a">
          <p>Then that is the answer, and you get it for free in about a minute. The Fit Check genuinely returns &ldquo;do not automate this yet&rdquo; when the work is infrequent or a miss costs nothing, and I have not tuned that away to win more business. A build on the wrong workflow is worse than no build: you pay for it, then you maintain it, then you work around it.</p>
        </div>
      </details>
      <details>
        <summary>Are you going to replace someone's job?</summary>
        <div class="faq__a">
          <p>That is not what this work is for and it is not usually where the money is. The jobs worth building are the ones nobody's title covers &mdash; the retyping, the chasing, the reconciling that gets done at seven in the evening by whoever is still there. Taking that off a person's plate is the point.</p>
        </div>
      </details>
      <details>
        <summary>How long before something is actually working?</summary>
        <div class="faq__a">
          <p>A Map takes about a week from the call. A first build is usually two to four weeks after that, depending on how many systems have to agree and how quickly I can get access to them. I would rather ship one workflow that works than four that half-work.</p>
        </div>
      </details>
    </div>
  </div>
</section>`;
}

function nearby (current) {
  const others = cities.filter(c => c.slug !== current.slug);
  if (!others.length) return '';
  return `
<section class="sec" style="padding-block:clamp(34px,4.4vw,54px);" aria-labelledby="near-h">
  <div class="wrap narrow rise">
    <p class="tag">Nearby</p>
    <h2 class="h-md" id="near-h" style="margin-block:11px 6px;">I work across south and east King County</h2>
    <p style="color:var(--steel); font-size:16px;">Same work, different local shape. Every one of these is close enough that a first meeting can happen in person.</p>
    <div class="near">
      ${others.map(o => `<a href="/local/${o.slug}/">${esc(o.city)}, ${esc(o.region)}</a>`).join('\n      ')}
      <a href="/local/">All areas</a>
    </div>
  </div>
</section>`;
}

/* Cross-link from a city page into the workflow pages most relevant to that
   city's economy. Both directions matter: the city page is the local-intent
   entry, the workflow page is the problem-intent entry, and a visitor can
   arrive at either one first. */
function cityWorkflows (city) {
  const list = workflowsByCity[city] || [];
  if (!list.length) return '';
  return `
<section class="sec sec--paper" style="padding-block:clamp(40px,5vw,68px);" aria-labelledby="cw-h">
  <div class="wrap narrow rise">
    <p class="tag tag--ink">Before you hire anyone</p>
    <h2 class="h-md" id="cw-h" style="margin-block:11px 8px;">Should you buy a tool instead?</h2>
    <p class="lede lede--ink" style="font-size:17px;">
      For the workflows that come up most in ${esc(city)}, I have written out the honest version of that decision &mdash; including when the right answer is an off-the-shelf product and you should keep your money.
    </p>
    <div class="near" style="margin-top:20px;">
      ${list.map(w => `<a class="near--ink" href="/workflows/${w.slug}/">${esc(w.short)}</a>`).join('\n      ')}
      <a class="near--ink" href="/workflows/">All workflows</a>
    </div>
  </div>
</section>`;
}

function closeBlock (city) {
  return `
<section class="sec sec--band" aria-labelledby="close-h">
  <div class="wrap narrow close rise">
    <p class="tag">Start at the bottom of the staircase</p>
    <h2 class="h-lg" id="close-h" style="margin-block:14px 16px;">Sixty seconds, and you will know whether this is worth another minute.</h2>
    <p class="lede">
      No account, no calendar, no waiting for a reply. Run the Fit Check and you get the read on your own screen.
      If it says the work is worth mapping, the next step is a free 20-minute call. If it says leave it alone, you have lost a minute and I have lost a customer I should not have had.
    </p>
    <div class="close__acts">
      <a class="btn btn--go" href="${ORIGIN}/#fitcheck">Run the 60-second Fit Check</a>
      <a class="btn btn--line" href="${CAL}" rel="noopener">Skip it, book the 20-minute call</a>
    </div>
    <p class="hero__note" style="margin-top:22px;">
      ${mail()}
      Or just write to me: <a href="mailto:${EMAIL}" style="color:var(--lamp);">${EMAIL}</a>
    </p>
  </div>
</section>`;
}

function footer (city) {
  return `
<footer class="foot">
  <div class="wrap">
    <div class="foot__in">
      <span class="foot__b">Perseid Echo Creations</span>
      <nav class="foot__nav" aria-label="Footer">
        <a href="${ORIGIN}/#fitcheck">Fit Check</a>
        <a href="${ORIGIN}/#cost">Pricing</a>
        <a href="/workflows/">Workflows</a>
        <a href="/local/">Areas served</a>
        <a href="${ORIGIN}/partners.html">Partners</a>
        <a href="${ORIGIN}/privacy.html">Privacy</a>
        <a href="mailto:${EMAIL}">Email</a>
      </nav>
    </div>
    <p class="foot__fine">
      Based in Renton, Washington. Built and operated by Bryan Piard.${city ? ` Serving ${esc(city)} and the surrounding King County area.` : ''}
      Any figures shown in the work I point at come from systems I own and run; they are not client results and are not a forecast of yours.
    </p>
  </div>
</footer>`;
}

function topbar (city) {
  return `
<div class="topbar">
  <div class="wrap topbar__in">
    <a class="topbar__b" href="${ORIGIN}/">Perseid Echo Creations</a>
    <nav class="topbar__in" style="gap:10px 22px;" aria-label="Primary">
      <a href="/workflows/">Workflows</a>
      <a href="/local/">Areas served</a>
      <a href="${ORIGIN}/#cost">Pricing</a>
      <a href="${ORIGIN}/#fitcheck">Run the Fit Check</a>
    </nav>
  </div>
</div>`;
}

/* ---------- structured data ----------
   ProfessionalService rather than LocalBusiness: there is no
   storefront and no published street address, so the entity is
   an area-served practice. Deliberately no "address" beyond
   city and region, and deliberately no aggregateRating or
   review markup — there is nothing real to put in them yet. */
function jsonLd (c) {
  const url = `${ORIGIN}/local/${c.slug}/`;
  const service = {
    '@context': 'https://schema.org',
    '@type': 'ProfessionalService',
    '@id': `${url}#business`,
    name: 'Perseid Echo Creations',
    description: plain(c.metaDesc),
    url,
    founder: { '@type': 'Person', name: 'Bryan Piard' },
    email: EMAIL,
    image: `${ORIGIN}/art/ind-street.webp`,
    priceRange: '$750 - $9,000',
    address: {
      '@type': 'PostalAddress',
      addressLocality: 'Renton',
      addressRegion: 'WA',
      addressCountry: 'US'
    },
    areaServed: cities.map(x => ({
      '@type': 'City',
      name: `${x.city}, ${x.region}`
    })),
    serviceType: [
      'Workflow automation',
      'Business process automation',
      'Custom internal tools',
      'Systems integration'
    ],
    knowsAbout: c.first.map(f => f.n),
    makesOffer: [
      {
        '@type': 'Offer',
        name: 'Workflow Opportunity Map',
        description: 'One workflow assessed end to end: current cost, what should stay human, and what a build would involve.',
        price: '750',
        priceCurrency: 'USD'
      },
      {
        '@type': 'Offer',
        name: 'Workflow build',
        description: 'Design, build and handover of one controlled workflow system.',
        priceSpecification: {
          '@type': 'PriceSpecification',
          minPrice: '2500',
          priceCurrency: 'USD'
        }
      }
    ]
  };

  const crumbs = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home', item: `${ORIGIN}/` },
      { '@type': 'ListItem', position: 2, name: 'Areas served', item: `${ORIGIN}/local/` },
      { '@type': 'ListItem', position: 3, name: `${c.city}, ${c.region}`, item: url }
    ]
  };

  const faq = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: c.faq.q,
        acceptedAnswer: { '@type': 'Answer', text: c.faq.a.replace(/<[^>]+>/g, '') }
      },
      {
        '@type': 'Question',
        name: 'What if the answer is that we should not automate this?',
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Then that is the answer, and you get it for free in about a minute. The Fit Check returns "do not automate this yet" when the work is infrequent or a miss costs nothing.'
        }
      }
    ]
  };

  return [service, crumbs, faq]
    .map(o => `<script type="application/ld+json">\n${JSON.stringify(o, null, 2)}\n</script>`)
    .join('\n');
}

/* ---------- the page ---------- */
function page (c) {
  const url = `${ORIGIN}/local/${c.slug}/`;
  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(c.title)}</title>
<meta name="description" content="${esc(c.metaDesc)}">
<meta name="theme-color" content="#0B1018">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="geo.region" content="US-WA">
<meta name="geo.placename" content="${esc(c.city)}, ${esc(c.regionLong)}">

<meta property="og:type" content="website">
<meta property="og:title" content="${esc(plain(c.h1))}">
<meta property="og:description" content="${esc(c.metaDesc)}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${ORIGIN}/art/ind-street.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="${url}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Spline+Sans+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/local/assets/local.css">

${jsonLd(c)}
</head>
<body>
${topbar(c.city)}

<main>

<!-- ======================= HERO ======================= -->
<header class="hero">
  <div class="hero__art" role="presentation"></div>
  <div class="hero__scrim" role="presentation"></div>
  <div class="wrap hero__inner">
    <nav class="crumb" aria-label="Breadcrumb">
      <ol>
        <li><a href="${ORIGIN}/">Home</a></li>
        <li><a href="/local/">Areas served</a></li>
        <li aria-current="page">${esc(c.city)}, ${esc(c.region)}</li>
      </ol>
    </nav>
    <p class="tag">${esc(c.city)}, ${esc(c.regionLong)}</p>
    <h1 class="h-xl hero__head">${c.h1}</h1>
    <p class="hero__sub">${esc(c.sub)}</p>
    <div class="hero__acts">
      <a class="btn btn--go" href="${ORIGIN}/#fitcheck">Run the 60-second Fit Check</a>
      <a class="btn btn--line" href="${ORIGIN}/#cost">See what it costs</a>
    </div>
    <p class="hero__note">
      ${mail()}
      Free, no account, and it will tell you to leave the work alone if that is the right answer.
    </p>
  </div>
</header>

<!-- ======================= THE LOCAL READ ======================= -->
<section class="sec" aria-labelledby="here-h">
  <div class="wrap narrow rise">
    <p class="tag">What the work looks like here</p>
    <h2 class="h-lg" id="here-h" style="margin-block:14px 16px;">${esc(c.city)} is not a generic market, and this is not a generic page.</h2>
    ${c.here.map(p => `<p class="lede" style="margin-bottom:14px;">${p}</p>`).join('\n    ')}
  </div>
</section>

<!-- ======================= FIRST CANDIDATES ======================= -->
<section class="sec sec--paper" aria-labelledby="first-h">
  <div class="wrap narrow rise">
    <p class="tag tag--ink">Where I would look first</p>
    <h2 class="h-lg" id="first-h" style="margin-block:14px 16px;">Three jobs worth checking in a ${esc(c.city)} business</h2>
    <p class="lede lede--ink">These are the patterns I see most often in this part of the county. Not a promise that yours is one of them &mdash; that is what the Fit Check and the Map are for.</p>
    <div class="cards">
      ${c.first.map((f, i) => `<article class="card">
        <span class="card__n">Candidate ${i + 1}</span>
        <h3 class="h-sm">${esc(f.n)}</h3>
        <p>${esc(f.p)}</p>
      </article>`).join('\n      ')}
    </div>
  </div>
</section>

${staircase(c.city)}
${cityWorkflows(c.city)}
${control()}
${proof(c.city)}
${faqBlock(c.city, c.faq)}
${nearby(c)}
${closeBlock(c.city)}

</main>
${footer(c.city)}

<script>window.PEC_PAGE = ${JSON.stringify('local:' + c.slug)};</script>
<script src="/local/assets/track.js" defer></script>
</body>
</html>
`;
}

/* ---------- the hub ---------- */
function hub () {
  const url = `${ORIGIN}/local/`;
  const ld = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'Areas served · Perseid Echo Creations',
    url,
    about: { '@type': 'ProfessionalService', name: 'Perseid Echo Creations' },
    hasPart: cities.map(c => ({
      '@type': 'WebPage',
      name: `Workflow automation in ${c.city}, ${c.region}`,
      url: `${ORIGIN}/local/${c.slug}/`
    }))
  };

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Areas served · Workflow automation in King County, WA</title>
<meta name="description" content="I am based in Renton and build workflow systems for owner-led businesses across King County. Renton, Kent, Bellevue, Tukwila, Auburn and Issaquah.">
<meta name="theme-color" content="#0B1018">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<meta property="og:type" content="website">
<meta property="og:title" content="Workflow automation across south and east King County">
<meta property="og:description" content="Based in Renton. Six areas, each with its own read on what the repetitive work actually looks like there.">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${ORIGIN}/art/ind-street.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="${url}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Spline+Sans+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/local/assets/local.css">

<script type="application/ld+json">
${JSON.stringify(ld, null, 2)}
</script>
</head>
<body>
${topbar('')}

<main>
<header class="hero">
  <div class="hero__art" role="presentation"></div>
  <div class="hero__scrim" role="presentation"></div>
  <div class="wrap hero__inner">
    <nav class="crumb" aria-label="Breadcrumb">
      <ol>
        <li><a href="${ORIGIN}/">Home</a></li>
        <li aria-current="page">Areas served</li>
      </ol>
    </nav>
    <p class="tag">King County, Washington</p>
    <h1 class="h-xl hero__head">Where I <em>work</em></h1>
    <p class="hero__sub">I am one operator based in Renton, so the list is short on purpose. These are the places I can get to, and each page says something specific about the businesses there rather than swapping a city name into the same paragraph.</p>
    <div class="hero__acts">
      <a class="btn btn--go" href="${ORIGIN}/#fitcheck">Run the 60-second Fit Check</a>
      <a class="btn btn--line" href="${ORIGIN}/#cost">See what it costs</a>
    </div>
  </div>
</header>

<section class="sec" aria-labelledby="areas-h">
  <div class="wrap rise">
    <p class="tag">Six areas</p>
    <h2 class="h-lg" id="areas-h" style="margin-block:14px 16px;">Pick the one you are in</h2>
    <p class="lede">If you are just outside these, write to me anyway &mdash; the boundary is drive time, not a rule.</p>
    <div class="hub">
      ${cities.map(c => `<a class="hub__a" href="/local/${c.slug}/">
        <h3 class="h-md">${esc(c.city)}${c.home ? ', WA &mdash; home' : ', WA'}</h3>
        <p>${esc(c.first[0].n)} is usually the first thing I look at here.</p>
        <span class="go">Read the ${esc(c.city)} page &rarr;</span>
      </a>`).join('\n      ')}
    </div>
  </div>
</section>

${staircase('King County')}
${closeBlock('King County')}

</main>
${footer('')}

<script>window.PEC_PAGE = "local:hub";</script>
<script src="/local/assets/track.js" defer></script>
</body>
</html>
`;
}

/* ---------- sitemap ----------
   Root pages are listed explicitly rather than parsed out of the
   existing file, so a hand edit to sitemap.xml does not silently
   survive a rebuild. Add root pages here when the site gains one. */
function sitemap () {
  const rootPages = [
    { loc: `${ORIGIN}/`,               priority: '1.0', changefreq: 'monthly' },
    { loc: `${ORIGIN}/partners.html`,  priority: '0.7', changefreq: 'monthly' },
    { loc: `${ORIGIN}/privacy.html`,   priority: '0.3', changefreq: 'yearly'  }
  ];
  const localPages = [
    { loc: `${ORIGIN}/local/`, priority: '0.8', changefreq: 'monthly' },
    ...cities.map(c => ({
      loc: `${ORIGIN}/local/${c.slug}/`,
      priority: c.home ? '0.9' : '0.8',
      changefreq: 'monthly'
    }))
  ];

  const entry = p => `  <url>
    <loc>${p.loc}</loc>
    <lastmod>${TODAY}</lastmod>
    <changefreq>${p.changefreq}</changefreq>
    <priority>${p.priority}</priority>
  </url>`;

  const workflowPages = [
    { loc: `${ORIGIN}/workflows/`, priority: '0.8', changefreq: 'monthly' },
    ...workflows.map(w => ({
      loc: `${ORIGIN}/workflows/${w.slug}/`,
      priority: '0.7',
      changefreq: 'monthly'
    }))
  ];

  return `<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated by local/_build/build.js. Do not hand-edit: add pages to
     rootPages in that file instead, or they vanish on the next build. -->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${[...rootPages, ...localPages, ...workflowPages].map(entry).join('\n')}
</urlset>
`;
}

/* ===========================================================
   WORKFLOW PAGES — problem-shaped entry
   -----------------------------------------------------------
   Deliberately NOT tool guides. The head terms in this space
   belong to Salesforce, NetSuite and a wall of vendor blogs,
   and a one-operator shop does not outrank them by writing the
   same article. What is winnable, and genuinely useful, is the
   question those searchers hit next: buy a tool, or build?
   "Buy the tool" has to stay a real and frequent answer on
   every one of these pages, or they turn into adverts and
   convert worse. See workflows.json for the full rule.
   =========================================================== */

function wfJsonLd (w) {
  const url = `${ORIGIN}/workflows/${w.slug}/`;
  const article = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    '@id': `${url}#article`,
    headline: plain(w.h1),
    description: plain(w.metaDesc),
    url,
    author:    { '@type': 'Person', name: 'Bryan Piard' },
    publisher: { '@type': 'Organization', name: 'Perseid Echo Creations', url: `${ORIGIN}/` },
    about: { '@type': 'Thing', name: w.short },
    isPartOf: { '@type': 'CollectionPage', url: `${ORIGIN}/workflows/` }
  };
  const crumbs = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Home',      item: `${ORIGIN}/` },
      { '@type': 'ListItem', position: 2, name: 'Workflows', item: `${ORIGIN}/workflows/` },
      { '@type': 'ListItem', position: 3, name: w.short,     item: url }
    ]
  };
  const faq = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: w.faq.map(f => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a.replace(/<[^>]+>/g, '') }
    }))
  };
  return [article, crumbs, faq]
    .map(o => `<script type="application/ld+json">\n${JSON.stringify(o, null, 2)}\n</script>`)
    .join('\n');
}

function wfPage (w) {
  const url = `${ORIGIN}/workflows/${w.slug}/`;
  const cityLinks = (w.cities || [])
    .map(name => cities.find(c => c.city === name))
    .filter(Boolean);

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(w.title)}</title>
<meta name="description" content="${esc(w.metaDesc)}">
<meta name="theme-color" content="#0B1018">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<meta property="og:type" content="article">
<meta property="og:title" content="${esc(plain(w.h1))}">
<meta property="og:description" content="${esc(w.metaDesc)}">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${ORIGIN}/art/ind-bench.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="${url}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Spline+Sans+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/local/assets/local.css">

${wfJsonLd(w)}
</head>
<body>
${topbar('')}

<main>

<header class="hero hero--bench">
  <div class="hero__art" role="presentation"></div>
  <div class="hero__scrim" role="presentation"></div>
  <div class="wrap hero__inner">
    <nav class="crumb" aria-label="Breadcrumb">
      <ol>
        <li><a href="${ORIGIN}/">Home</a></li>
        <li><a href="/workflows/">Workflows</a></li>
        <li aria-current="page">${esc(w.short)}</li>
      </ol>
    </nav>
    <p class="tag">${esc(w.short)}</p>
    <h1 class="h-xl hero__head">${w.h1}</h1>
    <p class="hero__sub">${esc(w.sub)}</p>
    <div class="hero__acts">
      <a class="btn btn--go" href="${ORIGIN}/#fitcheck">Run the 60-second Fit Check</a>
      <a class="btn btn--line" href="#decide">Buy or build?</a>
    </div>
  </div>
</header>

<!-- the problem, in the owner's words -->
<section class="sec" aria-labelledby="prob-h">
  <div class="wrap narrow rise">
    <p class="tag">What actually happens</p>
    <h2 class="h-lg" id="prob-h" style="margin-block:14px 16px;">Nobody decided to let this happen.</h2>
    ${w.problem.map(p => `<p class="lede" style="margin-bottom:14px;">${p}</p>`).join('\n    ')}
  </div>
</section>

<!-- work out your own number -->
<section class="sec sec--paper" aria-labelledby="cost-h">
  <div class="wrap narrow rise">
    <p class="tag tag--ink">Work out your own number</p>
    <h2 class="h-lg" id="cost-h" style="margin-block:14px 16px;">What is this costing you?</h2>
    <p class="lede lede--ink">${w.arithmetic.lede}</p>
    <ol class="steps steps--ink">
      ${w.arithmetic.steps.map((s, i) => `<li class="step">
        <span class="step__n">${i + 1}</span>
        <p>${s}</p>
      </li>`).join('\n      ')}
    </ol>
    <p class="lede lede--ink" style="margin-top:22px;">${w.arithmetic.close}</p>
  </div>
</section>

<!-- the decision -->
<section class="sec sec--band" id="decide" aria-labelledby="dec-h">
  <div class="wrap narrow rise">
    <p class="tag">The honest version</p>
    <h2 class="h-lg" id="dec-h" style="margin-block:14px 16px;">Buy a tool, or build it?</h2>
    <div class="duo">
      <div class="duo__col">
        <h3 class="h-sm duo__h">Buy the tool if</h3>
        <ul class="ticks">
          ${w.buyOrBuild.buy.map(b => `<li>${b}</li>`).join('\n          ')}
        </ul>
      </div>
      <div class="duo__col">
        <h3 class="h-sm duo__h">Build it if</h3>
        <ul class="ticks ticks--flame">
          ${w.buyOrBuild.build.map(b => `<li>${b}</li>`).join('\n          ')}
        </ul>
      </div>
    </div>
    <p class="lede" style="margin-top:26px;">${w.buyOrBuild.honest}</p>
  </div>
</section>

<!-- what a build looks like -->
<section class="sec" aria-labelledby="build-h">
  <div class="wrap narrow rise">
    <p class="tag">If it is the second one</p>
    <h2 class="h-lg" id="build-h" style="margin-block:14px 16px;">What a build actually has to do</h2>
    <div class="cards">
      ${w.build.map((b, i) => `<article class="card">
        <span class="card__n">Part ${i + 1}</span>
        <h3 class="h-sm">${esc(b.n)}</h3>
        <p>${esc(b.p)}</p>
      </article>`).join('\n      ')}
    </div>
  </div>
</section>

<!-- when not to -->
<section class="sec" style="padding-block:clamp(34px,4.4vw,54px);" aria-labelledby="not-h">
  <div class="wrap narrow rise">
    <div class="notyet">
      <p class="tag">When to leave this alone</p>
      <h2 class="h-md" id="not-h" style="margin-block:11px 8px;">Do not build this yet if&hellip;</h2>
      <p>${esc(w.notYet)}</p>
    </div>
  </div>
</section>

${control()}

<!-- FAQ -->
<section class="sec sec--band" aria-labelledby="wfaq-h">
  <div class="wrap narrow rise">
    <p class="tag">Straight answers</p>
    <h2 class="h-lg" id="wfaq-h" style="margin-block:14px 8px;">Questions this one always raises</h2>
    <div class="faq">
      ${w.faq.map(f => `<details>
        <summary>${esc(f.q)}</summary>
        <div class="faq__a"><p>${f.a}</p></div>
      </details>`).join('\n      ')}
    </div>
  </div>
</section>

${cityLinks.length ? `
<section class="sec" style="padding-block:clamp(34px,4.4vw,54px);" aria-labelledby="wc-h">
  <div class="wrap narrow rise">
    <p class="tag">Where this comes up</p>
    <h2 class="h-md" id="wc-h" style="margin-block:11px 6px;">Most common in these areas</h2>
    <p style="color:var(--steel); font-size:16px;">Not a rule, just where I see it most. I work across south and east King County.</p>
    <div class="near">
      ${cityLinks.map(c => `<a href="/local/${c.slug}/">${esc(c.city)}, ${esc(c.region)}</a>`).join('\n      ')}
      <a href="/workflows/">Other workflows</a>
    </div>
  </div>
</section>` : ''}

${closeBlock('')}

</main>
${footer('')}

<script>window.PEC_PAGE = ${JSON.stringify('wf:' + w.slug)};</script>
<script src="/local/assets/track.js" defer></script>
</body>
</html>
`;
}

function wfHub () {
  const url = `${ORIGIN}/workflows/`;
  const ld = {
    '@context': 'https://schema.org',
    '@type': 'CollectionPage',
    name: 'Workflows · Perseid Echo Creations',
    url,
    hasPart: workflows.map(w => ({
      '@type': 'Article',
      name: plain(w.h1),
      url: `${ORIGIN}/workflows/${w.slug}/`
    }))
  };

  return `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Workflows · Buy a tool, or build it?</title>
<meta name="description" content="The repetitive jobs I get asked about most, and an honest read on each: when an off-the-shelf tool is the right answer, and when it needs building.">
<meta name="theme-color" content="#0B1018">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">

<meta property="og:type" content="website">
<meta property="og:title" content="Buy a tool, or build it?">
<meta property="og:description" content="Five repetitive jobs, and an honest read on each. Sometimes the answer is buy the tool and keep your money.">
<meta property="og:url" content="${url}">
<meta property="og:image" content="${ORIGIN}/art/ind-bench.webp">
<meta name="twitter:card" content="summary_large_image">
<link rel="canonical" href="${url}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo:wght@400;500;600;700&family=Spline+Sans+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/local/assets/local.css">

<script type="application/ld+json">
${JSON.stringify(ld, null, 2)}
</script>
</head>
<body>
${topbar('')}

<main>
<header class="hero hero--bench">
  <div class="hero__art" role="presentation"></div>
  <div class="hero__scrim" role="presentation"></div>
  <div class="wrap hero__inner">
    <nav class="crumb" aria-label="Breadcrumb">
      <ol>
        <li><a href="${ORIGIN}/">Home</a></li>
        <li aria-current="page">Workflows</li>
      </ol>
    </nav>
    <p class="tag">The jobs I get asked about</p>
    <h1 class="h-xl hero__head">Buy a tool, or <em>build it?</em></h1>
    <p class="hero__sub">Five repetitive jobs that eat owner-led businesses, and the honest read on each. On more than one of them the right answer is to buy something off the shelf and keep your money &mdash; those pages say so.</p>
    <div class="hero__acts">
      <a class="btn btn--go" href="${ORIGIN}/#fitcheck">Run the 60-second Fit Check</a>
      <a class="btn btn--line" href="/local/">Areas served</a>
    </div>
  </div>
</header>

<section class="sec" aria-labelledby="wfs-h">
  <div class="wrap rise">
    <p class="tag">Five workflows</p>
    <h2 class="h-lg" id="wfs-h" style="margin-block:14px 16px;">Pick the one that sounds like your week</h2>
    <div class="hub">
      ${workflows.map(w => `<a class="hub__a" href="/workflows/${w.slug}/">
        <h3 class="h-md">${esc(w.short)}</h3>
        <p>${esc(plain(w.sub).slice(0, 128))}&hellip;</p>
        <span class="go">Read the honest version &rarr;</span>
      </a>`).join('\n      ')}
    </div>
  </div>
</section>

${staircase('King County')}
${closeBlock('')}

</main>
${footer('')}

<script>window.PEC_PAGE = "wf:hub";</script>
<script src="/local/assets/track.js" defer></script>
</body>
</html>
`;
}

/* ---------- write ---------- */
let written = 0;

for (const c of cities) {
  const dir = path.join(LOCAL, c.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), page(c), 'utf8');
  console.log(`  local/${c.slug}/index.html`);
  written++;
}

fs.writeFileSync(path.join(LOCAL, 'index.html'), hub(), 'utf8');
console.log('  local/index.html');
written++;

for (const w of workflows) {
  const dir = path.join(WORKDIR, w.slug);
  fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(path.join(dir, 'index.html'), wfPage(w), 'utf8');
  console.log(`  workflows/${w.slug}/index.html`);
  written++;
}

fs.mkdirSync(WORKDIR, { recursive: true });
fs.writeFileSync(path.join(WORKDIR, 'index.html'), wfHub(), 'utf8');
console.log('  workflows/index.html');
written++;

fs.writeFileSync(path.join(ROOT, 'sitemap.xml'), sitemap(), 'utf8');
console.log('  sitemap.xml');

console.log(`\n${written} pages written for ${cities.length} cities, lastmod ${TODAY}.`);
