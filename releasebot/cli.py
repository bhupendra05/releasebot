"""Command-line entrypoint: `releasebot`."""
from __future__ import annotations

import argparse
import sys
from typing import Optional, Sequence

from .changelog import build_changelog
from .gitlog import get_commits, get_latest_tag
from .render import to_markdown


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(
        prog="releasebot",
        description="Generate a changelog from git history (conventional commits).",
    )
    p.add_argument("--from", dest="from_ref", default=None,
                   help="Start ref (default: latest tag)")
    p.add_argument("--to", dest="to_ref", default="HEAD", help="End ref (default: HEAD)")
    p.add_argument("--version", default=None, help="Version label for the heading")
    p.add_argument("--repo", default=".", help="Path to the git repo (default: .)")
    p.add_argument("--json", action="store_true", help="Output JSON instead of markdown")
    p.add_argument("--out", default=None, help="Write the changelog to a file")
    args = p.parse_args(argv)

    from_ref = args.from_ref
    if from_ref is None:
        from_ref = get_latest_tag(args.repo)  # None => full history

    try:
        commits = get_commits(from_ref, args.to_ref, args.repo)
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 3

    changelog = build_changelog(
        commits, version=args.version, from_ref=from_ref, to_ref=args.to_ref
    )
    rendered = changelog.model_dump_json(indent=2) if args.json else to_markdown(changelog)

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(rendered)
        print(f"Changelog written to {args.out}  ({changelog.total} commits)")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    sys.exit(main())
