#!/usr/bin/env python3
"""Assemble the Cloudflare Pages deployment directory.

WHY THIS EXISTS
---------------
The board shipped for months as one self-contained 13MB HTML file, because it had
to run from a double-click with no server. That constraint is gone: it deploys to
Cloudflare Pages now. This script is the seam between the two worlds -- the build
still produces `dist/the-program.html`, and this turns it into a `site/` tree that
Pages can serve.

It is deliberately the ONLY place that knows about hosting. `build_dashboard.py`
still emits a file that works from `file://`, so the offline artifact never
regresses and the gate keeps checking the same thing it always did.
"""
import hashlib
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "dist", "the-program.html")
SITE = os.path.join(ROOT, "site")

# Pages serves index.html for these, so the client router sees the real path
# instead of a 404. A blanket `/* -> /index.html` would also swallow the data
# files once the payload is split, which is a bug that only shows up on the day
# you split it, so the routes are named.
REDIRECTS = """\
# Deep links. 200 means rewrite, not redirect -- the address bar keeps the path
# the reader was given, which is the whole point of having one.
/node/*   /index.html   200
/path/*   /index.html   200
/band/*   /index.html   200
/era/*    /index.html   200
/q/*      /index.html   200
"""

# The board is one immutable artifact per deploy, so the HTML must never be
# cached hard -- a reader holding a stale index would silently be reading an
# older board and have no way to know. Data files are content-addressed by the
# deploy itself and can be cached aggressively once the split lands.
HEADERS = """\
/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin

/index.html
  Cache-Control: no-cache

/data/*
  Cache-Control: public, max-age=31536000, immutable
"""


def main():
    if not os.path.exists(SRC):
        sys.exit("build_site: dist/the-program.html is missing -- run build_dashboard.py first")
    os.makedirs(SITE, exist_ok=True)
    shutil.copyfile(SRC, os.path.join(SITE, "index.html"))
    for name, body in (("_redirects", REDIRECTS), ("_headers", HEADERS)):
        with open(os.path.join(SITE, name), "w", encoding="utf-8") as fh:
            fh.write(body)
    size = os.path.getsize(SRC)
    digest = hashlib.sha256(open(SRC, "rb").read()).hexdigest()[:12]
    print("site/  index.html %.2f MB  sha256 %s" % (size / 1048576, digest))
    print("       _redirects %d routes" % sum(1 for l in REDIRECTS.splitlines()
                                              if l and not l.startswith("#")))
    print("       _headers")
    print("\ndeploy:  npx wrangler pages deploy site --project-name the-program")


if __name__ == "__main__":
    main()
