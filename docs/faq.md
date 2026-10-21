# Questions a platform team asks before it runs this stack

Kortix is open source, and every answer here names the page behind it. A reviewer can open any of them in one click, which is the only kind of answer worth having in a security review.

## Sign-in through your own identity provider

Can we sign people in through our own identity provider? Yes. Kortix documents SAML 2.0 single sign-on and SCIM 2.0, with guided setup for Microsoft Entra ID, Okta, Google Workspace, Cloudflare Access, OneLogin, JumpCloud, PingOne and Auth0, plus a custom SAML provider. An account holds one identity provider. The SAML app carries a group claim, which maps your IdP groups onto Kortix groups. Two conditions matter before a pilot. The account has to be an organization account, because a personal account refuses SSO with `sso_personal_account`, and both features sit behind the `sso` and `scim` entitlements. The setup, including the DNS TXT record that proves the email domain, is in [Sign-in, SSO and API keys](https://kortix.com/docs/accounts/identity).

## Audit export

Can we export the audit log? Recording is always on, and export is the part that depends on the plan. Reading, exporting and streaming the log need the Enterprise `auditAccess` entitlement. Events stay in the database for 90 days, where the web app, `kortix audit ls`, the API, webhooks and export all read them. From 90 to 365 days they live in a locked archive that nobody can shorten or delete, and export is the only way out. Past 365 days the events are deleted. Plan an export process around that archive rather than find it in month four. The detail is under [the audit log section](https://kortix.com/docs/accounts#audit-log) of the accounts docs.

## Approval before an action runs

Can an action run without a person approving it? Yes, and that is the default. `policy.default_mode` ships as `allow_all`, so a connector call that no rule matches simply runs. Approval gates are off until you set them. Switch the default to `risk` and reads run while writes and destructive calls wait for approval. Per-action rules can mark one tool as `require_approval` or `block`, and they match on the arguments when you need that. A held call returns `202` with `status: "pending_approval"` and nothing runs. An approval covers one exact request, so a changed argument needs a fresh one. The keys and the precedence order are in [the manifest reference](https://kortix.com/docs/project/manifest#policy-and-policies), and the approval flow is in [Policies and approvals](https://kortix.com/docs/connect/connectors#policies-and-approvals).

## Where the data sits

Where does the data sit? Where you put it, when you self-host. The Compose stack on your server carries the API, the Postgres database, file storage and the audit archive, so those stay inside your network. Three things leave the box. Sandboxes run on Platinum, images come from Docker Hub, and model requests go from the gateway to whichever providers your projects connect. If a project uses Kortix-managed models, those run on zero-data-retention endpoints. The `us_region` flag is narrower than it sounds: it places new Platinum sandboxes in a US region where the instance offers one, and leaves the API, the database and the archive where they were. The deployment detail is in [Self-hosting](https://kortix.com/docs/host).

## What self-hosting costs

What does self-hosting cost? Run it on Kortix Cloud, in your VPC, or on your own on-prem network. Self-host is free. Three costs sit around that. A Kortix Enterprise license is what unlocks single sign-on, directory sync, custom roles and reading the audit log on a self-hosted instance. Platinum bills the sandboxes through your own `PLATINUM_API_KEY`. Model usage is billed by whichever provider keys you connect. The managed plans and the Enterprise tier are on [the pricing page](https://kortix.com/pricing).

## What the check does and does not do

Does the check replace reading OpenAI's documentation? No. It answers one question per row: is the sentence this repository quoted still on the page it came from. That catches a control renamed, reworded or withdrawn, which is the failure a comparison usually misses. It does not judge whether the new sentence means the same thing, and it does not look at pages that have no row. A row that fails is a prompt to open the page and read it, not a verdict on the product.

## A control the matrix does not have

OpenAI documents a control this matrix does not have. What now? Open an issue with the control, the URL, and the sentence exactly as the page writes it. The row then goes into `rows.yaml` with the check to hold it. If the control appears on none of the three tracked pages, the row would read "not documented on the page cited", which is worth knowing too. Either way the entry needs a sentence and a link. A cell with neither is the reason this repository exists.
