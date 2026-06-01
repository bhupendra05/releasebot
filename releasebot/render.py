"""Render a Changelog as markdown."""
from __future__ import annotations

from datetime import date
from typing import Optional

from .models import Changelog, Commit, SECTION_ORDER, SECTION_TITLES


def _line(c: Commit) -> str:
    scope = f"**{c.scope}:** " if c.scope else ""
    short = f" (`{c.hash[:7]}`)" if c.hash else ""
    bang = " ⚠️" if c.breaking else ""
    return f"- {scope}{c.subject}{bang}{short}"


def to_markdown(changelog: Changelog, today: Optional[date] = None) -> str:
    stamp = (today or date.today()).isoformat()
    heading = changelog.version or "Unreleased"
    lines = [f"## {heading} — {stamp}", ""]

    if changelog.breaking:
        lines.append("### ⚠️ BREAKING CHANGES")
        lines.extend(_line(c) for c in changelog.breaking)
        lines.append("")

    for t in SECTION_ORDER:
        items = changelog.groups.get(t)
        if not items:
            continue
        lines.append(f"### {SECTION_TITLES[t]}")
        lines.extend(_line(c) for c in items)
        lines.append("")

    if changelog.contributors:
        lines.append(f"**Contributors:** {', '.join(changelog.contributors)}")
        lines.append("")

    if changelog.total == 0:
        lines.append("_No commits in this range._")

    return "\n".join(lines).rstrip() + "\n"
