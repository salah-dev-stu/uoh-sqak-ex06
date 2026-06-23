"""Single source of truth for the package version (R5).

The build backend (hatchling) reads ``__version__`` from this file, and the
runtime config carries a mirrored ``version`` field. ``check_version_sync.py``
and a unit test assert the two never drift apart.
"""

__version__ = "1.36"
