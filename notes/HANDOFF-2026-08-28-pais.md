# Handoff — 28 August 2026, the Pais file wrapper and everything around it

**Read `CLAUDE.md` first, then this.** Written mid-session against a compaction risk, so it is
a working handoff rather than an end-of-day one. Everything described here is **committed and
pushed** to `claude/repo-handoff-review-hyvs7b` and CI is green on it.

**Do not trust any figure below.** Run `python3 tools/state_snapshot.py --gate`.

---

## 1. Where the session got to

Three separate bodies of work landed today, in this order. PR
[#12](https://github.com/Samizdat-Publications/the-legacy-program-dashboard/pull/12) carries
all of it and is still an open draft.

| | note |
|---|---|
| NARA Air Force transfer into RG 615 | `notes/NARA-AIRFORCE-2026-08-28.md` |
| The gate made portable, and CI | `notes/GATE-PORTABILITY-2026-08-28.md` |
| Salvatore Pais and the five Navy filings | `notes/PAIS-PATENTS-2026-08-28.md` |
| this file | the Pais file wrapper, which is where the session ended |

## 2. What Stewart asked for that is NOT done

**In priority order. These are the live asks.**

1. **The Reasons for Allowance, 24 October 2018.** Sitting unread in the Drive folder. It says
   what actually persuaded the examiner to reverse a final rejection. It is the single most
   informative unread document in the set, more than either Rule 132 affidavit, because it is
   the examiner's own account of what changed his mind.
2. **The two Rule 131/132 affidavits** (received 24 May 2018 and 20 August 2018). One of these
   is the Sheehy declaration that all the secondary reporting is about. Still unread.
3. **Whether US-government-assigned patents owe maintenance fees on the ordinary schedule.**
   This gates the biggest finding of the day, see section 4. Unresolved and it must not be
   asserted either way until it is.
4. **The patents tab.** Stewart asked for it twice. NOT built, deliberately: CLAUDE.md section 9
   requires a mockup at 1366 / 1920 / 2560 shown to him first, because the last three layout
   changes built directly were all wrong on the first cut. The data and the drawings now exist
   to build it against.
5. **The five observables node.** Stewart supplied the list and says it is "key to this whole
   thing". Research done, node NOT built, and the finding is in section 5 because it changes
   what the node can be.
6. **The other four file wrappers.** Stewart is pulling them. Application numbers he needs:
   **14/807,943** (EM field generator), **15/431,823** (gravitational wave generator),
   **15/678,672** (superconductor), **15/928,703** (plasma compression fusion).
7. **Maury Island / Crisman / Dahl / Kelso B-25**, and LeMay and Eaker. Asked, not answered.
8. **3D craft models.** Stewart intends to try Claude Design for this himself.

## 3. The Drive folder is the source, and here is how to read it

Stewart uploaded the complete file wrapper for application 15/141,270 to Google Drive:

```
https://drive.google.com/drive/folders/1QApKwngnmcPYAbsH1oWB_bW5ars2NEgU
```

**The Drive connector works and is the way in.** `mcp__Google_Drive__search_files` with
`parentId = '1QApKwngnmcPYAbsH1oWB_bW5ars2NEgU'` lists it;
`mcp__Google_Drive__read_file_content` returns PDF text directly, which is how the application
as filed was read. The PDFs have opaque names like `INKRUA2VPXXIFW3.pdf`; there is no index, so
finding a specific document means reading content snippets. `search_files` with
`fullText contains '...'` scoped to that parentId is the efficient way to locate one.

`15141270.json` in that folder is the USPTO application-data record and is the most valuable
single file: it carries the complete event history, the attorneys, the examiner, the assignment
and the status. `download_file_content` returns it base64-encoded.

**Do NOT pull the drawings through Drive.** There is a much better route, section 6.

## 4. The finding that matters most, and its caveat

**US 10,144,532 is expired.** USPTO application data gives status *"Patent Expired Due to
NonPayment of Maintenance Fees Under 37 CFR 1.362"*, status date **9 January 2023**, after a
maintenance fee reminder mailed 25 July 2022.

The Navy fought a formal appeal for two years to obtain this grant and then did not pay the
first renewal, putting the invention into the public domain. Stewart, who has followed this
subject closely and listened to roughly ten hours of Pais interviews, had never heard it
raised. It is not in any of the secondary coverage this session found, and the reason is
probably mundane: it requires pulling maintenance status out of the application data rather
than reading the patent, and everybody reads the patent.

**The caveat is load-bearing and is recorded on the node as unverified.** Nobody has checked
whether patents assigned to a US government agency owe maintenance fees on the ordinary
schedule or are treated differently. Until that is settled the lapse cannot be read as a
decision rather than a bookkeeping outcome. **Check this before anyone uses the expiry as an
argument.** It would be a bad way to lose an audience.

The reading offered on the node, marked Tier 3 with its reasoning written out, is that the Navy
wanted the examining authority's *finding* rather than the property right: publication in
November 2017 already created permanent prior art, so the appeal bought nothing defensive, and
what it did buy was the reversal of an enablement rejection. A maintenance fee buys only the
right to exclude an infringer, which the Navy would never exercise. The competing reading, that
the docket simply lapsed after Pais transferred out of NAWCAD in June 2019, is equally
available and is recorded alongside it.

## 5. The five observables, and why the node was not built

Stewart supplied the canonical five and a secondary source. The research question asked before
building was whether the list appears in any released government document.

**It does not appear to.** It looks like Elizondo's public formulation, carried out after he
left the Pentagon, rather than something written into an AATIP or AAWSAP briefing that anyone
has released. Stated carefully because it is an absence claim: none was found, which is not the
same as none existing, and much AATIP material is described as still classified.

**That shapes the node rather than blocking it.** The five cap at Tier 2, attributed to
Elizondo rather than to the Pentagon, with the provenance gap recorded as a finding and a FOIA
target. The payoff is the Pais mapping, which is Tier 1: four of the five are itemised as
design goals in the NAVAIR PAX 205 briefing. Presented that way the absence is a strength.
Presented as "the government's framework" it is the hole a serious reader puts a finger
through, which is the failure mode Stewart explicitly asked to avoid.

## 6. Two retrieval routes worth keeping

**Patent PDFs including drawings, no key, no account:**

```
https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/<patent or pub number>
```

This works from a datacenter address where the obvious routes do not: FreePatentsOnline serves
a login wall for PDFs, and Google Patents returns 503 on every request. Eleven drawing sheets
came from here and are in `research/patents/drawings/` with full provenance.

**The file wrapper and the drawings both also live behind `api.uspto.gov`**, which answers 401
with no key and 403 with a bogus one, confirming `X-API-KEY` is the header. Stewart is
obtaining an ODP key from data.uspto.gov. **When he has it, the whole file wrapper for all five
applications can be pulled directly** rather than by hand, and that is the moment to do the
other four.

## 7. What is on the board now

`research/pais-patents.json`, one domain, seven nodes, 23 claims on the person alone.

The Tier 1 spine, all read off primary documents:

- Five filings 2015-2018, all assigned to the Secretary of the Navy, with application numbers
  and dates read off patent records rather than recalled.
- The NAVAIR PAX 205 invention-disclosure briefing released under FOIA, which describes a
  "hybrid aerospace / undersea craft" moving through air, space and water in a vacuum plasma
  sheath with extreme speed and non-linear RF and sonar scattering, and which states **twice**
  that there is no prototype in existence.
- The full prosecution history: third-level security review May 2016, non-final rejection,
  examiner interview, final rejection, two Rule 132 affidavits, Notice of Appeal, Appeal Brief,
  allowance before the PTAB ruled, grant, expiry.
- Paragraph [0020] of the application credits **Harold Puthoff** by name. Puthoff is already a
  Tier A node here. That link was on the face of the filing the whole time.
- Paragraph [0037] incorporates the EM field generator application by reference, so the two
  patents are linked as components of one design by the author, not by inference.

**No edge to AATIP, AAWSAP, KONA BLUE, any DIRD or any custody chain.** Nothing supports one,
`d-custody` was deliberately left off his domains, and the absence is stated on the node rather
than left as a silence. Drawing that edge is the thing that would get this board dismissed.

## 8. Standing instruction from Stewart, worth carrying forward verbatim

> "I want to not just have this be a conspiracy brain item but something I can put in front of
> respectable individuals and not have them immediately dismiss it."

He also said, when told the disconfirming NAWCAD result would go on the node: *"No you're doing
it right."* He holds strong personal views about Pais and is explicit that they are his
commentary rather than the board's content. **The tier system is doing that work and he
endorses it.** Keep putting his readings on as Tier 3 stated inference with reasoning written
out, and keep the disconfirming record on the node. That is what he is asking for.

## 9. Gate and CI

Green throughout, all ten steps including `--idempotent`. CI runs 1, 2, 3 and 5 succeeded; run
4 shows cancelled because the concurrency group killed a superseded run when a second push
arrived two minutes later, which is the configuration working.

Golden has been re-baselined five times today, each time deliberately and each time with every
moved count accounted for by what was authored. `l0_nodes` has stayed at 110 throughout, so the
map layout has not shifted and none of this touched the shell.
