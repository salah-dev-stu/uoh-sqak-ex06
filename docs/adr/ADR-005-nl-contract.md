# ADR-005 — Free-natural-language dialogue contract

**Status:** accepted · **Gates:** H2 (the central graded requirement)

**Decision.** The prompt forbids coordinates/JSON and demands prose; agents may
negotiate framing ("which corner is the top") in words. The reply is parsed into a
free-NL message + a trailing `MOVE:`/`BARRIER` token; any leaked `(x,y)` is scrubbed
from the message. A test scans committed dialogue for coordinate tuples and fails
on leakage.

**Consequences.** The graded artifact (the dialogue) stays free natural language;
the move token is mechanics only.
