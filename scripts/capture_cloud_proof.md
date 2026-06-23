# Capturing cloud-execution proof (H8)

Dr. Segal requires a demonstration that the servers run **outside the local
machine** ("לצאת החוצה"). Cloud execution is mandatory even for the solo phase.

## ngrok (default, free)

```bash
# 1. start the two FastMCP servers locally (separate ports, bearer-protected)
uv run python scripts/serve_servers.py

# 2. in two more terminals, open public HTTPS tunnels
ngrok http 8011 --log stdout     # Cop  → https://<rand>.ngrok-free.app
ngrok http 8012 --log stdout     # Thief → https://<rand>.ngrok-free.app

# 3. point the client at the public URLs (export the bearer tokens first)
export PARLEY_COP_TOKEN=... PARLEY_THIEF_TOKEN=...
#    set mcp.transport='http' and the public hosts in config/mcp.json, then:
uv run parley play
```

**Capture for submission:** a screenshot of the ngrok dashboard showing both
HTTPS tunnels live, plus the terminal log of `parley play` completing over them,
saved under `reports/cloud_proof/`. The URL is useless without the bearer token —
rotate (revoke) the token by changing the env var.

## Cloudflare Tunnel (no session limit, also free)

```bash
cloudflared tunnel --url http://localhost:8011   # Cop
cloudflared tunnel --url http://localhost:8012   # Thief
```

Same idea, but the tunnel does not expire after a session. See
[ADR-008](../docs/adr/ADR-008-deploy-ngrok-bearer.md).
