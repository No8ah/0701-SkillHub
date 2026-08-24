#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ADD_RE = re.compile(r"^(?P<prefix>\s*\\addcontentsline\{toc\}\{[^}]*\}\{)(?P<title>.*)(?P<suffix>\}\s*)$")


def add_star_to_title(title: str) -> str | None:
    if "$\\star$" in title:
        return None
    # Only touch the visible "定义 -" token with the expected spacing.
    needle = "定义 -"
    replacement = "定义 $\\star$ -"
    if needle not in title:
        return None
    return title.replace(needle, replacement, 1)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="List/apply Chapter3_DI.tex-style '$\\star$' insertion for \\addcontentsline TOC titles."
    )
    parser.add_argument("tex_path", type=Path, help="Path to a .tex file")
    parser.add_argument("--line", type=int, help="Only apply to this 1-based line number")
    parser.add_argument("--apply", action="store_true", help="Write changes back to file")
    args = parser.parse_args(argv)

    path: Path = args.tex_path
    if not path.exists():
        print(f"error: file not found: {path}", file=sys.stderr)
        return 2

    if args.line is None:
        print("This helper is intentionally conservative.")
        print("Pass --line <N> to target a specific \\addcontentsline line.")
        print(f"Example: python3 {Path(__file__).name} {path} --line 2652 --apply")
        return 0

    lines = path.read_text(encoding="utf-8").splitlines(True)
    if args.line < 1 or args.line > len(lines):
        print(f"error: --line out of range (1..{len(lines)}): {args.line}", file=sys.stderr)
        return 2

    idx = args.line
    line = lines[idx - 1]
    m = ADD_RE.match(line)
    if not m:
        print(f"No \\addcontentsline match at L{idx}.", file=sys.stderr)
        return 2

    title = m.group("title")
    new_title = add_star_to_title(title)
    if new_title is None:
        print(f"No change needed at L{idx} (already contains '$\\star$' or missing '定义 -').")
        return 0

    new_line = f"{m.group('prefix')}{new_title}{m.group('suffix')}"

    print("Proposed changes:")
    old_s = line.rstrip("\n")
    new_s = new_line.rstrip("\n")
    print(f"- L{idx}:")
    print(f"  - {old_s}")
    print(f"  + {new_s}")

    if not args.apply:
        print("\nRun again with --apply to write changes.")
        return 0

    lines[idx - 1] = new_line

    path.write_text("".join(lines), encoding="utf-8")
    print("\nApplied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
