#!/usr/bin/env python3
import argparse
import re
from pathlib import Path


def split_subqs(text: str) -> list[str]:
    parts = re.split(r"\n\s*(?:\([a-zA-Z]\)|\(\d+\))\s*", text)
    if len(parts) <= 1:
        return []
    return [p.strip() for p in parts[1:] if p.strip()]


def render(title: str, text: str) -> str:
    subqs = split_subqs(text)
    if not subqs:
        body = text.strip()
        enum = "\\begin{enumerate}\n\n    \\item \n\n\\end{enumerate}"
    else:
        items = []
        for q in subqs:
            items.append(
                "    \\item " + q + "\n\n" +
                "    \\begin{tcolorbox}\n\n    \\end{tcolorbox}\n"
            )
        enum = "\\begin{enumerate}\n\n" + "\n".join(items) + "\n\\end{enumerate}"
        body = text.strip().splitlines()[0]

    return f'''\\customproblem{{{title}}}{{
{body}
}}

\\addcontentsline{{toc}}{{subsubsection}}{{{title}}}

\\phantomsection\\label{{prob:<course>:<chap>:<id>}}

    \\textbf{{简明思路:}}

{enum}
'''


def main() -> int:
    p = argparse.ArgumentParser(description="Convert raw problem statement into customproblem template.")
    p.add_argument("--title", required=True)
    p.add_argument("--input", required=True)
    p.add_argument("--output", default="-")
    args = p.parse_args()

    text = Path(args.input).read_text(encoding="utf-8")
    out = render(args.title, text)
    if args.output == "-":
        print(out)
    else:
        Path(args.output).write_text(out, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
