#!/usr/bin/env python3
"""
Insert section/subsection heading blocks with "star star star" before
\customproblem definition/theorem blocks.

Rules from Example_根据定义添加section并添加3 star:
- For "补充 - 定义 - Content - <topic>", insert blue subsection heading.
- For "补充 - 定理 - Content - <topic>", insert red section heading.
- Topic uses the first segment after "Content -" split by " - ".
- Avoid duplicate insertion when a matching addcontentsline is already nearby.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, Optional


CP_RE = re.compile(r"^(?P<indent>[ \t]*)\\customproblem\{(?P<title>[^}]*)\}\{", re.MULTILINE)

DEF_PREFIX = "补充 - 定义 - Content - "
THM_PREFIX = "补充 - 定理 - Content - "


def _extract_topic(title: str, prefix: str) -> Optional[str]:
    if not title.startswith(prefix):
        return None
    tail = title[len(prefix) :].strip()
    if not tail:
        return None
    topic = tail.split(" - ", 1)[0].strip()
    return topic if topic else None


def _build_insert_block(kind: str, topic: str, indent: str) -> str:
    stars = r"$\star \star \star$"
    if kind == "def":
        heading = rf"\subsection*{{\textcolor{{blue}}{{{topic} {stars}}}}}"
        toc = rf"\addcontentsline{{toc}}{{subsection}}{{\textcolor{{blue}}{{{topic} {stars}}}}}"
    else:
        heading = rf"\section*{{\textcolor{{red}}{{{topic} {stars}}}}}"
        toc = rf"\addcontentsline{{toc}}{{section}}{{\textcolor{{red}}{{{topic} {stars}}}}}"

    return (
        f"{indent}\\clearpage\n"
        f"{indent}\\newpage\n\n"
        f"{indent}{heading}\n"
        f"{indent}{toc}\n\n"
    )


def _already_has_heading_block(prefix_text: str, topic: str, toc_level: str) -> bool:
    # Check the latest non-empty chunk before current \customproblem to avoid duplicate insertions.
    window = prefix_text[-1200:]
    for line in window.splitlines():
        if (
            f"\\addcontentsline{{toc}}{{{toc_level}}}" in line
            and topic in line
            and r"$\star \star \star$" in line
        ):
            return True
    return False


def _process_text(text: str) -> tuple[str, int]:
    out_parts: list[str] = []
    changed = 0
    last = 0

    for m in CP_RE.finditer(text):
        start = m.start()
        indent = m.group("indent")
        title = m.group("title")

        chunk = text[last:start]
        out_parts.append(chunk)

        topic_def = _extract_topic(title, DEF_PREFIX)
        topic_thm = _extract_topic(title, THM_PREFIX)

        if topic_def:
            if not _already_has_heading_block("".join(out_parts), topic_def, "subsection"):
                out_parts.append(_build_insert_block("def", topic_def, indent))
                changed += 1
        elif topic_thm:
            if not _already_has_heading_block("".join(out_parts), topic_thm, "section"):
                out_parts.append(_build_insert_block("thm", topic_thm, indent))
                changed += 1

        out_parts.append(text[start : m.end()])
        last = m.end()

    out_parts.append(text[last:])
    return "".join(out_parts), changed


def main(argv: Optional[Iterable[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Insert section/subsection + 3-star blocks before customproblem definition/theorem blocks."
    )
    parser.add_argument("paths", nargs="+", help="One or more .tex files")
    parser.add_argument("--in-place", action="store_true", help="Edit file(s) in place")
    parser.add_argument("--encoding", default="utf-8", help="File encoding (default: utf-8)")
    args = parser.parse_args(list(argv) if argv is not None else None)

    total_changed = 0
    for raw in args.paths:
        path = Path(raw)
        original = path.read_text(encoding=args.encoding)
        updated, changed = _process_text(original)
        total_changed += changed

        if args.in_place:
            if updated != original:
                path.write_text(updated, encoding=args.encoding)
            print(f"[OK] edited: {path} inserted_blocks={changed}", file=sys.stderr)
        else:
            sys.stdout.write(updated)
            print(f"[OK] previewed: {path} inserted_blocks={changed}", file=sys.stderr)

    print(f"[SUMMARY] inserted_blocks_total={total_changed}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
