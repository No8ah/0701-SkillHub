#!/usr/bin/env python3
"""
Toggle homework subsections between commented and uncommented states.

Keeps or restores:
  - Page * - T*  (problem subsections)
  - 第 * 次作业 - Exercise  (homework exercise subsections)

All other subsections are commented out.
"""

import os
import re
import sys


def find_homework_files(root_dir):
    """Find all homework .tex files recursively."""
    tex_files = []
    for dirpath, _, filenames in os.walk(root_dir):
        for f in filenames:
            if f.endswith('.tex') and '_Hw_' in f:
                tex_files.append(os.path.join(dirpath, f))
    return tex_files


def should_keep_subsection(name):
    """Check if a subsection name matches the keep patterns."""
    # Pattern: Page * - T*
    if re.match(r'.*Page\s+\d+\s*-\s*T\d+.*', name):
        return True
    # Pattern: 第 * 次作业 - Exercise
    if re.match(r'.*第\s+\d+\s*次作业\s*-\s*Exercise.*', name):
        return True
    return False


def find_subsections(lines):
    """Find all subsection boundaries.

    Returns list of (start_line, end_line, name, addcontents_start).
    """
    subsections = []
    subsection_starts = []

    for i, line in enumerate(lines):
        stripped = line.strip().lstrip('% ')
        if stripped.startswith(r'\subsection*{'):
            subsection_starts.append(i)

    for idx, start in enumerate(subsection_starts):
        end = subsection_starts[idx + 1] if idx + 1 < len(subsection_starts) else len(lines) - 1

        # Extract name (handle commented lines)
        clean_line = lines[start].lstrip('% ').strip()
        brace_start = clean_line.index('{')
        brace_end = clean_line.rindex('}')
        name = clean_line[brace_start + 1:brace_end]

        # Find preceding addcontentsline
        addcontents_start = start
        for j in range(start - 1, -1, -1):
            stripped_j = lines[j].strip()
            if stripped_j.startswith(r'\addcontentsline{toc}{subsection}'):
                addcontents_start = j
            elif stripped_j == '' or stripped_j.startswith('%'):
                continue
            else:
                break

        subsections.append((start, end, name, addcontents_start))

    return subsections


def toggle_file(filepath, dry_run=False):
    """Toggle subsections in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    subsections = find_subsections(lines)
    changes = []

    for start, end, name, addcontents_start in subsections:
        should_keep = should_keep_subsection(name)

        for i in range(addcontents_start, end):
            line = lines[i]
            stripped = line.strip()

            if should_keep:
                # Restore from commented to uncommented
                if stripped.startswith('%') and len(stripped) > 1:
                    # Find the first % that isn't part of %%
                    content = stripped.lstrip()
                    if content.startswith('% ') or content.startswith('%\\'):
                        new_line = line.replace('% ', '', 1) if '% ' in line else line.replace('%', '', 1)
                        if line != new_line:
                            changes.append((i, line, new_line))
                            if not dry_run:
                                lines[i] = new_line
                    elif content.startswith('%') and not content.startswith('%%'):
                        new_line = line.replace('%', '', 1)
                        if line != new_line:
                            changes.append((i, line, new_line))
                            if not dry_run:
                                lines[i] = new_line
            else:
                # Comment out
                if not stripped.startswith('%') and stripped:
                    # Don't comment out addcontentsline for subsubsection (they're finer-grained)
                    if stripped.startswith(r'\addcontentsline{toc}{subsubsection}'):
                        continue
                    # Don't comment out phantomsection labels
                    if stripped.startswith(r'\phantomsection'):
                        continue
                    new_line = '% ' + line
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
        description='Toggle homework subsections: keep Page T* and Exercise, comment others'
    )
    parser.add_argument('path', nargs='?', default=None,
                        help='File or directory path. Default: homework root for Ch10.')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show planned changes without modifying files')
    parser.add_argument('--uncomment-only', '-u', action='store_true',
                        help='Only uncomment kept subsections, do not comment others')

    args = parser.parse_args()

    # Default path
    path = args.path
    if path is None:
        path = "/Users/quzinan/Downloads/Code/study/Optimization_Method/Hw/Chapter10_OM_Hw_约束优化最优性条件"

    if os.path.isfile(path):
        files = [path]
    elif os.path.isdir(path):
        files = find_homework_files(path)
    else:
        print(f"Error: path not found: {path}", file=sys.stderr)
        sys.exit(1)

    total_changes = 0
    for filepath in sorted(files):
        print(f"\n{'=' * 60}")
        print(f"File: {os.path.relpath(filepath, os.path.commonpath(files))}")
        changes = toggle_file(filepath, dry_run=args.dry_run)

        if not changes:
            print("  No changes needed.")
            continue

        # Group by subsection
        kept = [c for c in changes if c[1].strip().startswith('%')]
        commented = [c for c in changes if not c[1].strip().startswith('%')]

        if kept:
            print(f"  Restored: {len(kept)} lines uncommented")
        if commented:
            print(f"  Commented: {len(commented)} lines")

        total_changes += len(changes)

        if args.dry_run:
            print(f"  Planned changes: {len(changes)}")
            for lineno, old, new in changes[:5]:
                print(f"    L{lineno + 1}: {old.rstrip()[:60]} -> {new.rstrip()[:60]}")
            if len(changes) > 5:
                print(f"    ... and {len(changes) - 5} more")

    summary_action = "dry-run" if args.dry_run else "applied"
    print(f"\n{'=' * 60}")
    print(f"Total: {total_changes} line changes {summary_action} across {len(files)} files.")


if __name__ == '__main__':
    main()
