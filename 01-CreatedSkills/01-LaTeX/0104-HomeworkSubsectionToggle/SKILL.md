---
name: 0104-HomeworkSubsectionToggle
description: Toggle homework subsections between commented and uncommented states. Keeps or restores Page * - T* and 第 * 次作业 - Exercise subsections while commenting out all other content. Use when the user asks to clean up homework files, keep only specific problems, or restore commented problems.
---

# Toggle Homework Subsections

## Workflow

1. Run the toggle script on a single homework `.tex` file or a chapter root directory.
2. The script will:
   - Keep `Page * - T*` and `第 * 次作业 - Exercise` subsections **uncommented**
   - Restore (uncomment) those subsections if they were previously commented
   - Comment out all other subsections

## Commands

Dry-run first to preview changes:

```bash
python3 /Users/quzinan/Downloads/Code/.claude/skills/toggle-homework-subsections/scripts/toggle_homework_subsections.py path/to/file.tex --dry-run
```

Apply changes:

```bash
python3 /Users/quzinan/Downloads/Code/.claude/skills/toggle-homework-subsections/scripts/toggle_homework_subsections.py path/to/file.tex
```

Run on a chapter root directory (batch mode):

```bash
python3 /Users/quzinan/Downloads/Code/.claude/skills/toggle-homework-subsections/scripts/toggle_homework_subsections.py /Users/quzinan/Downloads/Code/study/Optimization_Method/Hw/Chapter10_OM_Hw_约束优化最优性条件
```

## Options

- `--dry-run` / `-n`: Preview changes without modifying files
- `--uncomment-only` / `-u`: Only restore kept subsections without commenting others

## Default path

If no path is provided, defaults to Chapter 10 homework root:

```bash
python3 /Users/quzinan/Downloads/Code/.claude/skills/toggle-homework-subsections/scripts/toggle_homework_subsections.py
```

## What is kept

The following subsection patterns are never commented (and restored if commented):
- `Page * - T*` (problem subsections, e.g. `Page 178 - T4`)
- `第 * 次作业 - Exercise` (homework exercises, e.g. `第 10 次作业 - Exercise 1`)
