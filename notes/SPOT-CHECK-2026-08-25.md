# The sources say what the board says they say

**25 August 2026** — the first systematic run of `TESTING-CHECKLIST.md` §12.

## Why this was worth automating

§12 asks a human to "pick five claims at random from five different views and
verify against the source", and about a fabricated source it says: *"stop and
report immediately. That is the one failure mode that matters."* It had never been
started. Five is an anecdote, not a sample.

But most of §12 does not need a person. Whether a URL resolves is mechanical, and
so is whether the source **says what the claim says** — for the subset of claims
that quote the document verbatim. That subset is large: **630 claims carry both a
quoted phrase of four or more words and a URL**, and a quoted phrase is precisely
where a fabricated source shows itself. Paraphrase can drift honestly; a sentence
in quotation marks is either in the document or it is not.

`tools/spot_check.py` asserts that property: **every claim that quotes a phrase and
cites a fetchable URL must have that phrase in the document it cites.**

## The headline

**No fabricated source was found.** Not one quotation turned out to have been
invented, and not one cited a document that does not exist.

| | |
|---|---|
| claims quoting a document and citing a URL | 604 |
| host unreachable from this environment | 281 |
| **quote found in the cited document** | **278** |
| quote not found | 46 |
| — of those, scanned PDFs with no usable text layer | 41 |
| — **residual, each individually traced** | **5** |

Of the 283 claims this environment could actually adjudicate, **278 quote their
source correctly, and the five that do not are explained below.** Five real
defects were found and fixed; all five were citation or quotation-mark errors, not
invention.

## The five real defects, fixed

| node | what it said | what the document says |
|---|---|---|
| `waived-sap-notification-group` | 10 U.S.C. 119(e)(1) reaches "**a** requirement under subsection (a), (b), or (c)" | "may waive **any** requirement under subsection (a), (b), or (c)" |
| `cfr-32-117` | "defines SAP verbatim: '**Special access program (SAP)** means any program that is established…'" | 32 CFR 117.3 prints "**SAP** means any program that is established…" — the expansion was inside the quotation marks on a claim whose own words are *verbatim* |
| `gang-of-eight` | quoted "the chairman and ranking minority member of each of the defense committees", cited to 50 U.S.C. 3093 | that phrase appears **nowhere** in 50 U.S.C. 3093; it is verbatim 10 U.S.C. 119(e)(2), which the claim's own text says. The citation now names both |
| `burlison-mitre-letter-2026` | "The demand covers '**records transfers, destruction, or withholding**'" | the letter, as quoted by DefenseScoop, says MITRE "created, received, maintained, analyzed, **transferred, destroyed, withheld**, or otherwise controlled records" — the board's summary was wearing quotation marks |
| `ndaa-fy2023-sec-6802` | attributed "the date established in Section 6802" to the statute | the statute never uses that phrase; it is AARO's, from HRR Volume I. The citation now says so |

Also repaired: eight source URLs pointing at
`gov.br/arquivonacional/…/**copy_of_**noticias/…`, a staging path the Arquivo
Nacional has since removed. All eight now 404'd. The live page is the same URL
without that segment and carries the quoted sentence — *"Ele é composto de 743
registros"* — verbatim. The claim was right; the link had rotted.

Every one of these is small. That is the point: this is the class of error that
survives every other check on the board, because a slightly wrong quotation renders
perfectly and reads authoritatively.

## The four defects the check found in itself

The first run reported **86** missing quotes. Most were the tool's fault, and a
pass that manufactures findings is worse than no pass, because it teaches the
reader to skip the output. Each was fixed and is now commented at the site:

1. **An apostrophe is not a quotation mark.** `EarthTech's published citation list…`
   was read as a quote opening at the possessive and running to the next
   apostrophe. Fixed with lookarounds.
2. **Publishers write inside the sentence.** govinfo prints PL 117-263 §6802 as
   *"…enactment of the Intelligence Authorization `[[Page 136 STAT. 3590]]` Act for
   Fiscal Year 2023…"*, and interleaves `<<NOTE: Time period.>>` into statutory
   text. Four of the board's strongest statutory quotations read as missing
   because of it. Both markers are now stripped before comparison.
