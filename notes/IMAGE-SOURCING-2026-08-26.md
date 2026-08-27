# Image sourcing: 9 of 39, and the gap is the finding

26 August 2026. Stewart present and asked for all 39 institutions, using non-`.gov` sources.

## The first thing that changed the risk

**There are no PERSON nodes on the L0 map.** All 110 are documents, institutions, programs,
legislation and events. The category the register warns hardest about — *"a private person
who gave testimony has not thereby licensed their likeness"* — never arose. This is a
seals-and-marks question, not a faces question.

## The specific restrictions, read

The register says to treat a seal as `ask` *"until the specific restriction has been read"*.
Read, from the US Code:

| statute | covers | prohibits |
|---|---|---|
| **50 U.S.C. § 3513** | CIA name, initials, seal | use "in connection with any merchandise, impersonation, solicitation, or commercial activity in a manner reasonably calculated to convey the impression that such use is approved, endorsed, or authorized" |
| **50 U.S.C. § 3613** | NSA | identical scope |
| **10 U.S.C. § 425** | DIA, NRO, NGA (and the former NIMA/DMA) | identical, plus "merchandise, retail product" |

All three are **narrow and identical in shape**: commercial or impersonating use conveying
endorsement. Non-commercial identification on a research board is outside all of them — and
this board is adversarial toward several of these agencies, which makes an endorsement
impression implausible on its face. Clearance is `clears`, citing the section, because the
restriction has now actually been read rather than assumed.

*(Correcting myself: I first cited § 3613 as the CIA provision. It is NSA's. The CIA's is
§ 3513.)*

## Why 9 and not 39

**Automated search produced garbage, and some of it was dangerous.** Querying Wikimedia for
a mark per institution returned, among 39 results:

| node | what came back |
|---|---|
| `dod` | Seal of **Central Command** |
| `afosi` | a photo of **"Special Agent Adam Deem"** — a named private individual |
| `eg-and-g` | **Googleplex HQ** |
| `cometa` | a photo of **Comet Lemmon**, the astronomical object |
| `ttsa` | **"Ikenna Stars Academy"** |
| `wayne-state-university` | **"Wayne and Margie Mixson"** — two named people |
| `us-house`, `senate-armed-services`, +3 | the **Great Seal of the United States** |

A search engine returning a plausible result is not verification. Several of these are
photographs of real, named private individuals — precisely what the register forbids — and
they arrived looking exactly as authoritative as the correct ones.

After filtering to marks whose title actually matches the institution: **21**. Then, after
pulling each file's real licence and **looking at all 21 on a contact sheet**, and then at
the survivors on a real chip:

| dropped | why |
|---|---|
| `dod-sapco`, `waived-sap-notification-group`, `oversight-congress`, `congressional-uap-caucus`, `house-oversight-committee` | would have worn a **parent body's mark**. DoD SAPCO is not DoD; the Waived SAP Notification Group is certainly not DoD. Giving them the DoD seal asserts an identity the record does not support. |
| `senate-armed-services`, `fab` | **CC BY-SA** — attribution *and* share-alike. A real condition, not a formality, on a board that is not itself CC BY-SA. |
| `battelle` | black on transparent — **invisible on a dark board**. |
| `lockheed-martin`, `geipan` | wide wordmarks, 250×38 and 250×54. The slot is an **11px square** and a mark is contain-fitted, never cropped, so each became a 2px sliver. Lockheed rendered as an **empty amber ring** — less than the class letter it replaced. |
| `aaro` | opaque **white background**, verified at the pixel: would draw a white box. |
| the rest | no free-licensed own-mark exists, or the node is an abstraction with no mark at all (`oversight-congress` is a concept, not a body). |

**Nine survive**, eight `clears` and one `ask` (RAND: public domain as a simple shape but
`RESTRICTIONS: trademarked`, and this board is adversarial toward it, so the doubt ships).

## What it looks like

Verified on a real chip at 1:1, not assumed: **circular seals do read at 11px.** DIA, DoD,
CIA, DOE and the House seal are each distinguishable as seals and from one another by colour.
That was better than I predicted — I had expected an undifferentiated dot and said so before
looking. What fails is aspect ratio, not size.

## Two build consequences

**The marks are inlined as `data:` URIs, not linked.** `the built page fetches nothing at
runtime` is a gate check — the reason the typeface was embedded earlier today — and a remote
mark would break it while making first paint depend on Wikimedia being up.

**Inlining happens at dashboard-build time, not in the layout model.** Doing it in
`build_l0_layout.mjs` put ~695KB of base64 into that file **twice** (`current` and `legacy`
both carry nodes), taking it from 490KB to 1836KB — straight through the ~1MB GitHub API read
cap it exists to respect. Its own guard refused the build. The description of the page stays
small; the page carries the bytes.

And one that nearly shipped silently: `merge_packed` had to be taught to copy the photo
fields onto `model["l0"]`. Without it the register populated cleanly, the layout model carried
all the records, and the page drew 110 class letters — **the register working and the board
not showing it**, which is the same shape as the denial verdicts stopping at the layout model
earlier today. Twice in one session, the same missing hop.
