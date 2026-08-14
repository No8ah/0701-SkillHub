---
name: 0105-SurdSubsectionToggle
description: Comment or uncomment homework subsection units based on the \surd marker. A unit is from \subsection*{...} to the next, including preceding \addcontentsline, \clearpage, \newpage (but NOT the header area before % Content). Units whose first \addcontentsline{toc}{subsubsection} after \customproblem contains $\surd$ are toggled; others are left untouched.
---

# Toggle Surd-marked Subsections

## Workflow

1. Run the script on a single homework `.tex` file or a chapter root directory.
2. For each subsection unit, check if the first `\addcontentsline{toc}{subsubsection}` after `\customproblem` contains `$\surd$`.
3. If yes → comment out (default) or restore (`--uncomment`) the entire unit.
4. The header/TOC area before `% Content` is never modified.

## Commands

Comment out all surd-marked units (default):

```bash
python3 /Users/quzinan/Downloads/Code/.claude/skills/toggle-surd-subsections/scripts/toggle_surd_subsections.py [path]
```

Restore (uncomment) all surd-marked units:

```bash
python3 /Users/quzinan/Downloads/Code/.claude/skills/toggle-surd-subsections/scripts/toggle_surd_subsections.py [path] --uncomment
```

Dry-run to preview changes:

```bash
python3 /Users/quzinan/Downloads/Code/.claude/skills/toggle-surd-subsections/scripts/toggle_surd_subsections.py [path] --dry-run
```

## Default path

If no path is provided, defaults to Chapter 10 homework root.

## What is a unit

A unit = all content from one `\subsection*{...}` to the next (or `\end{document}`), including:

- Preceding `\addcontentsline{toc}{subsection}` (if any)
- Preceding `\clearpage` and `\newpage` (if any)

**But NOT** the header/TOC setup before the `% Content` marker.

## Marker detection

The script finds `\customproblem` within the unit, then scans the very next `\addcontentsline{toc}{subsubsection}`. If it contains `$\surd$`, the unit is toggled.
