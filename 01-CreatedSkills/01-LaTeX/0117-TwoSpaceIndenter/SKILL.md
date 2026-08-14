---
name: 0117-TwoSpaceIndenter
description: Reformat LaTeX/Markdown Step blocks into the “往后缩进两格” style. Use when prompts say “往后缩进两格” and the content has repeated `\textbf{StepN:}\quad ...` lines that should become a parent step plus numbered sub-steps and deeper indented third-level items.
---

# 往后缩进两格

## Quick Start

- Preview:

  `python3 scripts/indent_two_levels.py path/to/file.tex > /tmp/out.tex`

- Edit in place:

  `python3 scripts/indent_two_levels.py --in-place path/to/file.tex`

- stdin/stdout:

  `python3 scripts/indent_two_levels.py - < input.tex > output.tex`

## Deterministic Rules

- Locate a parent line: `\textbf{StepN:}\quad <TEXT>` (without inline `$...$`).
- Keep this parent as headline and ensure it has `\hspace*{2em}`.
- For subsequent sibling lines with the same `StepN` and inline math (`$...$`):
  - Rewrite as second-level numbered items:
  - `\hspace*{4em} 1. ...`
  - `\hspace*{4em} 2. ...`
- Under each rewritten second-level item, convert third-level lines:
  - from `\hspace*{2em} m. ...`
  - to `\hspace*{6em} i.m. ...` where `i` is the second-level index.
- Preserve all math content verbatim; only rewrite indentation/labels.

## Boundaries

- Only edit lines matching the Step pattern above.
- Do not modify unrelated blocks, formulas, `\customproblem` headers, or `\addcontentsline`.
- If no matching Step structure is found, leave file unchanged.

## Reference

- `references/Example_往后缩进两格.md`
