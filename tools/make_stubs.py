#!/usr/bin/env python3
"""
make_stubs.py — define every id that the board references but never defines.

Two kinds of output, and the difference matters:

  * RESEARCH DOMAINS (d-*) get real, hand-written descriptions. They are the
    taxonomy the whole scoring system hangs off, and a scored axis that points at
    an undefined domain is a broken promise to the reader.

  * LOCATIONS and ORGANISATIONS get structural stubs with `desc: null`. That is
    the parent board's own convention: the dock prints a null desc as a STATED
    GAP rather than as empty space. A stub is an honest "no dossier written yet",
    not a fake dossier. They land in the wave-3 queue.

Writes research/_stubs.json, which merge.py then picks up like any other domain file.
"""

import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --------------------------------------------------------------------------
# Research domains — written by hand. These carry editorial weight: each one
# names the documented dual-use route from an ordinary field into classified
# work, which is what a score on that axis is actually asserting.
# --------------------------------------------------------------------------
DOMAINS = {
    "d-witness": (
        "Witness testimony", "Evidence domain",
        "The domain of firsthand and secondhand testimony about the program: what a named "
        "individual states they saw, handled, were briefed on, or were denied access to. It is "
        "the domain that carries the most weight in public argument and the least in documentary "
        "terms, which is exactly why it is scored separately here. A person scored on this domain "
        "is not being credited with proof; they are being placed in a chain of attestation whose "
        "links can be traced, dated, and checked against each other. The strongest form is sworn "
        "testimony before Congress or a signed Inspector General complaint, because those carry "
        "criminal exposure for falsification and are themselves primary records of the statement "
        "having been made."),
    "d-research": (
        "Research & academia", "Institutional domain",
        "University and institute research, and the documented routes by which it connects to "
        "classified work: sponsored research agreements, DoD and IC grant funding, cleared faculty, "
        "university-affiliated research centers, and consulting arrangements that never appear on a "
        "CV. The relevance is structural rather than incriminating. An academic post is one of the "
        "few positions that provides deep technical capability alongside a plausible public identity, "
        "and the FFRDC and UARC system exists precisely to formalise that bridge."),
    "d-funding": (
        "Funding & contracts", "Money domain",
        "The contracting and appropriations layer: who received money, from which line, under which "
        "vehicle, and with what reporting obligation. This is the most documentable domain on the "
        "board — award data, contract numbers and appropriations text are public records — and it is "
        "therefore where an argument about the program is strongest. Where the money trail goes dark, "
        "that darkness is itself a documented fact with a date and a mechanism attached to it."),
    "d-money": (
        "Black budget", "Money domain",
        "The specific mechanics of concealed appropriation: classified annexes to the NDAA and "
        "appropriations acts, the National Intelligence Program and Military Intelligence Program "
        "toplines, pass-through and unallocated line items, reprogramming and transfer authority, "
        "and the accounting treatments that permit classified activity to be reported in modified "
        "form. Distinct from d-funding, which tracks identifiable awards; this domain tracks the "
        "instruments that make an award unidentifiable."),
    "d-international": (
        "International programs", "Geographic domain",
        "Foreign government UAP programs, investigations and document releases: the UK Ministry of "
        "Defence desk and the Condign report, France's GEIPAN and the COMETA study, Brazil's air "
        "force investigations and archive transfers, Chile's CEFAA, Canada's Project Magnet and "
        "Second Storey, and the Soviet and Russian programs. Their value to this board is "
        "comparative: several of these states have released their files, which establishes both "
        "what a government record on this subject looks like when it is opened and, by contrast, "
        "the scale of what remains closed in the United States."),
    "d-aviators": (
        "Military aviation", "Observational domain",
        "Naval and Air Force aircrew, radar operators, and the sensor and reporting systems that "
        "capture encounters: FLIR and ATFLIR pods, AN/SPY radar, range-fouler reporting, and the "
        "safety-reporting chain. Aviators occupy an unusual evidentiary position — they are trained "
        "observers, their instruments produce records, and their accounts are frequently the only "
        "part of the story that the government has been willing to confirm."),
    "d-ic": (
        "Intelligence community", "Institutional domain",
        "Career intelligence work across the eighteen IC elements: collection, all-source analysis, "
        "counterintelligence, and the special access and controlled access program structures that "
        "govern what any given officer may know. A person scored here holds the specific kind of "
        "access the board is trying to measure — not technical capability, but knowledge of what is "
        "compartmented and from whom."),
    "d-astro": (
        "Astronomy & astrophysics", "Technical domain",
        "Observational astronomy, astrophysics and the instrumentation behind them. The dual-use "
        "route is direct and well documented: faint-signal detection, adaptive optics, image "
        "processing and sensor characterisation transfer without modification to overhead "
        "reconnaissance, which is why the discipline has a long history of classified consulting "
        "and of recruitment into advisory bodies such as JASON."),
    "d-paranormal": (
        "Anomalous phenomena", "Research domain",
        "Research into anomalous phenomena that the government has itself funded at various points: "
        "remote viewing under Grill Flame, Center Lane and Stargate; the National Institute for "
        "Discovery Science work; and the poltergeist and physiological-effects reporting that AAWSAP "
        "collected at Skinwalker Ranch. Its presence on this board is not an endorsement of the "
        "phenomena but a record of the documented fact that federal money was spent studying them."),
    "d-bio": (
        "Biology & biotechnology", "Technical domain",
        "Biological and biomedical research, including the physiological-effects reporting attached "
        "to close-encounter cases, the anomalous health incident literature, and the tissue and "
        "materials analysis claims. The domain matters here chiefly because the program allegations "
        "include biological recoveries, which would place biologists in a custody chain that no "
        "public contract record reflects."),
    "d-nuclear": (
        "Nuclear", "Technical domain",
        "Nuclear weapons design, stewardship, propulsion and the facilities that house them. The "
        "documented correlation between UAP incidents and nuclear installations — Malmstrom, Minot, "
        "the 1975 Strategic Air Command overflights, Kirtland and Manzano — makes this the single "
        "most persistent geographic and institutional pattern in the entire record."),
    "d-medical": (
        "Medicine & clinical", "Technical domain",
        "Clinical medicine, radiology and the medical records that attach to encounter cases — the "
        "Cash-Landrum injuries, the Rendlesham exposure claims and John Burroughs' subsequent records "
        "battle with the Veterans Administration. Medical records are unusually valuable evidence "
        "because they are contemporaneous, independently generated, and hard to retroactively edit."),
}

