#!/usr/bin/env python3
"""Pull podcast transcripts into the SAME local cache the YouTube puller uses.

WHY THIS EXISTS
---------------
On 29-30 August 2026 YouTube durably blocked this project's home IP. Five passes
over eight hours returned 429 on every attempt, a single-video probe the next
morning returned 429, and cookie extraction is dead on Chrome 127+ because of
App-Bound Encryption. `tools/fetch_transcripts.py` documents all of that. The
conclusion drawn at the time was "you need a different IP".

That conclusion was right about the door and wrong about the building. Every show
this project cares about is a PODCAST, and a podcast has an RSS feed serving MP3s
from a podcast CDN -- Megaphone, Libsyn, Anchor. None of that is YouTube. None of
it is rate-limited against us. Measured 30 August 2026 from the cloud container
that YouTube refuses:

    feed             HTTP 200, 140 episodes, 1.2MB of XML
    audio            12.6 MB in 4 seconds, HTTP 206
    transcription    16x realtime, faster-whisper base.en, int8, CPU

285 hours of audio is roughly 18 hours of CPU. That is a long job and an entirely
unblocked one, which is the opposite of where this stood yesterday.

WHAT IT WRITES, AND WHAT IT NEVER COMMITS
-----------------------------------------
The same shape `fetch_transcripts.py` writes, into the same gitignored directory,
so `tools/read_transcript.py` and every downstream reader work unchanged:

    research/.transcripts/<id>.json   {"id": ..., "segments": [{"t": secs, "text": ...}]}

Ids are `<show>-<8 hex of the episode guid>`, so they can never collide with an
11-character YouTube id, and they are stable across runs because the guid is.

**The audio is deleted after each episode.** 285 hours of MP3 is about 15GB and
this container has a fixed disk allowance, so keeping it would fail the run
somewhere in the middle for a reason nobody would connect to the cause.

DO NOT RUN THIS ALONGSIDE THE BROWSER CHECKS
--------------------------------------------
Transcription holds about 1.4GB and pins a core or two for hours. `runtime_check`,
`test_packed_layout` and `look.js` each launch Chromium against a 15.8MB page, and
Chromium on that page is not cheap either. On 30 August 2026 a run that had already
proved it could transcribe the feed's LONGEST episode (5h00, 1.38GB peak, measured)
was OOM-killed on a shorter 4h17 one while two `runtime_check` passes ran beside it.
Peak for the box hit 15.2GB of 16GB.

That was contention, not a defect -- but the symptom is identical to the real OOM
this tool was fixed for, exit 137 with no traceback, so the next person to see it
will reach for the wrong cause. Run the gate, then run this; or run this, then the
gate. Nothing is lost either way: the cache resumes.

USAGE
-----
    python3 tools/fetch_podcast.py --show michels --limit 5
    python3 tools/fetch_podcast.py --show michels --oldest-first --until-done
    python3 tools/fetch_podcast.py --feed https://example.com/feed.xml --list
    python3 tools/fetch_podcast.py --show michels --model small.en

`--list` prints the catalogue and fetches no audio, which is the cheap way to see
what a feed holds before spending hours on it.
"""
import argparse, functools, html, json, os, re, sys, time, urllib.request, urllib.error

# Python block-buffers stdout when it is not a tty, so a run redirected to a file
# or piped shows NOTHING for minutes at a time and looks hung. This job takes
# hours; its progress has to be legible while it runs, not after it exits.
say = functools.partial(print, flush=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "research", ".transcripts")
UA = {"User-Agent": "Mozilla/5.0 (compatible; the-program/1.0)"}

# Known feeds. A show is added here only once its feed has been fetched and the
# episode count checked against the show's own public catalogue -- an RSS feed
# that silently truncates to the most recent 50 is a real and common thing, and
# it would look exactly like a complete run.
FEEDS = {
    # Resolved via Apple's podcast search API, which returns feedUrl directly and
    # needs no key: https://itunes.apple.com/search?term=<name>&entity=podcast
    # Each was then fetched and its item count and date range checked before it
    # was written down here. Counts are as of 30 August 2026.
    "michels":   ("American Alchemy with Jesse Michels",
                  "https://feeds.megaphone.fm/jessemichels"),          # 140, Oct 2024 ->
    "area52":    ("AREA52 - DEBRIEFED With Chris Ramsay",
                  "https://anchor.fm/s/e81d3f74/podcast/rss"),         # 107, Sep 2023 ->
    "dannyjones": ("Danny Jones Podcast",
                  "https://feeds.megaphone.fm/QCD2752074976"),         # 426, Nov 2018 ->
}

