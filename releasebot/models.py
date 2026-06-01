"""Data models and section ordering for ReleaseBot."""
from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class ChangeType(str, Enum):
    FEAT = "feat"
    FIX = "fix"
    PERF = "perf"
    REFACTOR = "refactor"
    DOCS = "docs"
    BUILD = "build"
    CI = "ci"
    TEST = "test"
    STYLE = "style"
    CHORE = "chore"
    REVERT = "revert"
    OTHER = "other"


SECTION_TITLES: Dict[ChangeType, str] = {
    ChangeType.FEAT: "🚀 Features",
    ChangeType.FIX: "🐛 Bug Fixes",
    ChangeType.PERF: "⚡ Performance",
    ChangeType.REFACTOR: "♻️ Refactors",
    ChangeType.DOCS: "📝 Documentation",
    ChangeType.BUILD: "📦 Build",
    ChangeType.CI: "🔧 CI",
    ChangeType.TEST: "✅ Tests",
    ChangeType.STYLE: "💄 Styles",
    ChangeType.CHORE: "🧹 Chores",
    ChangeType.REVERT: "⏪ Reverts",
    ChangeType.OTHER: "📌 Other",
}

# Order sections appear in the changelog.
SECTION_ORDER: List[ChangeType] = [
    ChangeType.FEAT, ChangeType.FIX, ChangeType.PERF, ChangeType.REFACTOR,
    ChangeType.DOCS, ChangeType.BUILD, ChangeType.CI, ChangeType.TEST,
    ChangeType.STYLE, ChangeType.CHORE, ChangeType.REVERT, ChangeType.OTHER,
]


class Commit(BaseModel):
    hash: str = ""
    type: ChangeType = ChangeType.OTHER
    scope: Optional[str] = None
    subject: str = ""
    breaking: bool = False
    author: Optional[str] = None


class Changelog(BaseModel):
    version: Optional[str] = None
    from_ref: Optional[str] = None
    to_ref: str = "HEAD"
    breaking: List[Commit] = Field(default_factory=list)
    groups: Dict[ChangeType, List[Commit]] = Field(default_factory=dict)
    contributors: List[str] = Field(default_factory=list)

    @property
    def total(self) -> int:
        return sum(len(v) for v in self.groups.values())
