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

    cd "C:\\Users\\stewa\\ClaudeProjects\\Missing individuals connected to defense contractors\\the-program"
    pip install youtube-transcript-api

    cd "C:\\Users\\stewa\\ClaudeProjects\\Missing individuals connected to defense contractors\\the-program"
    python tools\\fetch_transcripts.py --feed https://feeds.megaphone.fm/jessemichels

Then commit nothing and tell the session it is done; the cache is read from disk.

TWO STEPS, NOT ONE, FOR A BACK CATALOGUE.
The first pull of 25 episodes returned a guided breathing session, an interview
with a co-founder of Tinder, and a debate about archaeology. Four of nine files
in one slice were off topic. Fetching a hundred transcripts to discover that is
a waste of a residential connection and of an afternoon, so:

    step 1   --catalog   enumerate the channel: id, title, date, duration.
                         Writes research/leads/<name>-catalog.json, which IS
                         committed -- it is metadata, not anybody's words.
    step 2   --select    fetch transcripts for a chosen id list only.

Between them a session reads the catalogue and triages it by title and date.
That is cheap, it is reversible, and it means the transcripts that do get pulled
are the ones somebody decided were worth reading.

    python tools\\fetch_transcripts.py --catalog https://www.youtube.com/@JesseMichels --since 2025-01-01
    python tools\\fetch_transcripts.py --select research\\leads\\michels-selected.txt
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

# A bare id, anchored. Used to validate a selection file before spending
# requests on it.
_ID_OK = re.compile(r"^[A-Za-z0-9_-]{11}$")


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


def catalog_ytdlp(url):
    """The full channel listing via yt-dlp, if it is installed.

    `--flat-playlist` does not download anything; it enumerates. This is the only
    route that reaches a whole back catalogue -- YouTube's own channel RSS caps
    at the 15 most recent videos, which is useless for a year of episodes.
    """
    import subprocess
    # `pip install yt-dlp` puts the MODULE on the path and the SCRIPT in a
    # per-user Scripts directory that is often not on PATH -- which is exactly
    # what happened on Stewart's machine: pip said "Requirement already
    # satisfied" and this function still returned None. So try the executable,
    # then the module, then the Windows launcher, and only give up after all
    # three. Report which one worked.
    argv = ["--flat-playlist", "--dump-json", "--ignore-errors", url]
    attempts = [
        ["yt-dlp"] + argv,
        [sys.executable, "-m", "yt_dlp"] + argv,
        ["py", "-m", "yt_dlp"] + argv,
    ]
    r = None
    for cmd in attempts:
        try:
            r = subprocess.run(cmd, capture_output=True, timeout=1800)
        except (FileNotFoundError, OSError):
            continue
        if r.stdout:
            print("  enumerating with: %s" % " ".join(cmd[:3]))
            break
    if r is None:
        return None
    if r.returncode != 0 and not r.stdout:
        sys.stderr.write((r.stderr or b"").decode("utf-8", "replace")[-600:] + "\n")
        return None
    out = []
    for line in (r.stdout or b"").decode("utf-8", "replace").splitlines():
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if not d.get("id"):
            continue
        # yt-dlp gives upload_date on some extractors and timestamp on others;
        # a flat playlist often has neither. Record what is there, invent nothing.
        date = d.get("upload_date")
        if date and len(date) == 8:
            date = "%s-%s-%s" % (date[:4], date[4:6], date[6:])
        out.append({"id": d["id"], "title": d.get("title") or "",
                    "date": date, "duration": d.get("duration"),
                    "url": d.get("webpage_url") or d.get("url")})
    return out or None


_ITEM = re.compile(r"<item>(.*?)</item>", re.S)
_TITLE = re.compile(r"<title>\s*(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?\s*</title>", re.S)
_PUB = re.compile(r"<pubDate>\s*(.*?)\s*</pubDate>", re.S)


_DUR = re.compile(r"<itunes:duration>\s*(.*?)\s*</itunes:duration>", re.S)


def _norm_title(t):
    """Loose enough to survive punctuation and entity differences."""
    t = re.sub(r"&(amp|quot|#39|apos|nbsp);", " ", t or "")
    return re.sub(r"[^a-z0-9]+", "", t.lower())