3. **A catalogue page is not the document.** `archive.org/details/{id}` returns 36KB
   of navigation chrome. The check reported the board as misquoting the USAF and
   Condon Report citations *added the same night*. It now resolves to the item's
   text.
4. **A 200 is not a success.** One house.gov PDF answered 168 bytes on the first
   pass and 531KB minutes later. The empty body was cached as a success, so six
   claims stayed "not found" against a document that had never been read, and no
   retry could reach them because nothing was recorded as an error.

Two smaller ones: the U.S. Code prints `§` where the board writes "Sec.", and an
elided quote (`'any requirement ... that certain information be included'`) is
deliberately not contiguous, so each fragment is now matched in order.

## What it still cannot judge, and this is not a finding

**41 of the 46 remaining are scanned paper.** The 38 DIRDs on The Black Vault are
photocopies run through OCR, with FOIA redaction stamps sitting inside sentences.
One reads:

> under the Defense Intelligence Agency, l(b)(3):10 USC 424 It\dvanced Aerospace
> Weapon Syst…

where the board correctly quotes *"under the Defense Intelligence Agency Advanced
Aerospace Weapon System Applications (AAWSA) Program"*. Another prints the
document's own ICOD stamp as `reDO:` and its control number as `DIA-08-1004-00 1`.
**Every DIRD quote in the first run reported NOT FOUND, and every one of them was
the board quoting accurately.** They are grouped out of the findings rather than
counted as them.

The last four residuals, all traced and all the board being right or harmless: the
Condon Report scan reads *"UFO repoits there"* where the board silently corrected
the OCR to *"reports"*; the U.S. Code interleaves `(A)`/`(B)`/`(C)` subparagraph
letters through a list the board quotes as running text; an ODNI cover page is
quoted as two lines joined; and one citation points at a Google Books *about* page,
which never contains the book's text and is a weak citation on its own terms.

## The largest finding: 181 claims cite a DIA reading-room URL that no longer resolves

`spot_check.py` reported every `dia.mil` citation as unreachable, because curl gets a
403. Going after them with WebFetch turned up something worse than a 403.

**46 distinct `dia.mil/FOIA/FOIA-Electronic-Reading-Room/FileId/1700xx/` URLs on this
board no longer reach a document.** They render the reading room's index page instead.
The proof is simple: `FileId/999999999/` — an id that cannot exist — returns the same
index. DIA falls back silently for any unrecognised id, so a stale citation looks like
a live one.

**181 claims cite one of those URLs, and not one of them cites a second copy of the
document.** Among the nodes affected: `baass`, `aawsap`, `harry-reid`,
`reid-letter-2009-06-24`, `dia-sap-denial-2009`, `reid-dia-meetings-2008-2009`, and
every DIRD node on the board.

The documents are not lost. DIA renumbered the reading room into a `2376xx` range —
the PDFs carry `OmniPage CSDK 18` OCR metadata last modified 28 April 2025, which is
about when the renumbering must have happened. Two are repaired here, each verified by
opening the document and reading it rather than by trusting a listing:

| board node | was | is | verified by |
|---|---|---|---|
| `reid-letter-2009-06-24`, `harry-reid` | `FileId/170016/` | **`FileId/237659/`** | letterhead "HARRY REID NEVADA", addressed to Deputy Secretary William Lynn III, dated June 24, 2009 |
| `dia-sap-denial-2009`, `baass` | `FileId/170058/` | **`FileId/237611/`** | "INFO MEMO / NOV I 3 2009 / SUBJECT: (U) Review of Special Access Program Request" |

**43 of the 46 are now repaired**, each one verified by opening the document and
reading its own title page, document number and page count — never by trusting the
index listing. Examples of what "verified" meant in practice:

