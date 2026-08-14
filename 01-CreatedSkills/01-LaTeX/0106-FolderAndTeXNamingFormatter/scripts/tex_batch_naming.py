#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional


SECTION_DIR_RE = re.compile(r"^Section(?P<num>\d+)(?:_(?P<title>.+))?$")
SUBSECTION_DIR_RE = re.compile(r"^Subsection(?P<num>\d+)?(?:_(?P<title>.+))?$")
CHAPTER_DIR_RE = re.compile(r"^Chapter(?P<num>\d+)(?:_(?P<title>.+))?$")

MAIN_TEX_RE = re.compile(
    r"^Chapter(?P<chap>\d+)_Sc(?P<sec>\d+)_"
    r"(?P<code>[A-Za-z0-9]+)"
    r"(?:_(?P<title>.+))?\.tex$"
)


@dataclass(frozen=True)
class RenameOp:
    src: str
    dst: str
    kind: str  # "path" or "text"
    detail: str = ""


def _read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def _write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8")


def _strip_tex_wrappers(s: str) -> str:
    """
    Best-effort extraction of plain title text from simple wrappers like:
      \\textcolor{red}{TITLE}
      \\textbf{TITLE}
    """
    s = s.strip()
    while True:
        m = re.match(r"^\\textcolor\{[^}]*\}\{(.+)\}$", s)
        if m:
            s = m.group(1).strip()
            continue
        m = re.match(r"^\\textbf\{(.+)\}$", s)
        if m:
            s = m.group(1).strip()
            continue
        break
    s = re.sub(r"\s+", " ", s).strip()
    return s


def infer_title_from_tex(tex_path: Path) -> Optional[str]:
    """
    Deterministically infer a "Section title" from a LaTeX file by:
      1) Title block: {\\Huge \\textbf{...}} -> take last ' - ' fragment
      2) First \\section*{...} heading -> strip simple wrappers
    Returns None if inference fails.
    """
    text = _read_text(tex_path)

    # 1) Title block
    m = re.search(r"\{\\Huge\s+\\textbf\{([^}]*)\}\}", text)
    if m:
        title_line = m.group(1).strip()
        parts = [p.strip() for p in title_line.split(" - ") if p.strip()]
        if len(parts) >= 3:
            return parts[-1]

    # 2) First section heading
    m = re.search(r"\\section\*\{([^}]*)\}", text)
    if m:
        return _strip_tex_wrappers(m.group(1))

    return None


def infer_chapter_title_candidate_from_tex(tex_path: Path, chapter_num: str) -> Optional[str]:
    """
    Deterministically infer a chapter title candidate from:
      {\\Huge \\textbf{ChapterN - 章标题 - 小节标题}}
    Returns the middle fragment (章标题) when available.
    """
    text = _read_text(tex_path)
    m = re.search(r"\{\\Huge\s+\\textbf\{([^}]*)\}\}", text)
    if not m:
        return None
    title_line = m.group(1).strip()
    parts = [p.strip() for p in title_line.split(" - ") if p.strip()]
    if len(parts) < 3:
        return None
    if not parts[0].startswith(f"Chapter{chapter_num}"):
        return None
    return parts[1]


def infer_course_code(root: Path) -> Optional[str]:
    codes: list[str] = []
    for tex in root.rglob("*.tex"):
        if "Set" in tex.parts or "Template" in tex.parts:
            continue
        m = MAIN_TEX_RE.match(tex.name)
        if m:
            codes.append(m.group("code"))
    if not codes:
        return None
    # most common
    return max(set(codes), key=codes.count)


def iter_section_dirs(chapter_dir: Path) -> Iterable[Path]:
    for child in chapter_dir.iterdir():
        if not child.is_dir():
            continue
        if SECTION_DIR_RE.match(child.name):
            yield child


def _find_main_tex(section_dir: Path, chapter_num: str, section_num: str) -> Optional[Path]:
    candidates: list[Path] = []
    for tex in section_dir.glob("*.tex"):
        m = MAIN_TEX_RE.match(tex.name)
        if not m:
            continue
        if m.group("chap") == chapter_num and m.group("sec") == section_num:
            candidates.append(tex)
    if not candidates:
        return None
    candidates.sort(key=lambda p: (len(p.name), p.name))
    return candidates[0]


