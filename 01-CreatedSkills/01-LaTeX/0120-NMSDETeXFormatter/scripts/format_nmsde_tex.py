#!/usr/bin/env python3
import argparse
import re
from pathlib import Path

_CUSTOMPROBLEM_SIMPLE = re.compile(
    r"^(?P<indent>[ \t]*)\\customproblem\{(?P<title>[^}]*)\}\{(?P<body>[^{}\n]*)\}\s*$"
)


def _format_customproblem_simple(line: str) -> str:
    m = _CUSTOMPROBLEM_SIMPLE.match(line)
    if not m:
        return line

    indent = m.group("indent").replace("\t", "    ")
    title = m.group("title")
    body = m.group("body")

    # Keep empty placeholders unchanged.
    if body.strip() == "":
        return f"{indent}\\customproblem{{{title}}}{{}}"

    body_stripped = body.strip()
    return (
        f"{indent}\\customproblem{{{title}}}{{\n\n"
        f"{indent}    {body_stripped}\n\n"
        f"{indent}}}"
    )


def format_tex(text: str) -> str:
    # Normalize tabs first so indentation rules are stable.
    text = text.replace("\t", "    ")

    out_lines = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        line = _format_customproblem_simple(line)
        out_lines.append(line)

    out = "\n".join(out_lines) + "\n"
    return out


def process_file(path: Path, check: bool) -> int:
    original = path.read_text(encoding="utf-8")
    formatted = format_tex(original)

    if formatted == original:
        print(f"[OK] {path}")
        return 0

    if check:
        print(f"[CHANGE] {path}")
        return 1

    path.write_text(formatted, encoding="utf-8")
    print(f"[OK] Updated {path}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Format NMSDE LaTeX documents to match Chapter1_NMSDE.tex whitespace/block style (safe subset)."
    )
    parser.add_argument("--check", action="store_true", help="Check only; exit 1 if changes are needed")
    parser.add_argument("files", nargs="+", help=".tex file(s) to format")
    args = parser.parse_args()

    rc = 0
    for f in args.files:
        path = Path(f)
        if not path.exists():
            print(f"[ERROR] Not found: {path}")
            rc = 2
            continue
        rc = max(rc, process_file(path, args.check))
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
