---
name: 0203-ProblemInserter
description: Paste raw exercise/problem statements into existing LaTeX `\\customproblem{...}{...}` blocks, and (when present) split subquestions like (a)(b) or (1)(2) into an `enumerate` list where each item is followed by an empty `tcolorbox` solution placeholder. Use when the user says "将题目输入到这里", provides a raw problem statement that needs to be inserted into a `\\customproblem` template, or wants to turn inline subquestions into structured `enumerate` + `tcolorbox` placeholders without changing math content.
---

# Paste Problem

参考 `tools/skills_example/Example_将题目输入到这里.md`。

## Command

```bash
python3 scripts/paste_problem.py --title 'Page 214 - T4.18' --input raw.txt --output out.tex
```
