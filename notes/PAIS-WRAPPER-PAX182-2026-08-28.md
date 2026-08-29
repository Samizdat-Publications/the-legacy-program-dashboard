# The second file wrapper, and the maintenance fee question answered

28 August 2026. Continues `notes/PAIS-PATENTS-2026-08-28.md` and
`notes/HANDOFF-2026-08-28-pais.md`. Read `CLAUDE.md` first.

**Do not trust any figure here.** Run `python3 tools/state_snapshot.py --gate`.

Two things happened. Stewart pulled the file wrapper for a second application by hand,
because verify.me was down and USPTO could not be reached the easy way. And the question
that was blocking the biggest finding on this node turned out to have a one-line answer in
the Code of Federal Regulations.

---

## 1. The maintenance fee question is closed, and the finding survives

`notes/HANDOFF-2026-08-28-pais.md` §4 recorded the expiry of US 10,144,532 with a caveat it
called load-bearing: nobody had checked whether a patent assigned to a federal agency owes
maintenance fees on the ordinary schedule at all. If it did not, the lapse was a category
error rather than a decision, and the whole finding fell over.

It does. **37 CFR 1.362**, read from the govinfo XML of the 2024 CFR:

> (a) Maintenance fees ... are required to be paid in all patents based on applications filed
> on or after December 12, 1980, **except as noted in paragraph (b) of this section**, to
> maintain a patent in force beyond 4, 8 and 12 years after the date of grant.
>
> (b) Maintenance fees are not required for **any plant patents or for any design patents**.

That is the complete list of exemptions. There is no provision for a federally owned or
federally assigned patent anywhere in the section. Both Pais grants are utility patents from
applications filed decades after 1980. Both owed the fee. Neither was paid.

Paragraph (g) also fixes the date properly, which matters for how the board states it:

> A patent which expires for the failure to pay the maintenance fee will expire at the end of
> the same date (anniversary date) the patent was granted in the 4th, 8th, or 12th year after
> grant.

So the legal expiry runs from the fourth anniversary of grant, and the date in USPTO's event
log is the date the Office posted it, roughly five weeks later. The board now carries both
and says which is which.

## 2. It is not one expired patent. It is both of them

This is the substantive new finding and it changes how §4 of the handoff should be pitched.

| | granted | recorded expired | reminder mailed |
|---|---|---|---|
| US 10,135,366 electromagnetic field generator | 20 Nov 2018 | 26 Dec 2022 | 11 Jul 2022 |
| US 10,144,532 inertial mass reduction craft | 4 Dec 2018 | 9 Jan 2023 | 25 Jul 2022 |

Five weeks apart, same failure, same docket, same office of counsel.

**This cuts against the sharper reading as much as for it.** The handoff offered, as Tier 3,
that the Navy wanted the examining authority's *finding* on the craft rather than the property
right. That reading gets weaker when the sibling patent, which never had a finding worth
having because it was allowed on ordinary prior-art grounds, lapsed the same way five weeks
earlier. An office that renews nothing across a family is showing a maintenance practice, and
a practice is as consistent with routine cost control on patents the Navy would never sue to
enforce as it is with a judgement about these inventions. Both readings are on the node, and
the Tier 3 claim now says so.

What survives without inference: the Navy paid to obtain both patents, fought a two-year
appeal for one of them, and then let both go.

## 3. The second wrapper is the control case, and that is what makes it worth having

Application **14/807,943**, Navy docket **PAX 182**, the electromagnetic field generator.
Filed 24 July 2015, nine months before the craft. Granted as US 10,135,366.

It is the same physics and the same inventor. Paragraph [0037] of the craft application
incorporates *this* application by reference as its preferred generator. So the two cases are
not merely comparable, they are two claims on one design, and the Office handled them in
opposite ways:

| | 14/807,943 the component | 15/141,270 the craft |
|---|---|---|
| examiner | Thomas M. Dougherty | Philip J. Bonzell |
| art unit | 2837 | 3644, then 3642 |
| rejections | one non-final | non-final, then final |
| enablement raised | **never** | twice, as impossible |
| declarations under 1.132 | none | one, filed twice |
| appeal | none | Notice of Appeal and Appeal Brief |
| reason for allowance | **"the prior art fails to show"** | not in the wrapper, see §5 |
| claims allowed | 1-12 | 1-4 |

