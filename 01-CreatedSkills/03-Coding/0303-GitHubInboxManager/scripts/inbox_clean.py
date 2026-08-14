#!/usr/bin/env python3
"""Clean Zotero README Inbox blocks: keep listed items, remove archived ones.

Usage:
    python3 inbox_clean.py <path-to-README.tex> '["item1","item2",...]'

The keep-list is items that were NOT archived (not found on GitHub,
arXiv/DOI IDs, or intentionally kept). Everything else in the Inbox
sections is removed. Section headings (Project_Inbox, Skill_Inbox,
MCP_Inbox, Website_Inbox, arXiv_Inbox, DOI_Inbox) are always kept.
"""
import json, sys

def main():
    if len(sys.argv) < 3:
        print("Usage: inbox_clean.py <tex-file> '<keep-json-list>'")
        sys.exit(1)

    path = sys.argv[1]
    keep = json.loads(sys.argv[2])

    with open(path) as f:
        lines = f.readlines()

    # Locate the Inbox block: from Project\_Inbox to end of DOI\_Inbox content
    start = None
    end = None
    for i, l in enumerate(lines):
        if 'Project\\_Inbox' in l:
            start = i
        if 'DOI\\_Inbox' in l:
            end = i + 2  # heading + blank + item line

    if start is None or end is None:
        print("✗ Inbox 块未找到")
        sys.exit(1)

    # Parse the existing block into sections
    block = lines[start:end+1]
    sections = {}      # heading -> list of items
    order = []
    cur = None
    for l in block:
        s = l.strip()
        if s.endswith('_Inbox') or s.endswith('\\_Inbox'):
            cur = s
            sections[cur] = []
            order.append(cur)
        elif s and cur and not s.startswith('\\'):
            sections[cur].append(s)

    # Rebuild with keep-list filter
    def build_section(title, items):
        if items:
            return [title + '\n', '\n'] + [f'{it}\n' for it in items] + ['\n']
        return [title + '\n', '\n', '\n']

    new_block = []
    for title in order:
        kept = [it for it in sections[title] if it in keep]
        new_block += build_section(title, kept)

    # Also append any keep items whose section didn't exist (e.g. new headings)
    kept_any = set()
    for v in sections.values():
        kept_any.update(v)
    leftover = [k for k in keep if k not in kept_any]
    if leftover:
        print(f"⚠ 以下保留项不在现有 Inbox 中: {leftover}")

    lines = lines[:start] + new_block + ['\n'] + lines[end+1:]

    with open(path, 'w') as f:
        f.writelines(lines)

    removed = sum(len(v) for v in sections.values()) - sum(
        len([it for it in v if it in keep]) for v in sections.values())
    print(f"✓ Inbox 清理完成: 保留 {len(keep)} 项, 删除 {removed} 项")

if __name__ == '__main__':
    main()
