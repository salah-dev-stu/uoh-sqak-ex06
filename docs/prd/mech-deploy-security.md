# Mechanism PRD — Deployment & Security

**Modules:** `shared/auth`, `mcp/server_factory`, `scripts/{deploy_ngrok,serve_servers,gmail_oauth_setup}`

Bearer-token auth (`TokenStore`/`verify_bearer`, `StaticTokenVerifier`) on every
server URL — tokens from env, revocable by rotation, never committed. ngrok (free)
exposes the two HTTP servers over public HTTPS; Cloudflare Tunnel is the documented
no-session-limit alternative. Gmail OAuth uses a one-time consent → revocable
`token.json` (git-ignored). No secret literals anywhere (R11). **Gates:** H8.
