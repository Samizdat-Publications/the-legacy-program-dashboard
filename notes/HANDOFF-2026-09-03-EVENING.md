# Handoff, 3 September 2026, evening (the current one)

Written at the end of the session that ran the Danny Jones chain end to end and found
why CI had been red all day. `git fetch --all` before reading further; everything below
is on `master` and pushed. The morning handoff, `notes/HANDOFF-2026-09-03.md`, is still
accurate on the two boards side by side (its section 2), the new shell's checks and the
deploy recipe; its section 3 ordering is superseded by section 3 below.

## 1. What the session did, in one table

| | |
|---|---|
| the board | 1,027 -> 1,057 nodes (311 people, 746 entities), 5,120 -> 5,303 claims, 2,348 -> 2,460 edges, 912 -> 913 timeline events, L0 125 -> 137, all 137 with dossiers |
| Danny Jones | DONE end to end. Batches 22 to 35 mapped by 14 Sonnet agents (all 136 episodes now mapped); 981 confident names cross-checked (558 absent, 164 prose, 259 nodes); six Opus triage groups; 36 candidates opened by six Opus verifiers; decision list `research/leads/CANDIDATES-2026-09-03-DANNYJONES.md`; build `research/dannyjones-2026-09-03.json` (11 people, 19 entities, 112 edges, 1 timeline event, 29 gaps); 18 corrections in `research/_corrections.json`; 12 new L0 dossiers in `research/dossiers/dannyjones-2026-09-03-l0.json`; 7 chip labels in `data/l0-shorts.json` |
| the finding that matters most | The board's nitinol lineage (Battelle 1948-49 reports, per Bragalia) is unsupported by the federal literature Battelle itself wrote: NASA SP-5110 (1972) credits Buehler and Wiley at the Naval Ordnance Laboratory, the earliest NOL report is NOLTR 61-75 (1961), the patent was filed 1 December 1961, Battelle appears only as a 1968 subcontractor. The four nodes carrying the lineage now carry the record claim beside the allegation |
| other records opened | MKULTRA (the 1977 hearing print, the 1963 IG survey), BLUEBIRD's 5 April 1950 proposal to Hillenkoetter, Frank Olson (Rockefeller Commission, Private Law 94-126, D.D.C. 12-cv-01924), Project AZORIAN (the CIA's own 2010 history), the 341st SMW history that says the Echo Flight UFO rumours "were disproven", Operation Northwoods (JCS 1969/321 with Lemnitzer's signature block), Talbert's November 1955 Herald Tribune series (no Townsend Brown in it), the 1957 Chapel Hill conference front matter (IUPAP sponsored, WADC one of four funders), ARPA's founding directive (Roy W. Johnson first Director, not York), GAO/NSIAD-88-152 (Army SAP office September 1984) |
| the tools | `tools/corpus_absent_groups.py` (new, self-tested): merges per-batch candidate lists and splits ABSENT verdicts into triage groups. `corpus_crosscheck.py` gained six self-tested rules from the eleven false ABSENTs the triage agents caught (Labs abbreviation, USAF and AFB expansion, id variant, single-token word boundaries, hyphen-flexible prose needles, middle-name person needles, string-list fields); one false NODE (`United Nuclear` marrying `d-nuclear`) was caught on the way and poisoned |
| the two checks | `test_packed_layout.js` `thin-bands-print-amber` required a band under five nodes to exist; disclosure went 3 -> 6 so none does. It now passes on data with no thin band, says so in its detail, and its poison conjures one. `runtime_check.js` dpr-2 ink check scored 14 of 24 with zero boxes showing the bug and 10 with no ink at either position; it now samples 48 boxes, scores only inked ones, and its poison still inverts (25 the reverse) |
| CI | RED SINCE 01:45 ON 3 SEPTEMBER, on every commit. Cause found and fixed: see section 4. GREEN at `cdc99da` (gate and deploy both success, 21:45 UTC). The old shell had not deployed since the last Linux-built push until then |
| deploys | Review site redeployed twice from `git archive master app`, last at `cdc99da`. Old shell: deployed by CI at `cdc99da`, serving the 1,057-node board |
| housekeeping | `spot_check.py --links` run for the first time since 30 August: 1,651 URLs, ten dead (section 5) |

## 2. The two boards, side by side

Unchanged from the morning handoff's section 2 except: both consume the 1,057-node board
now; the new shell's `npm run check` (41) and `check:poison` (16) passed on it; the old
shell's gate is green at `cdc99da` with two checks amended as above.

One operational note for the new shell's checks on this machine: `npm run preview` binds
IPv6 only and the harness's `fetch` never reaches it. Start the preview as
`npx vite preview --host 127.0.0.1 --port 4173 --strictPort` in a persistent background
task, then `npm run check` and `npm run check:poison` work on their default APP_URL.

## 3. What is next, in order

1. **Stewart reviews the new shell** at https://the-program-next.pages.dev. It now carries
   the Danny Jones build. Nothing cuts over until he says yes. He was told on the evening of
   3 September that it is in a reviewable state, with the two known departures from
   Design's captures (Map without zoom at 1:1; Neighbourhood hop 2 at 136 nodes) and the
   post-cutover polish list.
2. **Cutover** once approved: the morning handoff's section 3 item 3, unchanged.
3. **The ten dead citations** (section 5): nine cufon.org pages and one Federal Register
   URL. An Opus agent with the spot-check brief: find each document at a live host (the
   Federal Register one is the same URL without its trailing slash; cufon.org is gone as a
   site and Wayback answers from this machine), open it, repoint the source, re-run
   `spot_check.py` on the affected claims.
4. **A Danny Jones section C pass**, the shape of the Michels one: the triage files'
   section C rows that no verifier opened are podcast claims about existing nodes, listed
   in the decision list's section D with the strongest named. Six Opus verifiers, Tier 2
   claims in the form "On the Danny Jones Podcast, <date>, <speaker> said".
5. **Polish after cutover** and the rest of **housekeeping**: as the morning handoff, plus
   audit finding 14 and the held candidates from all four decision lists (NURO is now NOT
   OPENED in three corpora; Jolly West's subproject file is open but his name is excised).

## 4. Things a next session must not undo

- **The L0 layout in `build_l0.py` uses `_sin`, `_cos` and `sqrt` of a sum, not
  `math.cos`, `math.sin` or `math.hypot`.** The layout is a chaotic relaxation; libm's
  transcendentals differ by an ulp between MSVC and glibc, and that one ulp became a
  different map (wall-clamp 1.5% on Windows, 3.6% on Linux, extents 1791x1065 against
  1711x1014). Every commit built on this Windows machine since 01:45 on 3 September failed
  the CI reproducibility step for that reason, and the failure showed only as "+4 bytes at
  byte 665". The series is accurate to 3e-15 and bit-identical everywhere. Do not put a
  libm call back into anything that feeds a layout.
- **`build_l0.py` writes its source path with forward slashes.** `os.path.relpath` wrote
  `data\\the-program.json` on Windows; that was the other byte.
- **`gate.yml` uploads the rebuilt artifacts when `check_rebuild.py` fails**
  (`rebuilt-artifacts`, seven days). `gh run download <id> -n rebuilt-artifacts` and diff;
  that is how the layout difference was found, and there is no other way from a Windows
  session.
- The corrections the records forced this week, from both handoffs: `sapoc` 5 January 1994;
  ATIC 1959 and 1 July 1961; CENTER LANE's office; Bluegill; Inman and SAIC; the Church
  Committee; the Oversight letters; and now the nitinol lineage, `wilson-davis-memo` typed
  not handwritten with two pages being Miller's letter, ARPA's first Director Roy W.
  Johnson, Cabell at USAF Intelligence not CIA when Blue Book launched, the Army SAP office
  of September 1984, GRILL FLAME to INSCOM 11 February 1981, and DRAGOON ABSORB.
- The decision list's section E: no Lemnitzer, York, Goldberger, Garwin, Jafari, Snowbird,
  Norton or Lovekin nodes, each for a reason; and the `sperry-rand` edge to the Talbert
  series is justified by that document and does not create a MacArthur edge.
- Denial direction is the adjudicated `denier` field. Transcripts are never committed or
  deployed. No em dashes for Stewart; every command block starts with its own quoted `cd`;
  tables over lists; he cannot read JSON.

## 5. The dead citations, 3 September sweep

| URL | Cited by |
|---|---|
| http://www.cufon.org/cufon/afr200-2.htm | `afr-200-2` and two edges |
| http://www.cufon.org/cufon/cashlanC.pdf | `cash-v-united-states` |
| http://www.cufon.org/cufon/cia-52-1.htm | `h-marshall-chadwell`, `washington-flap-1952` and an edge |
| http://www.cufon.org/cufon/janp146c.htm | `carroll-bolender`, `janap-146` and an edge |
| http://www.cufon.org/cufon/robert.htm | `afr-200-2`, `cia` and an edge |
| https://www.cufon.org/cufon/janp1462.htm | `janap-146` |
| https://www.cufon.org/cufon/pentacle.htm | `howard-c-cross` and two edges |
| https://www.cufon.org/cufon/stork1-7.htm | `gerb-battelle-investigation`, `project-stork` and an edge |
| https://www.cufon.org/cufon/stork1-7c.htm | `project-stork` |
| https://www.federalregister.gov/documents/1994/06/01/94-13279/ | `naval-criminal-investigative-service`; the same URL without the trailing slash answers 200 |

Everything else non-200 in the sweep is a host refusing this caller, as the tool says.

## 6. Working state

- `npx http-server dist -p 8899 --silent` and the IPv4 vite preview on 4173 were running as
  background tasks of this session and die with it.
- `/c/w/next` is a scratch export used for deploys; safe to delete.
- Stewart's usage window reset at 2pm and again at 4:20pm on 3 September; the fan-outs
  (14 Sonnet mappers, 6 Opus triage, 6 Opus verifiers, 1 Opus builder) ran between them.
