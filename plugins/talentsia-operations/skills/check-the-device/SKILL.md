---
name: check-the-device
description: "Inspect the device a worker runs on and repair only what its policy permits, reporting what was observed rather than what was expected."
---

## When to use

Use when somebody asks whether this device is healthy, or when a routine health check falls due. Never use it to change anything the device's policy does not explicitly permit.

## Steps

1. Observe before concluding: read the system with {{tool:host.observe/system}} and every service with {{tool:host.observe/services}}.
2. A service that is not installed on this device is not a stopped service. Report it as absent and move on.
3. For a stopped service, read its recent logs with {{tool:host.observe/logs}} before doing anything about it.
4. Restart only a service you are explicitly permitted to restart, with {{tool:host.services.restart/restart}}. A refusal is an answer, not an obstacle.
5. After any restart, read the state again with {{tool:host.observe/services}}. The restart call returning is not evidence that it worked.
6. If something is wrong that you may not repair, tell a person with {{tool:operator.notify/notify}}: what you saw, and since when.
7. Report what you observed, one sentence per problem. A healthy device is one line.

## Done when

- Any claim that a service is running is backed by a reading taken after the restart.
- Nothing was restarted that the device's policy did not permit.
- A problem you could not repair was put in front of a person.

## Notes

- Whether a restart is permitted is decided by the device's Host Controller, never by this skill. A refusal returns as an observation.
- A unit that does not exist here is not one that stopped: a fleet once escalated a missing demonstration service 159 times.
