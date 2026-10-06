#!/usr/bin/env python3
"""Reach a Talentsia workspace as an enrolled outside agent.

Part of the Talentsia Work plugin. A person enrols the seat on their Talentsia
device and is shown its key once; this client signs every request with it.

One machine may hold several seats — a designer and an engineer are different
seats with different reach — so credentials live in a file of named profiles
and every invocation names the one it is acting as:

    ~/.talentsia/agents.json          0600, one entry per seat

    {
      "designer": {
        "id": "designer",
        "key": "<the 64 hex characters shown once at enrolment>",
        "workspace": "https://<your-organisation>.talentsia.work/agents/v1"
      }
    }

    python3 talentsia_agent.py --as designer tasks
    python3 talentsia_agent.py --as designer post commitments/12 '{"state":"on_track","note":"…"}'

Reads:  intent (the organisation's objectives), craft (this seat's procedures),
        tasks, tasks/<id>, artifacts, artifacts/<id>, commitments, waiting.
Writes: post tasks '{"goal":"…"}', post tasks/<id>/progress '{"note":"…"}',
        post tasks/<id>/actions/take '{}',
        post tasks/<id>/actions/complete '{"note":"…"}',
        post commitments/<id> '{"state":"on_track","note":"…"}',
        post artifacts '{"title":"…","body":"…"}'.
Also:   `who` lists the seats this machine can act as (never the keys);
        `help` prints this.

There is deliberately no current seat and no default when more than one is
configured: an identity that drifts ends up doing one seat's work under
another's name.

A single seat may use the environment instead:

    export TALENTSIA_AGENT_ID=designer
    export TALENTSIA_AGENT_KEY=<the key>
    export TALENTSIA_WORKSPACE=https://<your-organisation>.talentsia.work/agents/v1

TALENTSIA_AGENTS_FILE points at a different profiles file, for example one
file per seat.

Everything that makes a request what it is goes into the signature — the
method, the path, the body, the moment and a nonce — so a captured request is
useless a minute later and useless twice. Standard library only.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import re
import secrets
import stat
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlsplit
from pathlib import Path

TIMEOUT_SECONDS = 60


PROFILES = Path(os.environ.get("TALENTSIA_AGENTS_FILE", "")
                or Path.home() / ".talentsia" / "agents.json")


def _profiles() -> dict:
    try:
        with PROFILES.open() as source:
            metadata = os.fstat(source.fileno())
            if os.name == 'posix' and (metadata.st_uid != os.getuid() or stat.S_IMODE(metadata.st_mode) & 0o077):
                raise SystemExit('credential file must be owned by this user and have mode 600')
            profiles = json.load(source)
        if not isinstance(profiles, dict) or any(not isinstance(profile, dict) for profile in profiles.values()):
            raise SystemExit('credential file must contain an object of named seat profiles')
        return profiles
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as error:
        raise SystemExit('credential file could not be read or is not valid JSON') from None


def _credentials(acting: str = "") -> tuple[str, bytes, str]:
    """Which agent this invocation is, and nothing ambient about it."""
    known = _profiles()
    if acting or known:
        if not acting:
            if len(known) != 1:
                raise SystemExit(
                    f"name which agent to act as: --as {' | --as '.join(sorted(known))}. "
                    "There is no default when more than one is configured, because an "
                    "identity that drifts does one seat's work under another's name.")
            acting = next(iter(known))
        profile = known.get(acting)
        if profile is None:
            raise SystemExit(f"no agent called {acting!r} in {PROFILES}. "
                             f"It holds: {', '.join(sorted(known)) or 'nothing'}")
        agent = str(profile.get("id") or acting)
        key = str(profile.get("key") or "")
        base = str(profile.get("workspace") or "").rstrip("/")
        if not (key and base):
            raise SystemExit(f"the {acting!r} profile needs a key and a workspace")
        return agent, _key(key, f"the {acting!r} profile in {PROFILES}"), base
    agent = os.environ.get("TALENTSIA_AGENT_ID", "").strip()
    key = os.environ.get("TALENTSIA_AGENT_KEY", "").strip()
    base = os.environ.get("TALENTSIA_WORKSPACE", "").strip().rstrip("/")
    if not (agent and key and base):
        raise SystemExit(f"no agent configured. Either write {PROFILES}, or set "
                         "TALENTSIA_AGENT_ID, TALENTSIA_AGENT_KEY and "
                         "TALENTSIA_WORKSPACE.")
    return agent, _key(key, "TALENTSIA_AGENT_KEY"), base


def _key(value: str, where: str) -> bytes:
    """The credential, or a sentence somebody can act on.

    It used to be `bytes.fromhex` with nothing around it, so pasting the
    placeholder out of the instructions — which is an ordinary thing to do —
    produced a traceback ending in "non-hexadecimal number found at position
    0". True, and it names neither the file nor what was expected.
    """
    if not re.fullmatch(r'[0-9a-fA-F]{64}', value):
        raise SystemExit('seat key must be exactly 64 hexadecimal characters; value withheld')
    return bytes.fromhex(value)


def _workspace(base: str) -> str:
    try:
        parsed = urlsplit(base)
        valid = (parsed.scheme == 'https' and parsed.hostname and not parsed.username
                 and not parsed.password and not parsed.query and not parsed.fragment
                 and parsed.path.rstrip('/') == '/agents/v1' and parsed.port != 0)
    except ValueError:
        valid = False
    if not valid:
        raise SystemExit('workspace must be an HTTPS URL ending in /agents/v1, without credentials, query or fragment')
    return base.rstrip('/')


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise urllib.error.HTTPError(req.full_url, code, 'redirect refused', headers, fp)


def call(path: str, body: dict | None = None, *, method: str = "",
         acting: str = "") -> dict:
    """One signed request, as exactly one agent. `path` is relative to its
    workspace address."""
    agent, key, base = _credentials(acting)
    base = _workspace(base)
    if not re.fullmatch(r'[a-zA-Z0-9_-]+(?:/[a-zA-Z0-9_-]+)*', path):
        raise SystemExit('request path must be a relative API path without query, fragment or traversal')
    method = method or ("POST" if body is not None else "GET")
    raw = json.dumps(body).encode() if body is not None else b""
    # The path as the device sees it, which is what it signs over.
    full = f"{base}/{path.lstrip('/')}"
    signed_path = urlsplit(full).path
    stamp = f"{time.time():.0f}"
    nonce = secrets.token_hex(16)
    material = "\n".join((method, signed_path, stamp, nonce,
                          hashlib.sha256(raw).hexdigest()))
    headers = {
        "X-Talentsia-Agent": agent,
        "X-Talentsia-Timestamp": stamp,
        "X-Talentsia-Nonce": nonce,
        "X-Talentsia-Signature": hmac.new(key, material.encode(),
                                          hashlib.sha256).hexdigest(),
    }
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(full, data=raw or None, headers=headers,
                                     method=method)
    try:
        with urllib.request.build_opener(_NoRedirect()).open(request, timeout=TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode() or "{}")
    except urllib.error.HTTPError as error:
        if error.code == 401:
            # The device will not say which way a credential failed, and that
            # is deliberate — so the useful guesses are listed here instead.
            raise SystemExit(
                "refused: the device did not accept this request. Either the "
                "agent is not enrolled there, the key is wrong, this machine's "
                "clock is more than a minute out, or the request was replayed."
            ) from None
        raise SystemExit(f'refused: HTTP {error.code}; response detail withheld') from None
    except OSError as error:
        raise SystemExit('the workspace is not reachable; network detail withheld') from None


def main(argv: list[str]) -> int:
    args = argv[1:]
    acting = ""
    if args and args[0] == "--as":
        if len(args) < 2:
            raise SystemExit("--as needs the name of an agent")
        acting, args = args[1], args[2:]
    if not args:
        print(__doc__)
        if _profiles():
            print("Configured here:", ", ".join(sorted(_profiles())))
        return 2
    if args[0] in ("help", "--help", "-h"):
        # The first thing anybody tries, and it answered "not found" — because
        # usage printed only when there were no arguments at all, which is not
        # what somebody who wants help types.
        print(__doc__)
        return 0
    if args[0] == "who":
        # What this machine can act as, and never the keys.
        for name, profile in sorted(_profiles().items()):
            print(f"{name}\t{profile.get('workspace', '')}")
        return 0
    if args[0] == "post":
        body = json.loads(args[2]) if len(args) > 2 else {}
        print(json.dumps(call(args[1], body, acting=acting), indent=1))
        return 0
    print(json.dumps(call(args[0], acting=acting), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
