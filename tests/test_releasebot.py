"""Tests for ReleaseBot parsing, grouping, and rendering (no git required)."""
from datetime import date

from releasebot.changelog import build_changelog
from releasebot.gitlog import parse_log_output
from releasebot.models import ChangeType
from releasebot.parse import parse_commit
from releasebot.render import to_markdown


def test_parse_feat_with_scope():
    c = parse_commit("feat(auth): add SSO login", hash="abc1234")
    assert c.type is ChangeType.FEAT
    assert c.scope == "auth"
    assert c.subject == "add SSO login"


def test_parse_fix_without_scope():
    c = parse_commit("fix: handle null pointer")
    assert c.type is ChangeType.FIX
    assert c.scope is None


def test_parse_breaking_bang():
    assert parse_commit("feat!: drop python 3.8").breaking


def test_parse_breaking_footer():
    c = parse_commit("refactor: rework api\n\nBREAKING CHANGE: removed endpoints")
    assert c.breaking


def test_parse_non_conventional():
    c = parse_commit("updated the readme")
    assert c.type is ChangeType.OTHER
    assert c.subject == "updated the readme"


def test_build_groups_and_contributors():
    commits = [
        parse_commit("feat: a", author="Alice"),
        parse_commit("fix: b", author="Bob"),
        parse_commit("feat: c", author="Alice"),
    ]
    cl = build_changelog(commits, version="v1.0.0")
    assert len(cl.groups[ChangeType.FEAT]) == 2
    assert cl.contributors == ["Alice", "Bob"]
    assert cl.total == 3


def test_render_markdown():
    commits = [
        parse_commit("feat(ui): a", hash="deadbeef1"),
        parse_commit("fix!: b", hash="cafe0000"),
    ]
    cl = build_changelog(commits, version="v1.2.0")
    md = to_markdown(cl, today=date(2026, 5, 30))
    assert "## v1.2.0 — 2026-05-30" in md
    assert "🚀 Features" in md
    assert "⚠️ BREAKING CHANGES" in md
    assert "**ui:**" in md


def test_parse_log_output():
    f, r = "\x1f", "\x1e"
    out = f"abc123{f}Alice{f}feat: x{f}{r}def456{f}Bob{f}fix: y{f}some body{r}"
    commits = parse_log_output(out)
    assert len(commits) == 2
    assert commits[0].type is ChangeType.FEAT
    assert commits[0].author == "Alice"
    assert commits[0].hash == "abc123"


def test_empty_changelog():
    cl = build_changelog([], version="v0.0.1")
    assert "_No commits in this range._" in to_markdown(cl, today=date(2026, 5, 30))
