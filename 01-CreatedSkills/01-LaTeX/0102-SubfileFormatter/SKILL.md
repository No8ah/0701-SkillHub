---
name: 0102-SubfileFormatter
description: "Format and repair LaTeX subfiles projects. Use when Codex needs to normalize subfiles children .tex files by fixing parent relative path, ensuring a single begin/end document pair, stripping standalone-document preambles, and producing a dry-run change list before writing."
---

# 格式化Subfiles

## Quick Start

Use `scripts/format_subfiles.py` to batch-normalize `.tex` subfiles under a directory.

1. Dry-run first (recommended)

```bash
python3 scripts/format_subfiles.py \
  --root '/path/to/project' \
  --glob 'Section*/*.tex' \
  --parent '/path/to/project/ChapterX_OM_Hw_....tex'
```

2. Write changes

```bash
python3 scripts/format_subfiles.py \
  --root '/path/to/project' \
  --glob 'Section*/*.tex' \
  --parent '/path/to/project/ChapterX_OM_Hw_....tex' \
  --write
```

## What It Fixes

- Ensures file starts with `\documentclass[REL_PARENT]{subfiles}` (when `--parent` is provided).
- Ensures exactly one `\begin{document}` and one `\end{document}`.
- If the file is a standalone `article`/`report`/`book`, keeps only the content inside the document body.
- Removes any trailing content after the last `\end{document}`.

## Inputs

- `--root`: Project root directory to scan.
- `--glob`: Glob pattern relative to `--root`, e.g. `Section*/*.tex`, `Section*_*/*.tex`, `**/*.tex`.
- `--parent`: Path to the parent `.tex` file (usually the chapter main file). Used to compute `REL_PARENT`.
- `--write`: Actually write changes. Without it, the script only prints what would change.

## Notes

- The script is intentionally conservative and does not try to re-indent LaTeX bodies.
- If you need a visual reference for the desired header shape, see `references/Example_格式化subfiles.md`.

## Resources

- `scripts/format_subfiles.py`: Batch normalizer for subfiles.
- `references/Example_格式化subfiles.md`: Example before/after formatting.