The Notice of Allowability of 13 September 2018 gives its whole reasoning as novelty:

> The following is an examiner's statement of reasons for allowance: the prior art fails to
> show a high energy electromagnetic field generator, comprising: a shell, the shell having
> embedded polycrystalline ferroelectric ceramic material ...

No enablement objection was ever raised against the component. The only amendment in the
whole case was the examiner deleting one line of claim 11 to fix a typo. Meanwhile, and this
is the part worth keeping, **at the moment that notice was signed the craft application was
under appeal for being impossible.**

**Why the two went to different art units is not in either wrapper**, and it is now a recorded
gap, because it decides how much of the difference is a judgement about physics and how much
is an accident of classification.

## 4. What the examiner actually wrote, and the argument he refused

The prior session established that the Sheehy letter says close to the opposite of the popular
account. The examiner's side of that exchange is now transcribed too, at
`research/patents/wrapper/final-rejection-2018-03-30.txt`, and it closes the loop.

**The paper the examiner calls a declaration is the letter.** The Final Rejection answers
"the declaration by Dr. James Sheehy under 37 CFR 1.132 filed 1/23/2018" in three parts, and
the three map exactly onto paragraphs 1, 2-4 and 5 of the 15 December 2017 letter: lasers
evolving, Pais being funded and running experiments, and China investing. No separate January
2018 declaration exists anywhere in the wrapper.

**The China argument was refused in writing.** This is the argument the secondary accounts
credit with winning the patent:

> With respect to third argument that China is already investing significantly in this area,
> this has nothing to do with what is patentable. **If anyone else filed this Application they
> would receive the same rejection.**

**And the rejection went to the physics, not just to the paperwork:**

> There is no such thing as a "repulsive EM energy field". Electromagnetism can be repulsive
> in certain circumstances, but there is no blanket field that repels everything.

> Presenting math at a conference doesn't prove anything physical. It like saying that you can
> math out tachyons by playing with relativistic equations but that doesn't "prove" that they
> exist nor can they then be used to create a physical object that can be patented.

> ... it is impossible to generate the electric and magnetic field that would be required to
> create the so called claimed effect of inertial mass reduction.

Set beside the Advisory Action's "the math and physics are sound ... the claims are still not
enabled", the record now shows an examiner who read the theory carefully, conceded it as
theory, refused every argument put to him including the China one, asked for a demonstration,
and was then overruled by something that is not in the file.

## 5. What is still missing, and it is the same document as yesterday

`research/patents/wrapper/MISSING.md` was written by the previous session and this one
confirms it independently: **the allowance papers for 15/141,270 are not in the Drive folder.**
Searching the folder for the exact form phrase "Comments on Statement of Reasons for Allowance"
returns the PAX 182 notice and nothing else. The 15/141,270 documents stop at the Appeal Brief
of 20 August 2018.

So the single most informative unobtained document on this node is unchanged, and it is now
sharper than it was: we know the examiner refused every argument on the record, and we know
he was reversed within three months without a demonstration. **The Reasons for Allowance says
why.** For Patent Center, it is the papers dated after 20 August 2018 only.

## 6. A small documentary trap, recorded so nobody springs it later

The after-final remarks received 24 May 2018 describe the Sheehy declaration as "dated May 11,
2017" and are signed "Date: 5/24/2017". Both years are a year out. The declaration in the
wrapper is dated 11 May 2018 and was refiled unchanged with the Appeal Brief in August. There
is no 2017 declaration in the file. This is on the node so that a future pass does not read
the typo as evidence of an earlier, separate declaration and go looking for it.

The application also changed art unit mid-prosecution, 3644 to 3642, without changing examiner
or supervisor. Worth knowing before anyone treats the two unit numbers as two cases.

## 7. Gate

All ten steps green, including `--idempotent`, which is the one the previous session flagged
as not having run. Golden re-baselined once, deliberately: T1 claims +18, T3 +1, timeline +3,
unique source URLs +1. Every movement is accounted for by what was authored here, and the T2
count did not move. `l0_nodes` stayed at 110, so nothing in this touched the map or the shell.