def catalog_feed(url, verify=True):
    """Every episode in a podcast feed: title, date, duration, and an id ONLY
    where the pairing can be proven.

    THE PAIRING IS THE WHOLE PROBLEM. An episode's show notes link other people's
    videos -- sponsors, references, the guest's own channel -- so "the first
    YouTube id inside this <item>" is not the episode's video. The first version
    of this function did exactly that and produced a catalogue in which
    `h7CJoGKvx3U` carried a Michels episode title while actually being "Joe Rogan
    Experience #1945 - Eric Weinstein" on PowerfulJRE. Of 24 ids paired that way,
    11 belonged to other channels entirely.

    So every candidate is resolved through oEmbed and kept only if the video's
    real title matches the feed item's. A mismatch is recorded as `id: None` with
    the reason, never silently dropped and never silently kept: an episode with no
    id is a fact about what this feed can tell us, and it is the reason a full
    back catalogue needs yt-dlp against the channel rather than the feed.
    """
    with urllib.request.urlopen(url, timeout=180) as r:
        xml = r.read().decode("utf-8", "replace")
    out = []
    for m in _ITEM.finditer(xml):
        block = m.group(1)
        t = _TITLE.search(block)
        title = (t.group(1).strip() if t else "")
        p = _PUB.search(block)
        date = None
        if p:
            try:
                from email.utils import parsedate_to_datetime
                date = parsedate_to_datetime(p.group(1)).date().isoformat()
            except Exception:
                date = None
        d = _DUR.search(block)
        row = {"id": None, "title": title, "date": date,
               "duration": (d.group(1) if d else None), "url": None, "note": None}
        cand = _VID.search(block)
        if cand:
            vid = cand.group(1)
            if not verify:
                row["id"] = vid
            else:
                r2 = oembed(vid)
                if r2.get("error"):
                    row["note"] = "unresolved candidate %s (%s)" % (vid, r2["error"])
                elif _norm_title(r2.get("title")) == _norm_title(title):
                    row["id"] = vid
                    row["url"] = "https://www.youtube.com/watch?v=" + vid
                else:
                    row["note"] = ("candidate %s is %r on %s -- a linked video, "
                                   "not this episode" % (vid, (r2.get("title") or "")[:60],
                                                         r2.get("channel")))
        out.append(row)
    return out


def oembed(vid, timeout=30):
    """The AUTHORITATIVE title and channel for a video id.

    YouTube's oEmbed endpoint answers from this container even though the
    transcript endpoint is IP-blocked -- they are different services and only one
    of them is defended. It needs no key.

    THIS EXISTS BECAUSE THE FEED PAIRING IS A LIE. `catalog_feed` takes the first
    YouTube link inside an <item>, and a show-notes block links other people's
    videos. Resolving the first pull that way paired `h7CJoGKvx3U` with a Michels
    episode title; oEmbed says it is "Joe Rogan Experience #1945 - Eric Weinstein"
    on PowerfulJRE, which is what the transcript itself opens by saying. Four of
    four spot-checks contradicted the feed. Never publish a title from the feed
    pairing; resolve it.
    """
    url = ("https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v="
           + vid + "&format=json")
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            d = json.loads(r.read().decode("utf-8", "replace"))
    except Exception as e:
        return {"id": vid, "title": None, "channel": None,
                "error": "%s: %s" % (type(e).__name__, str(e)[:90])}
    return {"id": vid, "title": d.get("title"), "channel": d.get("author_name"),
            "channel_url": d.get("author_url")}


def resolve_ids(ids):
    """oEmbed every id, in order, reporting failures rather than dropping them."""
    out = []
    for i, v in enumerate(ids, 1):
        r = oembed(v)
        out.append(r)
        mark = "!!" if r.get("error") else "ok"
        print("  %s  %-13s %-26s %s" % (mark, v, (r.get("channel") or "-")[:26],
                                        (r.get("title") or r.get("error") or "")[:76]))
    return out


def write_catalog(rows, path, since=None):
    # Deduplicate on id ONLY where there is an id. Keying on it unconditionally
    # collapsed every episode whose id could not be verified into a single row --
    # 140 episodes became 2, and the count printed underneath looked deliberate.
    seen, keep = set(), []
    for r in rows:
        rid = r.get("id")
        if rid:
            if rid in seen:
                continue
            seen.add(rid)
        if since and r.get("date") and r["date"] < since:
            continue
        keep.append(r)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"generated": None, "count": len(keep), "items": keep}, fh,
                  ensure_ascii=False, indent=1)
    withid = sum(1 for r in keep if r.get("id"))
    if withid != len(keep):
        print("  %d of %d carry a VERIFIED YouTube id. The rest are episodes this"
              % (withid, len(keep)))
        print("  feed lists without linking their own video -- enumerate the")
        print("  channel with yt-dlp to get those.")
    undated = sum(1 for r in keep if not r.get("date"))
    print("%d videos -> %s" % (len(keep), path))
    if since:
        print("  filtered to on or after %s" % since)
    if undated:
        print("  %d carry NO date -- a flat listing often omits it. They were kept,"
              % undated)
        print("  because dropping a video for having no date would silently shrink")
        print("  the catalogue in a way nobody could see.")
    print("\nCommit this file. It is titles and ids, not transcripts.")
    return keep


