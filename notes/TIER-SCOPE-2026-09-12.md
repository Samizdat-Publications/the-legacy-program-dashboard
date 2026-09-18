# The demotion rule is scoped to the node, not to the claim, 12 September 2026

Found by the analyst, on its third live question, unprompted. Written up here
because it is a research decision and research decisions are Stewart's.

## 1. What it said

Asked "what are this node's Tier 1 claims, and which one is weakest?" on
`battelle`, it named claim 3, the H. C. Cross memorandum of 9 January 1953, and
gave this reason:

> The identical assertions sit on `pentacle-memorandum`, and there they have been
> demoted to Tier 2 with the explicit note "DEMOTED from Tier 1 (node carries no
> primary-record URL); needs primary replacement". On `battelle` the same fact is
> still graded T1.

## 2. It is right, and this is why

| | |
|---|---|
| `battelle` | T1. Source: "CUFON transcription; Jacques Vallee, Forbidden Science" |
| `pentacle-memorandum` | T2. Source: the same, plus "DEMOTED from Tier 1 (node carries no primary-record URL); needs primary replacement" |

Both come from one record, `research/ffrdcs.json`, where all three instances of
this assertion are authored at tier 1: `.people[7]` is `howard-c-cross`,
`.entities[10]` is `battelle`, `.entities[13]` is `pentacle-memorandum`. Two of
the three survive at Tier 1 on the board and the third does not.

The split happens in `remediate_tiers` in `tools/merge.py`. Read the first two
lines of its body:

```python
urls = " ".join(s.get("url", "") for s in n.get("sources", []))
has_primary = bool(PRIMARY_URL_PAT.search(urls))
```

`has_primary` is a property of the **node**, not of the claim. `battelle` carries
primary URLs for other things entirely: its PNNL contract on USAspending, NASA
SP-5110 on NTRS. `pentacle-memorandum` carries none. So the same claim, with the
same sources, is demoted on the node that has no primary record anywhere and
survives at Tier 1 on the node that has one for something else.

## 3. How big the class is, exactly

`tools/DEMOTIONS.json` records why every demotion happened, so this needs no
estimating. 235 claims were demoted in all:

| ground | claims | claim-scoped? |
|---|---|---|
| cited to a secondary or encyclopedic source | 94 | yes, it reads the claim's own source |
| **node carries no primary-record URL** | **90** | **no. This is the one** |
| sourced to an interested party asserting an external fact | 50 | yes, and it is CLAUDE.md section 2's AARO rule working |
| no attributed source | 1 | yes |

Of the 90 demoted by the node-scoped ground, the number whose assertion is still
carried at Tier 1 on another node is **small and nameable**, not 72. The earlier
figure of 72 counted source strings appearing both demoted and undemoted, which
mostly catches a document backing both a quotation and an inference. Matching on
the claim's own wording instead finds two pairs, and the Battelle one makes three
because its two copies are worded differently and no text match can see it:

| demoted to T2 on | still Tier 1 on | the assertion |
|---|---|---|
| `pentacle-memorandum` | `battelle` **and** `howard-c-cross` | the memorandum of 9 January 1953, ref G-1579-4, to Miles E. Goll |
| `nyt-2017-12-16` | `l-nyc` | the New York Times published "Glowing Auras and Black Money" |
| `the-roswell-incident-1980` | `william-l-moore` | "The Roswell Incident" by Berlitz and Moore, its publisher and date |

**Four Tier 1 claims**, on three nodes. That is the whole of option B.

## 4. The decision, for Stewart

| | What it means |
|---|---|
| **A. Leave it** | The board keeps four claims at Tier 1 whose own twins say they cannot be. Visible to any reader who opens both nodes, and the analyst now finds it on request |
| **B. Fix the four** | Demote them in `research/ffrdcs.json` and the two other source files, with the same reason the twin already carries. T1 3,367 to 3,363 |
| **C. Fix the rule** | Make the no-primary-record ground claim-scoped rather than node-scoped |

