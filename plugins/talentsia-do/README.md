# Talentsia Do

Your productivity multiplier. / Seu multiplicador de produtividade.

Talentsia Do is a skills-only plugin from Talentsia for turning accepted commitments into clear outcomes, practical next actions, and reliable follow-up. Version 0.1.0. It responds in English or Portuguese and keeps ideas separate from commitments.

## Install from the marketplace

The public marketplace is [talentsia/talentsia-skills](https://github.com/talentsia/talentsia-skills).

For ChatGPT desktop / Codex, on a supported installation with the Codex CLI:

```sh
codex plugin marketplace add talentsia/talentsia-skills --ref v0.1.0
```

Restart the ChatGPT desktop app, open the Plugins Directory, select **Talentsia Skills**, and install **Talentsia Do**. Availability varies by client; adding a marketplace is not installing its plugins. See [official guidance](https://developers.openai.com/plugins/build/plugins).

For Claude Code:

```sh
claude plugin marketplace add https://github.com/talentsia/talentsia-skills.git#v0.1.0
claude plugin install talentsia-do@talentsia-skills
```

Use a new, independent test context with synthetic inputs. Try “Use Talentsia Do to clarify these inbox items” or “Use Talentsia Do para esclarecer estes itens”. In supported Codex clients invoke `$talentsia-do`. Run the [acceptance scenarios](skills/talentsia-do/references/examples-and-acceptance.md) in PT and EN and record actual outputs. The manifests have been validated. Runtime behavior must be checked after installation with the included acceptance scenarios.

## Use your own system

Reuse your existing registry and authorized storage. If initial setup is requested, adapt the [empty private context template](skills/talentsia-do/assets/private-context.example.md) into a separate private location. Never put completed personal context in this plugin.

Pages can be used when the host has a suitable connection and permissions; local records or another existing application can also serve as the registry. The package contains no storage backend, MCP server, connected account, running specialist, or review schedule. Installation does not create them.

## Teste e uso em português

Adicione o marketplace usando o comando do seu cliente acima e selecione Talentsia Do para instalar. O cadastro no site não é necessário para instalar pelo GitHub. Teste com dados sintéticos, sem memória, arquivos ou conexões pessoais de outro usuário.

Peça respostas em português ou inglês; o assistente segue o idioma solicitado e mantém um único registro. O dono dos compromissos decide os compromissos. O responsável pelo sistema mantém evidências, próximas ações e acompanhamento. Ideias permanecem possibilidades até serem aceitas.

## Contents and rights

- `plugin.json`: portable Agent Plugins 1.0 identity and presentation metadata.
- The repository contains separate marketplace catalogs for ChatGPT/Codex and Claude Code.
- `assets/talentsia-do.svg`: original product icon.
- `skills/talentsia-do/`: workflow, UI metadata, references, PT/EN scenarios, and empty private context template.
- `AGENTS.md`: package maintenance instructions.

Methodological attribution and source links are in [methodology sources](skills/talentsia-do/references/methodology-sources.md). This is an independent implementation; no endorsement or ownership of third-party methodology is claimed. The package is publicly available. No open-source license is designated; copyright and third-party rights remain with their respective owners. Installation does not authorize purchases, external messages, or account creation.
