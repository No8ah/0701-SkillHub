#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path

KIND_MAP = {
    "定义": "def",
    "定理": "thm",
    "引理": "lem",
    "命题": "prop",
    "推论": "prop",
}


def to_block(text: str) -> str:
    lines = [x.strip() for x in text.strip().splitlines() if x.strip()]
    title = lines[0] if lines else "Page ? - 定义 - Content"
    body = "\n".join(lines[1:]) if len(lines) > 1 else ""

    kind = "定义"
    for k in KIND_MAP:
        if k in title:
            kind = k
            break
    label_prefix = KIND_MAP.get(kind, "def")

    return f'''\\customproblem{{{title}}}{{

设:
\\begin{{enumerate}}

    \\item 

\\end{{enumerate}}
如果:
\\begin{{enumerate}}

    \\item 

\\end{{enumerate}}
则:
\\begin{{enumerate}}

    \\item {body}

\\end{{enumerate}}
}}

\\addcontentsline{{toc}}{{subsubsection}}{{{title}}}

\\phantomsection\\label{{{label_prefix}:<course>:<chap>:<id>}}
'''


def main() -> int:
    p = argparse.ArgumentParser(description="Convert raw theorem/lemma/definition text into customproblem scaffold.")
    p.add_argument("--input", default="-")
    p.add_argument("--output", default="-")
    args = p.parse_args()

    if args.input == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(args.input).read_text(encoding="utf-8")

    out = to_block(raw)

    if args.output == "-":
        sys.stdout.write(out)
    else:
        Path(args.output).write_text(out, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
