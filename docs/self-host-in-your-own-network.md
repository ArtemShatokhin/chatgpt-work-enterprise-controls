# Self-host Kortix in your own network, from the live install path

Kortix is open source, and the whole platform installs on a machine you own. This article follows the self-host path as the docs give it today, quotes the commands exactly, and says what each step leaves on disk. It is for the person who has to stand the stack up and then answer for it in a review.

## What the stack is

A self-hosted instance is the full platform: one Docker Compose stack that the `kortix self-host` CLI installs, configures and updates. Your database, your files and your configuration sit on your server. Two parts stay outside the box. Sessions run on Platinum sandboxes, not on the server. The instance has to be reachable from the internet so those sandboxes can call back to it. If nothing inbound may reach the instance, this path does not fit: the sandboxes need it to call back, so sessions do not start.

## Prepare the server

- Linux, with a public IP, plus Docker Engine and the Compose plugin already installed. The CLI runs on Linux and macOS, on x86_64 and arm64.
- A or AAAA records for `<domain>` and `api.<domain>`, both pointed at the server before the first start, because Caddy needs them to get the certificate.
- A wildcard record for `*.p.<domain>`, which serves sandbox previews. Skip it and previews fall back to a path proxy that breaks root-absolute links, and `doctor` fails.
- Inbound 80 and 443 open.
- A Platinum API key in `PLATINUM_API_KEY`. Without it, sessions do not start.
- A model provider key, added in the web app after the first sign-in.

A second wildcard, for example `*.apps.<domain>`, is only needed if the instance hosts Apps.

## Install

These three commands are the install-by-hand path from the self-hosting docs, for a server that already has Docker.

```sh
curl -fsSL https://kortix.com/install | bash
kortix self-host init --domain kortix.example.com --admin-email you@example.com
kortix self-host start
```

The first line installs the CLI. `init` writes four files into `~/.config/kortix/self-host/<instance>/`: `docker-compose.yml`, `.env`, a `Caddyfile` and `updater.sh`. A first `init` in a terminal asks every setup question; `--yes`, or a shell with no terminal, keeps the defaults. `start` runs `docker compose up`, and it runs `init` first when the instance has no configuration yet.

One Compose project, `kortix-<instance>`, holds every service. The interesting ones for a review:

| Service | What it does |
| --- | --- |
| `frontend` | The web app. |
| `kortix-api` | The REST API at `/v1`. |
| `llm-gateway` | The standalone model gateway, behind Caddy on `api.<domain>/v1/llm*`. |
| `kortix-migrate` | A one-shot job that migrates the database before the API starts. |
| `kortix-updater` | Pulls new images daily, migrates and rolls the app services. It mounts the Docker socket. |
| `supabase-*` | The Supabase distribution, images pinned by digest: Postgres, auth, REST, realtime, storage, Kong, the pooler, Studio. |
| `caddy` | Domain mode only. Terminates TLS on 80 and 443 with ACME HTTP-01. |

## Answer the setup questions

`init` asks the questions once, and `--yes` takes the defaults. Either way the Platinum key and the preview domain are easy to leave unset, and `init` and `start` only warn about a missing sandbox key before carrying on.

```sh
kortix self-host configure
kortix self-host start
```

`configure` asks the questions again, in a fixed order: reachability, admin email, the Enterprise license, account creation, the sandbox provider, Apps hosting, preview origins, the Composio key, and the update policy. Each answer is pre-filled with the current value, so Enter keeps it. It writes the files and nothing else. `start` applies them.

The account-creation answer is on by default, and it is worth leaving on. Only a platform admin can create an account once it is on, and everyone else gets `403 account_creation_restricted`. Sign-ups, invites, single sign-on and each person's personal account still work.

## Close the open sign-up window first

Do this before anything else after the stack answers on its domain. Until `EMAIL_URL` or `DISABLE_SIGNUP=true` is set, anyone who reaches the instance can create a confirmed account for any address, the admin address included. The window exists because a fresh instance has no mail provider yet. The docs put that warning in the sign-in step for exactly this reason.

## Check the instance

```sh
kortix self-host doctor
```

Fix every failing check before handing the URL to anyone. A missing preview wildcard is one of the failures it reports, and a missing Platinum key shows up later as sessions that never start.

## What runs outside your server

Three things leave the box, and a review should name them. Sandboxes run on Platinum, which `kortix-api` creates with `PLATINUM_API_KEY`, and each calls back to the instance's public API URL. Images come from `kortix/kortix-frontend`, `kortix/kortix-api` and `kortix/kortix-gateway` on Docker Hub, and the pulls need no credentials. Model requests go from the gateway to whichever providers your projects connect, so where inference happens is a choice you make per project.

## Turn on the enterprise controls

Single sign-on, directory sync, custom roles and reading the audit log are entitlements. On a self-hosted instance a Kortix Enterprise license unlocks all of them for every account. Set `ENTERPRISE_LICENSE_AVAILABLE=true`, or install with `kortix self-host init --enterprise-license`. Without the license the platform still records every request, and nobody can open the log to read it. That split is the one fact worth repeating to whoever signs the purchase order.

## Try it without a domain

To evaluate the stack on a laptop, the tunnel mode needs no DNS at all.

```sh
kortix self-host init --tunnel cloudflare
kortix self-host start
```

The web app opens at `http://localhost:13737`, and `cloudflared` publishes the API at a `trycloudflare.com` URL that changes each time it restarts. Domain mode is the production setup. Local mode, with neither flag, binds every port to `127.0.0.1`. It cannot start a session, because the sandbox has no route back to the API.

## What it costs

Run it on Kortix Cloud, in your VPC, or on your own on-prem network. Self-host is free. The Enterprise license is the paid part, and it turns on single sign-on, directory sync and the audit console. The Platinum key and the model keys are billed by those providers, not by Kortix. That is the whole bill for a self-hosted instance, and it is a shorter list than most platform teams expect.
