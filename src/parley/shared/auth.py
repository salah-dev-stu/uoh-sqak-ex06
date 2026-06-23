"""Bearer-token auth for the MCP servers (H8 — tokens not passwords, revocable)."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class TokenStore:
    """Reads each role's bearer token from the environment (R11 — never in code)."""

    token_env_by_role: dict[str, str]

    def token(self, role: str) -> str:
        env = self.token_env_by_role[role]
        value = os.environ.get(env)
        if not value:
            raise RuntimeError(f"bearer token env '{env}' is unset for role '{role}'")
        return value

    def header(self, role: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token(role)}"}


def verify_bearer(authorization: str | None, expected: str) -> bool:
    """True iff the Authorization header carries exactly ``Bearer <expected>``."""
    if not authorization or not expected:
        return False
    prefix = "Bearer "
    if not authorization.startswith(prefix):
        return False
    return authorization[len(prefix):].strip() == expected