- `170024` -> `237658` because the document's cover reads `DIA-08-1011-003` and it is
  50 pages, and the board's own claim says this DIRD is DIA-08-1011-003 and 50 pages.
  Its sibling `170025` -> `237644` is `DIA-08-1011-004` at 36 pages, matching the
  board's record of the second one.
- `170054` -> `237615` and `170055` -> `237614` because the board records the Talking
  Paper numbers U-326-09 and U-973-09, and the two documents carry exactly those.
  Without that the two are nearly interchangeable: both are titled "Senator Reid
  Visit", both open with the same Inouye/Reid appropriations paragraph.
- `170017` -> `237652` because that is the only document of the fourteen that contains
  BAASS's street address, which is what the board quotes from it.

**The last three were settled the next morning**, and the thing that settled them was
in the board all along. The first pass tried to match them on their quoted text, which
is why they looked hopeless: the quote on `170051` is the header common to all four
Contract Status Briefs. But the board's *claims* date the briefings.

| board id | what the board says it is | the document |
|---|---|---|
| `170051` | "DIA's own **16 December 2008** status briefing" | `237613` is the only brief bearing that date, and carries both of the board's quotes including "Advanced (unconventional) aerospace weapon" |
| `170052` | "DIA **8 May 2009** status briefing" | `237616` — see below |
| `170018` | not a document at all | the reading room's own index |

`170052` needed one more step, because DIA released the 8 May 2009 briefing **twice**.
`237616` and `237625` are the same briefing at 83% textual similarity, identical slide
structure, and both contain the board's quote. `237616` is the fuller release: 12 pages
against 11, and it carries a slide the other lacks — *"The Immediate Way Ahead: begin
publishing the 24 technical report deliverables"*. The board now cites the more complete
of the two, and this paragraph exists so nobody re-opens the question.

`170018` was never broken in the way the other 45 were. Its claim is Tier 2 and is
*about the listing*: "A DIA FOIA Electronic Reading Room item is titled 'Advanced
Aerospace Weapon System Applications Contract'". The index is what that URL renders, and
the index does carry that section — so the destination was right and only the
per-record `FileId` was misleading, implying a specific document that no longer exists
under that id. It now points at the reading room itself.

**All 46 are repaired. No DIA citation on the board is now dead.**

### The mistake the remap made, and how it was caught

Applying the remap as a string replace across `research/` rewrote 116 URLs it had no
business touching. A Wayback capture URL **contains** its target:

```
https://web.archive.org/web/20250309023844/https://www.dia.mil/.../FileId/170054/
```

Replacing `FileId/170054/` with `FileId/237615/` there does not update a citation. It
asserts that Wayback holds a capture, taken at that instant, of a page that did not
carry that id at that instant. That is a fabricated citation in the precise sense §2 of
CLAUDE.md forbids, and it was self-inflicted by the pass that existed to remove
fabricated citations.

It surfaced because the golden manifest moved by one URL and the number did not have an
obvious explanation. **Chasing an unexplained count of one is what found 116 bad URLs.**
The lesson is the general one, not the specific one: `--update-golden` is for counts you
can explain, and a drift you cannot explain is a finding, not a formality.

The repair used the **capture timestamp as the key** — whatever Wayback archived at that
instant is what the URL denotes, so the original inner path was restored from the
pre-remap file for each timestamp. All 116 now match the file as it stood before any of
this, verified by diffing timestamp-to-path against `git show`. The live URLs stay
remapped, which is correct: the document moved, and the capture is of where it used to
be.

Note for whoever runs the next bulk repoint: `web.archive.org` is unreachable from this
environment, so none of these captures can be verified from here either way. They were
on the board before this pass and are now exactly as they were.

After the remap **156 claims are unreachable, down from 281, and 362 verify, up from
278.** All 50 remaining `dia.mil` misses are OCR damage: every single one is a
*partial* match that breaks mid-word, none is a quote the document does not contain.

A note on what the DIA scans do to quotation checking. They are OCR'd photocopies and
they mangle exactly the things a quote turns on: Reid's letter reads "tar-term" where
he wrote "far-term", the INFO MEMO's date comes out "NOV I 3 2009", and "FY 2010"
becomes "FY 20 I 0". Every one of those reported as a missing quote and every one was
the board transcribing correctly.

