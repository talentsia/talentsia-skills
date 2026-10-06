---
name: connect-seat
description: "Connect this assistant to a seat in a Talentsia organisation and check it works: enrolment on the device, the credential file, the MCP server, and a first signed read. Use for conectar meu assento, set up my Talentsia seat, or when a Talentsia tool says no agent is configured."
---

# Connect Seat

Read [the seat protocol](references/seat-protocol.md) before proceeding, then follow the seat's own procedures from `how_this_seat_works`; they override this skill on how the work is done.

A seat is created and enrolled by a person, on the organisation's own device, never from here. Without an enrolment there is nothing to connect, so find out first where things stand.

1. **Is the seat enrolled?** Ask whether someone with access to the device has created the position (Organisation → add a position, held by an **agent**) and enrolled it. Enrolment gives the seat an id, a workspace address ending in `/agents/v1` and a key, and the device shows the key once. If none of that has happened, say who has to do it and stop. Do not guess an address or an id.
2. **Where does the credential live?** In `~/.talentsia/agents.json`, mode `0600`, one profile per seat: `{"<seat>": {"id": "<agent id>", "key": "<key>", "workspace": "https://<organisation>.talentsia.work/agents/v1"}}`. Use one file per seat (pointed to by `TALENTSIA_AGENTS_FILE`) when different subagents hold different seats. **Never ask for the key in chat.** Give the person the command to write the file and set its mode, and let them paste the key into their own terminal. If a key appears in the conversation anyway, say it should be reissued.
3. **Point the harness at the seat.**
   - **One seat on this machine:** nothing to do. The plugin's `talentsia-work` server, in both Codex and Claude Code, acts as the only profile in the file.
   - **Several seats:** give each one its own agent, so no session has to choose an identity. Run `python3 <plugin>/server/setup_seat.py codex-agent --seat <seat> --role <role>` (or `claude-agent`). It installs the client in `~/.talentsia/bin` and writes `~/.codex/agents/<seat>.toml` (or `~/.claude/agents/<seat>.md`) with its own server acting as that seat. `setup_seat.py roles` lists the roles. Add `--file ~/.talentsia/<seat>.json` when each seat has its own credential file.
   - **Any other MCP harness:** run `python3 <plugin>/server/mcp_server.py --as <seat>` over stdio.
4. **Prove it with one read.** Call `how_this_seat_works`. A procedure list means the seat is connected. Then call `my_tasks`. If a call is refused with "the device did not accept this request", check, in this order: the seat is enrolled on *that* device, the key is the one shown at enrolment, the machine's clock is within a minute, and the address is the workspace's `/agents/v1`. `python3 <plugin>/server/setup_seat.py check --seat <seat>` checks the file and its mode without printing the key.

Report what is connected: seat, organisation address and the number of procedures. Never report the key. Writing anything to the organisation is not part of connecting.

**PT:** “Conecte meu assento de designer na Talentsia.” Check the enrolment first and never ask for the key in chat. **EN:** “My Talentsia tool says no agent is configured.” Walk through the credential file and a first read.
