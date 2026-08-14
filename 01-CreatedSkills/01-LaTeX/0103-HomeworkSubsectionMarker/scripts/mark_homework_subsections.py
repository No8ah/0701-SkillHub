#!/usr/bin/env python3
"""Mark lecture subsections referenced by homework TOC entries."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


SKIP_MARKERS = (r"\surd", r"\times")
STAR = r"$\star \star \star$"


@dataclass(frozen=True)
class HomeworkEntry:
    file: Path
    title: str


@dataclass(frozen=True)
class Subsection:
    file: Path
    title: str
    start: int
    end: int


def normalize_tex_title(text: str) -> str:
    text = re.sub(r"%.*", "", text)
    text = re.sub(r"\\(?:mathrm|mathsf|mathbf|boldsymbol|textcolor)\s*\{([^{}]*)\}", r"\1", text)
    text = re.sub(r"\\[a-zA-Z]+", "", text)
    text = text.replace("{", "").replace("}", "")
    text = text.replace("$", "")
    text = re.sub(r"\s+", "", text)
    text = text.replace("（", "(").replace("）", ")")
    return text


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def balanced_argument(text: str, open_brace: int) -> tuple[str, int] | None:
    if open_brace >= len(text) or text[open_brace] != "{":
        return None
    depth = 0
    escaped = False
    for idx in range(open_brace, len(text)):
        char = text[idx]
        if escaped:
            escaped = False
            continue
        if char == "\\":
            escaped = True
            continue
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[open_brace + 1 : idx], idx + 1
    return None


def iter_latex_command_args(text: str, command: str) -> list[tuple[int, int, list[str]]]:
    out: list[tuple[int, int, list[str]]] = []
    pos = 0
    needle = "\\" + command
    while True:
        start = text.find(needle, pos)
        if start < 0:
            break
        idx = start + len(needle)
        args: list[str] = []
        ok = True
        while idx < len(text) and text[idx].isspace():
            idx += 1
        while idx < len(text) and text[idx] == "{":
            parsed = balanced_argument(text, idx)
            if parsed is None:
                ok = False
                break
            arg, idx = parsed
            args.append(arg)
            while idx < len(text) and text[idx].isspace():
                idx += 1
        if ok:
            out.append((start, idx, args))
        pos = max(idx, start + len(needle))
    return out


def resolve_subfile(parent: Path, raw: str) -> Path:
    raw = raw.strip()
    candidate = Path(raw)
    if candidate.suffix != ".tex":
        candidate = candidate.with_suffix(".tex")
    if not candidate.is_absolute():
        candidate = parent.parent / candidate
    return candidate.resolve()


def is_homework_root_tex(path: Path) -> bool:
    name = path.name
    return (
        path.suffix == ".tex"
        and name.startswith("Chapter")
        and "_Hw_" in name
    )


def is_canonical_homework_root(path: Path) -> bool:
    return is_homework_root_tex(path) and path.stem == path.parent.name


def discover_homework_roots(target: Path) -> list[Path]:
    target = target.resolve()
    roots: list[Path] = []
    seen: set[Path] = set()

    def add(path: Path, require_canonical: bool) -> None:
        path = path.resolve()
        if not path.exists() or path in seen:
            return
        if require_canonical and not is_canonical_homework_root(path):
            return
        if is_homework_root_tex(path):
            seen.add(path)
            roots.append(path)

    if target.is_file():
        # Keep single-file mode backward compatible: allow section-level homework files.
        add(target, require_canonical=False)
        return sorted(roots)

    if not target.is_dir():
        return []

    # Course lecture root mode: .../study/<LectureCourse>
    hw_dir = target / "Hw"
    scan_root = hw_dir if hw_dir.is_dir() else target
    for candidate in sorted(scan_root.rglob("Chapter*_Hw_*.tex")):
        add(candidate, require_canonical=True)
    return sorted(roots)


def collect_tex_subfiles(root: Path, hw_mode: bool) -> list[Path]:
    seen: set[Path] = set()
    ordered: list[Path] = []

    def visit(path: Path) -> None:
        path = path.resolve()
        if path in seen or not path.exists():
            return
        seen.add(path)
        if path.name.endswith(".tex") and (not hw_mode or "_Hw_" in path.name):
            ordered.append(path)
        text = read_text(path)
        for _, _, args in iter_latex_command_args(text, "subfile"):
            if args:
                visit(resolve_subfile(path, args[0]))

    visit(root)
    return ordered


def extract_homework_entries(files: list[Path]) -> list[HomeworkEntry]:
    entries: list[HomeworkEntry] = []
    for file in files:
        text = read_text(file)
        for _, _, args in iter_latex_command_args(text, "addcontentsline"):
            if len(args) != 3:
                continue
            _, level, title = args
            if level != "subsubsection":
                continue
            if any(marker in title for marker in SKIP_MARKERS):
                continue
            entries.append(HomeworkEntry(file, " ".join(title.split())))
    return entries


def infer_notes_file(hw_file: Path) -> Path | None:
    parts = list(hw_file.parts)
    try:
        idx = parts.index("Hw")
    except ValueError:
        return None
    parts[idx] = "Notes"
    note = Path(*parts)
    note = Path(str(note).replace("_Hw_", "_"))
    return note if note.exists() else None


def collect_notes_files(hw_files: list[Path], explicit_notes_root: Path | None) -> list[Path]:
    if explicit_notes_root:
        return collect_tex_subfiles(explicit_notes_root, hw_mode=False)
    notes: list[Path] = []
    seen: set[Path] = set()
    for hw_file in hw_files:
        note = infer_notes_file(hw_file)
        if note and note not in seen:
            for subfile in collect_tex_subfiles(note, hw_mode=False):
                if subfile not in seen:
                    seen.add(subfile)
                    notes.append(subfile)
    return notes


def extract_subsection_title(block: str) -> str | None:
    marker = r"\textcolor"
    idx = block.find(marker)
    if idx < 0:
        return None
    args = iter_latex_command_args(block[idx:], "textcolor")
    if not args or len(args[0][2]) < 2:
        return None
    return " ".join(args[0][2][1].split())


def extract_subsections(files: list[Path]) -> list[Subsection]:
    subsections: list[Subsection] = []
    for file in files:
        text = read_text(file)
        for start, end, args in iter_latex_command_args(text, "subsection*"):
            if len(args) != 1:
                continue
            title = extract_subsection_title(text[start:end])
            if title:
                subsections.append(Subsection(file, title, start, end))
    return subsections


def referenced_subsections(entries: list[HomeworkEntry], subsections: list[Subsection]) -> set[Subsection]:
    normalized_entries = [(entry, normalize_tex_title(entry.title)) for entry in entries]
    selected: set[Subsection] = set()
    for subsection in subsections:
        title_norm = normalize_tex_title(subsection.title)
        if not title_norm:
            continue
        for _, entry_norm in normalized_entries:
            if title_norm in entry_norm:
                selected.add(subsection)
                break
    return selected


def mark_title(title: str) -> str:
    clean = title.strip()
    if r"\star \star \star" in clean:
        return clean
    return f"{clean} {STAR}"


def mark_file(path: Path, targets: set[str], write: bool) -> int:
    text = read_text(path)
    original = text
    replacements = 0

    for command in ("subsection*", "addcontentsline"):
        spans = iter_latex_command_args(text, command)
        for start, end, args in reversed(spans):
            if command == "addcontentsline":
                if len(args) != 3 or args[1] != "subsection":
                    continue
                block = text[start:end]
            else:
                if len(args) != 1:
                    continue
                block = text[start:end]
            title = extract_subsection_title(block)
            if title is None or normalize_tex_title(title) not in targets:
                continue
            marked = mark_title(title)
            block2 = block.replace(r"\textcolor{blue}", r"\textcolor{purple}", 1)
            block2 = block2.replace("{" + title + "}", "{" + marked + "}", 1)
            if block2 != block:
                text = text[:start] + block2 + text[end:]
                replacements += 1

    if write and text != original:
        path.write_text(text, encoding="utf-8")
    return replacements


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "homework_tex",
        type=Path,
        help=(
            "Homework chapter root .tex, or a lecture-course directory that "
            "contains Hw/ and Notes/ (batch mode)"
        ),
    )
    parser.add_argument("--notes-root", type=Path, help="Optional notes root .tex or notes directory")
    parser.add_argument("--homework-root", type=Path, help="Optional override for homework root/file or course dir")
    parser.add_argument("--lecture", help="Accepted for prompt compatibility; path inference usually handles this")
    parser.add_argument("--write", action="store_true", help="Write changes. Default is dry-run.")
    args = parser.parse_args()

    discover_from = (args.homework_root or args.homework_tex).resolve()
    homework_roots = discover_homework_roots(discover_from)
    if not homework_roots:
        print(f"no Chapter*_Hw_*.tex found from: {discover_from}")
        return 1

    print(f"homework roots: {len(homework_roots)}")

    target_norms_by_file: dict[Path, set[str]] = {}
    titles_by_file: dict[Path, set[str]] = {}
    total_hw_files = 0
    total_entries = 0
    total_notes_files = 0
    total_matched = 0

    explicit_notes_root = args.notes_root.resolve() if args.notes_root else None

    for hw_root in homework_roots:
        hw_files = collect_tex_subfiles(hw_root, hw_mode=True)
        entries = extract_homework_entries(hw_files)
        notes_files = collect_notes_files(hw_files, explicit_notes_root)
        subsections = extract_subsections(notes_files)
        selected = referenced_subsections(entries, subsections)

        total_hw_files += len(hw_files)
        total_entries += len(entries)
        total_notes_files += len(notes_files)
        total_matched += len(selected)

        print(f"\n[{hw_root}]")
        print(f"  homework files: {len(hw_files)}")
        print(f"  homework entries without check/cross: {len(entries)}")
        print(f"  notes files: {len(notes_files)}")
        print(f"  matched subsections: {len(selected)}")

        for item in selected:
            norm = normalize_tex_title(item.title)
            target_norms_by_file.setdefault(item.file, set()).add(norm)
            titles_by_file.setdefault(item.file, set()).add(item.title)

    print(f"\nsummary:")
    print(f"  homework files: {total_hw_files}")
    print(f"  homework entries without check/cross: {total_entries}")
    print(f"  notes files: {total_notes_files}")
    print(f"  matched subsections: {total_matched}")

    for file in sorted(titles_by_file):
        print(f"\n{file}")
        for title in sorted(titles_by_file[file]):
            print(f"  - {title}")

    total = 0
    for file in sorted(target_norms_by_file):
        count = mark_file(file, target_norms_by_file[file], args.write)
        total += count
    mode = "changed" if args.write else "would change"
    print(f"\n{mode}: {total} title occurrences")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
