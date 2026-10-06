#!/usr/bin/env python3
"""Set a machine up to hold Talentsia seats. Never reads a key aloud.

    python3 setup_seat.py check --seat designer [--file PATH] [--online]
    python3 setup_seat.py install
    python3 setup_seat.py codex-agent  --seat designer --role content-designer [--name NAME] [--file PATH] [--force]
    python3 setup_seat.py claude-agent --seat designer --role content-designer [--name NAME] [--file PATH] [--force]
    python3 setup_seat.py roles

`check` verifies the credential file without printing the key: that it exists,
that only its owner can read it, and that the profile holds an id, a key of the
right shape and a workspace address. `--online` then makes one signed read of
the seat's procedures.

`install` copies the seat client to ~/.talentsia/bin, a path that does not
change when the plugin is updated, so a harness configured against it keeps
working. Run it again after updating the plugin.

`codex-agent` and `claude-agent` write a custom agent for one seat, built from
this plugin's role definitions, with its own MCP server acting as that seat and
nothing else (in ~/.codex/agents or ~/.claude/agents). A machine holding several
seats gets one agent per seat, so no session ever has to choose which identity
it is. The plugin's own server is for a machine with one seat.

Standard library only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PLUGIN = HERE.parent
ROLES = PLUGIN / "agents"
CLIENT = ("talentsia_agent.py", "mcp_server.py")
HOME = Path.home() / ".talentsia"
DEFAULT_FILE = HOME / "agents.json"
SEAT = re.compile(r"[a-z0-9][a-z0-9_-]{0,62}")


def _say(ok: bool, text: str) -> bool:
    print(("ok    " if ok else "FIX   ") + text)
    return ok


def _profiles_file(given: str) -> Path:
    return Path(given or os.environ.get("TALENTSIA_AGENTS_FILE", "") or DEFAULT_FILE).expanduser()


def check(seat: str, given: str, online: bool) -> int:
    path = _profiles_file(given)
    if not _say(path.is_file(), f"credential file {path}"):
        print(f"      Create it with the profile the device gave you, then: chmod 600 {path}")
        return 1
    mode = stat.S_IMODE(path.stat().st_mode)
    good = _say(mode & 0o077 == 0, f"only its owner can read it (mode {mode:o})")
    if not good:
        print(f"      chmod 600 {path}")
    try:
        profiles = json.loads(path.read_text())
    except ValueError:
        _say(False, "the file is not valid JSON")
        return 1
    if not seat and len(profiles) == 1:
        seat = next(iter(profiles))
    if not _say(seat in profiles, f"profile {seat!r}" + ("" if seat in profiles
                else f" (it holds: {', '.join(sorted(profiles)) or 'nothing'})")):
        return 1
    profile = profiles[seat]
    good &= _say(bool(str(profile.get("id", seat))), f"agent id {profile.get('id', seat)!r}")
    key = str(profile.get("key", ""))
    good &= _say(re.fullmatch(r"[0-9a-fA-F]{64,}", key) is not None,
                 "a key of the right shape (64 hex characters; not shown)")
    base = str(profile.get("workspace", ""))
    good &= _say(base.startswith("https://") and base.rstrip("/").endswith("/agents/v1"),
                 f"workspace address {base or '(missing)'} (https, ending in /agents/v1)")
    if online and good:
        sys.path.insert(0, str(HERE))
        os.environ["TALENTSIA_AGENTS_FILE"] = str(path)
        import talentsia_agent  # noqa: E402 - loaded after the file is chosen
        try:
            craft = talentsia_agent.call("craft", acting=seat)
        except SystemExit as refusal:
            return 0 if _say(False, f"signed read: {refusal}") else 1
        count = len(craft.get("skills") or craft.get("procedures") or [])
        _say(True, f"signed read accepted; the device returned {count} procedure(s)")
    return 0 if good else 1


def install(target: Path = HOME / "bin") -> Path:
    target.mkdir(parents=True, exist_ok=True)
    os.chmod(target.parent, 0o700)
    for name in CLIENT:
        shutil.copy2(HERE / name, target / name)
    print(f"ok    seat client installed in {target}")
    return target


def _role(role: str) -> tuple[str, str]:
    source = ROLES / f"{role}.md"
    if not source.is_file():
        raise SystemExit(f"no role {role!r}; roles: {', '.join(roles())}")
    _, front, body = source.read_text().split("---", 2)
    fields = dict(line.split(": ", 1) for line in front.strip().splitlines())
    return fields["description"], body.strip()


def roles() -> list[str]:
    return sorted(p.stem for p in ROLES.glob("*.md"))


def _toml(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _target(harness: str, name: str, force: bool) -> Path:
    if harness == "codex":
        root = Path(os.environ.get("CODEX_HOME", "") or Path.home() / ".codex")
        target = root.expanduser() / "agents" / f"{name}.toml"
    else:
        root = Path(os.environ.get("CLAUDE_CONFIG_DIR", "") or Path.home() / ".claude")
        target = root.expanduser() / "agents" / f"{name}.md"
    if target.exists() and not force:
        raise SystemExit(f"{target} exists; pass --force to replace it")
    return target


def write_agent(harness: str, seat: str, role: str, name: str, given: str,
                force: bool) -> int:
    for label, value in (("seat", seat), ("agent", name or seat)):
        if not SEAT.fullmatch(value):
            raise SystemExit(f"a {label} name is lower case letters, digits, '-' or '_'")
    name = name or seat
    description, instructions = _role(role)
    description += f" Holds the Talentsia seat {seat!r}."
    target = _target(harness, name, force)
    server = install() / "mcp_server.py"
    command = sys.executable or "python3"
    args = [str(server), "--as", seat]
    env = {"TALENTSIA_AGENTS_FILE": str(Path(given).expanduser())} if given else {}
    if harness == "codex":
        lines = [f"name = {_toml(name)}", f"description = {_toml(description)}",
                 f"developer_instructions = {_toml(instructions)}", "",
                 "[mcp_servers.talentsia]", f"command = {_toml(command)}",
                 f"args = {json.dumps(args)}"]
        if env:
            lines += ["", "[mcp_servers.talentsia.env]"] + [
                f"{k} = {_toml(v)}" for k, v in env.items()]
    else:
        # Inline servers are ignored in plugin agents, so a seat-specific
        # agent lives in the user's own agents directory instead.
        lines = ["---", f"name: {name}", f"description: {_toml(description)}",
                 "mcpServers:", "  - talentsia:", "      type: stdio",
                 f"      command: {_toml(command)}", f"      args: {json.dumps(args)}"]
        if env:
            lines.append(f"      env: {json.dumps(env)}")
        lines += ["---", "", instructions.replace(
            "through the `talentsia-work` tools", "through the `talentsia` tools")]
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("\n".join(lines) + "\n")
    print(f"ok    {harness} agent {name!r} written to {target}, acting as seat {seat!r}")
    print("      Start a new session and ask for it by name.")
    return 0


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    c = sub.add_parser("check")
    c.add_argument("--seat", default="")
    c.add_argument("--file", default="")
    c.add_argument("--online", action="store_true")
    sub.add_parser("install")
    sub.add_parser("roles")
    for harness in ("codex", "claude"):
        a = sub.add_parser(f"{harness}-agent")
        a.add_argument("--seat", required=True)
        a.add_argument("--role", required=True, choices=roles())
        a.add_argument("--name", default="")
        a.add_argument("--file", default="")
        a.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    if args.command == "check":
        return check(args.seat, args.file, args.online)
    if args.command == "install":
        install()
        return 0
    if args.command == "roles":
        print("\n".join(roles()))
        return 0
    return write_agent(args.command.split("-")[0], args.seat, args.role, args.name,
                       args.file, args.force)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
