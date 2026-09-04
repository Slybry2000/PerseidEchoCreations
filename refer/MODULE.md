# The "pass it on" module

A drop-in block for the surfaces a happy client already looks at — client document hubs, content approval pages, first-look microsites. It is the other half of `/refer/`: that page is where somebody goes when they have decided to refer, this is what causes them to decide.

**Nothing here is live.** These are snippets to be pasted into the generators that build those surfaces. See `refer/README.md` for the launch sequence.

## Where it goes

| Surface | Built by | Where in the page |
|---|---|---|
| Client document hub | `PMOS/scripts/build-client-hub.js` | Bottom of the left sidebar, under the document list |
| Content approval page | `content_pipe` `content-review.js` | After the approve/reject controls, only on the **thank-you state** |
| First-look microsite | per-client, published to here.now | Footer, above the PEC line |

## The one rule

**It only ever appears after the value has landed.** Below the documents, not above them. On the thank-you state, never next to the approve button. A referral ask that interrupts the work reads as a sales page and costs more trust than the referral is worth.

If you cannot place it after the value on a given surface, leave that surface out.

## The block

Self-contained: no external CSS, no script, inherits nothing. Safe to paste into any of the three generators, all of which have different stylesheets.

```html
<!-- pass-it-on · appears only after the value has landed -->
<aside class="pec-pass" aria-label="Refer Perseid Echo">
  <p class="pec-pass__k">If this is useful</p>
  <p class="pec-pass__t">
    Most of my work arrives because someone passed my name along.
    If you know a business with the same problem,
    <a class="pec-pass__a" href="https://perseidechocreations.com/refer/?r=REF_CODE&amp;n=REF_NAME">here is the easy way to hand me on</a>.
  </p>
</aside>

<style>
.pec-pass{
  margin-top:26px; padding:16px 18px;
  border-left:3px solid #F26B36;
  background:rgba(242,107,54,0.055);
  border-radius:0 3px 3px 0;
  font:400 14px/1.55 system-ui,-apple-system,"Segoe UI",sans-serif;
}
.pec-pass__k{
  margin:0 0 6px; font-size:10.5px; letter-spacing:.16em;
  text-transform:uppercase; font-weight:600; color:#B4491F;
}
.pec-pass__t{ margin:0; color:inherit; opacity:.92; }
.pec-pass__a{ color:#B4491F; font-weight:600; }
.pec-pass__a:hover{ color:#8f3616; }
@media (prefers-color-scheme:dark){
  .pec-pass__k,.pec-pass__a{ color:#F9A03F; }
  .pec-pass__a:hover{ color:#F26B36; }
}
</style>
```

## The two placeholders

`REF_CODE` and `REF_NAME` are substituted per client by the generator.

- `REF_CODE` — a short opaque token, one per client. `[A-Za-z0-9_-]`, 32 chars max. It is the only thing that travels: `/refer/` carries it into the Fit Check link as `?ref=`, and the tracker records it as `rc`. **Never put a name, an email or a company in it** — it ends up in a URL the referred person can see.
- `REF_NAME` — a first name, used once to say "Thanks, Dana" at the top of `/refer/`. Optional; omit the parameter entirely if there isn't a clean one.

Suggested codes live in `refer/codes.json` alongside this file. They are arbitrary — the only requirement is that they are unique and stable, because changing one orphans any link already sent.

## What it must never become

- No incentive language. No "get $X". Compensation is agreed individually, in writing, and that is a positioning rule (see `partners.html` rule 2 and `/refer/`).
- No pop-up, no interstitial, no email trigger. It is a line of text at the bottom of a page somebody already chose to open.
- Not on cold surfaces. This block never appears on anything a prospect sees before they are a client.