# NOT here, and the absence is a finding rather than an omission: **UAP Gerb has no
# podcast feed.** Three Apple searches ("UAP Gerb", "UAPGerb", "Gerb UFO legacy
# program") return no show under that name, only other people's episodes about him.
# He publishes to YouTube only, so his material is reachable only through the door
# that is blocked -- which is why the 35-episode corpus already in research/leads/
# is, for now, all of him this project has.


def fetch(url, timeout=180, rng=None):
    req = urllib.request.Request(url, headers=dict(UA))
    if rng:
        req.add_header("Range", "bytes=%d-" % rng)
    return urllib.request.urlopen(req, timeout=timeout)


def grab(block, tag):
    m = re.search(r"<%s[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</%s>" % (tag, tag), block, re.S)
    if not m:
        return None
    return html.unescape(re.sub(r"<[^>]+>", " ", m.group(1))).strip()


def parse_feed(xml, show):
    """Episodes oldest-last, as feeds order them. Each carries a stable id."""
    import hashlib
    out = []
    for it in re.findall(r"<item>(.*?)</item>", xml, re.S):
        enc = re.search(r'<enclosure[^>]*url="([^"]+)"', it)
        if not enc:
            continue
        guid = grab(it, "guid") or enc.group(1)
        out.append({
            "id": "%s-%s" % (show, hashlib.sha1(guid.encode()).hexdigest()[:8]),
            "title": grab(it, "title") or "",
            "date": grab(it, "pubDate") or "",
            "duration": grab(it, "itunes:duration") or "",
            "audio": enc.group(1),
            "guid": guid,
        })
    return out


def secs(d):
    if not d:
        return 0
    d = str(d)
    if ":" in d:
        try:
            p = [int(x) for x in d.split(":")]
        except ValueError:
            return 0
        return sum(v * 60 ** i for i, v in enumerate(reversed(p)))
    try:
        return int(d)
    except ValueError:
        return 0


