"""The PATENTS view.

A tab of its own, built to the mockup Stewart signed off on 29 August 2026 --
`notes/PATENTS-TAB-MOCKUP-2026-08-29.md`, all four questions in its section 5
answered. Its own module for the reason `l0_patches.py` is its own module: there is
no upstream surface in `ref/the-vanishing-v2.html` to patch against, so this is
written rather than adapted, and keeping it separate means the map module does not
grow a second subject.

WHAT IS HERE AND WHAT IS NOT
----------------------------
Here: a renderer, its stylesheet, and four string patches -- `VIEWS`, `VIEW_LABEL`,
the dispatch map, and the function. That is what a view costs on this shell.

NOT here: one word of the tab's content. Every string it draws is authored in
`research/patents-view.json` and `research/observables-view.json` and emitted as
`PATDATA` and `OBSDATA`, on the `data/l0-highlights.json` precedent. The reason is
CLAUDE.md section 2: content typed into a renderer cannot be gate-checked, and the
one rule that never bends on this board is about content. `verify.py` checks these
two files -- every quote against the transcript it cites, every filing against its
own status, the taxonomy against its Tier 2 cap.

THE OBSERVABLES ARE A SEPARATE FILE ON PURPOSE. Stewart, 29 August: reference how
the patents pertain to them here, "and reuse the five observables elsewhere ... call
it observables or something". A craft-types surface built later reads
`research/observables-view.json` directly. It must not have to read the patents
tab's data to find out what the five are, and two copies of a taxonomy is how the
two stop agreeing.

THE DRAWINGS SHIP AS DERIVATIVES. `research/patents/drawings/PROVENANCE.md` records
that the originals are 7112x9167 print renders, about 3MB, and warns that shipping
them whole would undo `notes/FIRST-PAINT-2026-08-26.md`.
`tools/make_drawing_thumbs.mjs` writes the display copies and they are committed;
this module base64s those. They are NOT registered in `data/l0-images.json` -- that
register is for photographic material whose licence has been individually
adjudicated, and these are document facsimiles, which is a different thing. Mixing
them would weaken what that register means.
"""

import base64
import json as _json
import os


def _root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_data():
    """The two authored files plus the drawing derivatives, as one payload.

    Raises rather than degrading. A tab that renders with no data does not look
    broken, it looks empty -- and an empty tab beside eight full ones reads as a
    board with nothing to say about patents, which is the opposite of the finding.
    """
    root = _root()
    out = {}
    for key, rel in (("patents", "research/patents-view.json"),
                     ("observables", "research/observables-view.json")):
        path = os.path.join(root, rel)
        if not os.path.exists(path):
            raise SystemExit("patents_patches: %s is missing. The PATENTS tab is a "
                             "renderer with no content of its own." % rel)
        with open(path, encoding="utf-8") as fh:
            out[key] = _json.load(fh)

    thumbs = os.path.join(root, "research", "patents", "drawings", "thumbs")
    imgs = {}
    for sheet in (out["patents"].get("drawings") or {}).get("sheets") or []:
        name = sheet.get("file")
        src = os.path.join(thumbs, name or "")
        if not name or not os.path.exists(src):
            # Named but absent is a defect, not a fallback. A silently missing
            # drawing is the image register's own failure mode: it does not error,
            # it just falls back to nothing and looks like never having tried.
            raise SystemExit(
                "patents_patches: research/patents-view.json names the drawing "
                "sheet %r and research/patents/drawings/thumbs/ does not have it. "
                "Run: node tools/make_drawing_thumbs.mjs" % name)
        with open(src, "rb") as fh:
            imgs[name] = ("data:image/png;base64,"
                          + base64.b64encode(fh.read()).decode("ascii"))
    out["images"] = imgs
    return out


