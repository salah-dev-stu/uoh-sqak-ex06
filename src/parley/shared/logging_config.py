"""Structured logger setup — one configured logger per component."""

from __future__ import annotations

import logging

_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
_configured = False


def _configure(level: str) -> None:
    global _configured
    if not _configured:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO), format=_FORMAT)
        _configured = True


def get_logger(component: str, level: str = "INFO") -> logging.Logger:
    """Return a logger namespaced under ``parley.<component>``."""
    _configure(level)
    return logging.getLogger(f"parley.{component}")
