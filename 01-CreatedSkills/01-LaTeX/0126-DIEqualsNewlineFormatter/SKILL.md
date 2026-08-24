---
name: 0126-DIEqualsNewlineFormatter
description: Format long LaTeX equation chains in display math so each top-level equals sign `=` is on its own line, matching Chapter3_DI.tex style. Use when the user says “长等式按Chapter3_DI.tex格式补全”, “长等式按等号换行”, or when completing LaTeX `.tex` notes and a long `=` chain should be line-broken without changing math content.
---

# TeX Equals Newline (DI Style)

## Overview

When a displayed equation is long and contains an equality chain, put every top-level `=` on a separate line: expression line, `=` line, expression line, `=` line, ...

Always follow the exact style shown in `references/chapter3_di_equals_newline_format.md`.

## Workflow

### 1) Apply only inside display math blocks

This style targets display math blocks like:

- `\[ ... \]`
- `$$ ... $$`
- `\begin{equation} ... \end{equation}` (only if it’s a single chain, not already an `align/align*`)

Do **not** force this style inside `align`, `aligned`, `split`, etc. where `&=` alignment is intended.

### 2) Break at top-level `=`

If you see a long chain like `A = B = C = D` (or a multi-token chain across a long line), rewrite it to:

```tex
\[
    A
    =
    B
    =
    C
    =
    D
\]
```

Rules:

- Keep each `=` as a standalone line, with the same indentation as the surrounding lines in the display math block.
- Keep sub-environments’ internal formatting unchanged (e.g., `bmatrix` rows stay as they are).
- Only change whitespace/newlines; do not change symbols, commands, or math grouping.

### 3) Optional helper script

Use this only for quick formatting of a snippet (not as a blind whole-file rewriter):

`python3 scripts/break_equals_lines.py --wrap < input.tex-snippet`