PATENTS_CSS = r"""/* ---- PATENTS tab ------------------------------------------------------- */
/* Every value here is lifted from the shell rather than picked: the 22px chip and
   its 9px/.10em uppercase come from .l0chip, the text ramp and the three accents
   from L0_PACK and the root variables, and the 396px rail from .l0reg. The mockup
   signed off on 29 August measured them off this file; this is the same file. */
.pat{display:flex;flex-direction:column;gap:11px;padding-bottom:8px}
.pat .patrow{display:flex;gap:11px;align-items:flex-start}
.pat .patmain{flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:11px}
.pat .patrail{flex:0 0 396px;display:flex;flex-direction:column;gap:11px}
@media (max-width:1550px){
  .pat .patrow{flex-direction:column}
  .pat .patrail{flex:1 1 auto;width:100%}
}
.patbox{background:#12171d;border:1px solid #262e36;padding:12px 13px}
.patbox>h3{font:600 11.5px/1.35 'IBM Plex Mono',monospace;color:#e6e9ee;margin:0 0 4px}
.patbox>p.lede{font:400 10.5px/1.65 'IBM Plex Mono',monospace;color:#8d97a4;
  margin:0 0 10px;max-width:96ch;text-wrap:pretty}
.pattag{display:inline-flex;align-items:center;height:22px;padding:0 8px;
  font:500 9px/1 'IBM Plex Mono',monospace;letter-spacing:.10em;text-transform:uppercase;
  border:1px solid #3b444f;color:#b9c2cd;background:#141920;margin:0 5px 0 0}
.pattag.on{border-color:#5ed4e6;color:#5ed4e6}
.pattag.warn{border-color:#3a2f1c;color:#efb555}
.pattag.bad{border-color:#5a3f3c;color:#e8705f}

/* the five filings, one size each -- size must never encode importance */
.patfil{display:grid;grid-template-columns:repeat(auto-fit,minmax(232px,1fr));gap:0;
  border:1px solid #1d242b}
.patfil>div{padding:11px 12px;border-right:1px solid #1d242b;min-width:0}
.patfil>div:last-child{border-right:none}
.patfil .lead{border:1px solid #5ed4e6;margin:-1px}
.patfil .dk{font:500 9px/1 'IBM Plex Mono',monospace;letter-spacing:.10em;color:#efb555;
  text-transform:uppercase}
.patfil .no{font:400 9px/1 'IBM Plex Mono',monospace;color:#5c6672;margin-left:6px}
.patfil h4{font:500 11px/1.4 'IBM Plex Mono',monospace;color:#e6e9ee;margin:7px 0 6px;
  text-wrap:pretty}
.patfil .meta{font:400 9px/1.6 'IBM Plex Mono',monospace;color:#5c6672;margin:0 0 9px}
.patfil .meta b{color:#8d97a4;font-weight:400}

/* two prosecution lanes on one axis */
.patlane{margin-top:2px}
.patlane .axis{position:relative;height:14px;margin:0 0 4px;border-bottom:1px solid #262e36}
.patlane .axis span{position:absolute;top:0;font:400 8.5px/1 'IBM Plex Mono',monospace;
  color:#5c6672;transform:translateX(-50%);white-space:nowrap}
.patlane .lane{position:relative;margin:14px 0 0}
.patlane .lname{font:500 9px/1 'IBM Plex Mono',monospace;letter-spacing:.10em;color:#efb555;
  text-transform:uppercase}
.patlane .lsum{font:400 9px/1 'IBM Plex Mono',monospace;color:#5c6672;margin-left:8px}
/* THE TRACK IS TALL ENOUGH FOR THE STAGGER, and the height is set from the number
   of rows the renderer actually used rather than from a constant -- PAX 205 has ten
   events inside three years and PAX 182 has six inside seven, so one height for
   both is either wasteful or overlapping. */
.patlane .track{position:relative;margin-top:9px;border-top:1px solid #1d242b}
.patlane .ev{position:absolute;top:0;width:0}
.patlane .ev i{display:block;width:9px;height:9px;margin:5px 0 0 -4px;
  border:1px solid #3b444f;background:#12171d;font-style:normal;text-align:center}
.patlane .ev.reject i{border-color:#efb555}
.patlane .ev.final i{border-color:#e8705f;background:#e8705f}
.patlane .ev.allow i{border-color:#5ed4e6;background:#5ed4e6}
.patlane .ev.grant i{border-color:#8d97a4}
.patlane .ev.mark i{border-color:#5ed4e6}
.patlane .ev.expire i{border:none;color:#e8705f;font:400 11px/9px 'IBM Plex Mono',monospace}
/* the leader, from the marker down to whichever row the label landed on */
.patlane .ev u{position:absolute;left:0;top:14px;width:1px;background:#262e36;
  text-decoration:none}
.patlane .ev b{position:absolute;left:0;font:400 8px/1.25 'IBM Plex Mono',monospace;
  letter-spacing:.06em;color:#5c6672;font-weight:400;white-space:nowrap;
  padding-left:4px;border-left:1px solid #262e36}
.patlane .ev.final b,.patlane .ev.allow b{color:#b9c2cd}
.patlane .find{font:400 10px/1.6 'IBM Plex Mono',monospace;color:#b9c2cd;margin:16px 0 0;
  padding-top:9px;border-top:1px solid #1d242b}

/* pull quotes */
.patq{display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:11px}
.patq blockquote{background:#141920;border:1px solid #262e36;border-left:2px solid #5ed4e6;
  padding:11px 13px;margin:0}
.patq .who{font:500 8.5px/1 'IBM Plex Mono',monospace;letter-spacing:.13em;color:#5ed4e6;
  text-transform:uppercase;margin-bottom:7px;display:block}
.patq q{display:block;font:400 10.5px/1.7 'IBM Plex Mono',monospace;color:#e6e9ee;
  quotes:'\201C' '\201D';text-wrap:pretty}
.patq q em{font-style:normal;color:#efb555}
.patq .gloss{display:block;font:400 9.5px/1.6 'IBM Plex Mono',monospace;color:#5c6672;
  margin-top:8px;text-wrap:pretty}

/* the observables mapping */
.patobs{width:100%;border-collapse:collapse;margin-top:2px}
.patobs td{padding:9px 10px;border-top:1px solid #1d242b;vertical-align:top;
  font:400 10.5px/1.55 'IBM Plex Mono',monospace}
.patobs tr:first-child td{border-top:none}
.patobs td.o{color:#e6e9ee;width:42%}
.patobs td.m{color:#8d97a4}
.patobs tr.no td.o{color:#5c6672}
.patobs .yes{color:#5ed4e6;margin-right:7px}
.patobs .no{color:#e8705f;margin-right:7px}
.patobs .why{display:block;color:#5c6672;font-size:9.5px;margin-top:5px;text-wrap:pretty}

/* the file wrapper list */
.patwrap ul{list-style:none;margin:0;padding:0}
.patwrap li{display:flex;align-items:baseline;gap:8px;padding:4px 0;
  font:400 10px/1.5 'IBM Plex Mono',monospace;color:#b9c2cd}
.patwrap li .t{color:#5ed4e6;flex:0 0 auto;font-size:9px}
.patwrap li .n{flex:1 1 auto;min-width:0;border-bottom:1px dotted #262e36;
  transform:translateY(-3px)}
.patwrap li .d{flex:0 0 auto;color:#5c6672;font-size:9px;letter-spacing:.04em}
.patwrap li.gone{color:#5c6672}
.patwrap li.gone .lbl{text-decoration:line-through}
.patwrap li.gone .t{color:#e8705f}
.patwrap li.gone .d{color:#e8705f}
.patwrap li.why{display:block;font:400 9.5px/1.6 'IBM Plex Mono',monospace;color:#5c6672;
  margin:2px 0 9px 17px;padding:0;text-wrap:pretty}
.patwrap .eyebrow{display:block;margin:12px 0 6px}
.patwrap .eyebrow.gone{color:#e8705f}

/* the maintenance-fee finding */
.patfind ul{list-style:none;margin:9px 0 0;padding:0}
.patfind li{display:flex;justify-content:space-between;gap:10px;padding:4px 0;
  font:400 10px/1.5 'IBM Plex Mono',monospace;color:#b9c2cd}
.patfind li .x{color:#e8705f;margin-right:6px}
.patfind li .d{color:#e8705f}
.patfind .coda{font:400 9.5px/1.65 'IBM Plex Mono',monospace;color:#5c6672;
  margin:11px 0 0;text-wrap:pretty}

/* drawings, as document facsimiles on their own paper ground */
.patdraw{display:grid;grid-template-columns:repeat(auto-fill,minmax(104px,1fr));gap:9px;
  margin-top:2px}
.patdraw figure{margin:0}
.patdraw .tile{background:#ffffff;border:1px solid #262e36;aspect-ratio:84/108;
  display:flex;align-items:center;justify-content:center;overflow:hidden}
.patdraw img{max-width:100%;max-height:100%;display:block}
.patdraw figcaption{display:block;font:400 8.5px/1.45 'IBM Plex Mono',monospace;
  color:#5c6672;margin-top:5px;text-wrap:pretty}
.patdraw figcaption b{display:block;color:#8d97a4;font-weight:400;letter-spacing:.04em}

/* open questions */
.patopen ul{list-style:none;margin:0;padding:0}
.patopen li{position:relative;padding:5px 0 5px 15px;
  font:400 10px/1.6 'IBM Plex Mono',monospace;color:#8d97a4;text-wrap:pretty}
.patopen li:before{content:'?';position:absolute;left:0;top:5px;color:#efb555}
.patopen li.closed{color:#5c6672}
.patopen li.closed:before{content:'\2713';color:#5ed4e6}
/* #5c6672 is the FLOOR of this board's text ramp, not below it. The first cut set
   this at #3b444f, which is bandN -- a rule colour, not a text colour -- and a Tier
   3 reading is meant to be quiet, not unreadable. Dimness carries the grade; it does
   not get to cost the sentence. */
.patsrc{font:400 9.5px/1.65 'IBM Plex Mono',monospace;color:#5c6672;margin:11px 0 0;
  padding-top:9px;border-top:1px solid #1d242b;text-wrap:pretty}
.patsrc a{color:#8d97a4}
"""

