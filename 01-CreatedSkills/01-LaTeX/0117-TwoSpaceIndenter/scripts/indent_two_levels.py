#!/usr/bin/env python3
"""
Reformat Step blocks to an "indent two levels deeper" layout.

Pattern (example):
- Keep the first "\\textbf{StepN:}\\quad ..." as the parent step, with "\\hspace*{2em}".
- Convert following sibling "StepN" lines to numbered second-level items:
  "\\hspace*{4em} 1. ...", "\\hspace*{4em} 2. ..."
- Convert third-level lines under each sibling from
  "\\hspace*{2em} m. ..." to "\\hspace*{6em} i.m. ...".

This is deterministic and conservative: it only edits lines that match this
specific StepN pattern.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, Optional

PARENT_STEP_RE = re.compile(
    r"^(?P<indent>[ \t]*)\\textbf\{Step(?P<n>\d+):\}\\quad(?P<sp>[ \t]*)(?P<body>.*)$"
)

CHILD_STEP_RE = re.compile(
    r"^(?P<indent>[ \t]*)\\textbf\{Step(?P<n>\d+):\}\\quad(?P<sp>[ \t]*)(?P<body>.*\$.*)$"
)

THIRD_LEVEL_RE = re.compile(
    r"^(?P<indent>[ \t]*)\\hspace\*\{2em\}[ \t]*(?P<num>\d+)\.[ \t]*(?P<rest>.*)$"
)

ANY_STEP_RE = re.compile(r"^[ \t]*\\textbf\{Step\d+:\}\\quad")


def _ensure_parent_indent(line: str) -> str:
    m = PARENT_STEP_RE.match(line)
    if not m:
        return line
    body = m.group("body")
    # Parent step should be textual headline (not formula line).
    if "$" in body:
        return line
    if r"\hspace*{2em}" in line:
        return line
    indent = m.group("indent")
    sp = m.group("sp")
    return f"{indent}\\hspace*{{2em}} \\textbf{{Step{m.group('n')}:}}\\quad{sp}{body}\n"


def _process_text(text: str) -> tuple[str, int]:
    lines = text.splitlines(True)
    changed = 0
    i = 0

    while i < len(lines):
        m = PARENT_STEP_RE.match(lines[i])
        if not m:
            i += 1
            continue

        step_n = m.group("n")
        # Parent line should not be a math child-line.
        if "$" in m.group("body"):
            i += 1
            continue

        new_parent = _ensure_parent_indent(lines[i])
        if new_parent != lines[i]:
            lines[i] = new_parent
            changed += 1

        # Collect sibling StepN formula lines after parent.
        sibling_idxs: list[int] = []
        j = i + 1
        while j < len(lines):
            cm = CHILD_STEP_RE.match(lines[j])
            if cm and cm.group("n") == step_n:
                sibling_idxs.append(j)
                j += 1
                continue
            # Stop when entering another Step line with different number.
            if ANY_STEP_RE.match(lines[j]):
                break
            j += 1

        if not sibling_idxs:
            i += 1
            continue

        # Rewrite sibling lines and their third-level numbered lines.
        for idx, sidx in enumerate(sibling_idxs, start=1):
            cm = CHILD_STEP_RE.match(lines[sidx])
            if not cm:
                continue
            child_body = cm.group("body").strip()
            new_child = f"{cm.group('indent')}\\hspace*{{4em}} {idx}. {child_body}\n"
            if lines[sidx] != new_child:
                lines[sidx] = new_child
                changed += 1

            # Segment under this child until next sibling/step.
            seg_end = len(lines)
            for nxt in sibling_idxs:
                if nxt > sidx:
                    seg_end = nxt
                    break
            k = sidx + 1
            while k < seg_end:
                tm = THIRD_LEVEL_RE.match(lines[k])
                if tm:
                    num = tm.group("num")
                    rest = tm.group("rest")
                    new_third = f"{tm.group('indent')}\\hspace*{{6em}} {idx}.{num}. {rest}\n"
                    if new_third != lines[k]:
                        lines[k] = new_third
                        changed += 1
                k += 1

        i = j

    return "".join(lines), changed


def main(argv: Optional[Iterable[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Indent Step blocks two levels deeper in Example_往后缩进两格 style.")
    p.add_argument("paths", nargs="+", help="One or more .tex/.md files, or '-' for stdin/stdout")
    p.add_argument("--in-place", action="store_true", help="Edit files in place")
    p.add_argument("--encoding", default="utf-8", help="File encoding (default: utf-8)")
    args = p.parse_args(list(argv) if argv is not None else None)

    total = 0
    for raw in args.paths:
        if raw == "-":
            original = sys.stdin.read()
            updated, changed = _process_text(original)
            total += changed
            sys.stdout.write(updated)
            print(f"[OK] stdin changed_units={changed}", file=sys.stderr)
            continue

        path = Path(raw)
        original = path.read_text(encoding=args.encoding)
        updated, changed = _process_text(original)
        total += changed

        if args.in_place:
            if updated != original:
                path.write_text(updated, encoding=args.encoding)
            print(f"[OK] edited: {path} changed_units={changed}", file=sys.stderr)
        else:
            sys.stdout.write(updated)
            print(f"[OK] previewed: {path} changed_units={changed}", file=sys.stderr)

    print(f"[SUMMARY] changed_units_total={total}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