def hhmm(s):
    return "%d:%02d" % (s // 3600, (s % 3600) // 60)


# ---------------------------------------------------------------- audio windows
# WINDOW_SECONDS bounds peak memory. faster_whisper's own decode path reads the
# WHOLE file into a buffer and converts it, so buffer, array and the conversion's
# intermediates are live at once, and whisper then works on the entire thing.
#
# MEASURED on "New Scans Show Massive Structures Under the Pyramids" (4h12,
# 44.1kHz stereo, 243MB), which OOM-killed three runs:
#
#   whole file, as shipped     12.37 GB peak, exit 137 after ~2 minutes
#   decode alone, windowed      0.24 GB peak, flat across all 12 windows
#   one 20-min window + model   1.52 GB peak, 281 segments in 56s
#   three windows in sequence   1.50 -> 1.56 -> 1.59 GB, so it does not accumulate
#
# Decoding sequentially in windows needs no seeking and no temp files.
#
# It runs for EVERY episode, not only long ones. Seven of 140 in this feed are
# over four hours; a branch that fires on 5% of input is a branch nobody knows
# works, which is CLAUDE.md section 5.
#
# The cost, stated rather than hidden: a word straddling a window boundary can be
# clipped. That is about 12 boundaries in a four-hour episode, against a
# transcript already labelled machine-generated and uncorrected.
WINDOW_SECONDS = 1200
SAMPLE_RATE = 16000


def iter_windows(path, window_s=WINDOW_SECONDS, rate=SAMPLE_RATE):
    """Yield (offset_seconds, float32 mono array), decoding straight through."""
    import av
    import numpy as np
    resampler = av.audio.resampler.AudioResampler(format="s16", layout="mono", rate=rate)
    buf, n, offset = [], 0, 0.0
    with av.open(path, mode="r", metadata_errors="ignore") as container:
        for frame in container.decode(audio=0):
            frame.pts = None                     # the resampler wants unstamped frames
            for f in resampler.resample(frame):
                a = f.to_ndarray().reshape(-1)
                buf.append(a)
                n += a.size
                if n >= window_s * rate:
                    arr = np.concatenate(buf).astype(np.float32) / 32768.0
                    buf, n = [], 0
                    yield offset, arr
                    offset += arr.size / rate
    if n:
        import numpy as np
        yield offset, np.concatenate(buf).astype(np.float32) / 32768.0


def transcribe_windowed(model, path):
    """Segments for a whole episode, timestamps in episode time."""
    rows = []
    for offset, audio in iter_windows(path):
        segs, _ = model.transcribe(audio, beam_size=1, vad_filter=True)
        for sg in segs:
            rows.append({"t": round(sg.start + offset, 2), "text": sg.text.strip()})
        del audio
    return rows


def download(url, path):
    """Resumable, because a 200MB episode over a flaky link should not restart."""
    have = os.path.getsize(path) if os.path.exists(path) else 0
    try:
        r = fetch(url, rng=have if have else None)
    except urllib.error.HTTPError as e:
        if e.code == 416 and have:          # already complete
            return have
        raise
    mode = "ab" if (have and r.status == 206) else "wb"
    if mode == "wb":
        have = 0
    with open(path, mode) as fh:
        while True:
            b = r.read(1 << 20)
            if not b:
                break
            fh.write(b)
            have += len(b)
    return have


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--show", choices=sorted(FEEDS), help="a known show")
    ap.add_argument("--feed", help="any podcast RSS URL")
    ap.add_argument("--name", help="short prefix for ids when using --feed")
    ap.add_argument("--out", default=CACHE)
    ap.add_argument("--model", default="base.en",
                    help="faster-whisper model. base.en is ~16x realtime on CPU and "
                         "readable; small.en is ~3x slower and better on names")
    ap.add_argument("--limit", type=int, help="stop after N new transcripts")
    ap.add_argument("--oldest-first", action="store_true",
                    help="work backwards through the archive instead of from the top")
    ap.add_argument("--list", action="store_true", help="print the catalogue and stop")
    ap.add_argument("--max-hours", type=float, help="stop starting new episodes after this long")
    args = ap.parse_args()

    if not args.show and not args.feed:
        ap.error("give --show or --feed")
    if args.show:
        label, url = FEEDS[args.show]
        name = args.show
    else:
        url, name = args.feed, (args.name or "feed")
        label = url

    say("feed: %s" % label)
    try:
        xml = fetch(url).read().decode("utf-8", "replace")
    except Exception as e:
        say("  !! could not fetch the feed: %s" % e, file=sys.stderr)
        return 2
    eps = parse_feed(xml, name)
    if not eps:
        say("  !! no <item> with an <enclosure> in that feed", file=sys.stderr)
        return 2

    total = sum(secs(e["duration"]) for e in eps)
    say("  %d episodes, %s of audio, %s to %s"
          % (len(eps), hhmm(total), eps[-1]["date"][:16], eps[0]["date"][:16]))

    os.makedirs(args.out, exist_ok=True)

    done = {e["id"] for e in eps
            if os.path.exists(os.path.join(args.out, e["id"] + ".json"))}
    todo = [e for e in eps if e["id"] not in done]
    if args.oldest_first:
        todo = list(reversed(todo))

    # --list is READ-ONLY and returns before the sweep below, which deletes files.
    if args.list:
        for e in eps:
            say("  %s  %5s  %-9s %s"
                  % (e["date"][5:16], hhmm(secs(e["duration"])),
                     "cached" if e["id"] in done else "", e["title"][:72]))
        say("\n%d cached, %d to fetch" % (len(done), len(todo)))
        return 0

    # Sweep audio abandoned by a run that was KILLED rather than interrupted. The
    # per-episode `finally` deletes the mp3, but a SIGKILL -- an OOM, a reaped
    # background process, a reclaimed container -- never runs it, and one abandoned
    # 3.5-hour episode is half a gigabyte.
    #
    # TWO GUARDS, both learned within a minute of writing the first version.
    #
    # It sits AFTER the --list return above, because a read-only mode must not
    # delete anything.
    #
    # And it only touches files older than STALE_AFTER, because a `.part` may
    # belong to a run happening RIGHT NOW -- this project transcribes one show in
    # one process while another lists or fetches a second. The first version had no
    # age check and deleted the 482MB episode a concurrent run was working on. The
    # longest episode in these feeds is 3.6 hours, which downloads in seconds and
    # transcribes in about twelve minutes, so a file untouched for two hours
    # belongs to nobody.
    STALE_AFTER = 2 * 3600
    now, stale, freed = time.time(), [], 0
    for f in os.listdir(args.out):
        if not f.endswith(".mp3.part"):
            continue
        fp = os.path.join(args.out, f)
        try:
            if now - os.path.getmtime(fp) < STALE_AFTER:
                continue                       # someone is probably using it
            freed += os.path.getsize(fp)
            os.remove(fp)
            stale.append(f)
        except OSError:
            pass
    if stale:
        say("  swept %d abandoned audio file(s), %.0f MB, untouched for over %dh"
              % (len(stale), freed / 1e6, STALE_AFTER // 3600))

    say("  %d already cached, %d to fetch" % (len(done), len(todo)))
    if not todo or args.limit == 0:
        # --limit 0 is the dry run: resolve the feed, sweep, report, fetch nothing.
        # It has to return HERE, before the model loads, or "fetch nothing" still
        # costs several seconds and a few hundred megabytes of resident memory.
        return 0

    try:
        from faster_whisper import WhisperModel
    except ImportError:
        say("\n  !! faster-whisper is not installed. It is the transcriber and there\n"
              "     is no fallback. Install it, then run this again:\n\n"
              "         pip install faster-whisper\n", file=sys.stderr)
        return 2

    say("  loading %s ..." % args.model)
    model = WhisperModel(args.model, device="cpu", compute_type="int8")

    started = time.time()
    n = 0
    for e in todo:
        if args.limit is not None and n >= args.limit:
            say("  stopping: --limit %d reached" % args.limit)
            break
        if args.max_hours and (time.time() - started) / 3600 >= args.max_hours:
            say("  stopping: --max-hours %.1f reached" % args.max_hours)
            break

        dur = secs(e["duration"])
        say("\n  [%d/%d] %s" % (n + 1, len(todo), e["title"][:70]))
        say("        %s  %s" % (e["date"][5:16], hhmm(dur)))
        mp3 = os.path.join(args.out, e["id"] + ".mp3.part")
        try:
            t = time.time()
            size = download(e["audio"], mp3)
            say("        %.1f MB in %ds" % (size / 1e6, time.time() - t))

            t = time.time()
            rows = transcribe_windowed(model, mp3)
            el = max(time.time() - t, 1)
            say("        %d segments in %s (%.1fx realtime)"
                  % (len(rows), hhmm(int(el)), (dur or el) / el))

            # Write only on success, and only via a temp file, so an interrupted
            # run never leaves a half transcript that the next run counts as done.
            tmp = os.path.join(args.out, e["id"] + ".json.part")
            with open(tmp, "w", encoding="utf-8") as fh:
                json.dump({"id": e["id"], "title": e["title"], "date": e["date"],
                           "show": label, "audio": e["audio"], "segments": rows},
                          fh, ensure_ascii=False)
            os.replace(tmp, os.path.join(args.out, e["id"] + ".json"))
            n += 1
        except KeyboardInterrupt:
            say("\n  interrupted; the part file is kept and the next run resumes it")
            break
        except Exception as ex:
            say("        !! %s: %s" % (type(ex).__name__, str(ex)[:160]), file=sys.stderr)
        finally:
            # ALWAYS, including on failure. 285 hours of MP3 is about 15GB and this
            # container has a fixed disk allowance.
            if os.path.exists(mp3):
                try:
                    os.remove(mp3)
                except OSError:
                    pass

    say("\n%d new transcript(s) in %s" % (n, hhmm(int(time.time() - started))))
    say("cache: %s" % args.out)
    say("This directory is gitignored on purpose. Do not commit it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
