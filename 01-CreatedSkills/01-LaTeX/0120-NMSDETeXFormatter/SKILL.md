---
name: 0120-NMSDETeXFormatter
description: Format LaTeX (.tex) notes/homework so the Definition/Example/Problem blocks and surrounding structure match the style used in `Chapter1_NMSDE.tex`. Use when the user says “格式化这个文档的定义以及其他内容时” (or asks to format NMSDE notes “按Chapter1_NMSDE.tex中的格式”).
---

# NMSDE TeX Format

Format NMSDE LaTeX documents to match the conventions in `Chapter1_NMSDE.tex` (indentation, `\customproblem{...}{...}` block layout, and consistent whitespace), while preserving mathematical/content meaning.

## Workflow

1. Use `references/style_snippet.tex` as the style source.
2. Run the formatter script for safe, deterministic changes (tabs/trailing spaces and simple `\customproblem` one-liners).
3. For any remaining sections, manually adjust structure to match the snippet (do not rewrite math/content).

## Quick start

- Check what would change (no write):
  - `python3 /Users/quzinan/.codex/skills/nmsde-tex-format/scripts/format_nmsde_tex.py --check /path/to/file.tex`

- Apply changes in place:
  - `python3 /Users/quzinan/.codex/skills/nmsde-tex-format/scripts/format_nmsde_tex.py /path/to/file.tex`

## What the script changes (and what it will not)

- It **will**:
  - Replace `\t` with 4 spaces.
  - Remove trailing whitespace.
  - Ensure the file ends with a newline.
  - Expand **simple** one-line `\customproblem{title}{body}` (body contains no braces) into the multi-line block style used in `Chapter1_NMSDE.tex`.

- It **will not**:
  - Reflow paragraphs or rewrap math environments.
  - Attempt to parse arbitrary nested LaTeX braces.
  - Invent missing sections (e.g. `\textbf{简明思路:}`) or change labels/titles.

## Style notes

- Prefer the multi-line `\customproblem{...}{ ... }` layout shown in `references/style_snippet.tex`.
- Keep content unchanged; only normalize whitespace/structure.
