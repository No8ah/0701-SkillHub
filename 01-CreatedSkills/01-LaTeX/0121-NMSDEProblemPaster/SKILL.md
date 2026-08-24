---
name: 0121-NMSDEProblemPaster
description: Paste an exercise/problem statement into LaTeX \\customproblem{...}{...} (second argument) and format sub-questions using \\begin{enumerate} ... \\item ... \\end{enumerate} following the style in Chapter1_NMSDE_Hw.tex. Use when the user says "将题目粘贴到这里" and provides a problem statement to insert into an existing NMSDE homework .tex file.
---

# TeX Paste Problem (NMSDE)

## Workflow

Goal: Given a pasted problem statement, insert it into the target `\\customproblem{...}{...}` second argument, and list each sub-question as an `\\item` under `\\begin{enumerate}` in the same block (style match to `Chapter1_NMSDE_Hw.tex`).

### 1) Fill `\\customproblem` second argument

- Find the target `\\customproblem{...}{...}` near where the user wants to paste the problem (often the second argument is empty `{}` or a placeholder like `\\textit{（请在此处粘贴题目原文）}`).
- If there are multiple candidates, prefer the one the user referenced by filename/line number; otherwise prefer the nearest one whose second argument is empty/placeholder.
- Replace only the **second** argument content with the full problem statement.
  - Keep math exactly the same.
  - Use `\\[` `\\]` for display math if the pasted text includes equations (match the existing file’s conventions).
  - Keep indentation/blank lines consistent with the surrounding style.

### 2) Add sub-questions with `enumerate` + `item`

- If the problem has multiple sub-questions (e.g., “(1)… (2)…”, “a)… b)…”, “(i)… (ii)…”, or separate sentences like “……，并……/并且……/且……”) then:
  - After the problem’s `\\phantomsection\\label{...}` line (and before any solution content), insert:
    - `\\begin{enumerate}`
    - one `\\item` per sub-question (each `\\item` should contain the exact text of that sub-question, including any display math blocks)
    - `\\end{enumerate}`
- If the block already contains an `enumerate`, only update the `\\item` contents/structure; do not duplicate environments.

### 3) Keep the existing solution scaffolding

- Do not change the math/derivation/solution steps the user already wrote.
- If you need placeholders for later solution writing, add empty `tcolorbox` blocks under each `\\item` only if the file’s local pattern already does so.

### 4) Style reference

- When unsure about spacing/indentation, open `references/chapter1_nmsde_hw_excerpt.tex` and mimic it.
