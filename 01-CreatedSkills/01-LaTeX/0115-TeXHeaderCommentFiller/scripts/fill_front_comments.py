#!/usr/bin/env python3
from __future__ import annotations

import argparse
import getpass
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path


@dataclass(frozen=True)
class HeaderEdits:
    file_name: str
    dir_path: str
    author: str
    modified: str


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fill/refresh the front comment header fields in a LaTeX .tex file."
    )
    parser.add_argument("--file", required=True, help="Target .tex file path.")
    parser.add_argument("--author", default=None, help="Author name to write into header.")
    parser.add_argument("--date", default=None, help="Override date as YYYY-MM-DD.")
    parser.add_argument("--dry-run", action="store_true", help="Do not write changes.")
    return parser.parse_args()


def _today_str() -> str:
    return date.today().isoformat()


def _validate_date_string(s: str) -> str:
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        raise SystemExit(f"invalid --date (expected YYYY-MM-DD): {s}")
    return s


def _compute_edits(file_path: Path, author: str | None, modified: str | None) -> HeaderEdits:
    resolved = file_path.resolve()
    file_name = resolved.name
    dir_path = str(resolved.parent) + "/"
    author_value = author if author else getpass.getuser()
    modified_value = _validate_date_string(modified) if modified else _today_str()
    return HeaderEdits(
        file_name=file_name,
        dir_path=dir_path,
        author=author_value,
        modified=modified_value,
    )


def _replace_field(line: str, *, key: str, value: str) -> str:
    # Preserve leading '%', spaces, and existing formatting around the key.
    # Example: "% AUTHOR: [Your Name]" -> "% AUTHOR: quzinan"
    pattern = rf"^(\s*%\s*{re.escape(key)}\s*:\s*).*$"
    m = re.match(pattern, line)
    if not m:
        return line
    return f"{m.group(1)}{value}\n"


def _apply_edits(lines: list[str], edits: HeaderEdits) -> list[str]:
    updated = []
    for line in lines:
        line2 = line
        line2 = _replace_field(line2, key="FILE", value=edits.file_name)
        line2 = _replace_field(line2, key="PATH", value=edits.dir_path)
        line2 = _replace_field(line2, key="AUTHOR", value=edits.author)
        line2 = _replace_field(line2, key="LAST MODIFIED", value=edits.modified)
        updated.append(line2)
    return updated


def main() -> None:
    args = _parse_args()
    file_path = Path(args.file)
    if not file_path.exists():
        raise SystemExit(f"file not found: {file_path}")

    original = file_path.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)

    edits = _compute_edits(file_path, author=args.author, modified=args.date)
    new_lines = _apply_edits(lines, edits)
    new_text = "".join(new_lines)

    if new_text == original:
        return

    if args.dry_run:
        return

    file_path.write_text(new_text, encoding="utf-8")


if __name__ == "__main__":
    main()

