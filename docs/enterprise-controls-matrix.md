# OpenAI's documented enterprise controls, beside your own stack

Sign-in, tool access, approval before an action, and what is left behind afterwards: buyers put the same four questions to ChatGPT Work and to whatever stack they might build themselves. This file sets the two sets of answers side by side, and keeps the source of every cell.

Read a row like this. The control is on the left. Next is what OpenAI documents, in a near copy of its own sentence, with that sentence's page linked in the same row. Then the equivalent mechanism in an open-source stack you own, with the Kortix docs page that describes it. All cells were checked on 2026-10-21.

Sometimes none of the three OpenAI pages documents a control. The cell then says "not documented on the page cited", which is a statement about the page and not about the product. OpenAI may do the thing and document it somewhere this repo does not track. A guessed cell would make the table worth less than no table at all.

## Access and identity

| Control | What OpenAI documents | OpenAI page | In a stack you own | Kortix docs |
| --- | --- | --- | --- | --- |
| Single sign-on | Admin console offers SSO, domain verification and usage insights | [2023 post](https://openai.com/index/introducing-chatgpt-enterprise/) | SAML 2.0 single sign-on and SCIM 2.0. | [docs/accounts/identity](https://kortix.com/docs/accounts/identity) |
| Directory sync | not documented on the page cited | [overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) | SCIM 2.0 provisioning, gated by an entitlement | [docs/accounts/identity](https://kortix.com/docs/accounts/identity#scim-provisioning) |
| Roles and permissions | Admins manage who can use agents, connected tools and actions | [enterprise](https://chatgpt.com/business/enterprise/) | Per-resource permissions for people and agents. Roles, groups, and an audit trail. | [docs/accounts](https://kortix.com/docs/accounts) |
| Approval before an action | Not every action requires an individual human confirmation | [overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) | Approval gates you set. Off until you set them. | [docs/connect/connectors](https://kortix.com/docs/connect/connectors#policies-and-approvals) |
| Domain claim | Domain verification | [2023 post](https://openai.com/index/introducing-chatgpt-enterprise/) | A DNS TXT record proves the domain before SSO enforcement | [docs/accounts/identity](https://kortix.com/docs/accounts/identity#verify-the-domain) |

Only the August 2023 announcement names SSO, domain verification and the admin console. Neither the Work overview nor the current enterprise page restates them. Those rows cite the older page, and the link in the row says so.

## Execution and isolation

| Control | What OpenAI documents | OpenAI page | In a stack you own | Kortix docs |
| --- | --- | --- | --- | --- |
| Where a task runs | Cloud execution runs supported steps on OpenAI-managed infrastructure | [overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) | One isolated sandbox per session, its own machine and branch | [docs/work/sessions](https://kortix.com/docs/work/sessions) |
| Access to a local computer | Owner enables Allow local computer access; it nests under Work Cloud | [overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) | A person's own machine connected to Kortix | [docs/connect/computers](https://kortix.com/docs/connect/computers) |
| Outbound destinations | Limits code and shell commands to required destinations on the managed allowlist | [overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) | No outbound allowlist documented; a secret can be egress-enforced | [docs/project/secrets](https://kortix.com/docs/project/secrets) |
| Which policy wins | MDM and legacy managed-device requirements rank above Agent Security | [overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) | Project rules first, then connector rules; first match wins | [docs/project/manifest](https://kortix.com/docs/project/manifest#policy-and-policies) |
| Hooks and audit coverage | MCP hooks do not provide a complete Compliance API audit trail | [overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) | Every connector call is checked by policy, then recorded | [docs/connect/connectors](https://kortix.com/docs/connect/connectors) |

Two rows here carry the weight in a security review. The first is outbound traffic. Kortix documents no allowlist for a sandbox's outbound destinations and claims none. What it documents is an egress-enforced secret: the sandbox holds a handle, and Kortix substitutes the real value outside it, on approved HTTPS hosts. The second is local computer access. OpenAI documents an admin toggle, its nesting under Work Cloud, and the order in which device policy and Agent Security apply. Kortix documents that a person's own machine can be connected, with no published command sequence and no policy-precedence table.

## Data, audit and retention

| Control | What OpenAI documents | OpenAI page | In a stack you own | Kortix docs |
| --- | --- | --- | --- | --- |
| Training on business data | Business data is not used to train models by default | [enterprise](https://chatgpt.com/business/enterprise/) | Zero data retention at the model provider | [docs/project/models](https://kortix.com/docs/project/models) |
| Audit visibility | Compliance API visibility for conversations and agent activity | [enterprise](https://chatgpt.com/business/enterprise/) | One row per API request: actor, credential, outcome | [docs/accounts](https://kortix.com/docs/accounts#audit-log) |
| Complete execution history | User-visible records don't establish a complete administrator-visible execution history | [overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) | Agent rows name the person the agent acted for | [docs/accounts](https://kortix.com/docs/accounts#what-is-recorded) |
| Retention | Compliance Platform records remain available in the platform for 30 days | [overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) | 0 to 90 days live, 90 to 365 in a locked archive | [docs/accounts](https://kortix.com/docs/accounts#retention-and-export) |
| Data residency | Covers only eligible content and supported workloads, regions and configurations | [overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) | The self-hosted stack keeps the API, database and files on your server | [docs/host](https://kortix.com/docs/host) |

The audit row decides most reviews. OpenAI's overview is plain about it: on-screen records are not an export path, and user-visible records do not add up to a complete administrator-visible history. Kortix records at the API boundary instead. Every request gets a row, an agent's row carries the person it acted for, and a refused request stays as a row with `denied` in it.

## Read the Kortix column honestly

Recording is always on. Reading, exporting and streaming the log need the Enterprise `auditAccess` entitlement. A self-hosted instance unlocks that entitlement with a Kortix Enterprise license, and the same split covers single sign-on, directory sync and custom roles. A team that self-hosts without a license gets the platform and the records, and not the console to read them.

Two limits belong in a review rather than in a footnote. The audit database keeps 90 days live, and a locked archive covers the rest up to 365 days for export only. The `us_region` flag moves new sandboxes to a US region where the instance offers one. It does not move the API, the database or the archive.

## Re-check it

```sh
uv run check.py
```

Each row in `rows.yaml` carries its OpenAI URL and the sentence quoted from that page. The script fetches every URL and fails on any quote it cannot find. That is how a renamed or withdrawn control surfaces. When a row fails, open the page and copy the sentence that replaced the old one. Update the row afterwards, and change the date at the top of this file. A cell with no source is the thing this repository exists to replace.
