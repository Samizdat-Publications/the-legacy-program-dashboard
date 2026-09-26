"""ship.py: what redesign phase 10 adds to the app's data.

Called by tools/build_app_data.py (three lines there, so the phase that owns that
file keeps its diff small):

  join_claim_meta(s, files, topics, alias)
      every node file's claims in scope gain `meta` (who made the claim, when, by what
      route); every node that made claims gains `claimsMade`, the claims whose
      claimant it is, each with the topic it is read under.
  questions_out(s, bd, meta) -> (questions.json object, {id: record})
      research/questions/<id>.json as shipped: the authored record with every cited
      id resolved (the shape topics/<id>.json uses) and the threads it folds in.

verify.py checks what ships against research/_claim_meta.json and
research/questions/ by its own route and does not import this file.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools", "topics"))
import topiclib  # noqa: E402

META = os.path.join(ROOT, "research", "_claim_meta.json")
QDIR = os.path.join(ROOT, "research", "questions")
Q_TEXT_KEYS = ("lead", "answer", "for", "against", "threads")


def _rd(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def claim_meta():
    return (_rd(META).get("claims") or {}) if os.path.exists(META) else {}


def _first_url(s):
    import re
    m = re.search(r"https?://[^\s)\]]+", s or "")
    return m.group(0) if m else None


def _host(url):
    import re
    m = re.match(r"https?://([^/?#:]+)", url or "")
    return m.group(1).lower() if m else None


def _source_row(text):
    url = _first_url(text)
    return {"domain": _host(url), "text": text, "url": url}


def claim_topics(topics, alias, appears):
    """claim id -> the topic it is read under: the first topic (by id) whose prose
    cites it; else None, and the caller falls back to the claim's node's primary
    topic."""
    by = {}
    for t in sorted(topics, key=lambda t: t["id"]):
        for cid in topiclib.cited_ids(t):
            by.setdefault(cid, t["id"])
    return by


def join_claim_meta(s, files, topics, alias, appears):
    rows = claim_meta()
    cited_in = claim_topics(topics, alias, appears)
    made = {}
    for n in s.nodes:
        rec = files.get(n["id"])
        if rec and rec.get("claims"):
            # a copy: node_files shares the board's own claim objects
            rec["claims"] = [dict(c) for c in rec["claims"]]
        for c in (rec.get("claims") if rec else None) or []:
            m = rows.get(c.get("id"))
            if not m:
                continue
            who = m.get("claimant")
            c["meta"] = {
                "claimant": who,
                "claimantLabel": (s.byid.get(who) or {}).get("label") if who else None,
                "speaker": m.get("speaker"),
                "artefactDate": m.get("artefactDate"),
                "eventDate": m.get("eventDate"),
                "route": m.get("route"),
                "via": m.get("via"),
            }
            if not who:
                continue
            prim = (appears.get(n["id"]) or [[None]])[0][0]
            made.setdefault(who, []).append({
                "id": c["id"],
                "text": c.get("text"),
                "tier": c.get("tier"),
                "source": _source_row(c.get("source")),
                "node": n["id"],
                "nodeLabel": n.get("label"),
                "artefactDate": m.get("artefactDate"),
                "eventDate": m.get("eventDate"),
                "route": m.get("route"),
                "via": m.get("via"),
                "topic": cited_in.get(c["id"]) or prim,
            })
    for who, xs in made.items():
        xs.sort(key=lambda r: (r["topic"] or "~", r["artefactDate"] or "~", r["id"]))
        if who in files:
            files[who]["claimsMade"] = xs
    return made


# ------------------------------------------------------------------ questions

def load_questions():
    if not os.path.isdir(QDIR):
        return []
    out = []
    for f in sorted(os.listdir(QDIR)):
        if f.endswith(".json") and not f.startswith("_"):
            out.append(_rd(os.path.join(QDIR, f)))
    return sorted(out, key=lambda q: (q.get("order") or 99, q["id"]))


def q_items(q):
    """[(where, item)] for every citable item of a question."""
    out = []
    if q.get("lead") is not None:
        out.append(("lead", q["lead"]))
    for k in Q_TEXT_KEYS[1:]:
        for i, it in enumerate(q.get(k) or []):
            out.append(("%s[%d]" % (k, i), it))
    return out


def q_cited(q):
    seen = []
    for _w, it in q_items(q):
        for c in (it.get("cite") or []) if isinstance(it, dict) else []:
            if c not in seen:
                seen.append(c)
    return seen


def questions_out(s, bd, meta):
    qs = load_questions()
    recs = {}
    rows = []
    for q in qs:
        rec = {k: v for k, v in q.items() if not k.startswith("_")}
        for k in ("answer", "for", "against", "open", "threads", "topics"):
            rec.setdefault(k, [])
        rec["cites"] = {cid: (topiclib.resolve(bd, {}, cid, _source_row)
                              or {"id": cid, "kind": None, "missing": True})
                        for cid in q_cited(q)}
        recs[q["id"]] = rec
        lead = q.get("lead")
        rows.append({
            "id": q["id"], "title": q.get("title"), "order": q.get("order"),
            "status": q.get("status"),
            "lead": lead.get("text") if isinstance(lead, dict) else None,
            "counts": {k: len(q.get(k) or []) for k in ("answer", "for", "against", "open", "threads")},
            "threads": [t.get("id") for t in q.get("threads") or [] if isinstance(t, dict)],
            "topics": list(q.get("topics") or []),
        })
    return {"generated": meta["generated"], "source": meta["source"], "questions": rows}, recs
