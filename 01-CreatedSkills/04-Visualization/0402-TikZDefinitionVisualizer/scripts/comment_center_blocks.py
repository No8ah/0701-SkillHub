#!/usr/bin/env python3
import argparse
import pathlib
import re
import sys

BEGIN_CENTER_RE = re.compile(r"^(\s*)\\begin\{center\}\s*$")
END_CENTER_RE = re.compile(r"^(\s*)\\end\{center\}\s*$")
FIG_LABEL_RE = re.compile(r"^(\s*)图示:\s*$")
COMMENTED_RE = re.compile(r"^(\s*)%\s?(.*)$")


def iter_tex_files(path: pathlib.Path):
    if path.is_file() and path.suffix == ".tex":
        yield path
        return
    if path.is_dir():
        for p in sorted(path.rglob("*.tex")):
            if p.is_file():
                yield p


def comment_line(line: str) -> str:
    if COMMENTED_RE.match(line):
        return line
    m = re.match(r"^(\s*)(.*)$", line)
    assert m is not None
    return f"{m.group(1)}% {m.group(2)}"


def uncomment_line(line: str) -> str:
    m = COMMENTED_RE.match(line)
    if not m:
        return line
    return f"{m.group(1)}{m.group(2)}"


def process_lines(lines, mode: str):
    out = list(lines)
    i = 0
    changed = 0

    while i < len(out):
        raw = out[i]
        candidate = uncomment_line(raw)

        m_begin = BEGIN_CENTER_RE.match(candidate)
        if not m_begin:
            i += 1
            continue

        # Find matching end of this center block.
        j = i
        end_idx = -1
        while j < len(out):
            cand_j = uncomment_line(out[j])
            if END_CENTER_RE.match(cand_j):
                end_idx = j
                break
            j += 1

        if end_idx == -1:
            i += 1
            continue

        # Optionally include the closest previous non-empty line if it is 图示:
        start_idx = i
        k = i - 1
        while k >= 0 and out[k].strip() == "":
            k -= 1
        if k >= 0 and FIG_LABEL_RE.match(uncomment_line(out[k])):
            start_idx = k

        for idx in range(start_idx, end_idx + 1):
            original = out[idx]
            updated = comment_line(original) if mode == "comment" else uncomment_line(original)
            if updated != original:
                out[idx] = updated
                changed += 1

        i = end_idx + 1

    return out, changed


def main():
    parser = argparse.ArgumentParser(
        description="Comment/uncomment figure label + center blocks in .tex files."
    )
    parser.add_argument("target", help="Path to a .tex file or directory")
    parser.add_argument("--mode", choices=["comment", "uncomment"], required=True)
    parser.add_argument("--dry-run", action="store_true", help="Only report changes")
    args = parser.parse_args()

    target = pathlib.Path(args.target).expanduser().resolve()
    files = list(iter_tex_files(target))
    if not files:
        print(f"No .tex files found under: {target}")
        return 2

    total_changed = 0
    touched_files = 0

    for tex in files:
        text = tex.read_text(encoding="utf-8")
        lines = text.splitlines()
        new_lines, changed = process_lines(lines, args.mode)
        if changed == 0:
            continue
        touched_files += 1
        total_changed += changed
        print(f"[CHANGED] {tex} ({changed} line(s))")
        if not args.dry_run:
            tex.write_text("\n".join(new_lines) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")

    action = "would change" if args.dry_run else "changed"
    print(f"[OK] {action} {total_changed} line(s) across {touched_files} file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
