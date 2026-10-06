# Talentsia Work 0.1.0

Hold a seat in your Talentsia organisation from Codex or Claude Code.

A **seat** is a position on your organisation's Talentsia chart that is filled by an outside agent rather than by a person or one of your own workers. Talentsia Work connects this assistant to that seat through a signed MCP connection to your organisation's Talentsia workspace. The seat reads its procedures live, takes work, posts progress somebody can watch, files deliverables, keeps its promises and hands work over. Authoritative records and procedures stay on your organisation's device; the assistant receives private context needed for the task. The seat key is stored locally on this machine, not in the plugin or chat.

## What is in it

- **Six skills:** Connect Seat, Start Work, Deliver Work, Keep Promises, Hand Over and What Needs Me. They share one seat protocol.
- **Four role agents:** Content Designer, Content Writer, Software Engineer and Executive Assistant. They carry general craft only; your organisation's procedures for the seat override them.
- **A seat client:** `server/talentsia_agent.py` signs each request, `server/mcp_server.py` presents it as 15 MCP tools, and `server/setup_seat.py` checks credentials and writes per-seat agents. Python 3.10 or later, standard library only.

## Before you install

You need a Talentsia organisation and a seat. Someone with access to your device creates the position (held by an **agent**) and enrols it. Enrolment gives the seat an id, a workspace address ending in `/agents/v1`, and a key that the device shows **once**.

Store the key yourself in a local editor, not chat, shell command arguments, or a command containing the key (shell history retains commands). In your own terminal, create the private directory and file without overwriting existing seats:

```bash
mkdir -p ~/.talentsia && chmod 700 ~/.talentsia
touch ~/.talentsia/agents.json
chmod 600 ~/.talentsia/agents.json
nano ~/.talentsia/agents.json
```

In the editor, add a profile using the id and HTTPS workspace URL supplied by enrolment, and replace the key placeholder with the 64 hex characters. Preserve existing profiles; each seat must have its own enrolled key:

```json
{
    "designer": {
        "id": "<seat id supplied by enrolment>",
        "key": "<64 hex characters; enter only in the local editor>",
        "workspace": "https://<your-organisation>.talentsia.work/agents/v1"
    }
}
```

The client refuses non-HTTPS URLs, redirects, URL-embedded credentials, invalid keys, and credential files readable by other users on POSIX systems. File profiles take precedence over single-seat environment variables. Do not put a key in a harness manifest or commit this file. If exposed, revoke/reissue it on the device; deleting the chat is not key rotation.

## Install

- **ChatGPT desktop / Codex:** add the marketplace `talentsia/talentsia-skills` (branch `main`, path `.agents/plugins`), then install Talentsia Work. On a supported Codex CLI: `codex plugin marketplace add talentsia/talentsia-skills --ref main --sparse .agents/plugins`, then `codex plugin add talentsia-work@talentsia-skills`.
- **Claude Code:** `claude plugin marketplace add https://github.com/talentsia/talentsia-skills.git`, then `claude plugin install talentsia-work@talentsia-skills`.

Then ask: "Use Connect Seat to connect this assistant to my Talentsia seat."

Alternatively, download and verify the plugin ZIP as described below, then extract it into a private local directory. In the commands below, replace `<plugin>` with the absolute path of that extracted `talentsia-work` folder or your harness's installed plugin folder; it is not a literal command argument. Verify Python availability with `python3 --version` (client requires 3.10+).

Before any live connection, run:

```bash
python3 <plugin>/server/setup_seat.py check --seat designer
```

Only after this passes, `check --seat designer --online` makes a signed read of this seat's procedures. The commands do not print the key. Do not attach the plugin ZIP or credentials to an ordinary ChatGPT/mobile chat: this pack requires a host that runs local MCP servers.

## One seat or several

With one seat in the credential file, the plugin's server acts as that seat and nothing else needs doing. With several seats, each gets its own agent, so a session never has to choose who it is:

```bash
python3 <plugin>/server/setup_seat.py roles
python3 <plugin>/server/setup_seat.py codex-agent  --seat designer --role content-designer
python3 <plugin>/server/setup_seat.py claude-agent --seat engineer --role software-engineer --file ~/.talentsia/engineer.json
python3 <plugin>/server/setup_seat.py check --seat designer --online
```

Agent generation first validates the named profile. Every generated agent pins an absolute credential-file path and `--as` seat name. For stronger isolation, use one private credential file per seat with `--file`; separate profiles select identities, but are not an OS sandbox. The plugin's single-seat server refuses an ambiguous multi-seat file. Your harness may still expose unrelated tools; authorize them separately.

The helper copies the client to `~/.talentsia/bin` so agents keep working across plugin updates. After updating the plugin, run `python3 <plugin>/server/setup_seat.py install` again. Existing agents continue using the copied client until this step; a plugin update alone does not refresh it. For role-instruction changes, regenerate the relevant agent with `--force` only after reviewing any local edits. Nothing migrates or changes existing live seats automatically.

## Verify the release

The release is tagged `talentsia-work-v0.1.0`, separately from Talentsia Do. The public GitHub Actions release workflow builds, checks and generates signed build-provenance attestations for the ZIP, checksum file and report. With a recent GitHub CLI, verify downloaded assets before extracting or executing them:

```bash
gh release download talentsia-work-v0.1.0 --repo talentsia/talentsia-skills --dir ./talentsia-work-download
cd talentsia-work-download
gh attestation verify talentsia-work-plugin-0.1.0.zip --repo talentsia/talentsia-skills --signer-workflow talentsia/talentsia-skills/.github/workflows/release-work.yml --source-ref refs/tags/talentsia-work-v0.1.0 --deny-self-hosted-runners
gh attestation verify talentsia-work-0.1.0.SHA256SUMS --repo talentsia/talentsia-skills --signer-workflow talentsia/talentsia-skills/.github/workflows/release-work.yml --source-ref refs/tags/talentsia-work-v0.1.0 --deny-self-hosted-runners
shasum -a 256 -c talentsia-work-0.1.0.SHA256SUMS
unzip talentsia-work-plugin-0.1.0.zip
```

The bundled attestation is available for offline verification. A local packaging run produces checksums but not a signed attestation. Marketplace clients fetch the tagged Git source, not this attested ZIP. Build provenance verifies origin/integrity, not model behavior or platform authorization.

## License and verification limits

The entire Work plugin (client, setup helper, skills, references and roles) is [MIT licensed](LICENSE): commercial/business use is permitted with its copyright/license notice. This license does not grant service access, override Talentsia account or subscription terms, or license trademarks. Talentsia Do and premium packs retain their separate licenses.

Offline security tests cover credential errors, permissions, request signing, redirect refusal, seat selection, bounded image reads and setup. Model behavior fixtures are authored, not executed. Runtime discovery and signed reads were reported by the implementation team before review; this release adds offline regressions and does not certify all versions of Codex, Claude Code or all seat permissions.

## What it will not do

It exposes no publishing, sending, merging, deploying, decision-answering, objective-setting or hiring tools. It does post progress and file authorized draft records. The platform must enforce the seat's actual scopes; these instructions are not an authorization firewall. Taking work, filing deliverables, closing tasks, changing direction and updating promises each require your explicit approval for that item in the skill instructions. Every deliverable ends with **What I could not establish**, so its open questions reach the people who can answer them.

Choose by need: set up → Connect Seat; begin a session → Start Work; file finished work → Deliver Work; report on what you owe → Keep Promises; give work to the right worker → Hand Over; clear what waits on you → What Needs Me. In Codex use `$start-work`; in Claude Code use `/talentsia-work:start-work`.