## Access, which changed under me during the run

**281 of 604 claims could not be checked at all**, and that is a fact about this
network vantage rather than about the board. It also moved twice in one night:

| host | earlier session recorded | tonight |
|---|---|---|
| `cbc.ca` | 403 | **200** |
| `today.wayne.edu` | blocked | **200** |
| `compassrosepllc.com` | 403 | **200** |
| `thehill.com`, `newsnationnow.com` | 403 | **429** — this crawl rate-limiting itself |
| `web.archive.org` | unreachable | unreachable |
| `dia.mil`, `aaro.mil`, `esd.whs.mil`, `gao.gov`, `vault.fbi.gov` | 403 to curl | 403 to curl |

**A host recorded as blocked should be re-tested, not trusted.** Two of tonight's
best results came from re-testing hosts an earlier pass had written off. And a 403
during a long crawl is often this session throttling itself, which is why the
fetch cache no longer treats a remembered failure as permanent (`--retry-errors`).

`dia.mil` and `aaro.mil` serve WebFetch but refuse curl, so 103 and 26 claims
respectively are checkable by hand and not by this script. That is the largest
single block of unverified quotation on the board and the obvious next pass.

## The link sweep, which asks a different question

`--links` does not check quotes. It checks whether a citation still reaches a document
at all, across **every** cited URL rather than only those attached to a quoting claim.
Link rot does not respect that distinction: the Arquivo Nacional citations died on a
staging path the board carried in eight places, and 46 DIA ids stopped resolving
without producing a single 404 between them.

The first version reused the quote checker's `fetch`, which downloads bodies and
extracts PDF text on a 90-second deadline. Over 1,324 URLs that is hours, nearly all
of it spent waiting on hosts that block this environment anyway. Link health is a
question about the status line, so it is now a parallel HEAD on a 20-second deadline
with a browser user agent, falling back to a ranged GET for the codes HEAD-hostile
servers actually emit — `cnes.fr` answers HEAD with 400 and GET with 200, which is why
400 sits in that list beside the usual refusals. Minutes, not hours.

**Three dead citations, all repaired.** The Black Vault renamed its Army/TTSA CRADA
item; the three edges that cited it now also carry the released instrument itself, 27
pages, *"CCDC Ground Vehicle Systems Center CRADA No. 19-15"*, naming Dr. Joseph Cannon
at Warren, Michigan — which matters because `jeffery-langhout -> l-detroit-arsenal`
says in its own note that "the signature block is the documentary anchor: an executed
federal instrument, not a press release", and until now it cited the press release.
Wikipedia moved `To_The_Stars_Inc`, 15 references repointed. And isaackoi.com's Blue
Book Special Report 14 page is gone and was redundant, since the edge citing it already
carried the released document.

One URL returned 500 on the sweep and 200 on a retry and was left alone. A transient
server error is not a dead citation, and repointing on one bad response would have been
the mistake.

**The board now has zero 4xx and zero 5xx citations.**

| what remains | count | whose problem |
|---|---|---|
| HTTP 403 | 254 | this environment — mostly `.mil` and `war.gov` |
| unreachable | 178 | `web.archive.org`, which does not answer here at all |
| HTTP 429 | 15 | this crawl; 13 of them are one host I hammered |
| HTTP 202 | 11 | `irp.fas.org` bot challenge |
| HTTP 406 / 405 / 503 | 4 | user-agent filtering and one blocked host |

## Running it

```
python3 tools/spot_check.py                 # every checkable claim
python3 tools/spot_check.py --sample 60     # a seeded random subset
python3 tools/spot_check.py --host govinfo.gov
python3 tools/spot_check.py --retry-errors  # ignore remembered 403s
```

It is **not** part of the build gate, deliberately. It depends on the network, and
a check that fails because a host is throttling is a check people learn to ignore
— which is exactly the failure `verify.py`'s docstring was written about.
