---
name: 0124-DIStarMarkerInserter
description: Add a visible LaTeX star marker `$\star$` in the correct position inside TOC/title strings (especially `\\addcontentsline{...}{...}{...}`) following Chapter3_DI.tex. Use when the user says “在合适的地方添加star”, or asks to mark a “补充 - 定义 …” entry as “定义 $\star$” without changing labels.
---

# TeX Add Star (DI Style)

## Overview

Insert `$\star$` into the **visible title/TOC text** at the same position as Chapter3_DI.tex (do not change `\label{...}` identifiers).

Always follow `references/chapter3_di_add_star_format.md`.

## Workflow

### 1) Find the target title/TOC string

This is usually the 3rd argument of:

`\\addcontentsline{toc}{subsubsection}{...}`

### 2) Insert the star marker at the correct position

Follow the Chapter3_DI.tex pattern:

- Replace `定义 -` with `定义 $\\star$ -`
- Keep spacing exactly: `定义␠$\star$␠-`

Do **not** add the star into `\\label{...}` (Chapter3_DI.tex keeps labels unstarred).

### 3) Guardrails (must follow)

- Only modify visible title strings / TOC entries; do not change math content outside the title string.
- Do not touch `\\phantomsection\\label{...}` content.
- Keep indentation and surrounding LaTeX structure unchanged.

## Optional helper

List candidate `\\addcontentsline` lines (and optionally apply to one specific line):

`python3 scripts/add_star_to_addcontentsline.py <path/to.tex>`
