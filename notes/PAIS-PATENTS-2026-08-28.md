# Salvatore Pais, five Navy filings, and the document that is better than the patents

**28 August 2026.** Stewart: *"This board absolutely needs to have him, his connections, and
his patents on file."* Built. This note is the record of what was opened, what was verified,
and the two things that were deliberately not done.

The standing instruction it was built to, in Stewart's words: *"I want to not just have this
be a conspiracy brain item but something I can put in front of respectable individuals and
not have them immediately dismiss it."* Every decision below follows from that sentence.

---

## 1. Two corrections to the brief, made before building

**It was not the Secretary of the Navy who intervened with the patent office.** Reporting
names **Dr James Sheehy, chief technology officer of the Naval Aviation Enterprise**. The
distinction is not pedantry: a reader who knows the case and sees "SecNav" discounts
everything around it, which is exactly the failure mode the board exists to avoid.

**The count is five filings, not three or four**, across 2015 to 2018. Three granted, two
published as applications. All five assigned to the United States as represented by the
Secretary of the Navy.

---

## 2. What is now on the board

Seven new nodes, one new research domain, `research/pais-patents.json`.

| id | what |
|---|---|
| `salvatore-pais` | person, Tier B |
| `pax-205-disclosure` | the NAVAIR invention-disclosure briefing, released under FOIA |
| `pais-patent-imrd` | US 10,144,532, craft using an inertial mass reduction device |
| `pais-patent-emfg` | US 10,135,366, electromagnetic field generator |
| `pais-patent-hfgw` | US 10,322,827, high frequency gravitational wave generator |
| `pais-app-superconductor` | US 2019/0058105, piezoelectricity-induced room temperature superconductor |
| `pais-app-fusion` | US 2019/0295733, plasma compression fusion device |

Ten edges, four timeline events, twenty-one claims: ten Tier 1, nine Tier 2, two Tier 3.

Every application number, filing date and publication date was read off a patent record, not
recalled. Google Patents returned 503 throughout; the working channel was FreePatentsOnline's
mirror of the USPTO full-text record.

| patent | application | filed | published |
|---|---|---|---|
| US 10,135,366 | 14/807943 | 2015-07-24 | 2018-11-20 |
| US 10,144,532 | 15/141270 | 2016-04-28 | 2018-12-04 |
| US 10,322,827 | 15/431823 | 2017-02-14 | 2019-06-18 |
| US 2019/0058105 | 15/678672 | 2017-08-16 | 2019-02-21 |
| US 2019/0295733 | 15/928703 | 2018-03-22 | 2019-09-26 |

## 3. The find: the Navy's own briefing beats the patents

`https://www.navair.navy.mil/foia/.../2021-003244 ... PAX 205 - INERTIAL MASS REDUCTION
DEVICE.pdf` is a six-page NAWCAD invention-disclosure briefing written by Pais and released
under FOIA. It is a **.gov primary source** and it is more useful than any of the patents,
because it was written for a Navy audience deciding whether to fund the work rather than for
an examiner deciding whether to grant it. Page one carries his name, his NAWCAD competency
code 4.4.5.1, his `navy.mil` address and his desk phone.

**The capability description is the reason this node matters.** Slide 5, verbatim:

> It makes possible the design of a hybrid aerospace / undersea craft (HAUC), which due to
> the physical mechanisms enabled with the Inertial Mass Reduction Device (IMRD), can
> function as a submersible craft capable of extreme aerial and underwater speeds (lack of
> air/water-skin friction) and enhanced stealth capabilities (non-linear scattering of RF and
> sonar signals). This hybrid craft would move with great ease through the air / space / water
> mediums, by being enclosed in a Vacuum plasma bubble/sheath

Transmedium travel, extreme speed without skin friction, and low observability, itemised as
design goals in a United States Navy invention disclosure. That is a documentary fact and it
does not depend on anyone's view of the physics. It is also the single most quotable thing in
the cluster for a sceptical reader, because the source is a Navy FOIA release rather than a
podcast.

The same slide says the IMRD can serve as an artificial gravitational wave generator
"(invention enables Gertsenshtein Effect)", with "tremendous air and space military
implications and applications (both offensive and defensive in nature)" and "Local spacetime
modification on a grand scale (planetary-size disruption) is thus feasible." That sentence is
why `pais-patent-imrd` and `pais-patent-hfgw` are wired together on the board: the link is
the author's own, not an inference.

## 4. The counterweight, which is in the same document

This is the part that makes the node usable in front of a hostile reader, and it comes from
Pais himself rather than from a critic. The briefing states, **twice**:

> this is a theoretical concept - no prototype in existence, as yet

It gives the invention original date as 6 March 2015 and proposes Section 219 NISE funding of
**250,000 USD in labour plus 250,000 USD in NAWCAD facility cost** to investigate the concept
experimentally, under a slide header reading "EXPERIMENT TRUMPS THEORY EVERYTIME!".

On its face the document is a request for money to test an idea.

And the test appears to have been run and failed. Reporting based on FOIA-released NAWCAD
records says the Navy spent roughly 500,000 dollars between 2016 and 2019 and concluded the
effect could not be demonstrated, with no further research. **That figure is the sum of the
two lines Pais proposed**, which is a real corroboration between two independent documents
and is worth noting as such.

