# Brief for the blind critic

You are reviewing screenshots of a website as its reader would meet it. You have not seen how it was built
and you must not look: do not open any code, any file in this repository other than the screenshots you
are given, or any note. Judge only what is on the screen.

## What the site is

A research board about the alleged United States programme for recovering and reverse-engineering
non-human craft, 1944 to now. It holds about 1,100 people, institutions, programmes, documents, laws,
places and events, joined by about 2,800 hand-written links that each cite a source, and about 6,000
claims, each graded by evidence strength:

- **Tier 1**: documented (a primary record says so);
- **Tier 2**: a named person on the record (testimony, an allegation, an official statement);
- **Tier 3**: a stated inference.

Nodes also carry a proximity grade (A, B, C) that is NOT about credibility. Statements by the office the
board investigates are treated as an interested party's. The board's promise is that nothing on it is
invented and that every link says why it exists.

## Who reads it

Informed readers: researchers, journalists, and friends of the owner who know the subject and want to check
it. They read on a laptop (1366 or 1920 wide) and sometimes on a phone (375 wide). They are patient with
density but not with confusion.

## The surfaces

Home (the front door and search), a node page (one person, institution, programme, document or event: what
it is, its claims with sources, the case against it, its connections grouped by relationship), an atlas of
topics, a neighbourhood view (a node and everything linked to it, grouped by relationship), a places page
(the board's places on a longitude and latitude grid, and listed by country), a timeline, an evidence
explorer (every claim, filterable), a thread (an authored chain of steps), a patent page, and a printable
report.

## The design rules the owner has set (hold the site to them)

- One label size; labels are never shrunk or truncated to fit; nothing is drawn without a name.
- Size never encodes importance.
- Nothing overlaps; nothing is clipped; no sideways scrolling on a phone.
- Every connection says in words why it exists.
- The case against a claim sits beside the claim, not somewhere else.

## What to return

The **five worst problems a reader would notice**, worst first. For each:

1. the screenshot file name(s);
2. what is wrong, in one or two plain sentences (what you see, where on the screen);
3. why a reader would care;
4. severity: **blocker** (a reader cannot use or trust this surface), **major** (a reader is misled,
   confused or slowed), **minor** (noticeable, does not mislead), **cosmetic**.

Then, in one line, the single thing that works best. Be concrete and unsparing; do not praise to soften.
Do not guess at causes in code. If a screenshot is ambiguous (for example a view that may be mid-load),
say so rather than inventing a problem.