PATENTS_JS = r"""/* --- PATENTS ------------------------------------------------------------------
   A RENDERER, NOT A DOCUMENT. Every string it draws comes from PATDATA and
   OBSDATA, which are authored in research/patents-view.json and
   research/observables-view.json and checked by verify.py. Nothing on this tab is
   typed into this file, for the reason data/l0-highlights.json is not typed into
   this file: content in a renderer cannot be gate-checked, and this board's one
   unbendable rule is about content.

   COUNTS ARE DERIVED. The header strip counts filings, grants, expiries and absent
   papers out of the arrays. The mockup's strip read "5 FILINGS · 2 GRANTED" and the
   data says three are granted -- which is exactly why renderStats derives its
   numbers rather than carrying them, and why this does too. */
function patCount(){
  const F = (PATDATA.filings || []);
  return {
    filings: F.length,
    granted: F.filter(f => (f.status||[]).indexOf('GRANTED') >= 0).length,
    expired: F.filter(f => (f.status||[]).indexOf('EXPIRED') >= 0).length,
    published: F.filter(f => (f.status||[]).indexOf('PUBLISHED') >= 0).length,
    absent: ((PATDATA.wrapper||{}).absent || []).length,
  };
}
/* A quote with one phrase lit. The emphasis is matched against the quote's own
   text and dropped silently if it is not a substring -- a highlight that does not
   appear in what it highlights would be an edit to a quotation, and section 2 of
   CLAUDE.md does not have a "just for display" case. verify.py asserts the match
   so the silence here is never the only thing standing between a typo and the
   page. */
function patQuote(q){
  const t = String(q.text || '');
  const em = String(q.emphasis || '');
  const i = em ? t.indexOf(em) : -1;
  return i < 0 ? esc(t)
    : esc(t.slice(0, i)) + '<em>' + esc(em) + '</em>' + esc(t.slice(i + em.length));
}
/* Where an event sits on the shared axis, 0..1. Two lanes on ONE axis is the whole
   argument of the section -- read apart they are two prosecutions, read against
   each other they are one design handled two ways -- so the position is computed
   from the axis the data declares rather than per lane. */
function patX(d, ax){
  const a = Date.parse(ax.from), b = Date.parse(ax.to), t = Date.parse(d);
  if (!(b > a) || !(t === t)) return 0;
  return Math.max(0, Math.min(1, (t - a) / (b - a)));
}
/* THE LABELS ARE STAGGERED, NOT SPREAD, and the difference is the whole point of
   drawing this on a real axis. PAX 205 has ten events inside three years: FILED,
   the Sheehy letter, two rejections, an interview, a declaration, an appeal, an
   advisory action, the grant and the expiry. Placed at their true dates and
   labelled on one row they overprint into an unreadable smear -- measured on the
   first cut: 'NON-FINAL', 'ALLOWED — PRIOR ART' and 'GRANTED' rendered as
   'NON-ALLOWED — PRIORARTED'.

   The two wrong fixes are worth naming. Spacing the events out evenly would make
   the axis a lie, and the axis IS the argument: PAX 182 runs clean across seven
   years while PAX 205 is fought out inside thirteen months. Dropping labels would
   hide exactly the events that make the comparison.

   So the dates stay put and the LABELS move down. Each label is given the first row
   on which it clears the previous label's measured width, and a leader runs from
   its marker to it. Rows are assigned greedily left to right, so the earliest event
   in a cluster keeps the top row and the reading order stays chronological. */
const ROW_H = 12;
/* Width in the track's own percentage units, measured off the resolved face rather
   than assumed. This board has been bitten by assumed monospace metrics before --
   the chip label bug, three times. */
function patLabelPct(text, trackPx){
  const cv = patLabelPct._c || (patLabelPct._c = document.createElement('canvas').getContext('2d'));
  cv.font = "400 8px 'IBM Plex Mono',monospace";
  const w = cv.measureText(String(text || '')).width + 10;   /* +padding and leader */
  return trackPx > 0 ? (w / trackPx) * 100 : 8;
}
function patStagger(ev, ax){
  /* The track's real pixel width, so the measure is in the same units as the layout.
     Falls back to a sane width before first layout rather than to zero, which would
     put every label on row 0 and reproduce the defect. */
  const el = document.querySelector('.pat .patlane');
  const trackPx = el ? Math.max(320, el.getBoundingClientRect().width) : 1100;
  const ends = [];                      /* right edge, in %, of the last label per row */
  const out = [];
  for (const e of ev){
    const x = patX(e.date, ax) * 100;
    const w = patLabelPct(e.label, trackPx);
    let r = 0;
    while (ends[r] != null && x < ends[r]) r++;
    ends[r] = x + w;
    out.push(r);
  }
  return out;
}
function viewPatents(v){
  const C = patCount();
  const cm = PATDATA.comparison || {};
  const W = PATDATA.wrapper || {};
  const D = PATDATA.drawings || {};
  const O = OBSDATA || {};
  let h = '<div class="view-head"><h2>' + esc(PATDATA.title || 'Patents') + '</h2>'
        + '<p>' + esc(PATDATA.standfirst || '') + '</p></div>';

  h += '<div class="pat">';

  /* ---- the five filings, all at one size. Size must never encode importance
     (CLAUDE.md section 4); the lead filing is marked with a rule, not a scale. */
  h += '<div class="patbox"><h3>' + esc(PATDATA.eyebrow || '') + '</h3>'
     + '<p class="lede">' + C.filings + ' filings &middot; ' + C.granted + ' granted &middot; '
     + C.expired + ' expired &middot; ' + C.published + ' published as applications</p>'
     + '<div class="patfil">'
     + (PATDATA.filings || []).map(f => {
        const st = (f.status || []).map(s =>
          '<span class="pattag ' + (s === 'EXPIRED' ? 'bad' : s === 'APPEALED' ? 'warn' : 'on')
          + '">' + esc(s) + '</span>').join('');
        return '<div' + (f.lead ? ' class="lead"' : '') + '>'
          + (f.docket ? '<span class="dk">' + esc(f.docket) + '</span>' : '')
          + '<span class="no">' + esc(f.application) + '</span>'
          + '<h4>' + esc(f.title) + '</h4>'
          + '<p class="meta">filed <b>' + fmtDate(f.filed) + '</b><br>'
          + esc(f.number)
          + (f.examiner ? '<br>' + esc(f.examiner) : '')
          + ((f.artUnits && f.artUnits.length)
              ? '<br>Art Unit ' + f.artUnits.map(esc).join(' then ') : '')
          + (f.note ? '<br>' + esc(f.note) : '')
          + '</p>' + st + '</div>';
       }).join('')
     + '</div></div>';

  /* ---- the comparison, which is what the tab argues ---------------------- */
  const ax = cm.axis || { from: '2015-01-01', to: '2023-06-30' };
  const y0 = new Date(ax.from).getUTCFullYear(), y1 = new Date(ax.to).getUTCFullYear();
  let ticks = '';
  for (let y = y0; y <= y1; y++){
    const p = patX(y + '-01-01', ax);
    if (p <= 0 || p >= 1) { if (y !== y0) continue; }
    ticks += '<span style="left:' + (patX(y + '-01-01', ax) * 100).toFixed(2) + '%">' + y + '</span>';
  }
  h += '<div class="patbox"><h3>' + esc(cm.title || '') + '</h3>'
     + '<p class="lede">' + esc(cm.standfirst || '') + '</p>'
     + '<div class="patlane"><div class="axis">' + ticks + '</div>'
     + (cm.lanes || []).map(L => {
        const ev = (L.events || []).slice().sort((a, b) => Date.parse(a.date) - Date.parse(b.date));
        const rows = patStagger(ev, ax);
        const depth = rows.length ? Math.max.apply(null, rows) + 1 : 1;
        return '<div class="lane"><span class="lname">' + esc(L.label) + '</span>'
        + '<span class="lsum">' + esc(L.summary || '') + '</span>'
        + '<div class="track" style="height:' + (20 + depth * ROW_H) + 'px">'
        + ev.map((e, i) => {
            const top = 18 + rows[i] * ROW_H;
            return '<span class="ev ' + esc(e.kind || 'plain') + '" style="left:'
            + (patX(e.date, ax) * 100).toFixed(2) + '%" title="' + esc(e.label) + ' — '
            + esc(fmtDate(e.date)) + (e.note ? ' — ' + esc(e.note) : '') + '">'
            + '<i>' + (e.kind === 'expire' ? '&times;' : '') + '</i>'
            + '<u style="height:' + (top - 14) + 'px"></u>'
            + '<b style="top:' + top + 'px">' + esc(e.label) + '</b></span>';
          }).join('')
        + '</div></div>';
       }).join('')
     + (cm.finding ? '<p class="find">' + esc(cm.finding) + '</p>' : '')
     + '</div></div>';

  /* ---- the quotes -------------------------------------------------------- */
  h += '<div class="patq">'
     + (PATDATA.quotes || []).map(q =>
        '<blockquote><span class="who">' + esc(q.speaker) + ' &middot; '
        + fmtDate(q.date) + '</span><q>' + patQuote(q) + '</q>'
        + (q.gloss ? '<span class="gloss">' + esc(q.gloss) + '</span>' : '')
        + '</blockquote>').join('')
     + '</div>';

  /* ---- the two-column body ---------------------------------------------- */
  h += '<div class="patrow"><div class="patmain">';

  /* the observables, capped at Tier 2 and mapped at Tier 1. The two grades are
     printed separately because merging them is the overclaim this node exists to
     avoid: four of five, never five. */
  const map = (O.mappings || [])[0] || { rows: [] };
  const met = (map.rows || []).filter(r => r.met).length;
  const byId = {}; (O.observables || []).forEach(o => { byId[o.id] = o; });
  h += '<div class="patbox"><h3>' + esc((PATDATA.observables || {}).title || '') + '</h3>'
     + '<p class="lede">' + esc((PATDATA.observables || {}).standfirst || '') + '</p>'
     + '<p style="margin:0 0 10px">'
     + '<span class="pattag warn">TIER ' + esc(String(O.tier)) + ' &middot; the taxonomy</span>'
     + '<span class="pattag on">TIER ' + esc(String(map.tier)) + ' &middot; the mapping</span>'
     + '<span class="pattag">' + met + ' of ' + (map.rows || []).length + ' mapped</span></p>'
     + '<p class="lede">' + esc(O.caveat || '') + '</p>'
     + '<table class="patobs">'
     + (map.rows || []).map(r => {
        const o = byId[r.observable] || { label: r.observable };
        return '<tr class="' + (r.met ? 'yes' : 'no') + '">'
          + '<td class="o">' + esc(o.label)
          + (o.unsettled ? '<span class="why">' + esc(o.note || '') + '</span>' : '')
          + '</td><td class="m">'
          + (r.met ? '<span class="yes">&#10003;</span>' : '<span class="no">&times;</span>')
          + esc(r.as)
          + (r.why ? '<span class="why">' + esc(r.why) + '</span>' : '')
          + '</td></tr>';
       }).join('')
     + '</table>'
     + (O.reading ? '<p class="patsrc">Tier ' + esc(String(O.reading.tier)) + ' &middot; '
                  + esc(O.reading.text) + '</p>' : '')
     + '</div>';

  /* the drawings */
  h += '<div class="patbox"><h3>' + esc(D.title || 'Drawings') + ' &middot; '
     + ((D.sheets || []).length) + ' sheets</h3>'
     + '<p class="lede">' + esc(D.standfirst || '') + '</p>'
     + '<div class="patdraw">'
     + (D.sheets || []).map(s => {
        const src = (PATIMG || {})[s.file];
        return '<figure><div class="tile">'
          + (src ? '<img loading="lazy" src="' + src + '" alt="'
                 + esc(s.patent + ' drawing sheet') + '">' : '')
          + '</div><figcaption><b>' + esc(s.patent) + '</b>' + esc(s.caption)
          + '</figcaption></figure>';
       }).join('')
     + '</div></div>';

  h += '</div><div class="patrail">';

  /* the file wrapper, with the absent papers DRAWN rather than omitted */
  h += '<div class="patbox patwrap"><h3>' + esc(W.title || '') + '</h3>'
     + '<p class="lede">' + esc(W.standfirst || '') + '</p>'
     + '<span class="eyebrow">Obtained</span><ul>'
     + (W.obtained || []).map(p =>
        '<li><span class="t">T' + esc(String(p.tier)) + '</span>'
        + '<span class="lbl">' + esc(p.label) + '</span>'
        + '<span class="n"></span><span class="d">' + fmtDate(p.date) + '</span></li>').join('')
     + '</ul>'
     + ((W.absent || []).length
        ? '<span class="eyebrow gone">Absent from the record</span><ul>'
          + (W.absent || []).map(p =>
             '<li class="gone"><span class="t">&times;</span>'
             + '<span class="lbl">' + esc(p.label) + '</span>'
             + '<span class="n"></span><span class="d">NOT OBTAINED</span></li>'
             + '<li class="why">' + esc(p.why) + '</li>').join('')
          + '</ul>'
        : '')
     + '</div>';

  /* the maintenance-fee finding */
  h += (PATDATA.findings || []).map(f =>
      '<div class="patbox patfind"><h3>' + esc(f.title) + '</h3>'
      + '<p class="lede">' + esc(f.text) + '</p><ul>'
      + (f.rows || []).map(r => '<li><span><span class="x">&times;</span>'
          + esc(r.number) + '</span><span class="d">' + fmtDate(r.date) + '</span></li>').join('')
      + '</ul>' + (f.coda ? '<p class="coda">' + esc(f.coda) + '</p>' : '')
      + '</div>').join('');

  /* open questions, from both files, with the closed one shown as closed --
     a negative result is a result and this board prints them. */
  const qs = (PATDATA.openQuestions || []).concat((O.openQuestions || []));
  h += '<div class="patbox patopen"><h3>Open questions</h3><ul>'
     + qs.map(q => '<li' + (q.closed ? ' class="closed"' : '') + '>' + esc(q.text) + '</li>').join('')
     + '</ul></div>';

  h += '</div></div></div>';
  v.innerHTML = h;
}
"""