# --------------------------------------------------------------------------
# Location labels. Derived from the id, then corrected where the id is opaque.
# --------------------------------------------------------------------------
LOC_FIX = {
    "l-dc": "Washington, DC", "l-washington-dc": "Washington, DC",
    "l-nyc": "New York, NY", "l-la": "Los Angeles, CA",
    "l-ft-meade": "Fort Meade, MD", "l-uk-mod-whitehall": "Whitehall, London (UK MoD)",
    "l-san-agustin": "Plains of San Agustin, NM", "l-woodshole": "Woods Hole, MA",
    "l-oro-valley": "Oro Valley, AZ", "l-windsor-co": "Windsor, CO",
    "l-gilbert-az": "Gilbert, AZ", "l-boise-id": "Boise, ID",
    "l-fort-worth-tx": "Fort Worth, TX", "l-huffman-tx": "Huffman, TX",
    "l-parkland-fl": "Parkland, FL", "l-charleston-sc": "Charleston, SC",
    "l-franklin-tn": "Franklin, TN", "l-takoma-park": "Takoma Park, MD",
    "l-glenbeulah": "Glenbeulah, WI", "l-michigan-state": "East Lansing, MI",
    "l-aztec": "Aztec, NM", "l-varginha": "Varginha, Minas Gerais, Brazil",
    "l-brasilia": "Brasília, Brazil", "l-uk": "United Kingdom",
    "l-france": "France", "l-brazil": "Brazil",
}

FOREIGN = {"l-brasilia", "l-paris", "l-toulouse", "l-ottawa", "l-santiago", "l-moscow",
           "l-london", "l-stockholm", "l-uk", "l-france", "l-brazil", "l-varginha",
           "l-fredericton", "l-sheffield", "l-uk-mod-whitehall"}

