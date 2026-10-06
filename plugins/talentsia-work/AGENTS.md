# Talentsia Work package instructions

This free plugin lets an assistant hold a seat in a Talentsia organisation. It contains six skills sharing one canonical protocol in `references/seat-protocol.md`, four role agents in `agents/`, and a standard-library MCP client in `server/`. Each skill reads its own exported copy of the protocol. The organisation, its device and the person decide what is done. The assistant works the seat inside the protocol.

The package holds no organisation content: no procedures, brand rules, records, workspace addresses or credentials. A seat reads its procedures live from the device with `how_this_seat_works`, so a role agent carries general craft only and defers to them. Never add an organisation's facts, a device address, a seat id or a key to any file here, an example or a test.

After editing the protocol, run `python3 scripts/package_work.py` from the repository root to synchronise the exports, validate the manifests, smoke-test the MCP server without credentials, and build the archive with its checksums. Never edit exported copies on their own.

Layout rules that the script enforces:

- Codex reads this plugin from `.codex-plugin/plugin.json`, whose `mcpServers` points to `codex-mcp.json`. Do not add a root `plugin.json`: when one exists, Codex reads it instead and starts no MCP server.
- Claude Code reads `.claude-plugin/plugin.json`, with the server inline under `${CLAUDE_PLUGIN_ROOT}`. Keep `userConfig` out until the Claude Code releases in use accept it.
- The client is standard library only. Keep the signing in `talentsia_agent.py`; `mcp_server.py` must never compute a signature of its own. When the client changes, bump the plugin version and the server's `VERSION` together.
- Skills never carry executable code. The code lives in `server/`, ships under a release tag with checksums, and is reviewed as code.

Before distribution, validate JSON, frontmatter, local references, six-skill discovery, the four role agents, icons, the MCP handshake and the archive contents. Packaging does not enrol seats, issue credentials, expand permissions, publish, send, approve or decide anything.
