# Pais patent drawing sheets — provenance

Eleven drawing sheets from the five Navy-assigned Pais filings, for the patents tab.

**Where they came from, exactly.** Rendered at 200 dpi from the official patent PDFs served by
USPTO's public image server:

```
https://image-ppubs.uspto.gov/dirsearch-public/print/downloadPdf/<number>
```

That endpoint needs **no API key and no account**, which is worth recording because two other
routes do not work from a datacenter address: FreePatentsOnline serves a login wall for PDFs,
and Google Patents returns 503 on every request. It is also the route to the drawings for any
other patent this board ever needs.

Retrieved 28 August 2026.

**Licence.** These are drawings from United States patents assigned to the United States as
represented by the Secretary of the Navy, each carrying the Statement of Government Interest.
They are federal public-domain documents. They are NOT registered in `data/l0-images.json`,
which is the register for photographic material whose provenance and licence have been
individually adjudicated; these are document facsimiles, a different thing, and mixing them
would weaken that register's meaning.

**How the sheets were identified.** The PDFs are scans with no text layer, so page role was
determined by ink density measured at 45 dpi greyscale: specification pages run 7.0-8.6% dark
pixels, front pages about 4.5%, and drawing sheets 0.3-3.5%. The separation is clean with no
overlap. It was verified rather than assumed: the front page of US 10,144,532 states "4 Claims,
1 Drawing Sheet", and the method selected exactly one sheet for that patent.

| file | source patent | sheet |
|---|---|---|
| `US10144532_fig1.png` | US 10,144,532, craft using an inertial mass reduction device | FIG-1 triangular craft, FIG-2 diamond craft, both inside the vacuum plasma sheath |
| `US20170313446_fig1.png` | US 2017/0313446 A1, the pre-grant publication of the same application | as published in 2017, before the appeal |
| `US10135366_fig1..3.png` | US 10,135,366, electromagnetic field generator | 3 sheets |
| `US10322827_fig1..3.png` | US 10,322,827, high frequency gravitational wave generator | 3 sheets |
| `US20190058105_fig1.png` | US 2019/0058105, room temperature superconductor | 1 sheet |
| `US20190295733_fig1..2.png` | US 2019/0295733, plasma compression fusion device | 2 sheets |

**A note for whoever builds the tab.** These are 7112x9167 print-resolution renders, roughly
3MB in total. They must be downsampled for display; shipping them at full size into a page
that is already 15MB would be a serious regression in first paint, and first paint on this
board has already been fixed once (`notes/FIRST-PAINT-2026-08-26.md`). Keep the full-size
originals here as the archival copy and generate display derivatives at build time.