**B, and C is now clearly the wrong shape rather than merely a bigger job.**

The node-level test is not laziness, it is load-bearing, and the numbers say why.
Of the board's 3,367 Tier 1 claims, only 1,285 carry a URL in their own source at
all, and only 1,018 of those URLs are primary by `PRIMARY_URL_PAT`. **A
claim-scoped URL test would demote 2,349 of 3,367 Tier 1 claims, 70% of the
board's documented tier.** And it would be wrong to do it: the claims it would
take are ones like

    509th-bomb-group      GAO/NSIAD-95-187
    alexandria-ocasio-cortez  Rep. Alexandria Ocasio-Cortez, 26 July 2023, GPO CHRG-118hhrg53022

which name a primary document precisely and simply do not link it. The node-level
test exists to let those stand.

So C is not "change the scope". C is "teach the rule to recognise a primary
document cited by identifier rather than by URL" -- a document-identifier pattern
to sit beside `PRIMARY_URL_PAT` -- and only then scope it to the claim. That is a
real piece of work with a real payoff, and it is a session of its own with the
gate, the golden manifest and a re-read of everything that moved. It is not
tonight's job and it is not a prerequisite for B.

Neither was done on 12 September, because both change claim tiers and
`CLAUDE.md` section 6 is explicit that tiers are the ammunition grading. If B is
taken, the counts that move are `index.json`, the golden manifest and the
NotebookLM export; `_figures` in `data/analyst-suggestions.json` declares 514
Tier 3 claims and is unaffected.

## 4a. DECIDED, 18 September 2026: B, all four

Stewart handed the decision over ("make whatever decision you think would be best for
our project"). **B is taken, for all four claims.** A was never a real option: it leaves
the board contradicting itself in a way its own analyst finds on request.

The four claims were read before deciding, and the three pairs are not the same kind:

| pair | what the claim is | is Tier 2 the honest grade? |
|---|---|---|
| Cross memorandum, on `battelle` and `howard-c-cross` | a SECRET memo known only from the CUFON transcription and Vallee's copy | **Yes.** `research/ffrdcs.json`'s own gaps say no signed original has ever been produced. This was a real over-grade, and the analyst was right to call it the weakest Tier 1 on the node |
| NYT article, on `l-nyc` | that the Times published the article, with its date and byline | Conservative rather than correct. The article is the primary record of its own publication and its nytimes.com URL is on both nodes |
| Roswell Incident book, on `william-l-moore` | publisher, city, year, ISBN | Conservative rather than correct. The archive.org scan of the book is on both nodes and its imprint page is the primary record |

So for the last two pairs the twin that was demoted is arguably the wrong one: the
node-level rule fired on `nyt-2017-12-16` and `the-roswell-incident-1980` because each
carries a Wikipedia URL and `PRIMARY_URL_PAT` does not recognise nytimes.com or a plain
archive.org scan as primary. **They are demoted anyway, and deliberately.** Promoting the
twins needs a change to the honesty pass, a wrongly low tier costs this board nothing in
a hostile read while a wrongly high or a self-contradicting one does, and all four now sit
in the re-sourcing queue with "needs primary replacement" where option C will find them.

**What this adds to option C's brief:** a document-class node (an article, a book, a
memo) whose own record is on the node is self-documenting for claims about what it says
and when it was published. All four demotions on `nyt-2017-12-16` and both on
`the-roswell-incident-1980` are of that kind. The C session should size that class among
the 90 node-scoped demotions before it writes the identifier pattern, because those
claims come back UP, and that is the direction that needs the most care.

## 5. What is NOT a defect, so nobody chases it

A source string carrying claims at more than one tier is normal and there are 102
of them over 706 claims. A primary document backs Tier 1 quotations of what it
says and Tier 3 inferences drawn from it, and both cite the same URL. Any check
written on "same source, different tier" would fire on all 706 and teach the next
session to ignore it. The narrow pattern in section 3, demoted on one node and
Tier 1 on another, is the one that carries signal, and section 3 names all of it:
four claims on three nodes.