def plan_renames(
    root: Path,
    course_code: Optional[str],
    include_subsections: bool,
    include_chapters: bool,
    chapter_min_count: int,
    update_headers: bool,
) -> list[RenameOp]:
    ops: list[RenameOp] = []

    inferred_code = course_code or infer_course_code(root)

    for chapter_dir in sorted(root.glob("Chapter*")):
        if not chapter_dir.is_dir():
            continue
        chap_m = CHAPTER_DIR_RE.match(chapter_dir.name)
        if not chap_m:
            continue
        chapter_num = chap_m.group("num")
        chapter_title_existing = chap_m.group("title")

        chapter_title_inferred: Optional[str] = None
        if include_chapters and chapter_title_existing is None:
            chapter_title_inferred = infer_chapter_title_for_chapter(
                chapter_dir=chapter_dir,
                chapter_num=chapter_num,
                chapter_min_count=chapter_min_count,
            )

        chapter_dst_dir = chapter_dir
        if include_chapters and chapter_title_existing is None and chapter_title_inferred:
            chapter_dst_dir = chapter_dir.with_name(f"Chapter{chapter_num}_{chapter_title_inferred}")
            if chapter_dst_dir != chapter_dir:
                ops.append(RenameOp(str(chapter_dir), str(chapter_dst_dir), "path", "chapter_dir"))

        for section_dir in sorted(iter_section_dirs(chapter_dir), key=lambda p: p.name):
            original_section_dir = section_dir
            m = SECTION_DIR_RE.match(section_dir.name)
            assert m
            section_num = m.group("num")
            existing_title = m.group("title")

            main_tex_original = _find_main_tex(section_dir, chapter_num, section_num)
            inferred_title = existing_title
            if not inferred_title and main_tex_original:
                inferred_title = infer_title_from_tex(main_tex_original)

            effective_section_dir = original_section_dir
            effective_main_tex = main_tex_original

            # Rename section folder if it is plain "SectionN"
            if existing_title is None and inferred_title:
                dst_dir = original_section_dir.with_name(f"Section{section_num}_{inferred_title}")
                if dst_dir != original_section_dir:
                    ops.append(RenameOp(str(original_section_dir), str(dst_dir), "path", "section_dir"))
                    effective_section_dir = dst_dir
                    if main_tex_original:
                        effective_main_tex = dst_dir / main_tex_original.name

            # Rename main tex if missing suffix title
            if main_tex_original and effective_main_tex:
                tex_m = MAIN_TEX_RE.match(main_tex_original.name)
                assert tex_m
                code = tex_m.group("code")
                title_in_name = tex_m.group("title")

                if inferred_code and code != inferred_code:
                    # Keep per-file code; do not rewrite.
                    pass

                if title_in_name is None and inferred_title:
                    new_name = f"Chapter{chapter_num}_Sc{section_num}_{code}_{inferred_title}.tex"
                    dst_tex = effective_main_tex.with_name(new_name)
                    if dst_tex != effective_main_tex:
                        ops.append(RenameOp(str(effective_main_tex), str(dst_tex), "path", "main_tex"))

                        if update_headers:
                            final_tex = _final_path_after_chapter_rename(
                                chapter_src_dir=chapter_dir,
                                chapter_dst_dir=chapter_dst_dir,
                                tex_path_in_chapter_src=dst_tex,
                            )
                            ops.extend(plan_header_updates(main_tex_original, final_tex, new_name))

                elif update_headers:
                    # Even if filename unchanged, header PATH might need sync after folder rename.
                    final_tex = _final_path_after_chapter_rename(
                        chapter_src_dir=chapter_dir,
                        chapter_dst_dir=chapter_dst_dir,
                        tex_path_in_chapter_src=effective_main_tex,
                    )
                    ops.extend(plan_header_updates(main_tex_original, final_tex, main_tex_original.name))

            if include_subsections:
                ops.extend(
                    plan_subsections(
                        effective_section_dir,
                        update_headers,
                        chapter_src_dir=chapter_dir,
                        chapter_dst_dir=chapter_dst_dir,
                    )
                )

    return ops


