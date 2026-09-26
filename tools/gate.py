#!/usr/bin/env python3
"""The whole gate, in one command.

    python tools/gate.py                 build, every check, the app, every poison
    python tools/gate.py --quick         the same without the app's poison sweep
    python tools/gate.py --no-build      check what is on disk; do not rebuild first
    python tools/gate.py --no-app        the Python side only; no browser
    python tools/gate.py --idempotent    also build twice and require identical output

Stops at the first failure. Ends with one table: step, result, seconds.

WHAT RUNS, IN ORDER

  1. tools/build.py                      unless --no-build
  2. verify.py, and its --self-test      every check, and every check seen failing
     audit_independent.py                the same facts re-derived independently
     build_app_data.py --check, --self-test
     build_places.py --check             the places page data re-derived
     check_rebuild.py --built-only, --self-test
     lint_no_em_dash.py, and its --self-test
     test_browser_env.js --self-test     no browser launched; guards the resolver
                                         look.js and make_drawing_thumbs.mjs use
     verify.py --idempotent              only with --idempotent; builds twice
  3. in app/, unless --no-app:
     npm run build
     a preview on 127.0.0.1:4173         reused if one already answers there;
                                         otherwise started here and ALWAYS stopped,
                                         including when a step fails
     npm run check                       C1 onwards, against the build
     npm run check:poison                unless --quick; every poison must be seen

check_rebuild runs with --built-only here: it compares only the files a build
writes, so hand edits in flight (a note, CLAUDE.md, a tool being changed) do not
turn the gate red. It does not run at all under --no-build, because it compares a
build against HEAD and there was none. CI runs it on the whole tree as a step of
its own, straight after building.

Until 25 September 2026 the gate was a list in CLAUDE.md section 3 and a
`state_snapshot.py --gate` that drove the old single-file shell. The old shell is
retired, and `state_snapshot.py --gate` now calls this.
"""

import os
import shutil
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APP = os.path.join(ROOT, "app")
PREVIEW = "http://127.0.0.1:4173/"
PY = sys.executable


def tool(*parts):
    return os.path.join(ROOT, "tools", *parts)


def _answers(url, timeout=2.0):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status == 200
    except Exception:
        return False


def _npm(*args):
    """npm on every platform. On Windows `which` resolves npm.cmd, a batch file
    that CreateProcess hands to cmd.exe itself, so no shell=True is needed."""
    exe = shutil.which("npm") or "npm"
    return [exe] + list(args)


