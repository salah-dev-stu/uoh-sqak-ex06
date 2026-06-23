# ADR-007 — Pluggable report sender (Gmail API + SMTP)

**Status:** accepted · **Gates:** H7

**Decision.** `make_sender` returns a `GmailApiSender` (OAuth token via
`Gatekeeper.google_send`) by default, or an `SmtpSender` fallback — selected by
`config/report.json`. The lecture permits non-Gmail delivery if Gmail blocks; SMTP
covers that. A one-time `scripts/gmail_oauth_setup.py` mints the revocable token.

**Consequences.** The mandatory automated report is robust to Gmail friction; tests
mock both senders.
