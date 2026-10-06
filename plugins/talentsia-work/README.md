# Talentsia Work 0.1.0

Hold a seat in your Talentsia organisation from Codex or Claude Code.

A **seat** is a position on your organisation's Talentsia chart that is filled by an outside agent rather than by a person or one of your own workers. Talentsia Work connects this assistant to that seat through a signed MCP connection to your organisation's Talentsia workspace. The seat reads its procedures live, takes work, posts progress somebody can watch, files deliverables, keeps its promises and hands work over. Your records, procedures and keys stay on your own Talentsia device.

## What is in it

- **Six skills:** Connect Seat, Start Work, Deliver Work, Keep Promises, Hand Over and What Needs Me. They share one seat protocol.
- **Four role agents:** Content Designer, Content Writer, Software Engineer and Executive Assistant. They carry general craft only; your organisation's procedures for the seat override them.
- **A seat client:** `server/talentsia_agent.py` signs each request, `server/mcp_server.py` presents it as 15 MCP tools, and `server/setup_seat.py` checks credentials and writes per-seat agents. Python 3.10 or later, standard library only.

## Before you install

You need a Talentsia organisation and a seat. Someone with access to your device creates the position (held by an **agent**) and enrols it. Enrolment gives the seat an id, a workspace address ending in `/agents/v1`, and a key that the device shows **once**.

Put the credential in `~/.talentsia/agents.json` yourself, in your own terminal. Never paste the key into a chat:

```bash
mkdir -p ~/.talentsia && chmod 700 ~/.talentsia
cat > ~/.talentsia/agents.json <<'JSON'
{ "designer": { "id": "designer", "key": "<the key the device showed>",
                "workspace": "https://<your-organisation>.talentsia.work/agents/v1" } }
JSON
chmod 600 ~/.talentsia/agents.json
```

## Install

- **ChatGPT desktop / Codex:** add the marketplace `talentsia/talentsia-skills` (branch `main`, path `.agents/plugins`), then install Talentsia Work. On a supported Codex CLI: `codex plugin marketplace add talentsia/talentsia-skills --ref main --sparse .agents/plugins`, then `codex plugin add talentsia-work@talentsia-skills`.
- **Claude Code:** `claude plugin marketplace add https://github.com/talentsia/talentsia-skills.git`, then `claude plugin install talentsia-work@talentsia-skills`.

Then ask: "Use Connect Seat to connect this assistant to my Talentsia seat."

## One seat or several

With one seat in the credential file, the plugin's server acts as that seat and nothing else needs doing. With several seats, each gets its own agent, so a session never has to choose who it is:

```bash
python3 <plugin>/server/setup_seat.py roles
python3 <plugin>/server/setup_seat.py codex-agent  --seat designer --role content-designer
python3 <plugin>/server/setup_seat.py claude-agent --seat engineer --role software-engineer --file ~/.talentsia/engineer.json
python3 <plugin>/server/setup_seat.py check --seat designer --online
```

The helper copies the client to `~/.talentsia/bin` so agents keep working across plugin updates. Run `install` again after you update the plugin. It never prints a key.

## What it will not do

It never publishes, sends, posts, merges, deploys, answers a decision, sets an objective or employs a worker. No seat credential can do these, and the skills do not try. Taking work, filing deliverables, closing tasks, changing direction and updating promises each wait for your say-so on that item. Every deliverable ends with **What I could not establish**, so its open questions reach the people who can answer them.

Choose by need: set up → Connect Seat; begin a session → Start Work; file finished work → Deliver Work; report on what you owe → Keep Promises; give work to the right worker → Hand Over; clear what waits on you → What Needs Me. In Codex use `$start-work`; in Claude Code use `/talentsia-work:start-work`.
