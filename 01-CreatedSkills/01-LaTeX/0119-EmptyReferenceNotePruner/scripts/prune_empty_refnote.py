#!/usr/bin/env python3

import argparse
import re
import sys
from pathlib import Path


HEADER_PATTERNS = {
    "ref": re.compile(r"^\s*\\textbf\{引用:\}\s*$"),
    "note": re.compile(r"^\s*\\textbf\{注:\}\s*$"),
}

PLACEHOLDER_ITEM_RE = re.compile(r"^\s*\\hspace\*\{2em\}\s*\d+\.\s*\\quad\s*$")


def _is_blank(line: str) -> bool:
    return line.strip() == ""


def _prune_empty_block(lines: list[str], header_re: re.Pattern[str]) -> tuple[list[str], bool]:
    """Remove an empty block starting with header_re.

    Empty block definition:
      header line
      then (blank lines + placeholder item lines) only
      then optional trailing blank lines

    Returns (new_lines, changed).
    """

    out: list[str] = []
    i = 0
    changed = False

    while i < len(lines):
        if not header_re.match(lines[i]):
            out.append(lines[i])
            i += 1
            continue

        header_index = i
        j = i + 1

        # Consume blanks after header
        while j < len(lines) and _is_blank(lines[j]):
            j += 1

        # Consume placeholder items (allow blank lines between items)
        saw_placeholder = False
        k = j
        while k < len(lines):
            if _is_blank(lines[k]):
                k += 1
                continue
            if PLACEHOLDER_ITEM_RE.match(lines[k]):
                saw_placeholder = True
                k += 1
                continue
            break

        # Consume trailing blanks
        m = k
        while m < len(lines) and _is_blank(lines[m]):
            m += 1

        # Only prune if we saw at least one placeholder and no other content
        if saw_placeholder:
            # Drop [header_index:m)
            changed = True
            i = m
            continue

        # Not an empty placeholder block -> keep as-is
        out.append(lines[header_index])
        i = header_index + 1

    return out, changed


def prune_text(text: str) -> tuple[str, bool]:
    lines = text.splitlines(keepends=True)

    changed_any = False
    for key in ("ref", "note"):
        lines, changed = _prune_empty_block(lines, HEADER_PATTERNS[key])
        changed_any = changed_any or changed

    return "".join(lines), changed_any


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Remove empty LaTeX \\textbf{引用:}/\\textbf{注:} placeholder blocks.",
    )
    parser.add_argument(
        "paths",
        nargs="+",
        help="One or more .tex files to process",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if a change would be made; do not write files",
    )

    args = parser.parse_args()

    changed_files: list[Path] = []
    for raw_path in args.paths:
        path = Path(raw_path)
        if not path.exists():
            print(f"[ERROR] File not found: {path}", file=sys.stderr)
            return 2
        if path.is_dir():
            print(f"[ERROR] Path is a directory: {path}", file=sys.stderr)
            return 2

        original = path.read_text(encoding="utf-8")
        updated, changed = prune_text(original)

        if changed:
            changed_files.append(path)
            if not args.check:
                path.write_text(updated, encoding="utf-8")

    if args.check:
        if changed_files:
            for p in changed_files:
                print(f"[CHANGE] {p}")
            return 1
        return 0

    for p in changed_files:
        print(f"[OK] Updated {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
