#!/usr/bin/env python3
"""
Comment or uncomment subsection units based on \surd marker.

A "unit" spans from a `\subsection*{...}` to the next, including its
preceding `\addcontentsline{toc}{subsection}`, `\clearpage`, and `\newpage`,
but NOT content before `% Content` (the header/TOC area).

If the first `\addcontentsline{toc}{subsubsection}` after `\customproblem`
contains `$\surd$`, the unit is toggled. Units without `$\surd$` are left
untouched.
"""

import os
import re
import sys


def find_content_start(lines):
    """Find the line index of % Content marker (1-indexed)."""
    for i, line in enumerate(lines):
        if line.strip() == '% Content':
            return i + 1  # content starts after this line
        if i > 0 and line.strip().startswith(r'\subsection*{'):
            return i
    return 0


def find_subsection_starts(lines):
    """Find line indices of all subsection starts (commented or not)."""
    starts = []
    for i, line in enumerate(lines):
        clean = line.lstrip('% ').strip()
        if clean.startswith(r'\subsection*{'):
            starts.append(i)
    return starts


def process_file(filepath, mode='comment', dry_run=False):
    """Process a single file: comment or uncomment surd-marked units.

    mode: 'comment' (default) or 'uncomment'
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    content_start = find_content_start(lines)
    starts = find_subsection_starts(lines)
    changes = []

    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(lines) - 1

        # Check first \addcontentsline after \customproblem for $\surd$
        has_surd = False
        custom_found = False
        for j in range(start, end):
            s = lines[j].strip()
            if r'\customproblem' in s:
                custom_found = True
            if custom_found and s.startswith(r'\addcontentsline{toc}{subsubsection}'):
                has_surd = r'$\surd$' in s
                break

        if not has_surd:
            continue

        # Extend start backward to include addcontentsline/clearpage/newpage,
        # but stop at content_start (header/TOC area)
        unit_start = start
        for j in range(start - 1, content_start - 1, -1):
            s = lines[j].strip()
            if s.startswith(r'\addcontentsline{toc}{subsection}') or \
               s.startswith(r'\clearpage') or s.startswith(r'\newpage'):
                unit_start = j
            elif s == '' or s.startswith('%'):
                continue
            else:
                break

        for i in range(unit_start, end):
            line = lines[i]
            s = line.strip()

            if mode == 'comment':
                if s and not s.startswith('%'):
                    new_line = '% ' + line
                    if new_line != line:
                        changes.append((i, line, new_line))
                        if not dry_run:
                            lines[i] = new_line
            elif mode == 'uncomment':
                if s.startswith('%') and not s.startswith('%%'):
                    rest = s
                    while rest.startswith('%'):
                        rest = rest[1:]
                        if rest.startswith(' '):
                            rest = rest[1:]
                    indent = line[:len(line) - len(s)]
                    new_line = indent + rest
                    if new_line != line:
                        changes.append((i, line, new_line))
                        if not dry_run:
                            lines[i] = new_line

    if not dry_run and changes:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(lines)

    return changes


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Toggle \\surd-marked subsection units in homework files'
    )
    parser.add_argument('path', nargs='?', default=None,
                        help='File or directory path. Default: Chapter 10 homework root')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Preview changes without modifying files')
    parser.add_argument('--uncomment', '-u', action='store_true',
                        help='Uncomment surd-marked units (default: comment them out)')
    args = parser.parse_args()

    path = args.path
    if path is None:
        path = "/Users/quzinan/Downloads/Code/study/Optimization_Method/Hw/Chapter10_OM_Hw_约束优化最优性条件"

    if os.path.isfile(path):
        files = [path]
    elif os.path.isdir(path):
        files = []
        for dirpath, _, filenames in os.walk(path):
            for f in filenames:
                if f.endswith('.tex') and '_Hw_' in f:
                    files.append(os.path.join(dirpath, f))
    else:
        print(f"Error: path not found: {path}", file=sys.stderr)
        sys.exit(1)

    mode = 'uncomment' if args.uncomment else 'comment'
    total_changes = 0

    for filepath in sorted(files):
        rel = os.path.relpath(filepath, os.path.commonpath(files) if len(files) > 1 else os.path.dirname(path))
        print(f"\n{'=' * 60}")
        print(f"File: {rel}")

        try:
            changes = process_file(filepath, mode=mode, dry_run=args.dry_run)
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        if not changes:
            print("  No changes needed.")
            continue

        print(f"  {len(changes)} lines {'to be' if args.dry_run else ''} {'uncommented' if args.uncomment else 'commented'}")
        if args.dry_run and changes:
            for lineno, old, new in changes[:5]:
                print(f"    L{lineno+1}: {old.rstrip()[:60]} -> {new.rstrip()[:60]}")
            if len(changes) > 5:
                print(f"    ... and {len(changes)-5} more")

        total_changes += len(changes)

    action = "dry-run" if args.dry_run else "applied"
    print(f"\n{'=' * 60}")
    print(f"Total: {total_changes} line changes {action} ({'uncomment' if args.uncomment else 'comment'}) across {len(files)} files.")


if __name__ == '__main__':
    main()
