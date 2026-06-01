"""Read commits from a git repository."""
from __future__ import annotations

import subprocess
from typing import List, Optional

from .models import Commit
from .parse import parse_commit

_FIELD = "\x1f"  # between fields within a commit record
_RECORD = "\x1e"  # between commit records


def parse_log_output(output: str) -> List[Commit]:
    """Parse the delimited output of `git log` into Commits (pure, testable)."""
    commits: List[Commit] = []
    for record in output.split(_RECORD):
        record = record.strip("\n")
        if not record.strip():
            continue
        parts = record.split(_FIELD)
        h = parts[0] if len(parts) > 0 else ""
        author = parts[1] if len(parts) > 1 else ""
        subject = parts[2] if len(parts) > 2 else ""
        body = parts[3] if len(parts) > 3 else ""
        commits.append(parse_commit(f"{subject}\n\n{body}", hash=h, author=author))
    return commits


def _run(args: List[str], repo: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", repo, *args], capture_output=True, text=True
        )
    except FileNotFoundError as e:
        raise RuntimeError("git is not installed or not on PATH.") from e
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return result.stdout


def get_latest_tag(repo: str = ".") -> Optional[str]:
    try:
        tag = _run(["describe", "--tags", "--abbrev=0"], repo).strip()
        return tag or None
    except RuntimeError:
        return None


def get_commits(from_ref: Optional[str], to_ref: str = "HEAD", repo: str = ".") -> List[Commit]:
    fmt = f"--pretty=format:%H{_FIELD}%an{_FIELD}%s{_FIELD}%b{_RECORD}"
    rng = f"{from_ref}..{to_ref}" if from_ref else to_ref
    return parse_log_output(_run(["log", "--no-merges", fmt, rng], repo))
