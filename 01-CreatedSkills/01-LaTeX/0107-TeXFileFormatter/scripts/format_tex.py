#!/usr/bin/env python3
"""Conservative TeX formatter used by the tex-format skill."""

from __future__ import annotations

import argparse
import difflib
import re
import sys
from pathlib import Path
from typing import Iterable, Optional

HEADING_RE = re.compile(r"^(?P<indent>[ \t]*)\\(?:section|subsection)\*\{")


def _collapse_tabs_and_trim(line: str) -> tuple[str, bool]:
    new_line = line.replace("\t", "    ").rstrip()
    return new_line, new_line != line


def _split_inline_math(line: str) -> list[tuple[bool, str]]:
    """Split into [(is_math, segment)] by unescaped '$'.

    If the line has unmatched '$', return as plain text segment for safety.
    """
    segments: list[tuple[bool, str]] = []
    buffer: list[str] = []
    in_math = False
    i = 0

    while i < len(line):
        ch = line[i]
        if ch == "$" and (i == 0 or line[i - 1] != "\\"):
            if buffer:
                segments.append((in_math, "".join(buffer)))
                buffer = []
            in_math = not in_math
            i += 1
            continue
        buffer.append(ch)
        i += 1

    if buffer:
        segments.append((in_math, "".join(buffer)))

    # Unmatched dollar -> do not touch.
    if in_math:
        return [(False, line)]
    return segments


def _break_math_segment(segment: str, cont_indent: str) -> tuple[str, bool]:
    new_segment = segment
    changed = False

    for token in (" \\leqslant ", " = "):
        if token in new_segment:
            repl = f"\n{cont_indent}{token.strip()}\n{cont_indent}"
            updated = new_segment.replace(token, repl)
            if updated != new_segment:
                changed = True
                new_segment = updated

    return new_segment, changed


def _break_long_math_line(line: str, min_len: int = 90) -> tuple[str, bool]:
    if "$" not in line or len(line) < min_len:
        return line, False

    leading_ws = re.match(r"^[ \t]*", line).group(0) if line else ""
    cont_indent = leading_ws + "    "

    segments = _split_inline_math(line)
    pieces: list[str] = []
    changed = False

    for is_math, seg in segments:
        if not is_math:
            pieces.append(seg)
            continue

        updated_seg, seg_changed = _break_math_segment(seg, cont_indent)
        changed = changed or seg_changed
        pieces.append(f"${updated_seg}$")

    if not changed:
        return line, False
    return "".join(pieces), True


def _has_pagebreak_pair(out_lines: list[str]) -> bool:
    recent = [x.strip() for x in out_lines if x.strip()]
    if len(recent) < 2:
        return False
    return recent[-2] == r"\clearpage" and recent[-1] == r"\newpage"


def _ensure_pagebreak_before_heading(lines: list[str]) -> tuple[list[str], int]:
    out: list[str] = []
    inserted = 0

    for line in lines:
        match = HEADING_RE.match(line)
        if match and not _has_pagebreak_pair(out):
            indent = match.group("indent")
            if out and out[-1].strip():
                out.append("")
            out.append(f"{indent}\\clearpage")
            out.append(f"{indent}\\newpage")
            out.append("")
            inserted += 1
        out.append(line)

    return out, inserted


def format_tex(text: str, break_long_math: bool) -> tuple[str, dict[str, int]]:
    raw_lines = text.splitlines()

    lines: list[str] = []
    ws_changed = 0
    math_changed = 0

    for raw in raw_lines:
        line, ws_line_changed = _collapse_tabs_and_trim(raw)
        ws_changed += int(ws_line_changed)

        if break_long_math:
            line, math_line_changed = _break_long_math_line(line)
            math_changed += int(math_line_changed)

        lines.extend(line.split("\n"))

    lines, pagebreak_inserted = _ensure_pagebreak_before_heading(lines)

    # Keep deterministic trailing newline.
    new_text = "\n".join(lines).rstrip() + "\n"
    stats = {
        "ws_changed": ws_changed,
        "math_lines_broken": math_changed,
        "pagebreak_inserted": pagebreak_inserted,
    }
    return new_text, stats


def _iter_target_files(paths: list[str]) -> list[Path]:
    results: list[Path] = []
    for raw in paths:
        path = Path(raw)
        if path.is_dir():
            results.extend(sorted(path.rglob("*.tex")))
        else:
            results.append(path)
    return results


def _print_diff(path: Path, old: str, new: str) -> None:
    diff = difflib.unified_diff(
        old.splitlines(),
        new.splitlines(),
        fromfile=f"a/{path}",
        tofile=f"b/{path}",
        lineterm="",
    )
    for line in diff:
        print(line)


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Format TeX files: whitespace cleanup + ensure \\clearpage/\\newpage before "
            "\\section* and \\subsection*, "
            "with optional long inline-math wrapping."
        )
    )
    parser.add_argument("paths", nargs="+", help="One or more .tex files or directories")
    parser.add_argument("--check", action="store_true", help="Exit 1 if any target file would change")
    parser.add_argument("--diff", action="store_true", help="Print unified diff for changed files")
    parser.add_argument(
        "--break-long-math",
        action="store_true",
        help="Wrap long inline math around '=' / '\\leqslant' inside $...$",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    files = _iter_target_files(args.paths)
    if not files:
        print("No target files found.", file=sys.stderr)
        return 2

    any_change = False
    has_error = False

    for path in files:
        if not path.exists():
            print(f"ERROR {path} not found", file=sys.stderr)
            has_error = True
            continue
        if path.is_dir():
            continue

        try:
            old = path.read_text(encoding="utf-8")
        except Exception as exc:  # pragma: no cover
            print(f"ERROR {path} read failed: {exc}", file=sys.stderr)
            has_error = True
            continue

        new, stats = format_tex(old, break_long_math=args.break_long_math)
        changed = old != new
        any_change = any_change or changed

        if args.diff and changed:
            _print_diff(path, old, new)

        if args.check:
            state = "CHANGE" if changed else "OK"
            print(
                f"{state} {path} ws_changed={stats['ws_changed']} "
                f"math_lines_broken={stats['math_lines_broken']} "
                f"pagebreak_inserted={stats['pagebreak_inserted']}"
            )
            continue

        if changed:
            try:
                path.write_text(new, encoding="utf-8")
            except Exception as exc:  # pragma: no cover
                print(f"ERROR {path} write failed: {exc}", file=sys.stderr)
                has_error = True
                continue

        print(
            f"OK {path} changed={int(changed)} ws_changed={stats['ws_changed']} "
            f"math_lines_broken={stats['math_lines_broken']} "
            f"pagebreak_inserted={stats['pagebreak_inserted']}"
        )

    if has_error:
        return 2
    if args.check and any_change:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
