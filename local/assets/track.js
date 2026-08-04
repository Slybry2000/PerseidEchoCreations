/* ---------- anonymous funnel measurement, local service pages ----------
   Same contract as the inline block on the homepage: no cookies, no third
   party, no IP stored server-side, and the opt-out check runs FIRST so a
   visitor sending Global Privacy Control or Do Not Track never causes a
   single request. Documented at /privacy.html.

   The one difference from the homepage copy: PAGE comes from
   window.PEC_PAGE, set by each page before this file loads, so the funnel
   can tell which city page earned the Fit Check. */
window.pecTrack = function(){};
(function(){
  "use strict";
  try {
    if (navigator.globalPrivacyControl === true ||
        navigator.doNotTrack === "1" || window.doNotTrack === "1" ||
        navigator.msDoNotTrack === "1") return;
  } catch (e) { return; }

  /* Traffic that is not a stranger is MARKED, not blocked, so the funnel can
     describe visitors only. navigator.webdriver covers every driven browser;
     ?qa=1 sets a sticky marker for a real browser doing hand testing, and
     ?qa=0 clears it again. Nothing about the visitor is stored either way —
     the flag says "do not count this as a stranger" and nothing else. */
  var qa = false;
  try {
    if (navigator.webdriver === true) qa = true;
    var qaFlag = new URLSearchParams(location.search).get("qa");
    if (qaFlag === "1") localStorage.setItem("pec_qa", "1");
    else if (qaFlag === "0") localStorage.removeItem("pec_qa");
    if (localStorage.getItem("pec_qa") === "1") qa = true;
  } catch (e) { /* a locked-down browser just counts as an ordinary visitor */ }

  var ENDPOINT = "https://approve.perseidechocreations.com/_e";
  var PAGE = window.PEC_PAGE || "local";

  var sid;
  try {
    sid = sessionStorage.getItem("pec_s");
    if (!sid) { sid = Math.random().toString(36).slice(2, 12); sessionStorage.setItem("pec_s", sid); }
  } catch (e) { sid = Math.random().toString(36).slice(2, 12); }

  var device = (window.innerWidth || 1024) < 700 ? "m" : "d";

  var attribution = {};
  try {
    var qs = new URLSearchParams(location.search);
    if (qs.get("utm_source"))   attribution.src = qs.get("utm_source");
    if (qs.get("utm_campaign")) attribution.cmp = qs.get("utm_campaign");

    /* Referral code from /refer/. Sanitised to an opaque token — it is a
       code, never a name or an email, so nothing identifying about the
       referrer or the person they sent leaves the page. Sent under its own
       key so it does not collide with the referrer-host fallback below. */
    var rc = qs.get("ref");
    if (rc) attribution.rc = rc.replace(/[^A-Za-z0-9_-]/g, "").slice(0, 32);

    if (!attribution.src && document.referrer) {
      var h = new URL(document.referrer).hostname;
      if (h && h !== location.hostname) attribution.ref = h;
    }
  } catch (e) { /* attribution is a bonus, never a blocker */ }

  var first = true;
  function send(name, extra) {
    try {
      var body = { e: name, s: sid, p: PAGE, d: device };
      if (qa) body.qa = 1;
      if (first) { for (var k in attribution) body[k] = attribution[k]; first = false; }
      if (extra) for (var j in extra) body[j] = extra[j];
      var payload = JSON.stringify(body);
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, new Blob([payload], { type: "text/plain" }));
      } else {
        fetch(ENDPOINT, { method: "POST", body: payload, mode: "no-cors", keepalive: true,
                          headers: { "Content-Type": "text/plain" } }).catch(function(){});
      }
    } catch (e) { /* measurement must never break the page */ }
  }

  window.pecTrack = send;
  send("view");

  /* Outbound intent, caught once at the document level. The one that matters
     here is the handoff to the homepage Fit Check: that is this page's job. */
  document.addEventListener("click", function(ev) {
    try {
      var a = ev.target && ev.target.closest ? ev.target.closest("a[href]") : null;
      if (!a) return;
      var href = a.getAttribute("href") || "";
      if (href.indexOf("#fitcheck") > -1)             send("cta_fitcheck");
      else if (href.indexOf("calendar.app.google") > -1) send("cta_call");
      else if (href.indexOf("mailto:") === 0)            send("cta_email");
      else if (href.indexOf("/local/") > -1)             send("cta_nearby");
      else if (href.indexOf("#cost") > -1)               send("cta_cost");
    } catch (e) { /* never interfere with the click itself */ }
  }, true);
})();

/* ---------- reveal ---------- */
(function(){
  "use strict";
  var els = document.querySelectorAll(".rise");
  if (!("IntersectionObserver" in window)) {
    for (var i = 0; i < els.length; i++) els[i].classList.add("is-in");
    return;
  }
  var io = new IntersectionObserver(function(entries){
    entries.forEach(function(en){
      if (en.isIntersecting) { en.target.classList.add("is-in"); io.unobserve(en.target); }
    });
  }, { rootMargin: "0px 0px -8% 0px", threshold: 0.06 });
  for (var j = 0; j < els.length; j++) io.observe(els[j]);
})();