def fetch(vid):
    """One transcript, as {id, segments:[{t, text}]}. Raises on failure."""
    from youtube_transcript_api import YouTubeTranscriptApi
    r = YouTubeTranscriptApi().fetch(vid)
    return {"id": vid,
            "segments": [{"t": round(s.start, 2), "text": s.text} for s in r]}


def _ytdlp_argv():
    """However yt-dlp can be invoked on this machine, cheapest first."""
    return [["yt-dlp"], [sys.executable, "-m", "yt_dlp"], ["py", "-m", "yt_dlp"]]


# Set once, when a cookie source turns out to be unusable, so the warning is
# printed once and every later video simply goes without cookies instead of
# failing for a reason that has nothing to do with the video.
_COOKIES_DEAD = [False]

# Every way a cookie source can be unusable. These are properties of the
# BROWSER, not of the video, so any of them means "stop asking for cookies"
# rather than "this video failed".
#
# `dpapi` is the one that matters most on Windows: since Chrome 127 the cookie
# file is sealed with App-Bound Encryption and yt-dlp cannot decrypt it at all
# (yt-dlp issue 10927). Closing Chrome does not help -- there is nothing to
# wait for. Firefox is unaffected.
_COOKIE_FAIL = ("could not copy", "cookie database", "unsupported platform",
                "could not find", "permission denied",
                "dpapi", "failed to decrypt", "app-bound")


def fetch_ytdlp(vid, cookies_from=None, sleep_requests=2, timeout=300):
    """The same transcript, via yt-dlp. Slower, and much harder to block.

    WHY THIS EXISTS. youtube_transcript_api talks to the caption endpoint
    directly and YouTube rate-limits that endpoint hard: after a burst it
    answers IpBlocked for every request from that address, for hours, and no
    amount of retrying helps. yt-dlp goes through the ordinary player API,
    throttles itself with --sleep-requests, and can carry the cookies of a
    signed-in browser -- which is also the only way to reach a members-only
    video, the other failure in that run (VideoUnplayable).

    `--skip-download` means no audio or video is fetched: this pulls the
    caption track and nothing else.

    json3 is asked for because it carries start times in milliseconds. The
    fallback to vtt exists because not every video offers json3, and a vtt
    timestamp parsed to the second is still a citable position.
    """
    import glob as _glob
    import shutil
    import subprocess
    import tempfile

    tmp = tempfile.mkdtemp(prefix="ytsub-")
    try:
        argv = ["--skip-download", "--write-auto-subs", "--write-subs",
                "--sub-langs", "en.*,en", "--sub-format", "json3/vtt/best",
                "--sleep-requests", str(sleep_requests),
                "--retries", "3", "--no-warnings",
                "-o", os.path.join(tmp, "%(id)s.%(ext)s"),
                "https://www.youtube.com/watch?v=" + vid]
        use_cookies = cookies_from and not _COOKIES_DEAD[0]

        def run(with_cookies):
            av = (["--cookies-from-browser", cookies_from] + argv) if with_cookies else argv
            for base in _ytdlp_argv():
                try:
                    return subprocess.run(base + av, capture_output=True, timeout=timeout)
                except (FileNotFoundError, OSError):
                    continue
            return None

        last = run(use_cookies)
        if last is None:
            raise RuntimeError("yt-dlp is not installed")

        # A LOCKED COOKIE DATABASE IS NOT A PROPERTY OF THE VIDEO.
        # Chrome holds its cookie file open on Windows even after the last
        # window closes, because it keeps running in the tray. Without this,
        # every one of 169 videos fails with the same message about a file
        # yt-dlp could not copy, which says nothing about any of them.
        # Fall back to no cookies, once, loudly. Members-only videos will
        # still fail -- those genuinely need a signed-in session -- but
        # everything public is fetched instead of lost.
        if use_cookies and last.returncode != 0:
            err = (last.stderr or b"").decode("utf-8", "replace").lower()
            if any(k in err for k in _COOKIE_FAIL):
                _COOKIES_DEAD[0] = True
                if "dpapi" in err or "decrypt" in err or "app-bound" in err:
                    print("  .. %s cookies cannot be decrypted. Since Chrome 127 the"
                          % cookies_from)
                    print("     cookie file is sealed with App-Bound Encryption and")
                    print("     yt-dlp cannot read it -- closing the browser does not")
                    print("     help. Use --cookies-from-browser firefox if you have")
                    print("     Firefox signed in to YouTube.")
                else:
                    print("  .. cookies from %s are not readable (the browser is still"
                          % cookies_from)
                    print("     running, or holds the file open).")
                print("     Continuing WITHOUT cookies: public videos will fetch,")
                print("     members-only ones will not.", flush=True)
                last = run(False)

        files = sorted(_glob.glob(os.path.join(tmp, "*")))
        j = [f for f in files if f.endswith(".json3")]
        v = [f for f in files if f.endswith(".vtt")]
        if j:
            return {"id": vid, "segments": _parse_json3(j[0])}
        if v:
            return {"id": vid, "segments": _parse_vtt(v[0])}
        err = (last.stderr or b"").decode("utf-8", "replace").strip().splitlines()
        raise RuntimeError(err[-1][:160] if err else "yt-dlp wrote no subtitle file")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _parse_json3(path):
    with open(path, encoding="utf-8") as fh:
        d = json.load(fh)
    out = []
    for ev in d.get("events") or []:
        segs = ev.get("segs")
        if not segs:
            continue
        text = "".join(x.get("utf8", "") for x in segs).strip()
        if text and text != "\n":
            out.append({"t": round((ev.get("tStartMs") or 0) / 1000.0, 2), "text": text})
    return out


