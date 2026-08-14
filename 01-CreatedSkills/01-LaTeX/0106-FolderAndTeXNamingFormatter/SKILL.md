---
name: 0106-FolderAndTeXNamingFormatter
description: Batch-rename lecture note folder names and main LaTeX .tex filenames to a consistent convention (e.g. SectionN_标题 and ChapterN_ScM_COURSE_标题.tex), and optionally update in-file header comments like % FILE: / % PATH:. Use when prompts say “批量重命名/统一命名格式/按某个目录下的命名格式更改/格式化命名文件夹以及.tex文件”, especially for course note repos under Lecture/*.
---

# Task

## When to use this skill:

- 格式化命名文件夹以及.tex文件

## Quick start

- Dry-run (recommended):

  `python3 scripts/tex_batch_naming.py /path/to/course --dry-run`

- Apply:

  `python3 scripts/tex_batch_naming.py /path/to/course --apply`

## What it enforces

- **Chapter folder names** (default): Rename `ChapterN` → `ChapterN_章标题` when the chapter title can be inferred reliably.
- **Folder names**: Rename `SectionN` → `SectionN_标题` when the title can be inferred.
- **Main note .tex**: Rename `ChapterN_ScM_<CODE>.tex` → `ChapterN_ScM_<CODE>_标题.tex` when missing the trailing title.
- **In-file header sync (optional)**: If a `.tex` contains `% FILE:` and/or `% PATH:` lines, update them to match the renamed file and directory (only when those lines already exist).

## Deterministic rules

- Never guess unknown titles: if the title cannot be inferred, skip that rename.
- Prefer titles from existing names (`SectionN_标题` / `..._标题.tex`); otherwise infer from `.tex` content:
  - Title block `{\Huge \textbf{...}}` (take the last ` - ` fragment), else
  - First `\section*{...}` heading (strip wrappers like `\textcolor{...}{...}`).
- Chapter title inference (for `ChapterN_章标题`):
  - Parse `{\Huge \textbf{ChapterN - 章标题 - 小节标题}}` and take the **second** fragment as the chapter title candidate.
  - Count candidates across the chapter; rename only if the best candidate appears at least `--chapter-min-count` times (default `2`).
- Default is **dry-run**; only rename when `--apply` is provided.
- Write a manifest JSON for undo when applying; support `--undo <manifest.json>`.

## Options

- `--course-code CODE`: Force course code (e.g. `NMSDE`, `OM`). Otherwise infer from existing filenames.
- `--no-include-chapters`: Disable Chapter folder renames.
- `--chapter-min-count N`: Minimum count threshold for chapter title inference (default `2`).
- `--include-subsections`: Also apply similar logic to `Subsection*` directories/files (off by default).
- `--update-headers/--no-update-headers`: Toggle `% FILE:` / `% PATH:` syncing (default on).

## Reference

See `references/naming_examples.md`.
