# Mechanism PRD — Reporting

**Modules:** `report/{builder,sender,gmail_sender,smtp_sender}`, `sdk/artifacts`

`build_report` aggregates all 6 sub-games, totals, timestamps, team names+IDs, repo
link, server URLs, and a config snapshot into parseable JSON. `make_sender` selects
`GmailApiSender` (OAuth via `Gatekeeper.google_send`) or `SmtpSender` (fallback) from
config. `write_artifacts` persists `transcript.md`, `moves.jsonl` (dispute log), the
report JSON, and the gate ledger. **Gates:** H7.
