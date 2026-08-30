#!/usr/bin/env python3
"""Set a GitHub Actions repository secret from the terminal, without the value
ever appearing on screen, in shell history, or in a file.

WHY THIS EXISTS
---------------
`.github/workflows/deploy.yml` needs two repository secrets before it can deploy.
The GitHub web UI is the normal way to set them; this is for when clicking through
Settings -> Secrets and variables -> Actions is the harder path, which for this
project it is.

It matters that this is not "paste the token into chat". A repository secret is
readable by nothing that can read the repository -- not a session, not a clone,
not a fork. A token pasted into a conversation is in a transcript for ever. On
30 August 2026 a Cloudflare GLOBAL API key went into chat and had to be rolled;
that is the failure this tool exists to make unnecessary.

HOW THE VALUE IS PROTECTED
--------------------------
GitHub does not accept a secret in plaintext. It publishes a per-repository
public key and requires the value sealed to it with libsodium's sealed-box
construction, which is what PyNaCl's SealedBox does. So the value is encrypted on
your machine before it goes anywhere, and GitHub's API never sees the plaintext.

The value is read with getpass, so it is not echoed and does not enter shell
history. It is never written to disk and never printed, including in errors.

USAGE
-----
    python tools/set_repo_secret.py CLOUDFLARE_API_TOKEN
    python tools/set_repo_secret.py CLOUDFLARE_ACCOUNT_ID

It reads your GitHub token from `.gh-token` in the repo root (gitignored), or
from the GH_TOKEN / GITHUB_TOKEN environment variable. That token needs the
`repo` scope to write a secret.

    pip install pynacl        # the only dependency
"""
import base64, getpass, json, os, sys, urllib.error, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = "Samizdat-Publications/the-legacy-program-dashboard"


def github_token():
    for var in ("GH_TOKEN", "GITHUB_TOKEN"):
        v = os.environ.get(var)
        if v and v.strip():
            return v.strip()
    p = os.path.join(ROOT, ".gh-token")
    if os.path.exists(p):
        with open(p, encoding="utf-8") as fh:
            v = fh.read().strip()
        if v:
            return v
    sys.exit("No GitHub token. Put one in .gh-token in the repo root (it is\n"
             "gitignored), or set GH_TOKEN. It needs the `repo` scope.")


def api(path, token, method="GET", body=None):
    req = urllib.request.Request(
        "https://api.github.com" + path,
        data=json.dumps(body).encode() if body is not None else None,
        method=method,
        headers={"Authorization": "Bearer " + token,
                 "Accept": "application/vnd.github+json",
                 "X-GitHub-Api-Version": "2022-11-28",
                 "User-Agent": "the-program-set-secret"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else {})
    except urllib.error.HTTPError as e:
        # Deliberately does not echo the request body, which holds the secret.
        detail = ""
        try:
            detail = json.loads(e.read()).get("message", "")
        except Exception:
            pass
        msg = "GitHub API %s on %s%s" % (e.code, path, (": " + detail) if detail else "")
        if e.code in (403, 404):
            # 403 "Resource not accessible by personal access token" is what a
            # fine-grained PAT returns when it can reach the repo but lacks this
            # one permission, and the message never names the permission. 404 is
            # what a classic token without `repo` returns, because GitHub hides
            # the endpoint rather than admitting it exists. Both look like the
            # tool is broken and neither is.
            msg += ("\n\nThis endpoint needs a permission your token does not have.\n"
                    "\n  FINE-GRAINED token (github_pat_...):\n"
                    "    https://github.com/settings/personal-access-tokens\n"
                    "    Open the token -> Repository permissions -> set\n"
                    "        Secrets: Read and write\n"
                    "    Make sure this repository is in its selected repositories.\n"
                    "\n  CLASSIC token (ghp_...):\n"
                    "    https://github.com/settings/tokens\n"
                    "    It needs the full `repo` scope.\n"
                    "\nThe token itself is fine for everything else; this is one\n"
                    "checkbox. Nothing was sent, and the value you typed is gone.\n"
                    "\nOr set the two secrets in the browser instead, which needs no\n"
                    "token at all:\n"
                    "    https://github.com/%s/settings/secrets/actions\n"
                    "    -> New repository secret" % REPO)
        sys.exit(msg)


def main():
    if len(sys.argv) != 2:
        sys.exit("usage: python tools/set_repo_secret.py <SECRET_NAME>\n"
                 "e.g.   python tools/set_repo_secret.py CLOUDFLARE_API_TOKEN")
    name = sys.argv[1].strip()
    if not name.replace("_", "").isalnum() or not name[0].isalpha():
        sys.exit("A secret name must be letters, digits and underscores, "
                 "starting with a letter. Got %r" % name)

    try:
        from nacl import encoding, public
    except ImportError:
        sys.exit("PyNaCl is not installed. It does the encryption and there is no\n"
                 "fallback -- GitHub will not accept a plaintext secret. Run:\n\n"
                 "    pip install pynacl\n")

    token = github_token()

    # Prompt BEFORE any network call, so a typo in the name fails fast and the
    # value is not sitting in memory while a request is in flight.
    value = getpass.getpass("Value for %s (input is hidden, nothing is echoed): " % name)
    if not value.strip():
        sys.exit("Empty value; nothing was sent.")

    _, key = api("/repos/%s/actions/secrets/public-key" % REPO, token)
    sealed = public.SealedBox(
        public.PublicKey(key["key"].encode(), encoding.Base64Encoder)
    ).encrypt(value.encode())

    status, _ = api("/repos/%s/actions/secrets/%s" % (REPO, name), token, "PUT",
                    {"encrypted_value": base64.b64encode(sealed).decode(),
                     "key_id": key["key_id"]})

    print("\n%s %s on %s." % (name, "created" if status == 201 else "updated", REPO))
    print("The value was encrypted on this machine before it was sent, was never")
    print("written to disk, and is not in your shell history.")
    print("\nCheck it at: https://github.com/%s/settings/secrets/actions" % REPO)
    return 0


if __name__ == "__main__":
    sys.exit(main())
