# Program Shell mockup — source

`Program Shell.dc.html` is the page every capture in `../shots/design-2026-09-02/` came
from. It is self-contained apart from two siblings, both included here:

- `support.js` — the template/logic runtime the page loads (`<script src="support.js">`).
- `data/design-extract.json` — fetched at runtime; a copy of `data/design-extract.json`
  from the repo root, unchanged.

Open `Program Shell.dc.html` over HTTP (any static server; `file://` blocks the fetch).
Routes are hash-driven as in section 2.1 of the response, plus `?w=1366|1920|2560` to set
the frame: `#/map?w=1366`, `#/n/aawsap?w=2560`, `#/hood/aawsap`, `#/t/custody`,
`#/timeline`, `#/patents/10144532?sheet=3`, `#/evidence`, `#/report/n/aawsap`. The last
view is also kept in `localStorage['program-shell-view']`.

Where the layout code lives (all inside the one `<script data-dc-script>` block):

- `layoutMap(W, H)` — chip width `cw`, cell packing `pack`, the label-mode / cell-mode
  decision (pitch steps 20→18, band gap 12→6, then cells), rest-budget edge selection
  and orthogonal routing, cell expansion panel.
- `chip(n, x, y, w)` — chip model incl. start-here numbering (`Component.SH`).
- `layoutHood(W, H)` — ring slots by y (15 px), fit test `lw`, hop-2 columns, spill
  count.
- `renderVals()` — node page, thread chain + small map + slice (`edgeBetween`), timeline
  row packing (`rowEnd`), evidence rows, report.
- `band(n)` and `strand(n)` — the approximations flagged in sections 4.1 and 1.7.

The template is the markup between `<x-dc>` and `</x-dc>`; styles are inline, the only
stylesheet rules are the font, body reset and two keyframes at the top.
