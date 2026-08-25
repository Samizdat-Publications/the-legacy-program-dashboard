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