ORG_FIX = {
    "pogo": ("Project On Government Oversight", "media", "Watchdog organisation"),
    "the-intercept": ("The Intercept", "media", "News organisation"),
    "saf-aaz": ("SAF/AAZ — Air Force Declassification & Special Programs", "ic", "USAF secretariat office"),
    "wayne-state-university": ("Wayne State University", "research", "Academic"),
    "vanderbilt-university": ("Vanderbilt University", "research", "Academic"),
    "sheffield-hallam": ("Sheffield Hallam University", "research", "Academic"),
    "blue-marble-space-institute": ("Blue Marble Space Institute of Science", "research", "Research institute"),
    "enigma-labs": ("Enigma Labs", "media", "UAP reporting platform"),
    "us-navy": ("United States Navy", "ic", "Military service"),
    "canada-dot": ("Canada Department of Transport", "ic", "Foreign government agency"),
    "dgac-chile": ("DGAC Chile — Dirección General de Aeronáutica Civil", "ic", "Foreign government agency"),
    "ocsa-canada": ("Office of the Chief Science Advisor of Canada", "ic", "Foreign government agency"),
    "soyuzufotsentr": ("Soyuzufotsentr", "research", "Russian UFO research body"),
    "izmiran": ("IZMIRAN — Pushkov Institute of Terrestrial Magnetism", "research", "Russian research institute"),
    "senado-brasil": ("Senado Federal do Brasil", "oversight", "Foreign legislature"),
    "hospital-regional-varginha": ("Hospital Regional de Varginha", "other", "Medical facility"),
    "509th-bomb-group": ("509th Bomb Group", "legacy", "USAAF unit"),
    "ndaa-fy2023": ("National Defense Authorization Act for Fiscal Year 2023", "oversight", "Statute"),
}


def label_from_id(i):
    s = re.sub(r"^[a-z]-", "", i).replace("-", " ")
    return " ".join(w.upper() if len(w) <= 3 and w.isalpha() and w in
                    {"dc", "us", "uk", "nm", "ny", "ca", "tx", "fl", "sc", "tn", "md",
                     "wi", "mi", "az", "co", "id", "ia", "ma"} else w.capitalize()
                    for w in s.split())


STUB_NOTE = ("Referenced by the board but no dossier written yet. This node exists so the "
             "graph resolves and so the gap is visible rather than silent — see the wave-3 queue.")


def main():
    missing = json.load(open("/tmp/missing.json"))
    ents = []

    for did, (label, sub, desc) in DOMAINS.items():
        ents.append({
            "id": did, "cls": "domain", "label": label, "cluster": "research", "sub": sub,
            "desc": desc, "tier": "C", "C": 0, "A": 0, "D": 0,
            "claims": [],
            "sources": [
                {"name": "NSF master government list of FFRDCs", "url": "https://www.nsf.gov/statistics/ffrdclist/", "date": "2026-08-12"},
                {"name": "Domain definition written for this board; see SCHEMA.md", "url": "", "date": "2026-08-12"},
            ],
        })

    for mid, (count, kind) in missing.items():
        if mid in DOMAINS:
            continue
        if mid.startswith("d-"):
            ents.append({"id": mid, "cls": "domain", "label": label_from_id(mid),
                         "cluster": "research", "sub": "Research domain", "desc": None,
                         "tier": "C", "C": 0, "A": 0, "D": 0,
                         "claims": [{"tier": 3, "text": STUB_NOTE, "source": "Board bookkeeping"}],
                         "sources": []})
        elif mid.startswith("l-"):
            ents.append({"id": mid, "cls": "location",
                         "label": LOC_FIX.get(mid, label_from_id(mid)),
                         "cluster": "other" if mid in FOREIGN else "other",
                         "sub": "Foreign location" if mid in FOREIGN else "Location",
                         "desc": None, "tier": "C", "C": 0, "A": 0, "D": 0,
                         "claims": [{"tier": 3, "text": STUB_NOTE, "source": "Board bookkeeping"}],
                         "sources": []})
        else:
            lbl, cluster, sub = ORG_FIX.get(mid, (label_from_id(mid), "other", "Organisation"))
            cls = "legislation" if "ndaa" in mid or "act" in mid else "institution"
            ents.append({"id": mid, "cls": cls, "label": lbl, "cluster": cluster, "sub": sub,
                         "desc": None, "tier": "C", "C": 0, "A": 0, "D": 0,
                         "claims": [{"tier": 3, "text": STUB_NOTE, "source": "Board bookkeeping"}],
                         "sources": []})

    out = {"domain": "_stubs", "people": [], "entities": ents, "edges": [],
           "timeline": [], "entityInfo": {},
           "gaps": [f"{e['id']} — structural stub, needs a real dossier"
                    for e in ents if e["desc"] is None]}

    path = os.path.join(ROOT, "research", "_stubs.json")
    json.dump(out, open(path, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    written = sum(1 for e in ents if e["desc"])
    print(f"wrote {len(ents)} stub entities to {path}")
    print(f"  {written} with real descriptions (research domains)")
    print(f"  {len(ents) - written} structural stubs with desc:null (wave-3 queue)")


if __name__ == "__main__":
    main()
