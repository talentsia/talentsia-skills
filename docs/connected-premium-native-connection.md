# Native connected Do pilot

Do 0.5.5 bundles the verified endpoint to root `mcp.json` in the existing portable
plugin. The ten Free workflows retain their instructions. No private method,
account identity, secret, grant, entitlement or second Premium plugin is bundled.
Marketplace authentication is `ON_USE`, not an installation prerequisite.

## Supported configuration

The [portable MCP schema](https://agent-plugins.org/schemas/1.0.0/mcp.schema.json)
supports `type: streamable-http` and `url`; its server object prohibits additional
properties. Consequently this package does not insert CLI-only OAuth fields or
the legacy `.mcp.json` OAuth object into portable `mcp.json`.

[OpenAI packaging documentation](https://developers.openai.com/plugins/build/plugins)
identifies root `mcp.json` as the bundled portable component. The
[Codex MCP/OAuth documentation](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)
describes automatic CIMD selection when issuer discovery advertises CIMD,
public `none` authentication and a supported loopback callback. Those conditions
are present in this deployed Talentsia issuer. No dynamic client registration or
new client needs to be invented. A native host test must confirm that this host's
plugin-provided connection uses the documented flow.

| Connection fact | Verified value |
| --- | --- |
| Resource / token audience | `https://api.talentsia.com/v1/do/mcp` |
| Protected resource metadata | `https://api.talentsia.com/.well-known/oauth-protected-resource/v1/do/mcp` |
| Issuer | `https://api.talentsia.com/v1/oidc` |
| Registered public Do client | `https://chatgpt.com/oauth/codex/EDrLtgxAifwZ/client.json` |
| Registered loopback callback | `http://127.0.0.1/callback/EDrLtgxAifwZ` |
| Client authentication | `none`; S256 PKCE required |
| Resource-advertised scopes | `do:access:read`, `do:plan-my-day:read` |

The callback ID is specific to the exact resource URL. The authorization server
matches its loopback host/path and permits the listener port chosen by Codex.
Do not replace it with a Work callback or fix an arbitrary port. The protected
resource supplies the two Do scopes; the package has no unsupported scope field.

## User validation

1. Update the Talentsia Skills marketplace and the existing Talentsia Do plugin;
   verify version 0.5.5 and ten skills. Start a fresh local Codex task. No source
   edits, second plugin or mandatory ZIP are part of this native route.
2. Use the host's authentication/account control for the bundled Do connection.
   The exact desktop control has not been observed. Sign in personally to
   Talentsia, choose an existing workspace and consent to the two Do read scopes.
   An organization owner's login is not a worker's login. A site session or Work
   seat does not substitute for this separate, explicitly consented Do grant.
3. Call `do_access_status({})`. Without an approved current entitlement it must
   return `access: unavailable`, `capabilities: []`. Consent alone does not enable
   Premium. Have the authorized operator assign an expiring pilot entitlement
   only to the confirmed user/workspace pair, independently of billing.
4. Repeat status: expected `active` and `plan-my-day`. Request Plan My Day with
   fictional inputs. The assistant must fetch `do_plan_my_day_method({})`, use
   the returned method 0.3.1 and Free 0.5.1 references, and disclose actual access.
   Five role descriptors are not proof that agents ran.
5. Revoke that pilot entitlement while the OAuth login remains valid; a fresh
   protected retrieval must fail and Free must remain usable. Previously
   returned content may remain in chats/files/cache and cannot be erased remotely.

## Evidence boundaries

Deployed Platform main `7e2629afd37098ff82ca1f33642c6451516c34d9` and private main
`ae177cfd19fbd6c3d66c8ea1a672b357d454be30` were checked in the authorized runtime:
metadata, initialize and tools/list returned 200; both anonymous protected calls
returned 401 with `resource_metadata`. Both source mounts are read-only and the
original Free snapshot digest was verified. Private fixtures passed 95 tests;
Platform fixtures passed 78 tests. These are not an authorized native host run.

The external Python probe received Cloudflare 1010 for its client signature.
No WAF rules were changed. Actual native OAuth/resource reachability remains to
be tested. A network or protocol failure is not a subscription result. The
website credential resolver and real paid-subscription synchronization are
separate work; this pilot uses explicit expiring assignments only.

## Observed native run and role handoff correction

The authorized October 7 native Codex pilot established OAuth, discovered both
Do tools and completed protected Plan My Day retrieval. Supported thread API
receipts confirm five user-authorized specialist agents started and completed.
Those agents explicitly used local Free references as fallback: the 0.3.0
protected payload omitted CONTRACT.md and METHOD.md required by its role TOMLs.
Agent execution therefore succeeded; exact Premium role-method coverage did not.

The isolated 0.3.1 private candidate adds hash-verified shared prerequisites and
model-readable MCP text for all five exact roles. Public routing instructs the
host to supply returned equivalents in assignments. No private instructions are
bundled here. Matching Platform changes enforce the existing 64 KiB envelope
limit without truncation. Local tests passed: 98 private, 82 Platform and 17 Work;
these are fixture checks, not a native run of the correction. Deployment and
a fresh native role handoff test remain pending. Keep the approved pilot active
until that test finishes, then perform the separately authorized revocation test.

## Connected v2 delivery

The unchanged 64 KiB limit applies to the entire JSON-RPC envelope. Each source
file is delivered exactly once in a `content` text block, prefixed by
`path:<name>` and a newline. The structured resource maps contain `content_index`
and SHA-256 of the source bytes following that newline, plus the private manifest
hashes and immutable Free lock. All fourteen source files must be accounted for:
five role TOMLs, roles.json, CONTRACT.md, METHOD.md, the Plan My Day extension and
five locked Free references. This is an explicit v2 transport contract change;
it does not add tools, scopes, storage or execution authority. Hosts should refresh
tool discovery; update the public Do plugin to 0.5.4 or later for the matching routing.
