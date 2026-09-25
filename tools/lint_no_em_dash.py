"""lint_no_em_dash.py: fail if U+2014 appears in the app's or the Worker's source.

Stewart's standing rule (global CLAUDE.md): no em dashes anywhere. Data is out of
scope here: verbatim quotations keep their characters, and display labels are
normalised in the pipeline (phase 3). app/src/analyst/tools.ts is exempt until
phase 12, because C19 parses its output and a change is a Worker redeploy.

  python tools/lint_no_em_dash.py              exit 1 on any hit
  python tools/lint_no_em_dash.py --self-test  shows the lint rejecting a planted dash
"""
import os
import sys
import tempfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
DIRS = ["app/src", "app/checks", "worker/src"]
EXEMPT = {os.path.normpath("app/src/analyst/tools.ts")}
EXTS = (".ts", ".mjs", ".js", ".css", ".html")
DASH = "—"


def hits(root: str) -> list[str]:
    out = []
    for d in DIRS:
        base = os.path.join(root, d)
        for dp, _, fns in os.walk(base):
            for fn in sorted(fns):
                if not fn.endswith(EXTS):
                    continue
                p = os.path.join(dp, fn)
                rel = os.path.normpath(os.path.relpath(p, root))
                if rel in EXEMPT:
                    continue
                with open(p, encoding="utf-8") as f:
                    for i, line in enumerate(f, 1):
                        if DASH in line:
                            out.append(f"{rel}:{i}")
    return out


def self_test() -> int:
    with tempfile.TemporaryDirectory() as t:
        os.makedirs(os.path.join(t, "app", "src", "analyst"))
        with open(os.path.join(t, "app", "src", "x.ts"), "w", encoding="utf-8") as f:
            f.write("const a = 'one " + DASH + " two';\n")
        # the exempt file must stay exempt, and a clean file must stay clean
        with open(os.path.join(t, "app", "src", "analyst", "tools.ts"), "w", encoding="utf-8") as f:
            f.write("// " + DASH + "\n")
        with open(os.path.join(t, "app", "src", "y.ts"), "w", encoding="utf-8") as f:
            f.write("const b = 'one - two';\n")
        got = hits(t)
    ok = got == [os.path.normpath("app/src/x.ts") + ":1"]
    print(("ok    " if ok else "FAIL  ") + "the lint rejects a planted em dash, and only it :: " + repr(got))
    return 0 if ok else 1


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    h = hits(ROOT)
    for x in h:
        print("em dash: " + x)
    print(("FAIL  " if h else "ok    ") + f"no em dash in {', '.join(DIRS)} :: {len(h)} line(s)")
    sys.exit(1 if h else 0)
