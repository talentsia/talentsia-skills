# Talentsia Skills

**Talentsia Do — Your productivity multiplier. / Seu multiplicador de produtividade.**

Talentsia Do 0.5.5 is one free plugin containing exactly ten productivity skills, in Portuguese and English. Each skill handles a distinct moment of work; all use one shared method and the user's existing trusted records. Ideas remain separate from accepted commitments. The native package bundles an optional read-only connection; no private Premium content or backend implementation is included.

Explore [skills.talentsia.com](https://skills.talentsia.com).

Talentsia Work 0.1.2 is a separate free plugin for business customers holding an enrolled seat on `talentsia.work`. It requires a local MCP-capable host, not a mobile chat attachment. See [installation, credential setup and release verification](plugins/talentsia-work/README.md). Its account/seat permissions and service terms are separate from the license on its files.

| Skill | Invocation name | Purpose |
| --- | --- | --- |
| Clear My Head | `clear-my-head` | Capture thoughts without inventing commitments |
| Organize My Work | `organize-my-work` | Turn inbox inputs into clear states and actions |
| Plan My Day | `plan-my-day` | Choose a realistic day from available capacity |
| Move Forward | `move-forward` | Find one concrete step that advances a project |
| Prepare | `prepare` | Prepare materials and readiness for an occasion |
| Do With Me | `do-with-me` | Produce real work and record the actual result |
| Follow Through | `follow-through` | Track promised results and close evidenced loops |
| Make Room | `make-room` | Propose practical tradeoffs to reduce overload |
| Resume | `resume` | Keep a checkpoint and restore the next step |
| Review | `review` | Reconcile commitments and expose project risks |

Ask naturally in PT/EN, or invoke a specific skill in supported clients: `$clear-my-head`, `$plan-my-day`, `$review`. A broader **Reset** can combine existing skills; **Someday/Maybe** is a record state. Neither is an additional skill.

## Choose a route by what you have in hand

You do not need to know which product tier or app variant you are using. Pick the first row that fits.

| You have… | Route | What you get |
| --- | --- | --- |
| Any chat app, on a phone or computer | [The skill file](#the-skill-file-one-file-no-installation) | One attached file with all ten skills; add it to a Project to keep it |
| ChatGPT desktop with a Plugins marketplace, or Codex | [ChatGPT desktop / Codex marketplace](#chatgpt-desktop--codex-marketplace) | Native installation with the ten skills listed separately; versioned updates |
| Claude Code | [Claude Code](#claude-code) | Native installation; versioned updates |
| Claude web/desktop, or another client that uploads skill ZIPs | [Skill ZIP upload](#skill-zip-upload-and-other-clients) | The same single skill, uploaded once |

Every route is generated from the same canonical source and carries the same version, so moving from the skill file to a native installation later changes nothing in your records.

## The skill file: one file, no installation

The ten skills are one pack: they share a method and hand work to each other, so they ship together. Each release publishes **`SKILL-talentsia-do-<version>.md`**: `SKILL.md` frontmatter, the shared method, the full instructions of all ten skills, and the review-and-planning and authority references. Get it from the [latest release](https://github.com/talentsia/talentsia-skills/releases/latest) or from [skills.talentsia.com](https://skills.talentsia.com).

**Try it in a new chat:** attach the file and send “Use the attached Talentsia Do skill in this conversation.”, then say what is on your mind. The assistant picks the fitting workflow or asks which one you want; you can also name one: “Use Plan My Day.”

**Keep it:** create a Project (or your app's equivalent space with instructions and files), add the same file, and set the Project instructions to: “Apply the attached Talentsia Do skill file as your operating instructions in every chat of this Project.” Replace the file when a new version is released; the version is in its first heading.

The file is instructions, not an installed plugin: it does not update itself and provides no storage, so records you want to keep belong in your own notes or files. Tested 2026-10-05 in the ChatGPT mobile app (free plan): attaching the file and sending the sentence worked. Other apps and plans have not been tested by Talentsia; try a fictional example first.

## ChatGPT desktop / Codex marketplace

Use **Add → Marketplace** with repository `talentsia/talentsia-skills`, branch `main`, catalog path `.agents/plugins`.

Alternatively, with a supported Codex CLI:

```sh
codex plugin marketplace add talentsia/talentsia-skills --ref main --sparse .agents/plugins
```

Restart the desktop app, choose Talentsia Skills in the Plugins Directory and install Talentsia Do. Adding a catalog does not install its plugin. The sparse catalog fetches the plugin independently from the immutable `v0.5.5` tag. Client and workspace availability can vary. This is a Git marketplace, not an OpenAI universal public-directory listing.

The same catalog now includes Talentsia Skill Builder. Install it with `codex plugin add talentsia-skill-builder@talentsia-skills`, or choose it in the desktop Plugins Directory after adding the marketplace. The entry tracks `main` until a versioned builder tag is published.

For an existing installation:

```sh
codex plugin marketplace upgrade talentsia-skills
```

Restart the app and update/reinstall Talentsia Do from its marketplace entry. Verify version **0.5.5** and the ten skills. Sources pinned to earlier tags stay on those versions. [Official OpenAI guide](https://developers.openai.com/plugins/build/plugins).

## Optional connected Plan My Day pilot

The native Do 0.5.5 package includes the read-only MCP endpoint in root `mcp.json`. Use the same plugin; no second Premium ZIP or manual MCP configuration is required on hosts supporting portable bundled MCP and Codex CIMD. Free workflows remain complete without login. The catalog uses `ON_USE` authentication, so installation does not require consent.

After updating the marketplace and installed plugin, open a fresh Codex task. Start the plugin's account/authentication flow when using the connected capability, sign in with your own Talentsia account, choose an existing accessible workspace and approve only the two Do read scopes. Exact account controls depend on the host; their presence and live execution still need a native host test. Talentsia Work connections and permissions are separate.

Ask “Use Plan My Day with my current connected Do access and these fictional constraints.” The assistant must first call `do_access_status({})`; active access permits `do_plan_my_day_method({})`. Unavailable access or connection failure continues Free, with the result disclosed. Only Plan My Day is covered by this pilot. A copied skill file/ZIP has no bundled live connection; keep using its Free instructions.

See the [verified connection and validation steps](docs/connected-premium-native-connection.md). Personal OAuth consent does not create a paid subscription or pilot entitlement.

## Claude Code

```sh
claude plugin marketplace add talentsia/talentsia-skills
claude plugin install talentsia-skill-builder@talentsia-skills
```

The marketplace follows `main`; the builder entry is `0.1.0`. Invoke `/talentsia-skill-builder:scope-a-skill`, `/talentsia-skill-builder:draft-a-skill`, `/talentsia-skill-builder:review-a-skill`, `/talentsia-skill-builder:test-a-skill` or `/talentsia-skill-builder:export-a-pack`. The same catalog contains Do and Work. [Official Claude Code guide](https://code.claude.com/docs/en/plugin-marketplaces).

These are repository marketplaces for ChatGPT desktop/Codex and Claude Code. They do not publish a plugin to ChatGPT's universal Plugins Directory; that requires a separate OpenAI submission and review. Other Agent Skills-compatible hosts can install the `plugins/talentsia-skill-builder/skills/<name>` folders directly according to their own skill procedure. Skill instructions are portable; subagent execution depends on the host, and the pack specifies sequential fallback where delegation is unavailable.

## Skill ZIP upload and other clients

Each release includes **`talentsia-do-skill-<version>.zip`**, which contains the same single skill as `talentsia-do/SKILL.md`, and **`talentsia-do-plugin-<version>.zip`**, the native ten-skill plugin folder for manual installation.

In Claude web/desktop, upload `talentsia-do-skill-<version>.zip` through **Customize → Skills → + → Create skill → Upload a skill**, then enable it; the assistant chooses among the ten workflows inside it. Do not upload the plugin ZIP as a skill. [Official skill guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

Other Agent Skills-compatible clients can use `plugins/talentsia-do/skills/<name>` folders from the plugin ZIP according to their installation procedure. A chat attachment or repository is not a universal installer.

## Try the pack

- PT: “Use Clear My Head para capturar o que está na minha cabeça, sem virar tudo obrigação.”
- EN: “Use Plan My Day to choose work that fits my available time and energy.”
- PT: “Use Do With Me para revisar este rascunho, sem publicar.”

Start with synthetic inputs. [Behavior evaluation cases](evals/README.md) cover routing, all ten scopes and shared boundaries. Static validation does not prove model behavior; record observed outputs in the target client before declaring behavioral tests passed.

## Talentsia Work (free)

**Talentsia Work 0.1.2** lets Codex or Claude Code hold a seat in an organisation that runs on Talentsia: a position on its chart filled by an outside agent. Six skills (Connect Seat, Start Work, Deliver Work, Keep Promises, Hand Over, What Needs Me) and four role agents work through a small signed MCP client that connects to the organisation's own Talentsia workspace. The seat reads its procedures live from the organisation's device. This package carries no organisation content and no credentials, and it never publishes, sends, approves or decides anything.

It needs a Talentsia organisation and a seat that a person has enrolled on its device, so it is installed natively rather than attached as a skill file. Install it from the same marketplaces: `codex plugin add talentsia-work@talentsia-skills`, or `claude plugin install talentsia-work@talentsia-skills`. Setup and the one-seat versus several-seat arrangement are in the [Talentsia Work README](plugins/talentsia-work/README.md). Releases are tagged `talentsia-work-v<version>`, separately from Talentsia Do's `v<version>`.

## Skills for Talentsia Edge workers (free)

Eight packages give the resident workers on a Talentsia Edge device their craft, the way a phone gains abilities from apps:

| Package | For |
|---|---|
| [`talentsia-operations`](plugins/talentsia-operations/README.md) | looking after the device, routing what arrives |
| [`talentsia-chief-of-staff`](plugins/talentsia-chief-of-staff/README.md) | briefing, triage, keeping and closing promises, meetings, time |
| [`talentsia-executive`](plugins/talentsia-executive/README.md) | running an area: moving its work, briefing specialists, judging what comes back |
| [`talentsia-recruiting`](plugins/talentsia-recruiting/README.md) | diagnosing what is missing, designing seats and procedures |
| [`talentsia-engineering`](plugins/talentsia-engineering/README.md) | changes, reviews and scans in authorised repositories |
| [`talentsia-bookkeeping`](plugins/talentsia-bookkeeping/README.md) | basic bookkeeping a worker can do safely |
| [`talentsia-insurance`](plugins/talentsia-insurance/README.md) | reading policies, comparing options, renewals |
| [`talentsia-content`](plugins/talentsia-content/README.md) | social posts an organisation can approve |

These are the free, basic editions, MIT licensed. Enhanced and practice-specific editions are premium. A skill here is prose only: it requires capabilities, never names tools, and grants nothing. The device decides what its worker may do. The contract, including subagents and per-model evals, is in [docs/edge-worker-skills.md](docs/edge-worker-skills.md). Validate with `python3 scripts/check_edge_skills.py`.

## Migration, privacy and rights

The legacy `$talentsia-do` catch-all skill is replaced by ten skills inside the same `talentsia-do` plugin; the single skill file is a distribution format of those same ten, not a return to the catch-all. See [CHANGELOG](CHANGELOG.md) for migration. Existing personal records need no conversion, copying or relocation. Remove a separately uploaded legacy skill only after checking the new installation; this release does not edit user settings, live Pages or personal projects.

This instructions-only plugin creates no storage backend, connected account, worker or schedule. Personal records stay in user-owned storage. Without tools/persistence, skills provide portable records marked not saved and disclose unperformed actions. Email, calendar and third-party actions require explicit human authorization. No guaranteed productivity result is promised.

© 2026 Talentsia. Everything in this repository, including Talentsia Do and Talentsia Work, is licensed under the [MIT License](LICENSE); business use is allowed. See [NOTICE.md](NOTICE.md) for what the license does not cover: premium packs, which are protected by entitlement in a separate private repository; Talentsia services and accounts; names and logos; and third-party rights, which remain with their owners.

## Maintain the package

Canonical shared references live under `plugins/talentsia-do/references/`; the hand-kept compressed method used in the skill file lives in `plugins/talentsia-do/pocket/method.md` and must be revised whenever `references/core.md` changes meaning. Run `python3 scripts/package.py` to synchronize identical self-contained exports and build the plugin ZIP outside the repository. It makes no network calls. The plugin has exactly ten `skills/*/SKILL.md` entrypoints; shared references are not skills.

Build the skill file and its upload ZIP with `python3 scripts/skill_file.py --output /tmp/talentsia-do-release`, then verify all artifacts with `python3 scripts/check_candidate.py --output /tmp/talentsia-do-release` and `python3 scripts/privacy_scan.py --output /tmp/talentsia-do-release`. A release has exactly three distributable artifacts: the skill file, the skill ZIP and the plugin ZIP, plus checksums and the validation report. The release includes 64 authored behavior cases; model runs and real app behavior remain unexecuted.

Talentsia Work is packaged separately. Run `python3 scripts/package_work.py --output /tmp/talentsia-work-release`, then `python3 scripts/privacy_scan.py --output /tmp/talentsia-work-release`. That build synchronises the seat-protocol exports, validates both harness manifests, smoke-tests the MCP server with no credentials, and writes the plugin ZIP, a `SHA256SUMS` file covering the ZIP and the client scripts, and a checks report. Its [synthetic cases](evals/talentsia-work-cases.json) are authored and not run.

To start a new pack, copy [`plugins/talentsia-skill-template`](plugins/talentsia-skill-template/README.md). It carries the Do layout — one canonical method under `references/`, byte-identical exports per skill, a pocket method, a subagent role template and package instructions — with placeholders instead of workflows. It is not installable, not listed in the marketplace manifests and not built by any release script.

[`plugins/talentsia-skill-builder`](plugins/talentsia-skill-builder/README.md) is the installable counterpart: five skills (Scope, Draft, Review, Test, Export) and six subagent roles that make packs in this layout from inside Codex, ChatGPT desktop or Claude Code, fed by references that carry the skill contract, template, subagent and eval contracts, capability vocabulary, review checklist and export layout. Build and validate it with `python3 scripts/package_builder.py --output /tmp/talentsia-skill-builder-release`. It is listed in both repository marketplace manifests on `main`; its conversational test is a rehearsal, and the measured pass rate still comes from `scripts/eval_edge_skills.py`.
