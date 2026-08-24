#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Finding:
    kind: str  # "empty" | "missing"
    line_no: int
    label: str
    context: str


LABEL_RE = re.compile(r"\\phantomsection\\label\{([^}]*)\}")
HYPERREF_RE = re.compile(r"\\hyperref\[([^\]]*)\]\{")


def _line_context(line: str, limit: int = 120) -> str:
    s = line.rstrip("\n")
    if len(s) <= limit:
        return s
    return s[: limit - 1] + "…"


def inspect_tex(path: Path) -> tuple[set[str], list[Finding], int, int]:
    text = path.read_text(encoding="utf-8")
    labels = set(LABEL_RE.findall(text))

    findings: list[Finding] = []
    hyperref_total = 0

    for idx, line in enumerate(text.splitlines(True), start=1):
        for m in HYPERREF_RE.finditer(line):
            hyperref_total += 1
            label = m.group(1).strip()
            if not label:
                findings.append(Finding("empty", idx, label, _line_context(line)))
            elif label not in labels:
                findings.append(Finding("missing", idx, label, _line_context(line)))

    return labels, findings, len(labels), hyperref_total


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Inspect LaTeX \\hyperref[...] labels against \\phantomsection\\label{...} definitions."
    )
    parser.add_argument("tex_path", type=Path, help="Path to a .tex file")
    args = parser.parse_args(argv)

    tex_path: Path = args.tex_path
    if not tex_path.exists():
        print(f"error: file not found: {tex_path}", file=sys.stderr)
        return 2

    labels, findings, label_count, hyperref_total = inspect_tex(tex_path)

    print(f"labels: {label_count}")
    print(f"hyperref: {hyperref_total}")

    if not findings:
        print("OK: all hyperref labels are non-empty and exist in this file")
        return 0

    empty = [f for f in findings if f.kind == "empty"]
    missing = [f for f in findings if f.kind == "missing"]

    if empty:
        print("\nEMPTY hyperref labels:")
        for f in empty:
            print(f"  L{f.line_no}: \\hyperref[]{{...}}  | {f.context}")

    if missing:
        print("\nMISSING hyperref labels (not found in any \\phantomsection\\label{...} in this file):")
        for f in missing:
            print(f"  L{f.line_no}: [{f.label}] | {f.context}")

        print("\nTip: if labels live in another file, run this script on that file too, or grep the repo for the label.")

    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
