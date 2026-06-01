# ReleaseBot 🤖📝

**Stop writing changelogs by hand.** ReleaseBot reads your git history, understands
[conventional commits](https://www.conventionalcommits.org), and generates clean, grouped
release notes — features, fixes, breaking changes, contributors — in seconds.

```bash
releasebot --version v1.2.0
```

```markdown
## v1.2.0 — 2026-05-30

### ⚠️ BREAKING CHANGES
- drop support for Python 3.8 ⚠️ (`a1b2c3d`)

### 🚀 Features
- **auth:** add SSO login (`e4f5a6b`)
- **billing:** monthly invoice export (`9c8d7e6`)

### 🐛 Bug Fixes
- **api:** handle null response from upstream (`3f2e1d0`)

**Contributors:** Alice, Bob
```

## Why

Every release, someone scrolls through `git log` and hand-writes the notes. ReleaseBot does
it in one command — consistent, grouped, and ready to paste into a GitHub release or
`CHANGELOG.md`. Drop it in CI and your release notes write themselves.

## Install

```bash
pip install releasebot
```

## Usage

```bash
releasebot                          # since the latest tag, to HEAD
releasebot --from v1.0.0 --to v1.1.0
releasebot --version v2.0.0 --out CHANGELOG.md
releasebot --json                   # machine-readable
releasebot --repo /path/to/repo
```

If you don't pass `--from`, ReleaseBot uses your **latest git tag** as the starting point —
exactly the range for your next release.

## Commit categories

`feat` → 🚀 Features · `fix` → 🐛 Bug Fixes · `perf` → ⚡ Performance ·
`refactor` → ♻️ Refactors · `docs` → 📝 Docs · plus build, ci, test, style, chore, revert.
A `!` (e.g. `feat!:`) or a `BREAKING CHANGE:` footer surfaces in the Breaking Changes section.
Non-conventional commits land under 📌 Other, so nothing is lost.

## Use in CI

```yaml
- run: pip install releasebot
- run: releasebot --version ${{ github.ref_name }} --out RELEASE_NOTES.md
```

## License

MIT
