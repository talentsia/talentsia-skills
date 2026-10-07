# skills.talentsia.com handoff — source candidate, not published

Keep the public Do install instructions and one plugin identity. Connected
Premium is planned as account-based access through the existing Talentsia OAuth
connection, with current server checks for every protected call. No mandatory ZIP
or second plugin in that flow. Pilot coverage is Plan My Day only; other nine
Premium extensions remain draft. Do not present the pilot as available until
Platform adapter, confirmed MCP discovery/scopes, host tests and release gates
pass. Free workflows work without signing in or subscribing.

Suggested website copy (informational):

PT: “Instale Talentsia Do uma vez. Os dez fluxos Free continuam disponíveis.
Com sua conta Talentsia conectada e acesso Premium ativo, os recursos conectados
liberados usam o mesmo plugin. O piloto de Plan My Day ainda está em validação.”

EN: “Install Talentsia Do once. All ten Free workflows remain available.
With your Talentsia account connected and active Premium access, released
connected capabilities use the same plugin. The Plan My Day pilot is still
being validated.”

Account states: disconnected → retain Free and offer existing account connection;
connected without entitlement → show current access as unavailable, retain Free;
active → show only released capabilities; revoked/expired → future protected
calls unavailable, retain Free; service error → state unknown, retry, retain Free.
Keep scopes missing distinct from unpaid subscription. Do not infer identity or
entitlement from a browser-provided account/workspace identifier. Subscription
status must come from authenticated server state. Work organisation/seat access
remains separate.

Explain that copied/downloaded/chat content may remain after cancellation and
that dynamic MCP responses are instructions, not installed native skills or
proof of subagent execution. Existing optional downloads require private storage,
subscriber terms, reviewed release and server authorization; never expose private
source as public assets. The website may handle external sales under its own
rules; plugin instructions/tool responses must avoid upsell and checkout links.

Site owner must implement/review copy and subscription UI in the actual website
source. This handoff does not deploy the site, change billing, promise a live
endpoint, install a plugin or create OAuth grants. Contract source:
`plugins/talentsia-do/references/connected-contract.json`; private counterpart:
`connected/README.md` in talentsia-premium-skills.

Release preparation: these isolated source edits keep current manifest version 0.5.1 for local review. Before any public release, assign and validate a new version/tag; the private pilot intentionally continues to reference the immutable original Free 0.5.1 snapshot, not this changed candidate.

Matching Platform source now implements a disabled non-seat OAuth/PKCE/consent/refresh pilot and MCP handler at source path `/v1/do/mcp`. The actual deployed URL/audience and verified callback remain unconfigured. Existing Talentsia sign-in is reused, but existing Work/userinfo tokens cannot silently gain Do scopes. Access currently comes from explicit server-side pilot assignments; paid billing sync is not implemented. The Site backend must call `do_access_status` with authenticated server-held OAuth credentials and empty arguments. Hosts must consume structured tool output; native skill import and agent execution remain unverified.
