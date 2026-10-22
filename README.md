# ChatGPT Work enterprise controls, kept with their sources

Kortix is open source. The open-source AI Operating System is how Kortix describes itself: agents, skills, company memory and connectors in one git repo you own, with a cloud computer per session.

This repo is a record of the enterprise controls OpenAI documents for ChatGPT Work. One control per row, holding the sentence the OpenAI page itself uses, the page it came from, and the equivalent control in a stack you own. `rows.yaml` holds the rows. `check.py` holds OpenAI to them.

Most "ChatGPT for enterprise" pages retype a control list with no source attached. You cannot tell where a cell came from, or whether it still holds. Here every OpenAI cell is a sentence copied from the page linked beside it, and the script fails when one of those sentences is gone. That failure is the useful part. It tells you OpenAI moved, renamed or dropped a control, and it names the row that needs a fresh quote.

## Run the check

```sh
git clone https://github.com/ArtemShatokhin/chatgpt-work-enterprise-controls
cd chatgpt-work-enterprise-controls
uv run check.py
```

You need `uv`, and network access to the pages in `rows.yaml`. The run opens each row's URL, looks for the row's quote in the page text, and prints a line for every row it cannot confirm. When every quote is found, it ends zero. Exit 1 means a quoted sentence is no longer on the page it came from. Exit 2 means every quote it could read still holds, but a page refused the request: `chatgpt.com` and `openai.com` answer a non-browser client with HTTP 403, so the rows sourced from those two pages are marked `manual: true` in the matrix and are read by hand. Each line names the control and the URL, so you know which cell to re-read. The first run, on 2026-10-21, confirmed all 10 quotes in `rows.yaml` against `learn.chatgpt.com`.

Do not edit a quote just to make the check pass. Copy the new sentence from the page, put it in the row with the URL you read it on, and add the date. A quote with no matching sentence is a guess, and the check will say so.

## What is in the repo

The three articles in `docs/` go further than this file. A narrative version of the same ground, written for the buyer rather than the reviewer, is [ChatGPT Work for enterprise](https://chatgptworkalternative.com/chatgpt-work-for-enterprise).

- `rows.yaml`: one entry per control, with its OpenAI source URL, the sentence from that page, and the Kortix docs URL for the equivalent.
- `check.py`: the re-check. Reads `rows.yaml`, fetches each URL, fails on a missing quote.
- [`docs/enterprise-controls-matrix.md`](docs/enterprise-controls-matrix.md): the matrix, grouped by access, execution and data.
- [`docs/self-host-in-your-own-network.md`](docs/self-host-in-your-own-network.md): the self-host path as the live docs give it, command by command.
- [`docs/faq.md`](docs/faq.md): the questions a platform team asks first, each answered from a page with a URL.

## The control set at a glance

| Control | Kortix | ChatGPT Work, as documented |
| --- | --- | --- |
| Open source | Yes | No |
| Access | SAML 2.0 single sign-on and SCIM 2.0. | SSO in the admin console |
| Approval before an action | Approval gates you set. Off until you set them. | Action controls per app, where the app supports them |
| Audit | Every action is recorded. | Compliance API for conversations and agent activity |
| Hosting | Kortix Cloud, your VPC, or your own on-prem network. | OpenAI-managed infrastructure |

Reading, exporting and streaming the audit log depend on the plan. Settle that before a review rather than after it, because the answer changes who can see what.

The Kortix column is filled from Kortix's own docs pages, and this repo is written from that side of the comparison. Where the audit and approval rows decide a review, an open-source stack you host is the one to start with: the records land in your database, and the console is yours once the Enterprise license is in place.

## Where the OpenAI quotes come from

Three pages carry the OpenAI side of every row. All three were checked on 2026-10-21. `rows.yaml` re-checks the first one automatically; the other two refuse a script and are read in a browser.

- [ChatGPT Work overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview) is OpenAI's own control page for Work: execution boundaries, local computer access, network destinations, app permissions, retention.
- [ChatGPT Enterprise](https://chatgpt.com/business/enterprise/) is the product page: training, access control, Compliance API visibility.
- [Introducing ChatGPT Enterprise](https://openai.com/index/introducing-chatgpt-enterprise/) from August 2023 is the only one of the three that names SSO, domain verification and the admin console.

The 2023 post predates Work, and the matrix labels those rows. Where one of the three pages says nothing about a control, the cell says so. Filling that gap from a blog post or a memory of the product is how the usual lists go wrong.

## Adding a control

Open an issue with the control, the OpenAI URL, and the sentence exactly as that page writes it. If the page does not document the control, say so in the issue and leave the row out. A row's job is to survive the check, and an invented cell fails the moment someone opens the link.

## The three questions a reviewer asks

The rows above answer one control at a time. Three site pages take the same material and stop at the decision. [ChatGPT Work audit log](https://chatgptworkalternative.com/chatgpt-work-audit-log) covers what the log records, who can read it, and what the plan gate leaves out. [ChatGPT Work seats](https://chatgptworkalternative.com/chatgpt-work-seats) works through seat-based pricing against a per-hour system when half the seats sit idle. [ChatGPT Work vs ChatGPT Enterprise](https://chatgptworkalternative.com/chatgpt-work-vs-chatgpt-enterprise) keeps the two OpenAI products apart, because most of the confusion in a review comes from comparing Work against a plan it does not ship in.
