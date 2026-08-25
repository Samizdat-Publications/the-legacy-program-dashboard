# The denial arrowheads were pointing at whatever sorted second

**26 August 2026.** Found while answering a question about Claude Design's motion layer.
The particle layer may only carry attested direction, so the first thing to check was
whether the board knows which end of a denial issued it. It does not, and it has been
drawing an arrowhead saying it does.

---

## 1. What was on screen

Every direct denial edge on the program map drew an arrowhead at its `b` end, read by a
reader as **a denied b**. 47 edges on the map, 174 on the board.

`b` came from `tools/build_l0_layout.mjs`:

```js
const k = [e.a, e.b].sort().join('|');   // pair key
...
const [a, b] = k.split('|');             // and then straight onto the aggregate edge
```

**Alphabetical order, rendered as a claim about who denied whom.** Checked against the
board's own raw records, **22 of 47 pointed the wrong way**. Among them:

| the map drew | the record says |
|---|---|
| AARO denied PURSUE releases | PURSUE releases denied AARO |
| House Oversight Committee denied MITRE | MITRE denied House Oversight |
| DoD denied Immaculate Constellation | Immaculate Constellation is the subject, DoD the denier |
| AARO denied its own historical record vol 2 | vol 2 is the vehicle, AARO the subject |

## 2. And the record itself does not carry the convention

`tools/build_l0.py` said so in a comment, and this is the part worth reading twice:

> *Denial direction. Convention CONFIRMED against the merged board: `a` issued it, `b` is
> the subject. Sample: susan-gough -> luis-elizondo, "no assigned responsibilities for
> AATIP".*

**Confirmed against one sample that agreed with it.** That is CLAUDE.md §5 exactly: a check
never shown the input it must reject.

Thirty denial edges adjudicated against their own `label` text:

| | n |
|---|---|
| `a` issued it, convention holds | 12 |
| `b` issued it, convention inverted | 7 |
| not a directed denial act at all | 11 |

The seven inverted include `immaculate-constellation -> dod` ("DoD spokesperson Sue Gough:
no record of any SAP by that name"), `nj-drone-incursions-2024 -> dod` ("Four-agency joint
statement"), `shootdowns-feb-2023 -> sean-kirkpatrick` ("Retrospective 'they were balloons'
characterisation"), and `aztec-1948 -> dod` ("Air Force denials of Hangar 18 bodies").

The eleven that are not directed acts matter just as much. `type: "denial"` is being used
for membership of the denial *theme*, not for a directed denial: `roswell -> official-denial`
("Four official explanations for one event"), `capco -> isoo` ("ISOO requests are routed
through CAPCO"), `sean-kirkpatrick -> kirkpatrick-article` (a person and their own byline),
`varginha -> roswell-report` ("Two official inquiries that explained the recovery activity").
None of those has an issuer and a subject to point between.

**So the arrowhead was not merely scrambled by the sort. Even unscrambled, it would have
been asserting a direction on about a third of edges that have none.**

## 3. The blast radius was wider than the arrowhead

The same `issued`/`received` counters feed four more surfaces:

| surface | what it said |
|---|---|
| member ledger | `denials 3 issued · 8 received` |
| chip tooltip | the same split |
| `mark_authority` -> `publicRecord` | `denialsIssued`, `denialsReceived` |
| scripted analyst | "N denial(s) issued. This office could answer from position alone" |

AARO's ledger read **3 issued, 8 received**. That number was derived from alphabetical
order, and it is the kind of figure a reader would quote.

## 4. What was done

Direction is now published **only where an edge names its denier**, and nothing does yet.

- `denier` is plumbed end to end: raw board -> `build_design_extract.py` (`denialPairs`
  gains the field) -> `build_l0_layout.mjs` -> the model's edges.
- **`denialPairs` was already being emitted and never joined.** The generator recorded only
  `figures.denialDir`, a boolean saying the array was non-empty, so `dn` came out empty on
  all 47 edges and the renderer fell back to the sorted `a`/`b`. It now joins, and all 47
  carry their raw unsorted pairs.
- The arrowhead draws only when `denier` is set, and points at the **other** end. Zero draw
  today.
- `di`/`dr` count only attested edges; `dnu` counts the rest. Every surface degrades to
  **"11 denial links · direction not attested"**.
- An aggregate takes a `denier` only when every underlying record agrees on one.
  Disagreement means unattested, never majority rule.

Nothing was invented and nothing was guessed. The board stopped saying the thing it could
not support.

## 5. The check that was missing

`motion is attested, not decorative` is one of Design's nine and it **passed for the whole
of the first build**, because it guards the *flags*: that a denial is marked as one, and
that no second motion flag exists. It never looked at the direction, which is the claim the
arrowhead actually makes.

New, 39th check: **`denial direction is published only where the record names a denier`**.
A published `denier` must be one of the edge's own ends and must be named by at least one
of the underlying records it rolls up. Its poison writes `denier: "not-an-end-of-this-edge"`
onto every denial edge, which is what publishing a sorted `a`/`b` amounts to.

## 6. What is left, and it is research, not code

**Author `denier` on the 174 raw denial edges**, and split the type while doing it: an edge
that is a directed denial gets a denier; an edge that merely belongs to the denial theme
should not be typed `denial` at all, or should be typed something that does not imply an
issuer. Roughly a third of them are in the second group.

The `label` text usually names the denier, which makes this tractable, but it must not be
automated from the label alone. That is the same move as "confirmed against one sample":
a rule that agrees with the thing it was derived from. Each one wants reading.

Until then the instrument is off, and the board says so on its face.
