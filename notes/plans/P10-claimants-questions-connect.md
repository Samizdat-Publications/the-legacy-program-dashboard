# Phase 10, detailed: claims that know who said them; Questions; Connect

Written 26 September 2026 from `notes/PLAN-2026-09-24.md` section "Phase 10" and every critic round since
round 0, which flagged sworn testimony shown at T1 against Home's short tier definitions. Branch
`redesign/p10-claimants`. Opus 5.5, high. Subagent concurrency: at most 2 at a time (larger fan-outs
stalled the connection twice on 26 September).

## Decisions made here

- **The tier contradiction is fixed in words, never by moving a tier.** The board's rule is that a claim
  ABOUT what someone said is documented when the record of the saying is (CLAUDE.md section 2). The "How
  to read a claim" key (phase 6, on Home, the evidence explorer and the report) says so plainly: "Tier 1
  means the record is documented. For a statement marked 'said on the record', what is documented is
  that it was said, not that it is true." Home's own paragraph is Stewart's wording and is not edited.
- Bookkeeping rows already left the claims in phase 7 (P5c); the plan's item on them is done.

## Tasks

1. **`research/_claim_meta.json`** per claim id: `claimant` (a person id, or an institution id for an
   office's statement), `artefactDate` (when the claim was made), `eventDate` (when the thing claimed
   happened), `route` (hearing, broadcast, book, interview, filing, press, document). The "On <show>,
   <date>, <speaker> said" pattern and P5b's attribution rule parse mechanically; Sonnet batches propose the
   rest for Tier 2 and the "said on the record" Tier 1 claims; Opus verifies a 10% sample and every
   claimant with 20 or more claims. Checks with poisons: claimants are nodes; dates are well formed; a
   claim marked "said on the record" has a claimant.
2. **"Claims this person has made"** on every person page (and "Statements by this office" on
   institutions), grouped by topic, each with its artefact date and route, and the provenance the
   notability rule requires where the record carries it (who brought the claim to the record, and when).
3. **Questions:** `research/questions/<id>.json`, authored like topics (lead, answer so far, for,
   against, open, the threads folded in as evidence chains), checked like topics (every sentence cites;
   quotes verbatim; the case against present). 8 to 12 questions from the redesign's section 5 list,
   drafted by one Opus drafter and verified by one Opus verifier working from the cites. `#/questions` and
   `#/q/<id>`; Home's "big questions" block links them.
4. **Connect:** `#/connect/<a>/<b>` finds up to 3 distinct paths by a weighted search preferring Tier 1
   edges, backbone families and specific nodes over connector hubs (a penalty of log degree); every hop
   shows its sentence, tier, predicate phrase and source; a route only through a connector hub says so;
   the old `/path/a/b` links redirect here. Check with a poison: AARO's historical record is not the answer
   for the 8 test pairs in Appendix B section 7 unless it is the only route, and then the page says so.
5. **The blind critic loop** (`notes/critic/p10-round-N.md`), routes including a person page, a question
   and a connect page.