def infer_chapter_title_for_chapter(chapter_dir: Path, chapter_num: str, chapter_min_count: int) -> Optional[str]:
    candidates: dict[str, int] = {}
    for tex in chapter_dir.rglob("*.tex"):
        if "Set" in tex.parts or "Template" in tex.parts:
            continue
        m = MAIN_TEX_RE.match(tex.name)
        if not m or m.group("chap") != chapter_num:
            continue
        cand = infer_chapter_title_candidate_from_tex(tex, chapter_num)
        if not cand:
            continue
        candidates[cand] = candidates.get(cand, 0) + 1

    if not candidates:
        return None

    best_count = max(candidates.values())
    if best_count < chapter_min_count:
        return None

    best_titles = sorted([t for t, c in candidates.items() if c == best_count])
    return best_titles[0] if best_titles else None


def _final_path_after_chapter_rename(chapter_src_dir: Path, chapter_dst_dir: Path, tex_path_in_chapter_src: Path) -> Path:
    """
    Given a path that is (planned to be) inside the original chapter directory, map it to the
    final path after an optional chapter directory rename.
    """
    if chapter_src_dir == chapter_dst_dir:
        return tex_path_in_chapter_src
    rel = tex_path_in_chapter_src.relative_to(chapter_src_dir)
    return chapter_dst_dir / rel


def plan_subsections(
    section_dir: Path,
    update_headers: bool,
    *,
    chapter_src_dir: Optional[Path] = None,
    chapter_dst_dir: Optional[Path] = None,
) -> list[RenameOp]:
    ops: list[RenameOp] = []
    for child in sorted(section_dir.iterdir(), key=lambda p: p.name):
        if not child.is_dir():
            continue
        m = SUBSECTION_DIR_RE.match(child.name)
        if not m:
            continue
        title = m.group("title")
        if title is None:
            # try infer from tex file with same base name
            tex = child / f"{child.name}.tex"
            if tex.exists():
                title = infer_title_from_tex(tex)
        if title and "_" not in child.name:
            # Subsection -> Subsection_标题 (keep optional numeric)
            prefix = "Subsection" + (m.group("num") or "")
            dst = child.with_name(f"{prefix}_{title}")
            if dst != child:
                ops.append(RenameOp(str(child), str(dst), "path", "subsection_dir"))
                child = dst
        if update_headers:
            for tex in child.glob("*.tex"):
                target_tex = tex
                if chapter_src_dir and chapter_dst_dir:
                    target_tex = _final_path_after_chapter_rename(chapter_src_dir, chapter_dst_dir, tex)
                ops.extend(plan_header_updates(tex, target_tex, tex.name))
    return ops


def plan_header_updates(src_tex_path: Path, target_tex_path: Path, expected_filename: str) -> list[RenameOp]:
    """
    Create text operations to update % FILE: and % PATH: lines if present.
    Only updates those lines; leaves the rest untouched.
    """
    ops: list[RenameOp] = []
    if not src_tex_path.exists():
        return ops

    try:
        text = _read_text(src_tex_path)
    except OSError:
        return ops

    file_line_re = re.compile(r"^(%+\s*FILE:\s*)(.+?)\s*$", re.MULTILINE)
    path_line_re = re.compile(r"^(%+\s*PATH:\s*)(.+?)\s*$", re.MULTILINE)

    new_text = text
    changed = False

    m = file_line_re.search(new_text)
    if m and m.group(2) != expected_filename:
        new_text = file_line_re.sub(rf"\\1{expected_filename}", new_text, count=1)
        changed = True

    m = path_line_re.search(new_text)
    if m:
        old_path = m.group(2)
        # Preserve style: only update when looks like an absolute path.
        if old_path.startswith("/"):
            new_path = str(target_tex_path.parent.resolve()) + "/"
            if old_path != new_path:
                new_text = path_line_re.sub(lambda mm: mm.group(1) + new_path, new_text, count=1)
                changed = True

    if changed:
        ops.append(RenameOp(str(target_tex_path), new_text, "text", "header_sync"))
    return ops


