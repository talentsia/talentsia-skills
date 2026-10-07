#!/usr/bin/env python3
"""Validate every Edge-worker skill package in this repository.

A package is a plugin with a `talentsia-package.json`. Its skills follow the
contract in docs/edge-worker-skills.md, which a Talentsia Edge device loads:
a SKILL.md in the open format, a skill.json for the catalog, optional subagent
specs, and graded eval cases. Standard library only, like every script here.

    python3 scripts/check_edge_skills.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CAPABILITIES = json.loads((ROOT / "capabilities" / "v1.json").read_text())["interfaces"]

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
SLUG = re.compile(r"^[a-z0-9-]{1,64}$")
WORK_KIND = re.compile(r"^[a-z][a-z0-9_]{1,63}$")
ALLOWED_FILES = {".md", ".json"}
TIERS = ("small-local", "large-local", "frontier")
TARGETS = {"edge-worker", "seat", "personal"}
MAX_STEPS, MAX_AGENT_STEPS, MAX_LINE = 8, 6, 300
MAX_ENTRYPOINT_TOKENS = 1500
REF = re.compile(r"\{\{(tool|agent):([a-z0-9._/-]+)\}\}")

errors: list[str] = []


def fail(where: Path | str, message: str) -> None:
    errors.append(f"{Path(where).relative_to(ROOT) if isinstance(where, Path) else where}: {message}")


def frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        fail(path, "must start with frontmatter")
        return {}, text
    head, _, body = text[4:].partition("\n---\n")
    fields: dict = {}
    for line in head.splitlines():
        key, sep, value = line.partition(":")
        if not sep or not re.fullmatch(r"[a-zA-Z][a-zA-Z0-9]*", key):
            fail(path, f"frontmatter line is not `key: value`: {line!r}")
            continue
        value = value.strip()
        if value[:1] in '"[{':
            try:
                fields[key] = json.loads(value)
            except ValueError as error:
                fail(path, f"frontmatter `{key}` is not valid JSON: {error}")
        else:
            fields[key] = value
    return fields, body


def sections(path: Path, body: str) -> dict[str, list[str]]:
    found: dict[str, list[str]] = {}
    current = None
    for line in body.splitlines():
        if line.startswith("## "):
            current = line[3:].strip()
            if current in found:
                fail(path, f"section `{current}` appears twice")
            found[current] = []
        elif current is not None:
            found[current].append(line)
    return found


def numbered(path: Path, lines: list[str], what: str, limit: int) -> list[str]:
    steps = [l for l in lines if re.match(r"^\d+\. ", l)]
    for i, step in enumerate(steps, 1):
        if not step.startswith(f"{i}. "):
            fail(path, f"{what} are not numbered 1..n in order")
            break
        if len(step) > MAX_LINE + 5:
            fail(path, f"{what} {i} is longer than {MAX_LINE} characters")
    if not steps:
        fail(path, f"{what}: none found")
    if len(steps) > limit:
        fail(path, f"{len(steps)} {what}, the limit is {limit}")
    return [re.sub(r"^\d+\. ", "", s) for s in steps]


def bullets(path: Path, lines: list[str], what: str) -> list[str]:
    items = [l[2:].strip() for l in lines if l.startswith("- ")]
    if not items:
        fail(path, f"{what}: no `- ` lines")
    for item in items:
        if len(item) > MAX_LINE:
            fail(path, f"a `{what}` line is longer than {MAX_LINE} characters")
    return items


def check_refs(path: Path, text: str, interfaces: set[str], agents: set[str]) -> None:
    for kind, target in REF.findall(text):
        if kind == "agent":
            if target not in agents:
                fail(path, f"{{{{agent:{target}}}}} is not one of this skill's subagents")
            continue
        iface, _, operation = target.partition("/")
        if iface not in interfaces:
            fail(path, f"{{{{tool:{target}}}}} names `{iface}`, which skill.json does not require")
        elif operation not in CAPABILITIES[iface]["operations"]:
            fail(path, f"{{{{tool:{target}}}}}: `{iface}` has no operation `{operation}`")


def check_agent(path: Path, interfaces: set[str]) -> None:
    fields, body = frontmatter(path)
    if set(fields) != {"name", "description", "tools", "model", "maxSteps", "input", "output"}:
        fail(path, "subagent frontmatter must be exactly name, description, tools, model, maxSteps, input, output")
        return
    if fields["name"] != path.stem:
        fail(path, "name must equal the file name")
    if not isinstance(fields["tools"], list):
        # Empty is allowed and common: a subagent that only reasons over its
        # input holds no tool at all, which is the narrowest it can be.
        fail(path, "tools must be a JSON list of interface/operation, empty if it uses none")
    else:
        for tool in fields["tools"]:
            iface, _, operation = str(tool).partition("/")
            if iface not in interfaces:
                fail(path, f"tool `{tool}`: a subagent may only narrow its skill's capabilities")
            elif operation not in CAPABILITIES[iface]["operations"]:
                fail(path, f"tool `{tool}`: no such operation")
    if fields["model"] not in TIERS:
        fail(path, f"model must be one of {TIERS}")
    if not isinstance(fields["maxSteps"], int) and not str(fields["maxSteps"]).isdigit():
        fail(path, "maxSteps must be a number")
    elif int(fields["maxSteps"]) > MAX_AGENT_STEPS:
        fail(path, f"maxSteps is at most {MAX_AGENT_STEPS}")
    if not isinstance(fields["input"], dict) or not fields["input"]:
        fail(path, "input must be a JSON object naming each field")
    output = fields["output"]
    if not isinstance(output, dict) or output.get("type") != "object" or not output.get("required"):
        fail(path, "output must be a JSON Schema object with `required` fields")
    found = sections(path, body)
    for needed in ("Steps", "Done when"):
        if needed not in found:
            fail(path, f"missing `## {needed}`")
    if "Steps" in found:
        numbered(path, found["Steps"], "steps", MAX_AGENT_STEPS)
    check_refs(path, body, interfaces, set())


def check_evals(path: Path, interfaces: set[str], agents: set[str]) -> None:
    if not path.exists():
        fail(path, "missing: every skill ships graded eval cases")
        return
    document = json.loads(path.read_text())
    cases = document.get("cases") if document.get("schema") == "talentsia-skill-evals/v1" else None
    if not isinstance(cases, list) or len(cases) < 3:
        fail(path, "needs schema talentsia-skill-evals/v1 and at least three cases")
        return
    seen = set()
    for case in cases:
        cid = case.get("id")
        if not cid or cid in seen:
            fail(path, f"case id missing or repeated: {cid!r}")
        seen.add(cid)
        given, expect = case.get("given"), case.get("expect")
        if not isinstance(given, dict) or not given.get("goal"):
            fail(path, f"{cid}: `given.goal` is required")
        if not isinstance(expect, dict) or not expect or set(expect) - {"calls", "notCalls", "says", "notSays", "agents"}:
            fail(path, f"{cid}: `expect` takes calls, notCalls, says, notSays, agents")
            continue
        for key in ("calls", "notCalls"):
            for call in expect.get(key, []):
                iface, _, operation = call.partition("/")
                if iface not in CAPABILITIES or operation not in CAPABILITIES[iface]["operations"]:
                    fail(path, f"{cid}: `{call}` is not a known interface/operation")
                elif key == "calls" and iface not in interfaces:
                    fail(path, f"{cid}: expects `{call}`, which the skill does not require")
        for agent in expect.get("agents", []):
            if agent not in agents:
                fail(path, f"{cid}: expects subagent `{agent}`, which the skill does not declare")


def check_skill(package: dict, folder: Path) -> None:
    for file in folder.rglob("*"):
        if file.is_file() and file.suffix not in ALLOWED_FILES:
            fail(file, "skills carry no code: only .md and .json are allowed")
    skill_md, spec_path = folder / "SKILL.md", folder / "skill.json"
    if not skill_md.exists() or not spec_path.exists():
        fail(folder, "needs SKILL.md and skill.json")
        return
    fields, body = frontmatter(skill_md)
    if set(fields) != {"name", "description"}:
        fail(skill_md, "frontmatter must be exactly name and description")
    if fields.get("name") != folder.name or not SLUG.match(folder.name):
        fail(skill_md, "name must equal the folder name, [a-z0-9-]")
    if not isinstance(fields.get("description"), str) or not 1 <= len(fields["description"]) <= 1024:
        fail(skill_md, "description must be a JSON-quoted string of 1 to 1024 characters")
    found = sections(skill_md, body)
    order = [s for s in found if s in ("When to use", "Steps", "Done when", "Notes")]
    if order[:3] != ["When to use", "Steps", "Done when"]:
        fail(skill_md, "sections must start: When to use, Steps, Done when (then optional Notes)")
    extra = set(found) - {"When to use", "Steps", "Done when", "Notes"}
    if extra:
        fail(skill_md, f"unexpected sections: {sorted(extra)}")
    steps = numbered(skill_md, found.get("Steps", []), "steps", MAX_STEPS)
    done = bullets(skill_md, found.get("Done when", []), "Done when")
    entrypoint = "\n".join(found.get("When to use", []) + found.get("Steps", []) + found.get("Done when", []))
    if len(entrypoint) / 4 > MAX_ENTRYPOINT_TOKENS:
        fail(skill_md, f"entrypoint is ~{len(entrypoint) // 4} tokens, the limit is {MAX_ENTRYPOINT_TOKENS}")

    spec = json.loads(spec_path.read_text())
    required = {"schema", "id", "version", "status", "publisher", "tier", "edition", "license",
                "targets", "summary", "appliesTo", "requires", "model", "budget", "verification",
                "reads", "subagents", "replaces"}
    missing = required - set(spec)
    if missing:
        fail(spec_path, f"missing fields: {sorted(missing)}")
        return
    unknown = set(spec) - required
    if unknown:
        fail(spec_path, f"unknown fields: {sorted(unknown)}")
    if spec["schema"] != "talentsia-skill/v1":
        fail(spec_path, "schema must be talentsia-skill/v1")
    parts = spec["id"].split(".")
    if len(parts) != 3 or parts[0] != "talentsia" or parts[2] != folder.name:
        fail(spec_path, "id is talentsia.<domain>.<folder name>")
    if not SEMVER.match(spec["version"]):
        fail(spec_path, "version must be semver")
    if spec["status"] not in ("draft", "released"):
        fail(spec_path, "status is draft or released")
    for key in ("publisher", "tier", "edition", "license"):
        if spec[key] != package[key]:
            fail(spec_path, f"{key} must match the package ({package[key]!r})")
    if not spec["targets"] or set(spec["targets"]) - TARGETS:
        fail(spec_path, f"targets must be from {sorted(TARGETS)}")
    if spec["summary"] != fields.get("description"):
        fail(spec_path, "summary must equal SKILL.md's description")
    if not isinstance(spec["appliesTo"], list) or not all(WORK_KIND.match(k) for k in spec["appliesTo"]):
        fail(spec_path, "appliesTo is a list of kinds of work, lower_snake_case")
    interfaces = set()
    for capability in spec["requires"].get("capabilities", []):
        iface, _, version = capability.partition("@")
        if iface not in CAPABILITIES:
            fail(spec_path, f"unknown capability interface `{iface}` (capabilities/v1.json)")
        elif version != str(CAPABILITIES[iface]["version"]):
            fail(spec_path, f"`{capability}`: v1 of the vocabulary defines @{CAPABILITIES[iface]['version']}")
        interfaces.add(iface)
    if not interfaces:
        fail(spec_path, "requires.capabilities must name at least one interface")
    model = spec["model"]
    if not isinstance(model.get("minContextTokens"), int) or set(model.get("tiers", [])) - set(TIERS):
        fail(spec_path, "model needs minContextTokens and tiers from " + ", ".join(TIERS))
    if spec["status"] == "released":
        for tier in model.get("tiers", []):
            if not any(model.get("evals", {}).values()):
                fail(spec_path, f"a released skill claiming `{tier}` needs published eval results")
    if spec["verification"] != done:
        fail(spec_path, "verification must equal SKILL.md's `Done when` lines exactly")
    agents = set(spec["subagents"])
    for agent in agents:
        if not (folder / "agents" / f"{agent}.md").exists():
            fail(spec_path, f"subagent `{agent}` has no agents/{agent}.md")
    for path in (folder / "agents").glob("*.md") if (folder / "agents").exists() else []:
        if path.stem not in agents:
            fail(path, "not listed in skill.json subagents")
        check_agent(path, interfaces)
    for entry in spec["replaces"]:
        if set(entry) != {"id", "version"}:
            fail(spec_path, "replaces entries are {id, version}")
    check_refs(skill_md, body, interfaces, agents)
    check_evals(folder / "evals" / "cases.json", interfaces, agents)
    if steps and not any("{{tool:" in s for s in steps):
        fail(skill_md, "no step names a tool through {{tool:…}}; a skill that uses no tool is advice")


def main() -> int:
    packages = sorted(ROOT.glob("plugins/*/talentsia-package.json"))
    for manifest in packages:
        package = json.loads(manifest.read_text())
        folder = manifest.parent
        for key in ("schema", "name", "version", "publisher", "tier", "edition", "license",
                    "targets", "description", "skills"):
            if key not in package:
                fail(manifest, f"missing `{key}`")
        if errors:
            continue
        if package["schema"] != "talentsia-package/v1" or package["name"] != folder.name:
            fail(manifest, "schema talentsia-package/v1, and name equal to the folder")
        if package["license"] != "MIT" or not (folder / "LICENSE").exists():
            fail(manifest, "everything on skills.talentsia.com is MIT, with a LICENSE file")
        if package["tier"] != "free" or package["edition"] != "basic":
            fail(manifest, "this public repository ships the free basic edition only")
        listed = set(package["skills"])
        present = {p.name for p in (folder / "skills").iterdir() if p.is_dir()}
        if listed != present:
            fail(manifest, f"skills listed {sorted(listed - present)} vs on disk {sorted(present - listed)}")
        for name in sorted(present):
            check_skill(package, folder / "skills" / name)
    for error in errors:
        print("FAIL", error)
    count = sum(len(json.loads(p.read_text())["skills"]) for p in packages)
    print(f"{len(packages)} packages, {count} skills: {'ok' if not errors else f'{len(errors)} problems'}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
