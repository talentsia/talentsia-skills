#!/usr/bin/env python3
"""A Talentsia seat, as MCP tools, for a harness that speaks MCP.

    python3 mcp_server.py --as designer

A thin wrapper, and deliberately one. Every call goes through
`talentsia_agent.call`, which does the signing; nothing here holds a second
copy of that arithmetic, so the two cannot drift. What the seat may do is what
the device enrolled it with: a tool listed here is still refused there if the
credential does not carry the permission. The tool list is convenience, never
authority.

Standard library only, stdio transport: a machine that runs a harness should
not need a package index to hold a seat.
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location(
    "talentsia_agent", HERE / "talentsia_agent.py")
agent = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(agent)

PROTOCOL = "2024-11-05"
VERSION = "0.1.2"

#: What this seat can do. Each maps to one signed request. The descriptions say
#: what the call is *for*, because a tool list is the whole of what a harness
#: knows before it chooses.
TOOLS = [
    {
        "name": "my_tasks",
        "description": (
            "The work waiting for this seat. Call it first, every session. "
            "Work delegated to it arrives as `ready` — take it with "
            "`take_task` before you begin. Work marked `waiting_for_user` is "
            "what the device's own worker could not finish. Omit `state` to "
            "see everything."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "state": {"type": "string",
                          "description": "one of: waiting_for_user, working, "
                                         "ready, completed, blocked"},
                "limit": {"type": "integer",
                          "description": "how many to return, 1 to 40; the newest come first"}},
        },
        # The device signs over the path and not the query, so the client
        # sends no query at all; the filter is applied here, over the most
        # recent work the device returns.
        "call": lambda a: ("tasks", None, "GET"),
        "after": lambda answer, a: _filter_tasks(answer, a),
    },
    {
        "name": "read_task",
        "description": (
            "Everything about one piece of work: what was asked, what has "
            "happened to it so far, what it is part of and what it produced."),
        "inputSchema": {
            "type": "object", "required": ["taskId"],
            "properties": {"taskId": {"type": "string",
                                      "description": "the task's id, as my_tasks returns it"}},
        },
        "call": lambda a: (f"tasks/{a['taskId']}", None, "GET"),
    },
    {
        "name": "how_this_seat_works",
        "description": (
            "The procedures this seat is on, and its standing rules, as the "
            "platform holds them. Read it at the start of a session: they are "
            "changed on the platform rather than here, so this is the current "
            "version and anything written into this machine's own files is "
            "not."),
        "inputSchema": {"type": "object", "properties": {}},
        "call": lambda a: ("craft", None, "GET"),
    },
    {
        "name": "objectives",
        "description": (
            "What this organisation is driving towards, and which area "
            "answers for each. Read it before deciding what a piece of work "
            "is for."),
        "inputSchema": {"type": "object", "properties": {}},
        "call": lambda a: ("intent", None, "GET"),
    },
    {
        "name": "say_what_you_are_doing",
        "description": (
            "A step somebody watching can see, on a task this seat holds. "
            "Your tools run on this machine, so the device shows nothing "
            "unless you post it — and work that is invisible for an hour "
            "looks like work nobody started. Post one when you begin, when "
            "you change approach, and when you file something."),
        "inputSchema": {
            "type": "object", "required": ["taskId", "note"],
            "properties": {
                "taskId": {"type": "string", "description": "the task this is about"},
                "note": {"type": "string",
                         "description": "what you just did, in one line, in English"}},
        },
        "call": lambda a: (f"tasks/{a['taskId']}/progress", {"note": a["note"]}, "POST"),
    },
    {
        "name": "file_deliverable",
        "description": (
            "File what you made, as a document in the organisation's own "
            "register. **Only when the person has said to file it** — this is "
            "the step that puts their name on work they have not seen. The "
            "body is the work itself, not a description of it. It lands as a "
            "draft; nothing here publishes. "
            "End it with a section headed exactly "
            "'## What I could not establish', in English, listing each thing "
            "and who could answer it: that section is lifted out and shown as "
            "the document's open questions, and a heading worded any other "
            "way is prose nobody can act on."),
        "inputSchema": {
            "type": "object", "required": ["title", "body"],
            "properties": {
                "title": {"type": "string", "description": "what the document is called"},
                "body": {"type": "string",
                         "description": "the work itself, in full, as markdown"},
                "taskId": {"type": "string",
                           "description": "the task it came from, so the two are linked"},
                "objectiveId": {"type": "string",
                                "description": "the objective it serves, from `objectives`"}},
        },
        "call": lambda a: ("artifacts", {
            "title": a["title"], "body": a["body"],
            **({"jobId": a["taskId"]} if a.get("taskId") else {}),
            **({"objectiveId": a["objectiveId"]} if a.get("objectiveId") else {})}, "POST"),
    },
    {
        "name": "file_image",
        "description": (
            "Put a picture you made on the device — the rendered post, the "
            "carousel slide, the thumbnail. Give it the file's path on this "
            "machine; it is read and sent. Do this before `file_deliverable`, "
            "and name what it returns in the deliverable so the two are one "
            "thing. PNG, JPEG or WebP, up to 8 MB."),
        "inputSchema": {
            "type": "object", "required": ["path"],
            "properties": {
                "path": {"type": "string",
                         "description": "the picture's path on this machine"},
                "name": {"type": "string",
                         "description": "what to call it on the device; the "
                                        "extension follows the bytes"}},
        },
        "call": "media",
    },
    {
        "name": "read_deliverables",
        "description": (
            "What has already been filed here, so you build on it rather "
            "than beside it. Without an id it lists them; with one it returns "
            "that document in full."),
        "inputSchema": {
            "type": "object",
            "properties": {"artifactId": {"type": "string",
                                          "description": "one document, in full"}},
        },
        "call": lambda a: (f"artifacts/{a['artifactId']}" if a.get("artifactId")
                           else "artifacts", None, "GET"),
    },
    {
        "name": "take_task",
        "description": (
            "Take a piece of work delegated to this seat, so it is yours and "
            "shows as working. **Only when the person has said to work on "
            "that one.** Taking it says somebody is on it; taking it because "
            "it was there says that falsely. Until it is taken the device "
            "could still start it itself."),
        "inputSchema": {
            "type": "object", "required": ["taskId"],
            "properties": {"taskId": {"type": "string",
                                      "description": "the task to take, as my_tasks returns it"}},
        },
        "call": lambda a: (f"tasks/{a['taskId']}/actions/take", {}, "POST"),
    },
    {
        "name": "finish_task",
        "description": (
            "Close a piece of work this seat was holding, saying what came of "
            "it. **Only when the person has said it is done.** Closing it "
            "takes it off their queue, so closing it on your own judgement "
            "removes the thing they were going to look at. Only work handed "
            "over or given up on can be closed."),
        "inputSchema": {
            "type": "object", "required": ["taskId", "note"],
            "properties": {
                "taskId": {"type": "string", "description": "the task to close"},
                "note": {"type": "string",
                         "description": "what was produced and where it was filed"}},
        },
        "call": lambda a: (f"tasks/{a['taskId']}/actions/complete",
                           {"note": a["note"]}, "POST"),
    },
    {
        "name": "file_task",
        "description": (
            "File a new piece of work. It is held in this seat's name and "
            "shows as working straight away, so the device's own worker does "
            "not start the same thing. Use `forWorker` to ask the device for "
            "something only it can do, and it is queued for that worker "
            "instead."),
        "inputSchema": {
            "type": "object", "required": ["goal"],
            "properties": {
                "goal": {"type": "string", "description": "what is to be done, in English"},
                "done": {"type": "string",
                         "description": ("what finished looks like, in one checkable line. "
                                         "Work without one cannot be finished by anybody — "
                                         "it is the difference between a piece of work and "
                                         "a theme.")},
                "objectiveId": {"type": "string", "description": "what it serves"},
                "forWorker": {"type": "string",
                              "description": "hand it to a worker on the device instead "
                                             "of holding it"}},
        },
        "call": lambda a: ("tasks", {
            "goal": (f"{a['goal']}\n\nDone when: {a['done']}"
                     if a.get("done") else a["goal"]),
            **({"objectiveId": a["objectiveId"]} if a.get("objectiveId") else {}),
            **({"forWorker": a["forWorker"]} if a.get("forWorker") else {})}, "POST"),
    },
    {
        "name": "what_is_waiting_for_me",
        "description": (
            "Everything this organisation has put in front of the person this "
            "seat acts for: decisions nobody has answered, alerts a worker "
            "raised, promises they owe, and work that gave up and escalated. "
            "Read it first — most of what looks like a stalled team is one "
            "unanswered question. You may draft an answer for each; you may "
            "not answer one."),
        "inputSchema": {"type": "object", "properties": {}},
        "call": lambda a: ("waiting", None, "GET"),
    },
    {
        "name": "change_direction",
        "description": (
            "Say what the organisation is doing instead, and close the work "
            "that no longer applies. One act: the reason goes into the "
            "decision log, the promises you name are superseded against it, "
            "any work already running for them is cancelled, and the new work "
            "is filed carrying what finished looks like.\n\n"
            "This is the act for 'stop that, do this'. Nothing else closes "
            "work nobody intends any more, so without it the team goes on "
            "chasing what was decided against. It changes what is being DONE "
            "about a goal; it never changes the goal itself, which is the "
            "person's own to set."),
        "inputSchema": {
            "type": "object", "required": ["what", "because"],
            "properties": {
                "what": {"type": "string",
                         "description": "the decision, in one line: what is happening now"},
                "because": {"type": "string",
                            "description": ("why — the half that is worth anything in six "
                                            "months. A sentence at least.")},
                "supersedes": {"type": "string",
                               "description": ("promise numbers this replaces, comma "
                                               "separated, from what_is_waiting_for_me or "
                                               "my_promises. Leave out if it replaces "
                                               "nothing.")},
                "do": {"type": "string",
                       "description": "the new work, if there is any, in English"},
                "done": {"type": "string",
                         "description": ("what finished looks like for that work, in one "
                                         "checkable line. Work without one cannot be "
                                         "finished by anybody.")},
                "forWorker": {"type": "string",
                              "description": "which worker on the device gets the new work"}},
        },
        "call": lambda a: ("directives", {
            "what": a["what"], "because": a["because"],
            "supersedes": {"commitments": [
                int(n) for n in str(a.get("supersedes") or "").replace(" ", "").split(",")
                if n.lstrip("-").isdigit()]},
            **({"do": a["do"]} if a.get("do") else {}),
            **({"done": a["done"]} if a.get("done") else {}),
            **({"forWorker": a["forWorker"]} if a.get("forWorker") else {})}, "POST"),
    },
    {
        "name": "my_promises",
        "description": (
            "What this seat owes and what its area answers for. Update one "
            "with `update_promise` — saying a state with nothing written "
            "against it records nothing."),
        "inputSchema": {"type": "object", "properties": {}},
        "call": lambda a: ("commitments", None, "GET"),
    },
    {
        "name": "update_promise",
        "description": (
            "Say what became of a promise written in this seat's name. A "
            "state with nothing written against it records nothing, and the "
            "executive accountable for it reads the note on its next pass."),
        "inputSchema": {
            "type": "object", "required": ["commitmentId", "state", "note"],
            "properties": {
                "commitmentId": {"type": "string", "description": "which promise"},
                "state": {"type": "string",
                          "description": "one of: on_track, at_risk, blocked, completed"},
                "note": {"type": "string", "description": "what you actually did about it"}},
        },
        "call": lambda a: (f"commitments/{a['commitmentId']}",
                           {"state": a["state"], "note": a["note"]}, "POST"),
    },
]
BY_NAME = {t["name"]: t for t in TOOLS}


#: What a picture's bytes say it is. The device checks this again and is the
#: one that decides; this only saves a round trip on an obvious mistake.
_MAGIC = ((b"\x89PNG\r\n\x1a\n", "image/png"), (b"\xff\xd8\xff", "image/jpeg"),
          (b"RIFF", "image/webp"))


def _picture(arguments: dict) -> tuple[str, dict, str]:
    """Read a picture off this machine and shape the request that carries it.

    The type comes from the bytes rather than from the name, because a name is
    something this machine chose and the bytes are what the device will check.
    """
    import base64
    from pathlib import Path

    where = Path(arguments["path"]).expanduser()
    maximum = 8 * 1024 * 1024
    with where.open('rb') as source:
        raw = source.read(maximum + 1)
    if len(raw) > maximum:
        raise SystemExit('picture exceeds the 8 MiB upload limit')
    kind = next((k for magic, k in _MAGIC if raw.startswith(magic)), "")
    if kind == 'image/webp' and raw[8:12] != b'WEBP':
        kind = ''
    if not kind:
        raise SystemExit(f"{where} is not a PNG, JPEG or WebP")
    return ("media", {"name": arguments.get("name") or where.name, "type": kind,
                      "bytes": base64.b64encode(raw).decode()}, "POST")


#: What the device returns for `tasks` with no filter: its most recent work,
#: newest first, dismissed work left out.
RECENT_TASKS = 40


def _filter_tasks(answer: dict, arguments: dict) -> dict:
    """Narrow the device's recent tasks to one state, and say what was looked at.

    The filter runs over the most recent tasks only, so an older task in the
    asked-for state can be missing. Saying so is the difference between "none
    waiting" and "none among the latest forty".
    """
    items = list(answer.get("items") or [])
    wanted = str(arguments.get("state") or "").strip()
    try:
        limit = max(1, min(int(arguments.get("limit") or 20), RECENT_TASKS))
    except (TypeError, ValueError):
        limit = 20
    matched = [i for i in items if not wanted or i.get("taskState") == wanted]
    out = {**answer, "items": matched[:limit]}
    out["note"] = (
        f"{len(matched)} of the {len(items)} most recent task(s)"
        + (f" are {wanted}" if wanted else "")
        + (f"; showing {limit}" if len(matched) > limit else "")
        + (". Only the most recent are searched; an older task can still exist."
           if len(items) >= RECENT_TASKS else "."))
    return out


def _listing() -> dict:
    return {"tools": [{k: t[k] for k in ("name", "description", "inputSchema")}
                      for t in TOOLS]}


def _invoke(name: str, arguments: dict, acting: str) -> dict:
    tool = BY_NAME.get(name)
    if tool is None:
        return {"content": [{"type": "text", "text": f"no such tool: {name}"}],
                "isError": True}
    try:
        if tool["call"] == "media":
            path, body, method = _picture(arguments or {})
        else:
            path, body, method = tool["call"](arguments or {})
        answer = agent.call(path, body, method=method, acting=acting)
        if tool.get("after"):
            answer = tool["after"](answer, arguments or {})
        return {"content": [{"type": "text",
                             "text": json.dumps(answer, indent=1, ensure_ascii=False)}]}
    except SystemExit as refusal:
        # The client turns a refusal into an exit; here it is an answer the
        # harness reads and can act on. A refusal that travels as success is
        # the worse failure, which is what isError is for.
        return {"content": [{"type": "text", "text": str(refusal)}], "isError": True}
    except Exception as error:  # noqa: BLE001 — a tool reports, it does not crash the server
        return {"content": [{"type": "text", "text": f"{type(error).__name__}: tool failed; detail withheld"}],
                "isError": True}


def serve(acting: str = "") -> int:
    """One JSON-RPC message per line, on stdin and stdout."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            message = json.loads(line)
        except ValueError:
            continue
        method, mid = message.get("method"), message.get("id")
        if method == "initialize":
            result = {"protocolVersion": PROTOCOL, "capabilities": {"tools": {}},
                      "serverInfo": {"name": "talentsia-work", "version": VERSION}}
        elif method == "tools/list":
            result = _listing()
        elif method == "tools/call":
            params = message.get("params") or {}
            result = _invoke(params.get("name", ""), params.get("arguments") or {}, acting)
        elif mid is None:
            continue           # a notification; nothing is owed back
        else:
            result = {}
        sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": mid, "result": result}) + "\n")
        sys.stdout.flush()
    return 0


def _acting(args: list[str]) -> str:
    """The seat named on the command line, or none.

    A harness that substitutes a setting nobody filled in may pass the
    placeholder through unexpanded; that is no seat, not a seat called that.
    """
    who = ""
    if "--as" in args:
        at = args.index("--as") + 1
        who = args[at] if at < len(args) else ""
    elif args and not args[0].startswith("-"):
        who = args[0]
    return "" if "${" in who else who.strip()


if __name__ == "__main__":
    sys.exit(serve(_acting(sys.argv[1:])))
