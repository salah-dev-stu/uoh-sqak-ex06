# Gmail API setup — sending the autonomous game report (H7)

> **Scope (read first).** HW6 needs exactly **one** Google action: at the end of a game,
> the autonomous pipeline **sends the JSON report by email** to
> **`rmisegal+uoh26b@gmail.com`** (the recipient is already set in
> [`config/report.json`](../config/report.json)). That is the whole H7 requirement.
>
> Dr. Segal's two tutorial videos ([Part A](../materials/gmail-video-A.md),
> [Part B](../materials/gmail-video-B.md)) also enable the **Google Calendar API** and
> demonstrate **reading** mail / writing a **draft** / adding a calendar event. That is
> the videos' generic demo of the OAuth client — **it is NOT a HW6 requirement.** For
> this project you only need the **Gmail _send_** half; don't over-build a
> calendar/inbox agent.

This project's Gmail path is already wired:

- **Scope:** `https://www.googleapis.com/auth/gmail.send` (only) — `config/report.json`.
- **OAuth client type:** **Desktop app**.
- **Token minting:** [`scripts/gmail_oauth_setup.py`](../scripts/gmail_oauth_setup.py)
  uses `InstalledAppFlow.from_client_secrets_file(...).run_local_server(port=0)`.
- **The send:** [`src/parley/report/gmail_sender.py`](../src/parley/report/gmail_sender.py)
  builds a MIME message → base64url → calls `ApiGatekeeper.google_send(token_path, raw)`,
  which runs `gmail.users().messages().send(userId="me", body={"raw": ...})` (R3: every
  external call goes through the Gatekeeper).
- **Secrets stay out of the repo.** Two env vars point at files kept **outside** the
  project: `PARLEY_GMAIL_CREDENTIALS` (the downloaded client `credentials.json`) and
  `PARLEY_GMAIL_TOKEN` (the cached `token.json`). `.env`, `credentials.json`, and
  `token.json` are all git-ignored — never commit them.

---

## Part A — create the OAuth client (Google Cloud Console)

Distilled from [`materials/gmail-video-A.md`](../materials/gmail-video-A.md), tailored to
our group. Sign in to the Gmail account you'll send from first.

1. **Create a project.** [Google Cloud Console](https://console.cloud.google.com/) →
   *Select project* → **New project** → name it **`uoh-sqak`** (lowercase, no spaces —
   snake/kebab style avoids quoting headaches) → **Create**.
2. **Enable the Gmail API.** Search bar → *Gmail API* → **Enable**.
   *(The videos also enable the Calendar API. Skip it — HW6 doesn't use Calendar.)*
3. **Configure the consent screen / branding.** *APIs & Services* → *OAuth consent screen*
   → **Get started** → fill app name (e.g. `parley-uoh-sqak`) + your support email →
   **User type = External** → finish. The project stays in **Testing**.
4. **Add Test users.** *Audience* → **Test users → Add users** → add **both teammates'**
   Gmail addresses (Salah Qadah, Andalus Kalash), including the sending account. Only
   listed test users can authorize the app while it's in Testing. **Save.**
5. **Add the scope.** *Data Access* → **Add or remove scopes** → paste
   `https://www.googleapis.com/auth/gmail.send` → **Update**.
   *(One scope is enough — don't add the "all permissions" set the video uses for
   convenience.)*
6. **Create the Desktop client.** *Credentials* (or *Clients*) → **Create credentials →
   OAuth client ID** → **Application type = Desktop app** → name it
   (e.g. `desktop-client-parley`) → **Create**.
7. **Download `credentials.json` OUTSIDE the repo.** Use the **Download JSON** button and
   save it to a private folder **outside** `hw6/` (e.g. `~/parley-secrets/credentials.json`).
   Never place real credentials inside the project.

## Part B — mint the token + send for real

From [`materials/gmail-video-B.md`](../materials/gmail-video-B.md): the client + token live
together **outside** the project; first run opens a browser for the test-user consent and
caches `token.json`. Exact commands:

```bash
cd hw6
export PARLEY_GMAIL_CREDENTIALS=/abs/path/to/credentials.json
export PARLEY_GMAIL_TOKEN=/abs/path/to/token.json      # will be created on first run

uv run python scripts/gmail_oauth_setup.py   # opens browser → consent as a Test user → writes token.json
uv run parley play                           # real game → emails the JSON report to rmisegal+uoh26b@gmail.com
```

- **First run only** triggers the browser consent; afterwards the cached `token.json` is
  reused, so `parley play` stays fully autonomous (zero manual steps at runtime — H4).
- **Token refresh.** The token expires or can be invalidated. If sending starts failing,
  **delete `token.json`** and re-run `scripts/gmail_oauth_setup.py` to re-consent.
- **Prefer env vars in `.env`.** Copy from [`.env-example`](../.env-example) and set the
  two paths there instead of exporting each shell; `.env` is git-ignored.

## Proof to capture for submission

The Gmail API returns a JSON acknowledgement (a message id + `labelIds: ["SENT"]`). Save
that send confirmation under `reports/` as evidence the report was delivered — e.g.
`reports/gmail_send_proof.json`. **Never commit** real credentials, tokens, or the
personal email body; the committed [`reports/sample_report.json`](../reports/sample_report.json)
already proves the report's structure offline (the test suite mocks the actual send, so
graders need no Google account).

## Source transcripts

- [`materials/gmail-video-A.md`](../materials/gmail-video-A.md) — Part A: create the OAuth client.
- [`materials/gmail-video-B.md`](../materials/gmail-video-B.md) — Part B: mint the token + send from Python.
