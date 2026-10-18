# Redactions before the repository goes public (17 October 2026)

Stewart approved making `Samizdat-Publications/the-legacy-program-dashboard` public. Before that, the
current files were swept for private contact details of real people, credentials, and anything from
his day job. This note records what was changed and why, so a later session does not "restore" it.

## What was removed

**Personal email addresses** that the board had copied out of the WikiLeaks Podesta release and out of
recorded headers. Each is replaced by a bracketed description of whose address it is, so every
sentence still says what the record shows. The addresses themselves stay on the cited WikiLeaks
pages; the board cites them and does not need to republish them.

| Was | Now reads |
|---|---|
| Podesta's Gmail address | `[Podesta's personal Gmail address]` |
| DeLonge's personal address | `[DeLonge's personal address]` |
| The "Neil McC" Gmail address, two other Gmail correspondents | `[a personal Gmail address]` |
| Leslie Kean's Gmail address | `[Kean's personal Gmail address]` |
| Bob Fish's EarthLink address | `[a personal EarthLink address]` |
| A Clinton campaign staff address | `[a Clinton campaign staff address]` |
| Rob Weiss's Lockheed Martin address | `[Weiss's Lockheed Martin address]` |
| Podesta's Georgetown Law address | `[Podesta's Georgetown Law address]` |

One inference is weaker for it: the "Neil McC" thread's address contained a string that reads as a
name. The claims still carry the signature "Neil McC", the calendar invitation and the cited page.

**Private street addresses**: the house number and street of the place of death in the McCandlish
Verdict of Death (now "a street address in Redding, Shasta County, CA"); inventor home addresses
printed on old patents (Puharich, Lawrence, King); Stringfield's self-publishing address; and the
street address of the Warp Drive Metrics letterhead. Town and state stay. Quoted text marks the cut
as `[street address omitted]`.

**Kept on purpose**: institutional and official addresses (agencies, universities, MITRE, a sheriff's
office, NARA), office or role mailboxes, addresses a person or group publishes as a public contact
(the UAP-GERB intake address, the Flux Liner site footer, the Jesse Michels show-note business
addresses), work addresses printed in public government records (Navy patent filings), and message
ids, which identify an email and reach nobody. The NIDS reporting line and the DIA contracting
office number are public institutional numbers. Every other ten-digit match was a DOI fragment.

## Ids

A claim's id hashes its text (`tools/merge.py`, `claim_id`), so nine claims got new ids. The old ids
were replaced by the new ones everywhere they were referenced (`research/_claim_sources.json`,
`research/_claim_meta.json`, topics, questions). Counts did not move: 1138 nodes, 2788 edges, 6060
claims (T1 3786, T2 1694, T3 580).

## Also changed

- Two mentions of Stewart's employer by name (`CLAUDE.md`, `notes/HISTORY-TO-2026-09-24.md`) now say
  "day-job work". The employer's name must never be public.
- `exports/notebooklm/` was redacted in place, not regenerated: regenerating it would also pull in
  every board change since 25 September, which is a separate decision.

## Not fixed: history

Every one of the above is still in earlier commits. The coordinator decides whether the history is
rewritten before the flip; a per-repo session never rewrites it.
