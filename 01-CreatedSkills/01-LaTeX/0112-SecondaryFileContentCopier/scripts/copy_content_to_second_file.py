#!/usr/bin/env python3
import argparse
from pathlib import Path


def read_lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines(keepends=True)


def main() -> int:
    p = argparse.ArgumentParser(description="Copy line range to target file and optionally delete source lines.")
    p.add_argument("--src", required=True)
    p.add_argument("--start", type=int, required=True)
    p.add_argument("--end", type=int, required=True)
    p.add_argument("--dst", required=True)
    p.add_argument("--before-line", type=int, required=True)
    p.add_argument("--delete-source", action="store_true")
    p.add_argument("--section-title", default="")
    p.add_argument("--add-contentsline", action="store_true")
    args = p.parse_args()

    src = Path(args.src)
    dst = Path(args.dst)
    src_lines = read_lines(src)
    dst_lines = read_lines(dst)

    s = max(args.start - 1, 0)
    e = min(args.end, len(src_lines))
    block = src_lines[s:e]

    if args.section_title:
        head = [f"\\section*{{{args.section_title}}}\n"]
        if args.add_contentsline:
            head.append(f"\\addcontentsline{{toc}}{{section}}{{{args.section_title}}}\n")
        block = head + ["\n"] + block

    ins = max(args.before_line - 1, 0)
    dst_lines = dst_lines[:ins] + block + dst_lines[ins:]
    dst.write_text("".join(dst_lines), encoding="utf-8")

    if args.delete_source:
        src_lines = src_lines[:s] + src_lines[e:]
        src.write_text("".join(src_lines), encoding="utf-8")

    print("ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
