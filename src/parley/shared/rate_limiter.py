"""Per-service token-bucket rate limiter + budget counter (R4 — limits in config)."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class _Bucket:
    capacity: int
    tokens: float
    budget: int
    spent: int = 0


@dataclass
class RateLimiter:
    """Allows up to ``rate_per_min`` calls per service and caps total ``budget``.

    Time is injected via ``now()`` (a monotonic seconds source) so tests are
    deterministic — no wall-clock reads.
    """

    limits: dict[str, dict[str, int]]
    now: object  # callable[[], float]
    _buckets: dict[str, _Bucket] = field(default_factory=dict)
    _last: dict[str, float] = field(default_factory=dict)

    def _bucket(self, service: str) -> _Bucket:
        if service not in self._buckets:
            cfg = self.limits.get(service, {"rate_per_min": 60, "budget": 1000})
            cap = int(cfg["rate_per_min"])
            self._buckets[service] = _Bucket(capacity=cap, tokens=float(cap), budget=int(cfg["budget"]))
            self._last[service] = float(self.now())  # type: ignore[operator]
        return self._buckets[service]

    def allow(self, service: str) -> bool:
        b = self._bucket(service)
        t = float(self.now())  # type: ignore[operator]
        elapsed = t - self._last[service]
        self._last[service] = t
        b.tokens = min(b.capacity, b.tokens + elapsed * (b.capacity / 60.0))
        if b.spent >= b.budget:
            return False
        if b.tokens < 1.0:
            return False
        b.tokens -= 1.0
        b.spent += 1
        return True
