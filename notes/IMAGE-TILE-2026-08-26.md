# The image tile: the render half, built and tested against an empty register

26 August 2026.

## What was actually blocking

`data/l0-images.json` has been plumbed, validated and empty since 24 August, and the
reason it is empty is good: **a record there asserts that a specific image exists at a
specific URL under a specific licence, which is a sourcing claim like any other.** The one
rule that never bends applies to image URLs exactly as it applies to document numbers.

But two separate things were being deferred under one heading, and only one of them
needed to be:

| half | needs | status before today |
|---|---|---|
| **sourcing** | licence judgement about real people's faces, one node at a time | rightly deferred, still deferred |
| **render** | code | deferred with it, for no reason that survives examination |

The stated reason was *"a render branch with no data is untested code"*. That is true and
it is the argument for **testing** it, not for leaving it unwritten. Leaving it unwritten
meant the first person to populate the register — after doing the hardest and least
reversible research on this board — would be the one to discover whether the renderer
worked.

## What is built

The chip's third slot is `[rule][image|glyph][label][rank][mark]`. It now draws the image
when one is on the model, and the class letter when one is not.

| | |
|---|---|
| **portrait** | cover-fitted and clipped to a circle. A face may be cropped. |
| **mark** | contain-fitted in the square, undistorted, **never clipped**. |
| **`ask`** | an amber ring on the tile, so the state is visible without opening anything |
| **load failure** | permanent, silent, falls back to the class letter. Never a broken-image box. |

`photoKind` being load-bearing is not a style preference. **An institutional seal cropped
to a circle is a different mark**, and several of the seals on this board carry statutory
restrictions on alteration that are stricter than copyright. The register's own notes
already said so; nothing enforced it until now.

The dossier prints the credit — attribution is the condition most of these licences are
granted on, not decoration — and for `ask`, the specific reason, so the doubt travels with
the picture instead of being resolved silently in its favour.

## How it is tested with no data

Five canvas assertions, against **injected fixtures**: two 16x16 PNGs generated in the test
process, in colours that appear nowhere in the palette, assigned to a real map node. The
chip is parked at a known screen position at `k=2` so the 11px slot becomes 22px and its
corners are addressable, and the pixels are read back.

| assertion | reads |
|---|---|
| the class letter is what draws when no image clears | slot carries no fixture colour before injection |
| a cleared image replaces the class letter | slot centre carries the fixture |
| a portrait is cropped to a circle | centre inked, **corner empty** |
| a mark is never cropped to a circle | centre inked, **corner inked** |
| an image that will not load falls back to the class letter | slot is **byte-identical** to the no-image state, carrying the letter's 68 inked pixels |

The last one started as two sampled pixels and failed, correctly: the glyph is thin type
and a single pixel through it is luck. What the fallback claim actually needs is that the
slot returns to *exactly* the state it was in with no image at all, which a byte sum states
and a sample does not.

**The poisons are page-level, not predicate-level.** Nine of this file's existing poisons
corrupt the probe object, which proves each predicate rejects bad input and nothing more.
These do the harder thing:

- **The two treatments swapped** — the portrait drawn by the mark path and the mark by the
  portrait path. Both shape checks must collapse, and do. Nothing else in the render
  distinguishes them, so a check that survives this is not reading the shape, and the shape
  is the entire licensing claim.
- **A "dead" URL that resolves.** The fallback claim is byte-identity with the no-image
  state; an image that loads must break it, and does.

## And the register itself

`nothing in the image register fails silently`, in `verify.py`, self-tested against five
records.

The failure mode of a plumbed-and-empty channel is specific and quiet: `build_l0_layout.mjs`
puts a record on the model only when it clears, so **a malformed record simply does not
clear**, the node falls back to its class letter, and that is indistinguishable from never
having tried. A record that was meant to publish an image and does not must fail loudly, or
the sourcing pass will produce work that silently does not ship.

Five ways to do that, each its own poison: `clears` with no `photo`; `ask` with no `note`;
a `photoKind` the renderer has never heard of, which would let a seal be cropped; a
clearance word outside the vocabulary; and `clears` with no `photoCredit`, which is the one
that runs the other way — a licensing failure rather than a rendering one.

`no` and `none` records are welcome and assert nothing. Recording that an image was found
and does **not** clear is research; deleting it means the next pass redoes the work.

## What is still deferred, and still should be

The sourcing pass. Unchanged, and unchanged for the right reason. §9 item 7 stands:

- Federal works are the strongest candidates (17 U.S.C. 105) but must trace to a `.gov`
  original, not an aggregator — the exemption covers the federal work, not a wire-service
  photograph of the same person.
- Agency seals are usually reproducible for identification, but misuse-of-seal provisions
  are stricter than copyright. `ask` until the specific restriction has been read.
- Contractor logos are trademarks, and this board is adversarial toward several of those
  organisations. Default to `ask` with the reason recorded.
- **Witnesses and private individuals are the hardest category and the one where getting it
  wrong matters most.** A private person who gave testimony has not thereby licensed their
  likeness. Default to the class letter.

The class letter is not a failure state. It says what the node *is*, rather than implying a
face nobody found. **110 of 110 nodes will keep drawing it until someone does the work**,
and that is a supported, tested state rather than a gap.