def apply_ops(ops: list[RenameOp], dry_run: bool) -> dict:
    """
    Apply path renames first (deepest paths first), then text updates.
    Return a manifest suitable for undo.
    """
    path_ops = [op for op in ops if op.kind == "path"]
    text_ops = [op for op in ops if op.kind == "text"]

    section_dir_ops = [op for op in path_ops if op.detail in ("section_dir", "subsection_dir")]
    chapter_dir_ops = [op for op in path_ops if op.detail == "chapter_dir"]
    file_ops = [op for op in path_ops if op.detail == "main_tex"]

    # Rename section/subsection dirs first (inner dirs first), then files, then chapter dirs.
    section_dir_ops.sort(key=lambda op: op.src.count(os.sep), reverse=True)
    file_ops.sort(key=lambda op: op.src.count(os.sep))
    chapter_dir_ops.sort(key=lambda op: op.src.count(os.sep), reverse=True)

    manifest = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "ops": [],
    }

    for op in section_dir_ops:
        src = Path(op.src)
        dst = Path(op.dst)
        if dry_run:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        manifest["ops"].append({"kind": "path", "src": op.src, "dst": op.dst})

    for op in file_ops:
        src = Path(op.src)
        dst = Path(op.dst)
        if dry_run:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        manifest["ops"].append({"kind": "path", "src": op.src, "dst": op.dst})

    for op in chapter_dir_ops:
        src = Path(op.src)
        dst = Path(op.dst)
        if dry_run:
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)
        manifest["ops"].append({"kind": "path", "src": op.src, "dst": op.dst})

    for op in text_ops:
        path = Path(op.src)
        if dry_run:
            continue
        before = _read_text(path)
        after = op.dst
        _write_text(path, after)
        manifest["ops"].append({"kind": "text", "path": op.src, "before": before, "after": after})

    return manifest


def undo_manifest(manifest_path: Path, dry_run: bool) -> None:
    manifest = json.loads(_read_text(manifest_path))
    ops = manifest.get("ops", [])
    # undo in reverse order
    for op in reversed(ops):
        if op["kind"] == "text":
            if dry_run:
                print(f"UNDO-EDIT: {op['path']}")
                continue
            _write_text(Path(op["path"]), op["before"])
        elif op["kind"] == "path":
            src = Path(op["src"])
            dst = Path(op["dst"])
            if dry_run:
                print(f"UNDO-RENAME: {dst} -> {src}")
                continue
            if dst.exists():
                dst.rename(src)


def print_plan(ops: list[RenameOp]) -> None:
    if not ops:
        print("No changes planned.")
        return
    for op in ops:
        if op.kind == "path":
            print(f"RENAME: {op.src} -> {op.dst} [{op.detail}]")
        else:
            print(f"EDIT:   {op.src} [{op.detail}]")


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Batch-rename Section folders and main Chapter*_Sc* LaTeX notes to a consistent convention."
    )
    parser.add_argument("root", type=Path, help="Course root folder (e.g. Lecture/.../Numerical Methods...)")
    parser.add_argument("--course-code", help="Force course code (e.g. NMSDE, OM). Otherwise inferred.")
    parser.add_argument(
        "--no-include-chapters",
        dest="include_chapters",
        action="store_false",
        default=True,
        help="Disable Chapter folder renames (default: enabled).",
    )
    parser.add_argument(
        "--chapter-min-count",
        type=int,
        default=2,
        help="Minimum count threshold for chapter title inference (default: 2).",
    )
    parser.add_argument("--include-subsections", action="store_true", help="Also rename Subsection* folders/files.")
    parser.add_argument(
        "--update-headers",
        dest="update_headers",
        action="store_true",
        default=True,
        help="Update % FILE: / % PATH: headers when present (default).",
    )
    parser.add_argument("--no-update-headers", dest="update_headers", action="store_false")

    parser.add_argument("--dry-run", action="store_true", help="Print plan only (default when --apply is not set).")
    parser.add_argument("--apply", action="store_true", help="Apply renames/edits.")
    parser.add_argument("--undo", type=Path, help="Undo using a manifest JSON created by --apply.")

    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("/tmp/tex_batch_naming_manifest.json"),
        help="Where to write the apply manifest (default: /tmp/tex_batch_naming_manifest.json).",
    )

    args = parser.parse_args(argv)
    root: Path = args.root

    if args.apply and args.undo:
        print("Error: --apply and --undo cannot be used together.", file=sys.stderr)
        return 2

    if args.undo:
        print(f"Undoing from manifest: {args.undo}")
        undo_manifest(args.undo, dry_run=args.dry_run)
        return 0

    ops = plan_renames(
        root=root,
        course_code=args.course_code,
        include_subsections=args.include_subsections,
        include_chapters=args.include_chapters,
        chapter_min_count=args.chapter_min_count,
        update_headers=args.update_headers,
    )

    print_plan(ops)

    if not args.apply:
        return 0

    manifest = apply_ops(ops, dry_run=False)
    _write_text(args.manifest, json.dumps(manifest, ensure_ascii=False, indent=2))
    print(f"Wrote manifest: {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