_VTT_T = re.compile(r"(\d{2}):(\d{2}):(\d{2})[.,](\d{3})\s*-->")


def _parse_vtt(path):
    out, t = [], None
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            line = line.rstrip("\n")
            m = _VTT_T.search(line)
            if m:
                h, mi, sec, ms = (int(x) for x in m.groups())
                t = round(h * 3600 + mi * 60 + sec + ms / 1000.0, 2)
                continue
            if t is None or not line.strip():
                continue
            if line.strip().upper() in ("WEBVTT",) or line.strip().isdigit():
                continue
            txt = re.sub(r"<[^>]+>", "", line).strip()
            if txt:
                out.append({"t": t, "text": txt})
    return out


def _run_pass(ids, a, announce=False):
    """One sweep over the ids. Returns a tally; never raises on a video.

    Anything already in the cache is skipped, so a pass is safe to repeat and
    a re-run costs nothing for work already done. That is what makes the
    overnight loop below simply a matter of calling this again.
    """
    import time
    got = skipped = failed = blocked = members = 0
    run429 = 0
    for i, vid in enumerate(ids, 1):
        path = os.path.join(a.out, vid + ".json")
        if os.path.exists(path):
            skipped += 1
            continue
        if a.sleep and (got or failed):
            time.sleep(a.sleep)
        try:
            if a.ytdlp or a.cookies:
                d = fetch_ytdlp(vid, a.cookies, max(2, int(a.sleep or 2)))
            else:
                d = fetch(vid)
        except Exception as e:
            name = type(e).__name__
            msg = str(e).split("\n")[0]
            print("  !! %s  %s: %s" % (vid, name, msg[:110]), flush=True)
            failed += 1

            low = msg.lower()
            # MEMBERS-ONLY IS NOT A RATE LIMIT, and must not be counted as one:
            # it is a permanent property of the video, it will fail identically
            # on every future run, and it says nothing about the connection.
            if "members-only" in low or "join this channel" in low:
                members += 1
                run429 = 0
                continue

            rate = ("429" in low or "too many requests" in low
                    or "IpBlocked" in name or "TooManyRequests" in name)
            if not rate:
                run429 = 0
                continue

            blocked += 1
            run429 += 1
            if announce and not (a.ytdlp or a.cookies) and blocked == 3:
                print("\n  Three IP blocks. YouTube rate-limits the caption endpoint")
                print("  per address. Re-run with --ytdlp --sleep 2, which goes")
                print("  through the player API and throttles itself.\n")
            # STOP. Every further request extends the block rather than working
            # around it, and there are 169 of them in this list.
            if run429 >= 5:
                print("  .. five rate limits in a row; ending this pass.", flush=True)
                break
            continue
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False)
        got += 1
        run429 = 0
        print("  ok  %s  %d segments" % (vid, len(d["segments"])), flush=True)

    print("\n%d fetched, %d already cached, %d failed, of %d ids"
          % (got, skipped, failed, len(ids)), flush=True)
    if members:
        print("%d were members-only. Those need a channel membership AND readable"
              % members)
        print("  cookies: fully quit the browser first, then "
              "--cookies-from-browser chrome")
    if blocked:
        print("%d were rate limits." % blocked)
    remaining = len(ids) - got - skipped
    if remaining > 0:
        print("%d id(s) still have no transcript." % remaining)
    return {"got": got, "skipped": skipped, "failed": failed,
            "blocked": blocked, "members": members, "remaining": remaining}


