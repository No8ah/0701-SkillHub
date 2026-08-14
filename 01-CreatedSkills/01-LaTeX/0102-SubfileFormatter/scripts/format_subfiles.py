#!/usr/bin/env python3
"""
Batch-normalize LaTeX subfiles.

Goals (conservative):
- Normalize/repair the wrapper: \\documentclass[..]{subfiles}, \\begin{document}, \\end{document}
- If the file is a standalone document (article/book/report), keep only the body.
- Fix the parent relative path when --parent is provided.
- Dry-run by default; write only with --write.
"""

from __future__ import annotations

import argparse
import glob
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Optional, Tuple


BEGIN_DOC = r"\begin{document}"
END_DOC = r"\end{document}"


@dataclass
class Change:
    path: Path
    changed: bool
    reason: str


def _read_text(path: Path) -> str:
    # Use UTF-8; most TeX sources here are UTF-8.
    return path.read_text(encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _strip_trailing_whitespace(lines: List[str]) -> List[str]:
    return [ln.rstrip() for ln in lines]


def _find_first_stripped(lines: List[str], needle: str) -> Optional[int]:
    for i, ln in enumerate(lines):
        if ln.strip() == needle:
            return i
    return None


def _find_last_stripped(lines: List[str], needle: str) -> Optional[int]:
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == needle:
            return i
    return None


def _compute_rel_parent(child_file: Path, parent_file: Path) -> str:
    rel = os.path.relpath(parent_file.resolve(), child_file.parent.resolve())
    # TeX accepts forward slashes on all platforms; keep output stable.
    return rel.replace(os.sep, "/")


def _extract_body(lines: List[str]) -> Tuple[List[str], str]:
    """
    Extract "document body" lines.

    Prefer content between the first \\begin{document} and the last \\end{document}.
    If not found, return the full file content.
    """
    begin_idx = _find_first_stripped(lines, BEGIN_DOC)
    end_idx = _find_last_stripped(lines, END_DOC)

    if begin_idx is not None and end_idx is not None and begin_idx < end_idx:
        body = lines[begin_idx + 1 : end_idx]
        return body, "extracted_body_between_begin_end"

    return lines[:], "used_full_file_as_body"


def _build_subfile_text(
    *,
    body_lines: List[str],
    rel_parent: Optional[str],
    ensure_wrapper: bool,
) -> str:
    out: List[str] = []

    if ensure_wrapper:
        if rel_parent is None:
            # Still output a wrapper, but with a placeholder that keeps TeX invalid
            # so the user is forced to supply a parent if they want consistency.
            rel_parent = "../PARENT.tex"
        out.append(fr"\documentclass[{rel_parent}]{{subfiles}}")
        out.append("")
        out.append(BEGIN_DOC)
        out.append("")

    # Keep body mostly as-is; only normalize trailing whitespace.
    body = _strip_trailing_whitespace(body_lines)
    # Avoid leading excessive empty lines.
    while body and body[0] == "":
        body.pop(0)
    # Avoid trailing excessive empty lines.
    while body and body[-1] == "":
        body.pop()
    out.extend(body)
    out.append("")
    out.append(END_DOC)
    out.append("")

    return "\n".join(out)


def format_one(
    *,
    path: Path,
    parent: Optional[Path],
    force_wrapper: bool,
) -> Tuple[bool, str, str]:
    original = _read_text(path)
    lines = original.splitlines()
    lines = _strip_trailing_whitespace(lines)

    body_lines, body_mode = _extract_body(lines)

    rel_parent = _compute_rel_parent(path, parent) if parent is not None else None
    new_text = _build_subfile_text(
        body_lines=body_lines,
        rel_parent=rel_parent,
        ensure_wrapper=force_wrapper,
    )

    changed = new_text != (original if original.endswith("\n") else original + "\n")
    reason = f"{body_mode}" + (", set_parent_relpath" if parent is not None else "")
    return changed, reason, new_text


def iter_targets(root: Path, pattern: str) -> Iterable[Path]:
    full_pattern = str(root / pattern)
    for match in glob.glob(full_pattern, recursive=True):
        p = Path(match)
        if p.is_file() and p.suffix == ".tex":
            yield p


def main() -> int:
    parser = argparse.ArgumentParser(description="Format LaTeX subfiles (dry-run by default).")
    parser.add_argument("--root", type=Path, help="Root directory to scan.")
    parser.add_argument("--glob", default="**/*.tex", help="Glob under --root (default: **/*.tex).")
    parser.add_argument(
        "--parent",
        type=Path,
        help="Parent .tex file path; used to compute \\documentclass[REL]{subfiles}.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write changes in-place. Without this flag, only prints planned changes.",
    )
    parser.add_argument(
        "--no-wrapper",
        action="store_true",
        help="Do not rewrite wrapper; only trims to body if begin/end exist.",
    )
    parser.add_argument("files", nargs="*", help="Optional explicit .tex file paths (override --root/--glob).")
    args = parser.parse_args()

    parent = args.parent.resolve() if args.parent is not None else None
    force_wrapper = not args.no_wrapper

    if args.files:
        targets = [Path(f) for f in args.files]
    else:
        if args.root is None:
            parser.error("Provide --root/--glob or explicit file paths.")
        targets = list(iter_targets(args.root, args.glob))

    targets = [p for p in targets if p.is_file()]
    if not targets:
        print("No .tex targets found.")
        return 0

    changes: List[Change] = []
    for path in sorted(targets):
        changed, reason, new_text = format_one(path=path, parent=parent, force_wrapper=force_wrapper)
        if changed:
            changes.append(Change(path=path, changed=True, reason=reason))
            if args.write:
                _write_text(path, new_text)

    if not changes:
        print("No changes needed.")
        return 0

    mode = "WROTE" if args.write else "DRY-RUN"
    print(f"{mode}: {len(changes)} file(s) would change:" if not args.write else f"{mode}: changed {len(changes)} file(s):")
    for ch in changes:
        print(f"- {ch.path} ({ch.reason})")

    if not args.write:
        print("Re-run with --write to apply changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
