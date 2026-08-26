# Embedded typeface

`IBM Plex Mono`, weights 400 / 500 / 600, latin and latin-ext subsets.

**Why these files are in the repo.** Until 26 August 2026 the built board opened
with three `<link>` tags pointing at `fonts.googleapis.com`, inherited verbatim
from `ref/the-vanishing-v2.html`. The third of them is a stylesheet, and a
stylesheet blocks first paint. That made a file whose whole premise is "single
self-contained HTML, no server, no runtime deps" unable to draw anything at all
until a Google server answered.

**Provenance.** `google-fonts-css2.css` is the exact response from
`https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&display=swap`,
kept so the build has a source for the `unicode-range` of each subset rather
than a transcription of one. The six `.woff2` files are the latin and latin-ext
faces that stylesheet points at, fetched from `fonts.gstatic.com`.

**Licence.** SIL Open Font License 1.1, copied verbatim into `OFL.txt` from
`https://raw.githubusercontent.com/google/fonts/main/ofl/ibmplexmono/OFL.txt`.
Its PERMISSION & CONDITIONS clause names `embed` explicitly. Copyright (c) 2017
IBM Corp. with Reserved Font Name "Plex".

**Refreshing them.** Re-fetch the css2 URL above, re-fetch the latin and
latin-ext `.woff2` it names, and rebuild. The build reads the `unicode-range`
and `font-weight` out of the stylesheet and substitutes a `data:` URI for each
`url()`, so nothing about the mapping is hand-maintained. If Google ever changes
the file naming, `build_dashboard.py` fails loudly rather than shipping a page
with a missing weight -- `verify.py` also asserts all six faces are present.
