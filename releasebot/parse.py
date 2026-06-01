"""Parse conventional-commit messages into structured commits."""
from __future__ import annotations

import re

from .models import ChangeType, Commit

# type(scope)!: subject
_HEADER = re.compile(
    r"^(?P<type>\w+)(?:\((?P<scope>[^)]+)\))?(?P<bang>!)?:\s*(?P<subject>.+)$"
)
_TYPES = {t.value: t for t in ChangeType}


def parse_commit(message: str, hash: str = "", author: str = "") -> Commit:
    """Parse a (possibly multi-line) commit message into a Commit."""
    stripped = message.strip()
    first = stripped.splitlines()[0] if stripped else ""
    breaking = "BREAKING CHANGE" in message or "BREAKING-CHANGE" in message

    m = _HEADER.match(first)
    if not m:
        return Commit(hash=hash, type=ChangeType.OTHER, subject=first,
                      breaking=breaking, author=author or None)

    if m.group("bang"):
        breaking = True
    return Commit(
        hash=hash,
        type=_TYPES.get(m.group("type").lower(), ChangeType.OTHER),
        scope=m.group("scope"),
        subject=m.group("subject").strip(),
        breaking=breaking,
        author=author or None,
    )