class Preview(object):
    """Serve app/dist on 127.0.0.1:4173 for the app's checks.

    `--host 127.0.0.1` is spelled out because plain `vite preview` binds IPv6 only
    on some machines and the checks fetch 127.0.0.1. `--strictPort` makes a busy
    port fail loudly rather than quietly moving to 4174, which nothing watches.

    Vite is started with node directly rather than through npx, so the process
    this holds is the server itself and stopping it stops the server. Through npx
    on Windows it would be a cmd.exe whose child outlives it."""

    def __init__(self):
        self.proc = None
        self.reused = False

    def start(self):
        if _answers(PREVIEW):
            self.reused = True
            return "reused the server already on 4173"
        vite = os.path.join(APP, "node_modules", "vite", "bin", "vite.js")
        args = ["preview", "--host", "127.0.0.1", "--port", "4173", "--strictPort"]
        if os.path.exists(vite):
            cmd = ["node", vite] + args
        else:
            cmd = [shutil.which("npx") or "npx", "vite"] + args
        kw = {}
        if os.name != "nt":
            kw["start_new_session"] = True
        self.proc = subprocess.Popen(cmd, cwd=APP, stdout=subprocess.DEVNULL,
                                     stderr=subprocess.DEVNULL, **kw)
        deadline = time.time() + 45
        while time.time() < deadline:
            if self.proc.poll() is not None:
                raise RuntimeError("vite preview exited %d before it answered"
                                   % self.proc.returncode)
            if _answers(PREVIEW, timeout=1.0):
                return "started on 4173"
            time.sleep(0.5)
        raise RuntimeError("vite preview did not answer on 4173 within 45s")

    def stop(self):
        if self.proc is None or self.proc.poll() is not None:
            return
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(self.proc.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        else:
            import signal
            try:
                os.killpg(self.proc.pid, signal.SIGTERM)
            except OSError:
                self.proc.terminate()
        try:
            self.proc.wait(timeout=15)
        except subprocess.TimeoutExpired:
            self.proc.kill()


def plan(opts):
    """[(name, argv, cwd)] in order. A None argv is a marker handled by run()."""
    steps = []
    if not opts["no_build"]:
        steps.append(("build", [PY, tool("build.py")], ROOT))
    steps += [
        ("verify", [PY, tool("verify.py")], ROOT),
        ("verify --self-test", [PY, tool("verify.py"), "--self-test"], ROOT),
        ("audit_independent", [PY, tool("audit_independent.py")], ROOT),
        ("build_app_data --check", [PY, tool("build_app_data.py"), "--check"], ROOT),
        ("build_app_data --self-test", [PY, tool("build_app_data.py"), "--self-test"], ROOT),
        ("check_rebuild --self-test", [PY, tool("check_rebuild.py"), "--self-test"], ROOT),
        ("lint_no_em_dash", [PY, tool("lint_no_em_dash.py")], ROOT),
        ("lint_no_em_dash --self-test", [PY, tool("lint_no_em_dash.py"), "--self-test"], ROOT),
        ("browser_env --self-test", ["node", tool("test_browser_env.js"), "--self-test"], ROOT),
        ("build_places --check", [PY, tool("build_places.py"), "--check"], ROOT),
    ]
    if not opts["no_build"]:
        # It compares a build against HEAD, so without a build in this run there
        # is nothing for it to compare. CI runs it as its own step after building.
        steps.insert(6, ("check_rebuild --built-only",
                         [PY, tool("check_rebuild.py"), "--built-only"], ROOT))
    if opts["idempotent"]:
        steps.append(("verify --idempotent", [PY, tool("verify.py"), "--idempotent"], ROOT))
    if not opts["no_app"]:
        steps.append(("app: npm run build", _npm("run", "build"), APP))
        steps.append(("app: preview", None, APP))
        steps.append(("app: npm run check", _npm("run", "check"), APP))
        if not opts["quick"]:
            steps.append(("app: npm run check:poison", _npm("run", "check:poison"), APP))
    return steps


def main(argv):
    known = {"--quick", "--no-build", "--no-app", "--idempotent", "-h", "--help"}
    bad = [a for a in argv if a not in known]
    if bad or "-h" in argv or "--help" in argv:
        print(__doc__)
        return 2 if bad else 0
    opts = {"quick": "--quick" in argv, "no_build": "--no-build" in argv,
            "no_app": "--no-app" in argv, "idempotent": "--idempotent" in argv}

    rows = []
    failed = None
    preview = Preview()
    t_all = time.time()
    try:
        for name, cmd, cwd in plan(opts):
            print("\n== " + name, flush=True)
            t0 = time.time()
            if cmd is None:
                try:
                    note = preview.start()
                    rows.append((name, "ok (%s)" % note, time.time() - t0))
                    print("   " + note, flush=True)
                    continue
                except RuntimeError as e:
                    rows.append((name, "FAIL", time.time() - t0))
                    print("   " + str(e), flush=True)
                    failed = name
                    break
            try:
                rc = subprocess.run(cmd, cwd=cwd).returncode
            except OSError as e:
                print("   could not run: %s" % e, flush=True)
                rc = 127
            rows.append((name, "ok" if rc == 0 else "FAIL (%d)" % rc, time.time() - t0))
            if rc != 0:
                failed = name
                break
    finally:
        preview.stop()

    total = time.time() - t_all
    w = max([len(r[0]) for r in rows] + [4]) + 2
    rw = max([len(r[1]) for r in rows] + [6]) + 2
    print("\n" + "step".ljust(w) + "result".ljust(rw) + "seconds".rjust(8))
    for name, res, dt in rows:
        print(name.ljust(w) + res.ljust(rw) + ("%.1f" % dt).rjust(8))
    print("total".ljust(w) + "".ljust(rw) + ("%.1f" % total).rjust(8))
    if failed:
        print("\nGATE FAILED at %s. Later steps did not run." % failed)
        return 1
    skipped = [k for k, v in (("the build", opts["no_build"]), ("the app", opts["no_app"]),
                              ("the poison sweep", opts["quick"] and not opts["no_app"]))
               if v]
    print("\nGATE PASSED" + (" (skipped: " + ", ".join(skipped) + ")" if skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
