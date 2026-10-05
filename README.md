# Talentsia Skills

**Talentsia Do — Your productivity multiplier. / Seu multiplicador de produtividade.**

Talentsia Do 0.4.3 is one free plugin containing exactly ten productivity skills, in Portuguese and English. Each skill handles a distinct moment of work; all use one shared method and the user's existing trusted records. Ideas remain separate from accepted commitments. No premium content or backend is included.

Explore [skills.talentsia.com](https://skills.talentsia.com).

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
| Any chat app, on a phone or computer, and want to try it now | **Pocket pack file** (below) | One attached file with all ten skills; works in a single conversation |
| Any chat app and prefer to paste text rather than attach a file | **Pocket start text** (below) | One pasted message with the method and a map of the ten skills |
| A chat app with Projects (or an equivalent space with instructions + files) and want it to persist | **Project instructions + reference file** (below) | Reusable setup you own; not a native plugin |
| ChatGPT desktop with a Plugins marketplace, or Codex | [ChatGPT desktop / Codex marketplace](#chatgpt-desktop--codex-marketplace) | Native installation and versioned updates |
| Claude Code | [Claude Code](#claude-code) | Native installation and versioned updates |
| Claude web/desktop with custom skills | [Individual skill ZIPs](#individual-skill-zips-and-other-clients) | One uploaded skill at a time |

All routes are generated from the same canonical source and carry the same version, so moving from the pocket edition to a native installation later changes nothing in your records.

## Pocket edition: one file, no installation

The ten skills are one pack: they share a method and hand work to each other, so the pocket edition ships them together. The [0.4.3 release](https://github.com/talentsia/talentsia-skills/releases/tag/v0.4.3) publishes:

- `SKILL-talentsia-do-0.4.3.md`: **the complete pack.** Shaped like a `SKILL.md` (frontmatter with name and description), then the shared method, the full instructions of all ten skills, and the review-and-planning and authority references. Attach it to a new chat.
- `SKILL-talentsia-do-start-0.4.3.md`: a short version with the shared method and a map of the ten skills, sized to paste as a first message when attaching a file is inconvenient.
- `talentsia-do-project-instructions-0.4.3.md` + `talentsia-do-project-reference-0.4.3.md`: for a persistent Project, paste the instructions into the Project's instruction field and upload the reference file to the same Project.

**In a new chat:** attach `SKILL-talentsia-do-0.4.3.md` and send “Use the attached Talentsia Do skill in this conversation.”, then say what is on your mind; the assistant picks the fitting workflow or asks which one you want. Do not attach `talentsia-do-pocket-0.4.3.zip` to a chat; it bundles the files for the website and bulk download, and an assistant given a zip tends to summarize it rather than follow it.

A skill file is instructions for one conversation or Project. It is not an installed plugin, does not persist by itself, and provides no storage; records you want to keep belong in your own notes or files. Tested 2026-10-05 in the ChatGPT mobile app (free plan): the pasted start text worked; an attached file was followed once the user sent the sentence above; an attached zip was not followed strictly. Other apps and plans have not been tested by Talentsia; try a fictional example first.

## ChatGPT desktop / Codex marketplace

Use **Add → Marketplace** with repository `talentsia/talentsia-skills`, branch `main`, catalog path `.agents/plugins`.

Alternatively, with a supported Codex CLI:

```sh
codex plugin marketplace add talentsia/talentsia-skills --ref main --sparse .agents/plugins
```

Restart the desktop app, choose Talentsia Skills in the Plugins Directory and install Talentsia Do. Adding a catalog does not install its plugin. The sparse catalog fetches the plugin independently from the immutable `v0.4.3` tag. Client and workspace availability can vary. This is a Git marketplace, not an OpenAI universal public-directory listing.

For an existing installation:

```sh
codex plugin marketplace upgrade talentsia-skills
```

Restart the app and update/reinstall Talentsia Do from its marketplace entry. Verify version **0.4.3** and the ten skills. Sources pinned to earlier tags stay on those versions. [Official OpenAI guide](https://developers.openai.com/plugins/build/plugins).

## Claude Code

```sh
claude plugin marketplace add https://github.com/talentsia/talentsia-skills.git#v0.4.3
claude plugin install talentsia-do@talentsia-skills
```

Invoke, for example, `/talentsia-do:clear-my-head` or `/talentsia-do:review`. Existing marketplace sources pinned to an earlier tag must be changed to the new tag before updating the plugin. [Official Claude Code guide](https://code.claude.com/docs/en/plugin-marketplaces).

## Individual skill ZIPs and other clients

The [0.4.3 release](https://github.com/talentsia/talentsia-skills/releases/tag/v0.4.3) includes one plugin ZIP and ten individual skill ZIPs, named such as `clear-my-head-0.4.3.zip`. Each individual ZIP is self-contained and includes the shared reference export.

In Claude web/desktop, upload each desired individual skill ZIP through **Customize → Skills → + → Create skill → Upload a skill**, then enable it. Do not upload the whole plugin ZIP as a single skill. [Official skill guide](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

Other Agent Skills-compatible clients use the appropriate `plugins/talentsia-do/skills/<name>` folder according to their installation procedure. A chat attachment or repository is not a universal installer.

## Try the pack

- PT: “Use Clear My Head para capturar o que está na minha cabeça, sem virar tudo obrigação.”
- EN: “Use Plan My Day to choose work that fits my available time and energy.”
- PT: “Use Do With Me para revisar este rascunho, sem publicar.”

Start with synthetic inputs. [Behavior evaluation cases](evals/README.md) cover routing, all ten scopes and shared boundaries. Static validation does not prove model behavior; record observed outputs in the target client before declaring behavioral tests passed.

## Migration, privacy and rights

The legacy `$talentsia-do` catch-all skill is replaced by ten skills inside the same `talentsia-do` plugin. See [CHANGELOG](CHANGELOG.md) for migration. Existing personal records need no conversion, copying or relocation. Remove a separately uploaded legacy skill only after checking the new installation; this release does not edit user settings, live Pages or personal projects.

This instructions-only plugin creates no storage backend, connected account, worker or schedule. Personal records stay in user-owned storage. Without tools/persistence, skills provide portable records marked not saved and disclose unperformed actions. Email, calendar and third-party actions require explicit human authorization. No guaranteed productivity result is promised.

[Methodology sources](plugins/talentsia-do/references/methodology-sources.md) identify influences without endorsement or certification. Copyright © 2026 Talentsia. No open-source license is designated; copyright and third-party rights remain with their respective owners.

## Maintain the package

Canonical shared references live under `plugins/talentsia-do/references/`; the hand-kept compressed method for pasteable artifacts lives in `plugins/talentsia-do/pocket/method.md` and must be revised whenever `references/core.md` changes meaning. Run `python3 scripts/package.py` to synchronize identical self-contained exports, validate package structure and build ZIPs outside the repository. It makes no network calls. The plugin has exactly ten `skills/*/SKILL.md` entrypoints; shared references are not skills.

Generate the indexed Project adaptation with `python3 scripts/mobile_reference.py --output /tmp/talentsia-do-release/talentsia-do-project-reference-0.4.3.md`, then the pocket texts and ZIP with `python3 scripts/pocket.py --output /tmp/talentsia-do-release`, then check archives, reference closure and pocket budgets with `python3 scripts/check_candidate.py --output /tmp/talentsia-do-release`. The Project reference and pocket texts are context, not native installation or automatic storage. The release includes 64 authored behavior cases; model runs, real mobile app behavior and pasted-text behavior remain unexecuted.
