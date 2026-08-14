#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

ITEM_RE = re.compile(r"^\s*\\item\s+(.*)$", re.M)


def split_block(text: str) -> str:
    m = re.search(r"\\customproblem\{([^}]*)\}\{", text)
    if not m:
        return text
    title = m.group(1)

    items = ITEM_RE.findall(text)
    if len(items) <= 1:
        return text

    chunks = []
    for i, it in enumerate(items, start=1):
        chunks.append(
            f"\\customproblem{{{title}({i})}}{{\n\n设:\n\\begin{{enumerate}}\n\n    \\item \n\n\\end{{enumerate}}\n如果:\n\\begin{{enumerate}}\n\n    \\item {it}\n\n\\end{{enumerate}}\n}}\n\n"
        )
    return "\n".join(chunks)


def main() -> int:
    p = argparse.ArgumentParser(description="Split one definition block into multiple blocks by top-level items.")
    p.add_argument("--file", required=True)
    p.add_argument("--in-place", action="store_true")
    args = p.parse_args()

    path = Path(args.file)
    src = path.read_text(encoding="utf-8")
    out = split_block(src)
    if args.in_place:
        path.write_text(out, encoding="utf-8")
    else:
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
