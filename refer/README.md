# Referral and partner loops

**STAGED, NOT LAUNCHED.** Built 2026-07-30 on branch `referral-loops`. Nothing is on `main`, nothing is deployed, no link has been sent, no client surface has been touched. Ticket #65.

## The gap this closes

Every surface a happy client already looks at — their document hub, a content approval page, a first-look microsite — is a place where they could hand PEC to the next customer. None of them ask. Meanwhile cold outreach costs money per booked call and referral costs nothing, which makes this the cheapest unbuilt channel PEC has.

## What is built

| Piece | Path | State |
|---|---|---|
| The referral page | `refer/index.html` (generated) | Built, noindex, not linked from anywhere |
| Drop-in module for client surfaces | `refer/MODULE.md` | Snippet written, **not pasted into any generator** |
| Per-client referral codes | `refer/codes.json` | Codes allocated, all `live: false` |
| `?ref=` attribution | `local/assets/track.js` + `index.html` inline tracker | Wired, harmless until links exist |

### `/refer/`

A page you send someone to by link, after they have had a good experience. Not in the nav, not in the sitemap, `noindex,follow`. A public "please refer us" page reads as needy on a one-operator site.

It does three things: gives them a link to send, gives them words to send with it (editable, and it says so), and tells them exactly what happens to the person they send — including that nobody gets chased.

Takes two optional parameters:

- `?r=CODE` — the referrer's code, carried into the Fit Check link as `?ref=`
- `?n=Name` — a first name, used once for "Thanks, Dana"

Both are sanitised client-side. Without them the page still works; it just shows the plain link.

### Attribution

`?ref=` is read by both trackers and sent as `rc` on the first event of a session. The existing privacy contract is unchanged: opt-out check still runs first, no cookies, no third party, and the code is an opaque token — **never a name, email or company**, because it travels in a URL the referred person can see.

That makes the loop measurable rather than assumed: a Fit Check can be traced to the introduction that caused it.

## Decisions made, and why

**No incentive language anywhere.** No percentage, no points, no "get $250". This matches `partners.html` rule 2 (compensation agreed per engagement, in writing) and it is a positioning choice, not a gap to fill later. The page says so out loud and adds that a favour with no money attached is fine and is what usually happens.

If you want to change that, change it deliberately — but a published percentage changes *why* people refer, and for a channel this small that is the thing worth protecting.

**The module only appears after the value has landed.** Below the documents in a hub, on the thank-you state of an approval page, never beside an approve button. A referral ask that interrupts the work costs more trust than the referral is worth. If a surface cannot place it after the value, that surface is left out.

**No email sequence, no pop-up, no automated ask.** Everything here is a line of text on a page somebody already chose to open, plus a link you send by hand.

## What is blocked on you

1. **Which clients get a code.** `codes.json` has five rows from the existing hub list. Referring is a favour, and asking the wrong client at the wrong moment is worse than not asking. Review the list and mark who is fair to ask — I have not made that call.
2. **The names.** `name` is empty on every row rather than guessed.
3. **Whether the thanks stay unpriced.** Recommendation is yes, per above. Your business, your call.

## Launch sequence, when you want it

Nothing below has been run.

```bash
cd /c/Projects/PECWEB
git checkout main
git merge referral-loops
git push origin main
```

That publishes `/refer/` (still unlinked and noindex) and the `?ref=` capture. Harmless on its own — the page exists but nobody can reach it.

Then, in order:

1. Fill in `codes.json` — who is fair to ask, and their first names.
2. Test one link end to end before any client sees it: open `/refer/?r=<code>&n=<name>`, copy the link, run the Fit Check through it, and confirm `rc` appears in `fitcheck-stats`. **Do not skip this** — an attribution bug means you cannot tell whether the channel works, which is the only reason to build it.
3. Paste the module from `MODULE.md` into `PMOS/scripts/build-client-hub.js`, one client first, not all five.
4. Watch that one hub for a fortnight. If nothing happens, the placement or the wording is wrong — fix it before rolling out, not after.
5. Roll out to the rest, flipping `live: true` per row as you go.

## Deliberately not built

- **No approval-page or content_pipe change.** Those generators live on the VPS and editing them is deploying, not staging. `MODULE.md` documents exactly where the block goes.
- **No automated "ask for a referral" trigger** on project completion. Tempting and easy to build; it is also how a referral channel turns into spam. Worth doing by hand until there is enough volume that by hand stops working.
- **No partner-side changes.** `partners.html` already covers the advisor channel and its positioning rules hold. The `?ref=` scheme works for partner links too without any page change.
