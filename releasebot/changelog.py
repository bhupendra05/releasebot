"""Assemble commits into a grouped Changelog."""
from __future__ import annotations

from typing import List, Optional

from .models import Changelog, ChangeType, Commit, SECTION_ORDER


def build_changelog(
    commits: List[Commit],
    version: Optional[str] = None,
    from_ref: Optional[str] = None,
    to_ref: str = "HEAD",
) -> Changelog:
    groups = {}
    breaking: List[Commit] = []
    contributors: List[str] = []

    for c in commits:
        groups.setdefault(c.type, []).append(c)
        if c.breaking:
            breaking.append(c)
        if c.author and c.author not in contributors:
            contributors.append(c.author)

    ordered = {t: groups[t] for t in SECTION_ORDER if t in groups}
    return Changelog(
        version=version,
        from_ref=from_ref,
        to_ref=to_ref,
        breaking=breaking,
        groups=ordered,
        contributors=sorted(contributors),
    )
