# Four maintenance passes, and three of them are negative results

**29 August 2026.** Items 4 to 7 from the outstanding list, run after the day's research
wave. Three returned negative results, and a negative result that is *checked* is worth
more here than an unchecked positive.

---

## 1. Link sweep: the board still has zero dead citations

`python3 tools/spot_check.py --links`, 1,350 distinct cited URLs.

| outcome | count | what it means |
|---|---|---|
| ok | 858 | 200 |
| HTTP 403 | 263 | this environment; mostly `.mil` and `war.gov` |
| HTTP 503 | 160 | `patents.google` refusing automated access |
| HTTP 429 | 40 | this crawl, not the board; these answer 200 asked once |
| curl failed | 12 | unreachable from here, almost all `web.archive.org` |
| HTTP 202 | 11 | `irp.fas.org` bot challenge |
| 406 / 405 / 500 | 6 | user-agent or method filtering |

**No 404 and no 410 anywhere.** Only those two count as dead, and the sweep found none.
The property held across a research wave that added USPTO file-wrapper citations, the
govinfo CFR, History and To The Stars. Worth re-running after the next wave rather than
assuming; link rot is silent.

## 2. Elizondo's written testimony does not state the five observables

`notes/HANDOFF-2026-08-29.md` left this as the best remaining route to move the taxonomy
off reporting: if he states the five in sworn written testimony, the set moves to the
congressional record.

**He does not.** The written statement for the House Oversight hearing of 13 November
2024 contains none of: `observable`, `acceleration`, `trans-medium`, `lift`,
`hypersonic`, `signature`, `cloak`, `AATIP`. Full text at
`research/testimony/elizondo-house-oversight-2024-11-13.txt`.

**The earlier "cannot extract this PDF" was wrong**, and the correction matters more than
the result. The file uses subset fonts with per-font ToUnicode CMaps, so decompressing the
content streams by hand yields scrambled text — which is what the previous attempt did, and
it recorded the document as unreadable on that basis. It reads fine with a real PDF text
layer. The blocker was a broken system `cryptography` package that made both `pypdf` and
`pdfminer.six` panic on import; `pip install --force-reinstall cryptography` shadows it and
both work. That is the same shape as §3's "a cloud session cannot look at the board":
a tooling gap recorded as an impossibility.

What is still open is narrower and stated on the node: his **oral** testimony at the same
hearing has not been obtained, and no AATIP or AAWSAP briefing has been.

## 3. The ISOO seal exists, on a .gov original, and still cannot ship

`notes/IMAGE-CEILING-2026-08-28.md` said the remaining route was agency websites rather
than Commons, because AFOSI and AARO both cleared that way. Tried for ISOO.

**The mark exists**: `archives.gov/files/isoo/images/isoo-logo.jpg`, alt text "The
Information Security Oversight Office (ISOO) logo". Federal work on a federal site.

**It fails on pixels, not on licence.** Measured through a canvas the same way the 26 and
27 August passes measured theirs: it is a JPEG, so it has no alpha, and all four corner
pixels are `255,255,255,255`. Contain-fitted into the 11px chip box on the board's
`#12171d` fill it draws a **white card**, not a mark. That is the identical failure the
26 August pass recorded when it dropped AARO's first candidate — "verified at the pixel:
would draw a white box" — and unlike AARO there is no transparent PNG alternative.

**It could be made to clear by keying the white to transparency, and that decision is
Stewart's, not this session's.** CLAUDE.md §9 item 7 is explicit that a seal may not be
altered the way a portrait may be cropped, and several carry statutory restrictions on
alteration stricter than copyright. Flagged, not done.

The register stays at 13. OUSD(I) was not retried: Commons has no seal and the 28 August
search returned intelligence-law syllabi and a photograph containing identifiable faces.

## 4. The deployed board, looked at

Production was fetched and rendered rather than trusted. Canvas 1688x829 drawing, **964
entities and 2,172 sourced links** matching the merged data exactly, zero offsite requests,
and all five `_redirects` deep-link routes serving. One defect found and fixed the same
day, in `notes/` and in the commit log: the `<title>` still carried the parent board's
subtitle. It is the only thing the deploy verification found, and no check had been
looking at it.