**Both facts are on the node.** Omitting them would not have made the case stronger. It would
have made it dismissible by the first reader who knows the file, which is precisely the
audience this board is being built for.

## 5. What survives the negative result

The physics claim is not what is interesting after a failed test. The **institutional
behaviour** is, and it is untouched by whether the effect is real:

An examiner's job is to reject a claim that is not enabled. The record as reported is that one
was rejected on exactly that ground, and then granted after a service chief technology officer
wrote to the USPTO asserting operability and invoking Chinese development of the same
capability. Agencies do not usually spend senior technical credibility forcing through a
patent they believe describes nothing.

Two readings are live and the board records both without choosing: the Navy believed the
physics, or the Navy wanted the priority date on the public record for reasons it has not
stated. That is Tier 3, marked as stated inference, with the reasoning written out.

## 6. What was deliberately NOT done

**No link to AATIP, AAWSAP, KONA BLUE, any DIRD, or any material-custody chain.** Nothing in
the released record connects Pais to any of them, and the temptation to draw that edge is
exactly the thing that would get this board dismissed. The absence is recorded on the node as
a positive statement rather than left as a silence, and `d-custody` was deliberately left off
his domain list. If a document later connects him, the edge gets drawn then.

**No patents tab.** Stewart asked for one and it is the right idea, but CLAUDE.md section 9 is
explicit that the last three layout changes built directly were all wrong on the first cut,
and that a shell change needs a mockup screenshotted at 1366 / 1920 / 2560 and shown to him
first. Research first, mockup next, build after he has looked. Section 8 has the shape.

## 6a. Two gate checks that were quietly wrong, found by adding one person

Adding `salvatore-pais` was the first new person node since `runtime_check.js` was written,
and it exposed two defects in the check file itself. Both are the CLAUDE.md section 5 shape
and both are now fixed.

**`case view shows every record` hardcoded `278 of 278`.** Eight lines above it, in the same
file, is a comment explaining that the stats-strip checks read their expected values from
`tools/GOLDEN.json` precisely because *"the first version of this file hardcoded them and went
stale the moment two claims were added, which made the check fail on a correct build -- a
check that cries wolf gets switched off, and then it is no check."* The lesson was written
down and then not applied to the line directly beneath it. It now reads golden, and asserts
shown === total === golden, which is strictly stronger than the literal: it still catches a
dropped record and it additionally catches the two printed numbers disagreeing with each
other.

**`the full graph asserts no time direction at rest` was intermittently failing.** Not a
flake to be re-run away: `settle()` returned true on the **first** pair of matching frame
hashes, and a force layout still converging can produce two identical frames and then carry on
moving, which the following `holdsStill()` then reported as "settled and then started moving
again". Seven new nodes made it fail roughly one run in two. Quiet must now be established
over three consecutive matches rather than glimpsed once.

That change does not weaken it, and the weakening question was tested rather than argued: with
the quiet threshold set unreachable the check fails with *"never settled within 18s, which is
what a flow on every line looks like"*, and restored it passes. A genuine time-direction flow
never produces any run of identical frames, so it still fails on the settle timeout. The
timeout in that message now derives from the actual budget instead of being a second hardcoded
number waiting to go stale.

## 7. The gaps, which are the next session's work

1. **The Sheehy correspondence has not been obtained.** It is the most load-bearing document
   in the cluster and everything about the intervention is currently Tier 2 on secondary
   reporting. It should be in the file wrapper for application 15/141270, retrievable from
   USPTO Patent Center. **No API key needed.** This is the highest-value single retrieval
   available on this node.
2. **The NAWCAD test records have not been obtained.** Same problem, opposite sign: the
   strongest disconfirming fact rests on secondary reporting. It should be a NAVAIR FOIA
   release like PAX 205 was.
3. **Only bibliographic records and abstracts were read, not the claim sets.** What the
   examiner actually allowed in US 10,144,532 is a different question from what the abstract
   describes, and it is the question a patent attorney would ask first.
4. **No primary personnel record** establishes Pais's current office or title.
5. **The other four filings have no PAX-205-equivalent disclosure on the board.** If NAVAIR
   released one invention-disclosure briefing under FOIA, the other four plausibly exist.

## 8. The two things Stewart asked for that are downstream of this

**A patents tab.** The data now exists to drive it: five filings with dates, application
numbers, assignee and a capability description, plus one disclosure document that ties them
together. The natural shape is a small timeline of filing-to-grant with the capability claims
called out, not another network view. Needs a mockup first.

**The craft-shape reference layer with the five observables.** Two things to flag before that
gets built, neither of them a refusal:

- **The board has no five-observables node and the phrase appears nowhere in `research/`.**
  That has to be built and sourced properly first, because the observables are the frame the
  rest would hang on.
- **Generated renders are a section 2 problem and need a rule before they are a feature.**
  This board's whole value is that nothing on it is invented. An AI-rendered craft image sitting
  beside sourced material will be read as evidence no matter what the caption says. If it is
  built: never in `data/l0-images.json`, which asserts provenance and licensing; a separate
  register with a different visual treatment; and every render labelled as an illustration of a
  described shape, citing the description it renders. Worth doing properly, not worth doing
  casually.
