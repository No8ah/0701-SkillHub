#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys

TIKZ_BEGIN = re.compile(r"\\begin\{tikzpicture\}")
TIKZ_END = re.compile(r"\\end\{tikzpicture\}")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
FULL_COMMENT_RE = re.compile(r"^\s*%")


def iter_tex_files(path: pathlib.Path):
    if path.is_file() and path.suffix == ".tex":
        yield path
        return
    if path.is_dir():
        for p in sorted(path.rglob("*.tex")):
            if p.is_file():
                yield p


def check_file(path: pathlib.Path):
    issues = []
    in_tikz = False
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        return [(0, "Cannot decode file as UTF-8")]

    for idx, line in enumerate(lines, start=1):
        is_full_comment = FULL_COMMENT_RE.match(line) is not None

        # Only uncommented begin/end delimit active tikzpicture ranges.
        if (not is_full_comment) and TIKZ_BEGIN.search(line):
            in_tikz = True

        if in_tikz and CJK_RE.search(line):
            issues.append((idx, line.rstrip()))

        if (not is_full_comment) and TIKZ_END.search(line):
            in_tikz = False

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Fail if any Chinese character appears inside tikzpicture environments."
    )
    parser.add_argument("target", help="Path to a .tex file or directory")
    args = parser.parse_args()

    target = pathlib.Path(args.target).expanduser().resolve()
    files = list(iter_tex_files(target))
    if not files:
        print(f"No .tex files found under: {target}")
        return 2

    failed = False
    for tex_file in files:
        issues = check_file(tex_file)
        if not issues:
            continue
        failed = True
        print(f"[FAIL] {tex_file}")
        for lineno, content in issues:
            if lineno == 0:
                print(f"  - {content}")
            else:
                print(f"  - line {lineno}: {content}")

    if failed:
        return 1

    print(f"[OK] Checked {len(files)} .tex file(s); no Chinese found inside tikzpicture.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
