#!/usr/bin/env python3
"""
spot_cache_put.py — put a locally obtained document into spot_check.py's cache.

WHY THIS EXISTS
---------------
spot_check.py fetches with curl. dia.mil and aaro.mil answer curl with 403 and
serve WebFetch, which between them puts 128 quoted claims -- the largest block of
unverified quotation on the board -- out of the script's reach.

WebFetch hands back a model's reading of the document. That is the wrong instrument
for this job: asking a model "does this sentence appear" invites it to agree, and a
confirmation nobody can re-derive is not verification. But WebFetch also writes the
raw bytes to disk, and those bytes are the document.

So: fetch by whatever route the host allows, then drop the file here. The text is
extracted mechanically and stored under the URL spot_check.py would have used, and
the quote comparison stays a substring test that anyone can repeat.

Usage:
    python3 tools/spot_cache_put.py <url> <local-file>
"""

import hashlib, io, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, "tools", ".spot-cache")


def main():
    if len(sys.argv) != 3:
        print(__doc__.strip().split("Usage:")[-1].strip())
        return 2
    url, path = sys.argv[1], sys.argv[2]
    data = open(path, "rb").read()
    if data[:5] == b"%PDF-":
        from pypdf import PdfReader
        text = "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(data)).pages)
    else:
        text = data.decode("utf-8", errors="replace")
        text = re.sub(r"(?is)<(script|style).*?</\1>", " ", text)
        text = re.sub(r"(?s)<[^>]+>", " ", text)
        import html as _html
        text = _html.unescape(text)
    if len(text.strip()) < 500:
        print(f"REFUSED: only {len(text.strip())} chars of text — this is an image-only "
              f"scan, and caching it would report every quote in it as missing.")
        return 1
    os.makedirs(CACHE, exist_ok=True)
    key = os.path.join(CACHE, hashlib.sha1(url.encode()).hexdigest())
    for stale in (key + ".err",):
        if os.path.exists(stale):
            os.remove(stale)
    with open(key + ".txt", "w", encoding="utf-8") as f:
        f.write(text)
    print(f"cached {len(text):,} chars for {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