def _until_done(ids, a):
    """Sweep, back off, sweep again, until nothing is left that waiting can fix.

    FOR AN UNATTENDED RUN. YouTube's rate limit on this endpoint is per address
    and lasts hours, so the only thing that clears it is time -- and the only
    thing a fetcher can usefully do is stop asking, wait a long time, and try
    again. Each sweep skips what is already cached, so the work accumulates.

    It stops for one of three reasons, and says which:
      - nothing left to fetch;
      - a sweep fetched nothing AND hit no rate limit, which means everything
        still missing is permanently unavailable (members-only, deleted) and
        waiting cannot help;
      - the wall-clock budget ran out.

    The backoff resets on progress: if a sweep got anything, the block has
    lifted and there is no reason to keep waiting an hour between tries.
    """
    import time
    # monotonic, not wall clock: an unattended run spans a night, and a clock
    # change or a DST shift must not extend or truncate the budget.
    start = time.monotonic()
    budget = a.max_hours * 3600
    wait = a.backoff * 60
    cycle = 0
    while cycle < a.max_passes:
        cycle += 1
        left = [v for v in ids if not os.path.exists(os.path.join(a.out, v + ".json"))]
        print("\n=== pass %d — %s — %d still to fetch ==="
              % (cycle, time.strftime("%H:%M:%S"), len(left)), flush=True)
        if not left:
            print("Everything on the list is cached. Done.", flush=True)
            return
        r = _run_pass(ids, a)
        if r["remaining"] <= 0:
            print("\nDone: everything fetched.", flush=True)
            return
        if r["got"] == 0 and r["blocked"] == 0:
            print("\nStopping: a whole pass fetched nothing and hit no rate limit,"
                  " so the %d still missing are permanently unavailable"
                  " (members-only or removed). Waiting cannot fix those."
                  % r["remaining"], flush=True)
            return
        if r["got"] > 0:
            wait = a.backoff * 60      # progress means the block lifted
        else:
            wait = min(wait * 2, 3600)  # still blocked: back off, cap at an hour
        spent = time.monotonic() - start
        if spent + wait > budget:
            print("\nStopping: the %.1f hour budget is spent. %d still missing."
                  % (a.max_hours, r["remaining"]), flush=True)
            print("Re-run the same command whenever you like; nothing repeats.",
                  flush=True)
            return
        print("\nWaiting %d minutes before the next pass (%.1f h of %.1f h used)."
              % (wait / 60, spent / 3600, a.max_hours), flush=True)
        time.sleep(wait)
    else:
        # A HARD CEILING ON PASSES, independent of the clock. The budget check
        # assumes time.sleep really sleeps; a signal, a suspend/resume or a
        # clock change can make it return early, and this loop would then spin
        # against a rate limit all night making it worse. Belt and braces for
        # code that runs unattended.
        print("\nStopping: %d passes is the ceiling. Re-run the same command "
              "whenever you like; nothing already fetched is repeated."
              % a.max_passes, flush=True)



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--feed", help="RSS feed to harvest video ids from")
    ap.add_argument("--ids", nargs="*", default=[], help="explicit video ids")
    ap.add_argument("--out", default=CACHE)
    ap.add_argument("--catalog", help="channel or feed URL: enumerate, do not fetch")
    ap.add_argument("--catalog-out", default=os.path.join(ROOT, "research", "leads", "catalog.json"))
    ap.add_argument("--since", help="YYYY-MM-DD; drop catalogue entries older than this")
    ap.add_argument("--select", help="file of video ids, one per line, to fetch")
    ap.add_argument("--resolve", action="store_true",
                    help="oEmbed every id already in the cache and write a manifest")
    ap.add_argument("--ytdlp", action="store_true",
                    help="fetch through yt-dlp instead of the caption endpoint. "
                         "Slower, throttled, far harder to rate-limit")
    ap.add_argument("--cookies-from-browser", dest="cookies",
                    help="chrome, edge, firefox ... needed for members-only videos "
                         "and it makes a block much less likely")
    ap.add_argument("--sleep", type=float, default=0.0,
                    help="seconds to wait between videos (default 0; try 10 after a block)")
    ap.add_argument("--until-done", action="store_true",
                    help="unattended: sweep, back off on a rate limit, sweep again, "
                         "until nothing is left that waiting can fix")
    ap.add_argument("--max-hours", type=float, default=10.0,
                    help="wall-clock budget for --until-done (default 10)")
    ap.add_argument("--max-passes", type=int, default=24,
                    help="hard ceiling on sweeps for --until-done, independent "
                         "of the clock (default 24)")
    ap.add_argument("--backoff", type=float, default=25.0,
                    help="minutes to wait after a blocked pass; doubles up to 60 "
                         "while still blocked, resets on progress (default 25)")
    a = ap.parse_args()

    if a.resolve:
        import glob
        ids = sorted(os.path.basename(f)[:-5]
                     for f in glob.glob(os.path.join(a.out, "*.json")))
        if not ids:
            sys.exit("no cached transcripts in %s" % a.out)
        print("resolving %d cached ids against YouTube oEmbed\n" % len(ids))
        rows = resolve_ids(ids)
        write_catalog([{"id": r["id"], "title": r.get("title") or "",
                        "channel": r.get("channel"), "date": None,
                        "duration": None, "url": None} for r in rows],
                      a.catalog_out)
        return

    if a.catalog:
        rows = None
        if not a.catalog.rstrip("/").endswith(".xml") and "feeds." not in a.catalog:
            rows = catalog_ytdlp(a.catalog)
            if rows is None:
                print("yt-dlp did not run. Tried the executable, `%s -m yt_dlp`"
                      % os.path.basename(sys.executable))
                print("and `py -m yt_dlp`. Install it with:")
                print("    pip install -U yt-dlp")
                print("Falling back to reading it as a feed, which for a CHANNEL url")
                print("yields nothing -- a channel page is not an RSS feed.\n")
        if rows is None:
            rows = catalog_feed(a.catalog)
        if not rows:
            sys.exit("no videos enumerated -- refusing to write an empty catalogue "
                     "over %s" % a.catalog_out)
        write_catalog(rows, a.catalog_out, a.since)
        return

    ids = list(a.ids)
    if a.select:
        # STRIP THE INLINE COMMENT. The selection file is written as
        # `<id>  # <title>` so a human can read it, and the first version of
        # this loop took the whole line as the id. Every request then went out
        # as "RTEWLSTyUic  # The CIA Scientist Who Built UFOs..." and came back
        # VideoUnavailable -- 169 of 169, including nine ids that had been
        # fetched successfully the same day. It also meant the already-cached
        # check never matched, so it reported "0 already cached" against a
        # cache holding 24 files. Both symptoms pointed at YouTube and neither
        # was YouTube.
        bad = []
        with open(a.select, encoding="utf-8") as fh:
            for n, line in enumerate(fh, 1):
                v = line.split("#", 1)[0].strip()
                if not v:
                    continue
                if not _ID_OK.match(v):
                    bad.append((n, line.rstrip()[:70]))
                    continue
                if v not in ids:
                    ids.append(v)
        if bad:
            # Loudly, and before spending a single request. A malformed id is a
            # broken selection file, not a missing video, and the two look
            # identical once the API has answered.
            print("%d line(s) in %s are not video ids:" % (len(bad), a.select))
            for n, txt in bad[:10]:
                print("  line %d: %r" % (n, txt))
            sys.exit("refusing to fetch: fix the selection file")
    if a.feed:
        ids += [v for v in ids_from_feed(a.feed) if v not in ids]
    if not ids:
        sys.exit("nothing to fetch: pass --catalog, --select, --feed or --ids")

    os.makedirs(a.out, exist_ok=True)

    if a.until_done:
        _until_done(ids, a)
    else:
        _run_pass(ids, a, announce=True)

    print("cache: %s" % a.out)
    print("This directory is gitignored on purpose. Do not commit it.")


if __name__ == "__main__":
    main()
