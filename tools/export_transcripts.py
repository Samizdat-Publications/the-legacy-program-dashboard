#!/usr/bin/env python3
"""Turn the transcript cache into readable files a person or NotebookLM can use.

WHY THIS IS SEPARATE FROM THE CACHE
-----------------------------------
`research/.transcripts/*.json` is a WORKING cache: one object per episode holding
a few thousand `{"t": seconds, "text": "..."}` segments, each a few words long. It
is the right shape for grep, for `read_transcript.py`, and for a research pass
looking for a phrase. It is the wrong shape for reading, and the wrong shape for
anything that ingests documents -- a thousand two-second fragments is not prose.

This writes the other shape: one Markdown file per episode, segments merged into
paragraphs, with a timestamp marker every so often so a quote can still be found
in the audio.

    python3 tools/export_transcripts.py                      # everything cached
    python3 tools/export_transcripts.py --show michels
    python3 tools/export_transcripts.py --out ~/transcripts

WHERE THE FILES GO, AND WHY THAT MATTERS
----------------------------------------
Default `dist/transcripts/`, which is gitignored like the cache. Stewart's
standing instruction is that the transcripts are not published -- "we don't need
to publish the transcripts, just obtain them and process them for leads" -- so
nothing here is ever committed. Point `--out` at a real folder to keep them.

**A cloud container is reclaimed without warning.** Transcripts produced in one
are gone with it. If they are wanted permanently, run `fetch_podcast.py` on a
machine that persists, or export with `--out` to somewhere synced. The podcast
route works from any IP, which is the whole reason it exists.

NOTEBOOKLM
----------
One file per episode is the right granularity: NotebookLM caps a single source at
roughly half a million words, and this catalogue is several million. `--index`
also writes a contents file listing every episode with its date and duration, so
a reader can see the shape of the corpus without opening 140 documents.
"""
import argparse, json, os, re, sys, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "research", ".transcripts")
OUT = os.path.join(ROOT, "dist", "transcripts")

# A paragraph break every ~45s of speech reads about right: long enough not to be
# choppy, short enough that a timestamp is never far from a quote.
PARA_SECONDS = 45


def hhmmss(t):
    t = int(t)
    return "%d:%02d:%02d" % (t // 3600, (t % 3600) // 60, t % 60)


def slug(s, n=70):
    s = re.sub(r"[^\w\s-]", "", s or "").strip()
    s = re.sub(r"[\s_-]+", "-", s).lower()
    return s[:n].strip("-") or "episode"


def to_markdown(d):
    """Segments -> paragraphs with periodic timestamps."""
    segs = d.get("segments") or []
    title = (d.get("title") or d.get("id") or "").strip()
    lines = ["# %s" % title, ""]
    meta = []
    if d.get("show"):
        meta.append("**Show:** %s" % d["show"])
    if d.get("date"):
        meta.append("**Published:** %s" % d["date"])
    if segs:
        meta.append("**Duration:** %s" % hhmmss(segs[-1]["t"]))
    meta.append("**Transcript:** machine-generated (faster-whisper), not corrected")
    if d.get("audio"):
        meta.append("**Audio:** %s" % d["audio"])
    lines += [" · ".join(meta[:3]), "", *meta[3:], "", "---", ""]

    buf, start = [], None
    for s in segs:
        if start is None:
            start = s["t"]
        buf.append(s["text"].strip())
        if s["t"] - start >= PARA_SECONDS:
            lines.append("**[%s]** %s" % (hhmmss(start), " ".join(buf).strip()))
            lines.append("")
            buf, start = [], None
    if buf:
        lines.append("**[%s]** %s" % (hhmmss(start or 0), " ".join(buf).strip()))
        lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cache", default=CACHE)
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--show", help="only episodes whose id starts with this prefix")
    ap.add_argument("--index", action="store_true", default=True,
                    help="also write CONTENTS.md (default on)")
    a = ap.parse_args()

    pat = os.path.join(a.cache, (a.show + "-*" if a.show else "*") + ".json")
    files = sorted(glob.glob(pat))
    if not files:
        print("no transcripts in %s%s" % (a.cache, " for --show " + a.show if a.show else ""),
              file=sys.stderr)
        return 1

    os.makedirs(a.out, exist_ok=True)
    rows, written, words = [], 0, 0
    for f in files:
        try:
            d = json.load(open(f, encoding="utf-8"))
        except Exception as e:
            print("  !! %s: %s" % (os.path.basename(f), e), file=sys.stderr)
            continue
        if not d.get("segments"):
            continue
        md = to_markdown(d)
        words += len(md.split())
        # Date first, so the directory sorts chronologically in any file browser.
        date = ""
        m = re.search(r"(\d{1,2})\s+(\w{3})\s+(\d{4})", d.get("date") or "")
        if m:
            mo = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05",
                  "Jun": "06", "Jul": "07", "Aug": "08", "Sep": "09", "Oct": "10",
                  "Nov": "11", "Dec": "12"}.get(m.group(2), "00")
            date = "%s-%s-%02d " % (m.group(3), mo, int(m.group(1)))
        name = "%s%s.md" % (date, slug(d.get("title") or d.get("id")))
        with open(os.path.join(a.out, name), "w", encoding="utf-8") as fh:
            fh.write(md)
        written += 1
        rows.append((date.strip() or "?", hhmmss(d["segments"][-1]["t"]),
                     d.get("title") or d.get("id"), name))

    if a.index and rows:
        with open(os.path.join(a.out, "CONTENTS.md"), "w", encoding="utf-8") as fh:
            fh.write("# Transcripts\n\n")
            fh.write("%d episodes, machine-generated with faster-whisper and not "
                     "corrected. Times are into the episode.\n\n" % len(rows))
            fh.write("| date | length | episode |\n|---|---|---|\n")
            for date, dur, title, name in sorted(rows, reverse=True):
                safe = title.replace("|", "\\|")
                fh.write("| %s | %s | [%s](%s) |\n" % (date, dur, safe, name))

    print("%d episode(s) -> %s" % (written, a.out))
    print("about %s words in total" % f"{words:,}")
    if a.index and rows:
        print("contents: %s" % os.path.join(a.out, "CONTENTS.md"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
