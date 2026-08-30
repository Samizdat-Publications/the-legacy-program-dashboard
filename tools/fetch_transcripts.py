"""Pull YouTube transcripts into a LOCAL CACHE. Nothing here is ever committed.

WHY THIS RUNS ON STEWART'S MACHINE AND NOT IN A CLOUD SESSION.
YouTube blocks the transcript endpoint from datacenter IPs. Measured 30 August
2026 from the cloud container: youtube.com serves the homepage (HTTP 200) and the
transcript endpoint returns `IpBlocked`. It is not a rate limit and waiting does
not clear it. A residential IP -- an ordinary home connection -- is not blocked.

WHAT THE CACHE IS FOR, and what it is NOT for.
Stewart, 30 August 2026: "we don't need to publish the transcripts, just obtain
them and process them for leads." So:

  - the cache is a WORKING FILE, gitignored, like tools/.spot-cache/
  - the repo carries CLAIMS with a video id, a timestamp and a short quote
  - the transcript body is what a claim is checked against, never what ships

That is the same shape the board already uses for sourcing: a transcript is a
SOURCE, and the repo stores claims. It also keeps the licensing simple -- these
are somebody else's words and they stay on the machine that fetched them.

AUTO-TRANSCRIPTS ARE NOT QUOTABLE, and this is not a hypothetical. A prior session
on the sibling board chased "Holocron Engineering" out of a Gerb auto-transcript
and found the real entity was HoloChron LLC -- an Alabama company with a formation
date, a dissolution date and two named founders. The mistranscription was one
character from useless. Treat every proper noun as a lead to verify, never as a
quote to cite. CLAUDE.md section 2 has no exception for "the transcript said so".

USAGE (PowerShell 5.1, one command per line, `&&` is a syntax error):

    cd "C:\\Users\\stewa\\OneDrive\\Documents\\Claude\\Projects\\Missing individuals connected to defense contractors\\the-program"
    pip install youtube-transcript-api

    cd "C:\\Users\\stewa\\OneDrive\\Documents\\Claude\\Projects\\Missing individuals connected to defense contractors\\the-program"
    python tools\\fetch_transcripts.py --feed https://feeds.megaphone.fm/jessemichels

Then commit nothing and tell the session it is done; the cache is read from disk.
"""

import argparse
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "research", ".transcripts")

# A YouTube id is 11 characters of [A-Za-z0-9_-]. Anchored so a stray match inside
# a URL query string cannot masquerade as one.
_VID = re.compile(r"(?:v=|youtu\.be/|/embed/)([A-Za-z0-9_-]{11})(?![A-Za-z0-9_-])")


def ids_from_feed(url):
    """Every distinct video id an RSS feed mentions, in feed order.

    The Michels feed carries 140 episodes with descriptions and timestamped chapter
    lists; the YouTube links inside them are what this is after. Order is preserved
    so a partial run is resumable by eye.
    """
    with urllib.request.urlopen(url, timeout=120) as r:
        xml = r.read().decode("utf-8", "replace")
    seen, out = set(), []
    for m in _VID.finditer(xml):
        v = m.group(1)
        if v not in seen:
            seen.add(v)
            out.append(v)
    return out


def fetch(vid):
    """One transcript, as {id, segments:[{t, text}]}. Raises on failure."""
    from youtube_transcript_api import YouTubeTranscriptApi
    r = YouTubeTranscriptApi().fetch(vid)
    return {"id": vid,
            "segments": [{"t": round(s.start, 2), "text": s.text} for s in r]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed", help="RSS feed to harvest video ids from")
    ap.add_argument("--ids", nargs="*", default=[], help="explicit video ids")
    ap.add_argument("--out", default=CACHE)
    a = ap.parse_args()

    ids = list(a.ids)
    if a.feed:
        ids += [v for v in ids_from_feed(a.feed) if v not in ids]
    if not ids:
        sys.exit("nothing to fetch: pass --feed or --ids")

    os.makedirs(a.out, exist_ok=True)
    got = skipped = failed = 0
    for i, vid in enumerate(ids, 1):
        path = os.path.join(a.out, vid + ".json")
        if os.path.exists(path):
            skipped += 1
            continue
        try:
            d = fetch(vid)
        except Exception as e:
            # Named, not swallowed. A video with captions disabled is a fact about
            # that video; a block is a fact about the machine. They look identical
            # in a counter and completely different in a log.
            print("  !! %s  %s: %s" % (vid, type(e).__name__, str(e).split("\n")[0][:110]))
            failed += 1
            continue
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False)
        got += 1
        print("  ok  %s  %d segments" % (vid, len(d["segments"])))

    print("\n%d fetched, %d already cached, %d failed, of %d ids"
          % (got, skipped, failed, len(ids)))
    print("cache: %s" % a.out)
    print("This directory is gitignored on purpose. Do not commit it.")


if __name__ == "__main__":
    main()
