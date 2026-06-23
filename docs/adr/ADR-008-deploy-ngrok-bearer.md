# ADR-008 — ngrok + Bearer-token deploy (Cloudflare alternative)

**Status:** accepted · **Gates:** H8

**Decision.** The two HTTP servers are exposed via ngrok (free, lecture-demoed),
each behind a `StaticTokenVerifier` bearer token from env — "no URL without a
token", revocable by rotating the env var. Cloudflare Tunnel is documented as a
zero-session-limit alternative. Auth is tunnel-agnostic.

**Consequences.** Cloud execution (mandatory even solo) is demonstrable;
`scripts/capture_cloud_proof.md` describes capturing the proof.
