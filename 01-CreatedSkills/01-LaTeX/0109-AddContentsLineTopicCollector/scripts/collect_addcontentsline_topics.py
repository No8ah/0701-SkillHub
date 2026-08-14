#!/usr/bin/env python3
"""Collect and normalize \addcontentsline subsubsection topics from TeX files.

Features:
- Collect topics from \addcontentsline{toc}{subsubsection}{...}
- Remove \surd markers and trailing empty math tails (e.g. - $$)
- Optional prefix normalization for patterns like: 第N次作业 - Exercise M
- Deduplicate while preserving first-seen order
- Optional in-place rewrite into the "考点" subsection area
- Optional sync mode: collect topic names from homework TOC entries and add
  purple star subsection headers before matching Notes customproblem blocks.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable, List, NamedTuple, Tuple

KAODIAN_SUBSECTION_RE = re.compile(r"\\subsection\*\{\\textcolor\{blue\}\{考点\}\}")
KAODIAN_TOC_RE = re.compile(r"\\addcontentsline\s*\{toc\}\s*\{subsection\}\s*\{\\textcolor\{blue\}\{考点\}\}")
ADDCONTENTS_PREFIX_RE = re.compile(
    r"\\addcontentsline\s*\{toc\}\s*\{subsubsection\}\s*\{", re.M
)
HW_PREFIX_RE = re.compile(r"^第\d+次作业\s*-\s*Exercise\s*\d+\s*-\s*")
SUBFILE_RE = re.compile(r"\\subfile\{([^}]+)\}")
SUBSECTION_HEADER_RE = re.compile(
    r"(?ms)([ \t]*\\subsection\*\{\\textcolor\{(?:red|blue|purple|black)\}\{.*?\}\}\n"
    r"[ \t]*\\addcontentsline\{toc\}\{subsection\}\{\\textcolor\{(?:red|blue|purple|black)\}\{.*?\}\}\n\n?)$"
)


class TextEdit(NamedTuple):
    start: int
    end: int
    replacement: str
    label: str
    kind: str


def find_matching_brace(text: str, open_brace_idx: int) -> int:
    """Return index of matching '}' for text[open_brace_idx] == '{'."""
    if open_brace_idx >= len(text) or text[open_brace_idx] != "{":
        raise ValueError("open_brace_idx must point to '{'")

    depth = 0
    i = open_brace_idx
    while i < len(text):
        ch = text[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    raise ValueError("Unbalanced braces while parsing addcontentsline")


def find_subsubsection_commands(text: str, start: int = 0, end: int | None = None) -> List[Tuple[int, int, str]]:
    """Find addcontentsline subsubsection commands.

    Returns list of (span_start, span_end, content_inside_braces).
    span_end is exclusive.
    """
    if end is None:
        end = len(text)
    segment = text[start:end]
    out: List[Tuple[int, int, str]] = []
    for m in ADDCONTENTS_PREFIX_RE.finditer(segment):
        global_start = start + m.start()
        open_brace = start + m.end() - 1
        close_brace = find_matching_brace(text, open_brace)

        cmd_end = close_brace + 1
        while cmd_end < len(text) and text[cmd_end] in " \t":
            cmd_end += 1
        if cmd_end < len(text) and text[cmd_end] == "\n":
            cmd_end += 1

        content = text[open_brace + 1 : close_brace]
        out.append((global_start, cmd_end, content))
    return out


def split_toc_tokens(payload: str) -> List[str]:
    """Split TOC payload on top-level ' - ', ignoring delimiters inside $...$."""
    parts: List[str] = []
    buf: List[str] = []
    in_math = False
    escaped = False
    i = 0
    while i < len(payload):
        ch = payload[i]
        if escaped:
            buf.append(ch)
            escaped = False
            i += 1
            continue
        if ch == "\\":
            buf.append(ch)
            escaped = True
            i += 1
            continue
        if ch == "$":
            in_math = not in_math
            buf.append(ch)
            i += 1
            continue
        if not in_math and payload.startswith(" - ", i):
            parts.append("".join(buf).strip())
            buf = []
            i += 3
            continue
        buf.append(ch)
        i += 1
    parts.append("".join(buf).strip())
    return parts


def parse_line_range(spec: str) -> Tuple[int, int]:
    m = re.fullmatch(r"\s*(\d+)\s*[:-]\s*(\d+)\s*", spec)
    if not m:
        raise argparse.ArgumentTypeError("line ranges must look like START:END")
    start, end = int(m.group(1)), int(m.group(2))
    if start <= 0 or end < start:
        raise argparse.ArgumentTypeError("invalid line range")
    return start, end


def slice_line_ranges(text: str, ranges: Iterable[Tuple[int, int]] | None) -> str:
    if not ranges:
        return text
    lines = text.splitlines(keepends=True)
    chunks = []
    for start, end in ranges:
        chunks.append("".join(lines[start - 1 : end]))
    return "".join(chunks)


def extract_homework_topic_names(text: str, ranges: Iterable[Tuple[int, int]] | None = None) -> List[str]:
    """Extract <匹配名称> from homework TOC entries.

    Expected payload shape:
      Page * - Content/T* - <匹配名称> - ...
    """
    segment = slice_line_ranges(text, ranges)
    names: List[str] = []
    for _, _, payload in find_subsubsection_commands(segment):
        tokens = split_toc_tokens(payload)
        if len(tokens) >= 3 and tokens[0].startswith("Page"):
            names.append(tokens[2])
    return dedupe_keep_order([n for n in names if n])


def extract_notes_content_name(payload: str) -> str | None:
    """Extract name from Notes payload: * - * - Content - <name> - *."""
    tokens = split_toc_tokens(payload)
    try:
        idx = tokens.index("Content")
    except ValueError:
        return None
    if idx + 1 >= len(tokens):
        return None
    return tokens[idx + 1]


def subfiles_from_main(main_path: Path, ranges: Iterable[Tuple[int, int]] | None) -> List[Path]:
    text = main_path.read_text(encoding="utf-8")
    segment = slice_line_ranges(text, ranges)
    paths: List[Path] = []
    for m in SUBFILE_RE.finditer(segment):
        p = main_path.parent / m.group(1)
        if p not in paths:
            paths.append(p)
    return paths


def purple_star_header(name: str) -> str:
    return (
        f"\\subsection*{{\\textcolor{{purple}}{{{name} $\\star \\star \\star$}}}}\n"
        f"\\addcontentsline{{toc}}{{subsection}}{{\\textcolor{{purple}}{{{name} $\\star \\star \\star$}}}}\n\n"
    )


def mark_matching_notes_headers(text: str, names: set[str]) -> Tuple[str, List[TextEdit]]:
    """Insert or normalize purple star headers before matching customproblem blocks."""
    edits: List[TextEdit] = []
    for pos, _, payload in find_subsubsection_commands(text):
        name = extract_notes_content_name(payload)
        if not name or name not in names:
            continue

        customproblem_pos = text.rfind("\\customproblem", 0, pos)
        if customproblem_pos < 0:
            continue

        previous_boundary = max(
            text.rfind("\\clearpage", 0, customproblem_pos),
            text.rfind("\\newpage", 0, customproblem_pos),
            text.rfind("\\phantomsection", 0, customproblem_pos),
            text.rfind("\\end{tcolorbox}", 0, customproblem_pos),
        )
        search_start = previous_boundary + 1 if previous_boundary >= 0 else 0
        preamble = text[search_start:customproblem_pos]
        target = purple_star_header(name)

        header_match = SUBSECTION_HEADER_RE.search(preamble)
        if header_match:
            start = search_start + header_match.start(1)
            end = search_start + header_match.end(1)
            if text[start:end] != target:
                edits.append(TextEdit(start, end, target, name, "replace"))
        else:
            edits.append(TextEdit(customproblem_pos, customproblem_pos, target, name, "insert"))

    if not edits:
        return text, []

    unique: List[TextEdit] = []
    seen_spans: set[Tuple[int, int]] = set()
    for edit in edits:
        key = (edit.start, edit.end)
        if key not in seen_spans:
            unique.append(edit)
            seen_spans.add(key)

    new_text = text
    for edit in sorted(unique, key=lambda e: e.start, reverse=True):
        new_text = new_text[: edit.start] + edit.replacement + new_text[edit.end :]

    # Remove immediate duplicate non-purple header that precedes the target header.
    duplicate_before_purple = re.compile(
        r"(?ms)^[ \t]*\\subsection\*\{\\textcolor\{(?:red|blue|black)\}\{([^{}]+)\}\}\n"
        r"[ \t]*\\addcontentsline\{toc\}\{subsection\}\{\\textcolor\{(?:red|blue|black)\}\{\1\}\}\n[ \t]*\n"
        r"(?=[ \t]*\\subsection\*\{\\textcolor\{purple\}\{\1 \$\\star \\star \\star\$\}\})"
    )
    new_text = duplicate_before_purple.sub("", new_text)
    return new_text, unique


def sync_notes_headers(
    source_path: Path,
    source_ranges: List[Tuple[int, int]],
    notes_main: Path,
    notes_ranges: List[Tuple[int, int]],
    check: bool,
) -> int:
    source_text = source_path.read_text(encoding="utf-8")
    names = set(extract_homework_topic_names(source_text, source_ranges))
    subfiles = subfiles_from_main(notes_main, notes_ranges)

    any_changes = False
    print(f"Topics: {len(names)}")
    print(f"Subfiles: {len(subfiles)}")

    for subfile in subfiles:
        if not subfile.exists():
            print(f"[MISSING] {subfile}")
            continue
        text = subfile.read_text(encoding="utf-8")
        new_text, edits = mark_matching_notes_headers(text, names)
        if not edits:
            continue
        any_changes = True
        print(f"[CHANGE] {subfile}")
        for edit in edits:
            print(f"  {edit.kind}: {edit.label}")
        if not check:
            subfile.write_text(new_text, encoding="utf-8")

    if check:
        return 1 if any_changes else 0
    return 0


def normalize_topic(raw: str, prefix: str | None) -> str:
    s = raw
    s = s.replace("\\surd", "")
    s = re.sub(r"\s*[-—]\s*\$\s*\$\s*$", "", s)
    s = re.sub(r"\s*[-—]\s*\$\s+\$\s*$", "", s)
    s = re.sub(r"\s+", " ", s).strip()

    if prefix:
        s = HW_PREFIX_RE.sub(prefix + " - ", s)

    s = re.sub(r"\s*-\s*", " - ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out


def collect_topics(text: str, prefix: str | None) -> List[str]:
    kaodian_anchor = len(text)
    m1 = KAODIAN_SUBSECTION_RE.search(text)
    m2 = KAODIAN_TOC_RE.search(text)
    candidates = [m.start() for m in (m1, m2) if m]
    if candidates:
        kaodian_anchor = min(candidates)

    cmds = find_subsubsection_commands(text, 0, kaodian_anchor)
    topics = [normalize_topic(content, prefix) for _, _, content in cmds]
    topics = [t for t in topics if t]
    return dedupe_keep_order(topics)


def rewrite_kaodian_block(text: str, topics: List[str]) -> str:
    m_toc = KAODIAN_TOC_RE.search(text)
    if not m_toc:
        raise ValueError("未找到考点目录行: \\addcontentsline{toc}{subsection}{\\textcolor{blue}{考点}}")

    insert_pos = m_toc.end()

    end_doc = text.find("\\end{document}", insert_pos)
    if end_doc == -1:
        end_doc = len(text)

    after_anchor = text[insert_pos:end_doc]
    spans = find_subsubsection_commands(after_anchor)

    cleaned_after = after_anchor
    if spans:
        rebuilt = []
        cursor = 0
        for s, e, _ in spans:
            rebuilt.append(after_anchor[cursor:s])
            cursor = e
        rebuilt.append(after_anchor[cursor:])
        cleaned_after = "".join(rebuilt)

    lines = ["", ""]
    for t in topics:
        lines.append(f"\\addcontentsline{{toc}}{{subsubsection}}{{{t}}}")
        lines.append("")
    block = "\n".join(lines)

    return text[:insert_pos] + block + cleaned_after + text[end_doc:]


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect/normalize addcontentsline topics")
    parser.add_argument("--input", required=True, help="Path to input .tex/.md file")
    parser.add_argument("--prefix", default=None, help="Replace '第N次作业 - Exercise M' prefix with this text")
    parser.add_argument("--rewrite", action="store_true", help="Rewrite topics into the 考点 section in place")
    parser.add_argument(
        "--source-lines",
        action="append",
        type=parse_line_range,
        default=[],
        help="Line range START:END in --input used for homework topic-name extraction",
    )
    parser.add_argument("--notes-main", default=None, help="Notes chapter main .tex containing subfile references")
    parser.add_argument(
        "--notes-lines",
        action="append",
        type=parse_line_range,
        default=[],
        help="Line range START:END in --notes-main used to find subfiles",
    )
    parser.add_argument(
        "--mark-notes-headers",
        action="store_true",
        help="Add/normalize purple star subsection headers in Notes subfiles matching homework topics",
    )
    parser.add_argument("--check", action="store_true", help="Preview changes for --mark-notes-headers")
    args = parser.parse_args()

    path = Path(args.input)
    text = path.read_text(encoding="utf-8")

    if args.mark_notes_headers:
        if not args.notes_main:
            parser.error("--mark-notes-headers requires --notes-main")
        return sync_notes_headers(
            source_path=path,
            source_ranges=args.source_lines,
            notes_main=Path(args.notes_main),
            notes_ranges=args.notes_lines,
            check=args.check,
        )

    topics = collect_topics(text, args.prefix)

    if args.rewrite:
        new_text = rewrite_kaodian_block(text, topics)
        path.write_text(new_text, encoding="utf-8")
        print(f"Rewritten: {path}")
        print(f"Topics: {len(topics)}")
    else:
        for t in topics:
            print(f"\\addcontentsline{{toc}}{{subsubsection}}{{{t}}}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
