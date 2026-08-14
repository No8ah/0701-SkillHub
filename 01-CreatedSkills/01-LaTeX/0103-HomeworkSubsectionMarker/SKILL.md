---
name: 0103-HomeworkSubsectionMarker
description: Mark lecture note subsections referenced by Optimization Method homework addcontentsline entries. Use when a user asks to traverse Chapter*_LECTURE_Hw_*.tex subfiles, ignore homework TOC entries containing \surd or \times, find matching Chapter*_LECTURE_*.tex lecture subsection titles, change textcolor from blue to purple, and append $\star \star \star$.
---

# Mark Homework Subsections

## Workflow

Use `scripts/mark_homework_subsections.py` for the deterministic pass.

1. Start from either:
   - a chapter homework root `.tex` file, or
   - a lecture-course folder containing `Hw/` and `Notes/` (batch mode).
2. In batch mode, discover every `Chapter*_Hw_*.tex` under `Hw/` and process each chapter root.
3. Extract all `\subfile{...}` children recursively, plus the provided file itself when it matches `Chapter*_Hw_*.tex`.
4. Read every `\addcontentsline{toc}{subsubsection}{...}` in those homework files.
5. Ignore entries containing `\surd` or `\times`.
6. Find the corresponding lecture note subfiles by replacing `/Hw/` with `/Notes/` and `_Hw_` with `_`.
7. Match homework TOC text against lecture `\subsection*{\textcolor{...}{...}}` titles after normalization.
8. For every matched lecture subsection, update both the visible `\subsection*` title and the matching `\addcontentsline{toc}{subsection}` title:
   - `\textcolor{blue}{...}` to `\textcolor{purple}{...}`
   - append ` $\star \star \star$` unless already present

## Commands

Dry-run first:

```bash
python3 /Users/quzinan/.codex/skills/mark-homework-subsections/scripts/mark_homework_subsections.py path/to/Chapter7_OM_Hw_最小二乘问题.tex
```

Batch dry-run for a lecture-course folder:

```bash
python3 /Users/quzinan/.codex/skills/mark-homework-subsections/scripts/mark_homework_subsections.py /Users/quzinan/Downloads/Code/study/Optimization_Method
```

Write changes after inspecting the planned edits:

```bash
python3 /Users/quzinan/.codex/skills/mark-homework-subsections/scripts/mark_homework_subsections.py path/to/Chapter7_OM_Hw_最小二乘问题.tex --write
```

Batch write for a lecture-course folder:

```bash
python3 /Users/quzinan/.codex/skills/mark-homework-subsections/scripts/mark_homework_subsections.py /Users/quzinan/Downloads/Code/study/Optimization_Method --write
```

Useful options:

- `--notes-root PATH`: override the inferred lecture-notes root.
- `--homework-root PATH`: override the inferred homework root.
- `--lecture OM`: restrict matching to a specific lecture token when inference is ambiguous.

## Guardrails

- Treat generated `.aux`, `.toc`, and `.log` files as outputs; do not edit them.
- Preserve unrelated user edits.
- If the script reports ambiguous or unmatched entries, inspect the relevant homework TOC entry and lecture subsection manually before applying a broader edit.
- Re-run the script without `--write` after edits to confirm no additional changes are pending.