def apply(s, must_replace, data=None):
    """Patch the PATENTS view into the built page.

    `must_replace` is build_dashboard's helper, so a failed anchor reports through
    the same channel as every other patch.

    ORDER. This runs AFTER l0_patches, and both add a view. The anchors below are
    written against the array as l0_patches leaves it -- NETWORK, PROGRAM, then the
    rest -- so PATENTS lands third: the two maps, and then the patent record. An
    anchor that no longer matches fails loudly rather than silently, which is what
    must_replace is for.
    """
    ok = True
    d = data if data is not None else load_data()

    # -- the payload. Serialised compactly; the drawings dominate its size and they
    #    are already downsampled.
    block = ("const PATDATA = " + _json.dumps(d["patents"], separators=(",", ":")) + ";\n"
             "const OBSDATA = " + _json.dumps(d["observables"], separators=(",", ":")) + ";\n"
             "const PATIMG = " + _json.dumps(d["images"], separators=(",", ":")) + ";\n")
    s, o = must_replace(s, "const CMD = {", block + "\n" + PATENTS_JS + "\nconst CMD = {",
                        "PATENTS data + renderer", 1)
    ok &= o

    s, o = must_replace(s, "</style>", PATENTS_CSS + "</style>", "PATENTS styles",
                        s.count("</style>"))
    ok &= o

    # -- the four string patches a view costs.
    s, o = must_replace(s,
                        "const VIEWS = ['NETWORK','PROGRAM','TIMELINE',",
                        "const VIEWS = ['NETWORK','PROGRAM','PATENTS','TIMELINE',",
                        "VIEWS gains PATENTS", 1)
    ok &= o
    s, o = must_replace(s,
                        "PROGRAM:'Program map', TIMELINE:'Timeline',",
                        "PROGRAM:'Program map', PATENTS:'Patents', TIMELINE:'Timeline',",
                        "VIEW_LABEL gains PATENTS", 1)
    ok &= o
    s, o = must_replace(s,
                        "PROGRAM:viewProgramMap, TIMELINE:viewTimeline,",
                        "PROGRAM:viewProgramMap, PATENTS:viewPatents, TIMELINE:viewTimeline,",
                        "view dispatch gains PATENTS", 1)
    ok &= o

    # -- the analyst is meant to be able to operate every control on the board. A
    #    view it is not told about is a view it cannot send anyone to.
    s, o = must_replace(s,
                        'setView("NETWORK"|"PROGRAM"|"TIMELINE"',
                        'setView("NETWORK"|"PROGRAM"|"PATENTS"|"TIMELINE"',
                        "the analyst is told about the patents tab", 1)
    ok &= o

    return s, ok
