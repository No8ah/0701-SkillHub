---
name: 0123-TeXHyperrefFiller
description: Fill LaTeX `\\hyperref[...]{...}` entries in `.tex` notes using the Chapter3_DI.tex style. Use when the user says “在hyperref中填写合适的内容” or “fill hyperref”, or when `\\hyperref[...]` must match the target definition’s `\\phantomsection\\label{...}` and the displayed link text must follow “定义名称 - 数学表达式”.
---

# TeX Hyperref Fill

## Overview

Fill or fix incomplete / inconsistent `\hyperref[...]{...}` links in LaTeX notes, using the exact label from the referenced definition and generating a consistent green-box display text.

## Workflow

### 1) Identify the target label (must match `\phantomsection\label{...}`)

For each citation line like:

- Find the definition being referenced (usually in the same `.tex`).
- Locate its exact label string at `\phantomsection\label{...}`.
- Copy that exact label into the `\hyperref[...]` brackets (do not “normalize” or re-type; copy/paste).

Special case (common in these notes): if the citation is directly under a just-defined block, the label is often within a few lines above the `\textbf{引用:}` block. Prefer copying that nearest preceding `\phantomsection\label{...}`.

If helpful, run the checker:

`python3 scripts/inspect_hyperref.py <path/to.tex>`

It reports empty/missing labels and labels that do not exist in the file.

### 2) Generate the displayed link text (green box, “定义名称 - 数学表达式”)

Use the Chapter3_DI.tex pattern:

- In this repo’s LaTeX, `\hyperref[<label>]{<text>}` uses `[...]` for the target label and `{...}` for the displayed text; keep the label in brackets and put “定义名称 - 数学表达式” in the displayed text.
- **Definition name**: use the definition’s name as shown in the document (e.g., the `\addcontentsline{...}{...}` entry or the definition title).
- **Math expression**: use the key defining expression (prefer the one used in the definition statement; if it is too long, use a shorter representative expression like the one in the TOC line).
- Wrap it as a green boxed link text, consistent with Chapter3_DI.tex.

Reference snippet: `references/chapter3_di_hyperref_format.md`.

If the definition block has a nearby TOC line like:

`\\addcontentsline{...}{...}{补充 - ... - <定义名称> - $<数学表达式>$}`

then you can take:

- `<定义名称>` from the last “- ... -” segment
- `<数学表达式>` from the last `$...$` segment (remove the surrounding `$` when placing inside the `$\displaystyle ...$` of the green box)

### 3) Guardrails (must follow)

- `\hyperref[...]` **must** point to an existing `\phantomsection\label{...}`.
- Do not change the target label’s punctuation, spacing, or angle brackets — copy exactly.
- Keep existing indentation and list formatting around `\textbf{引用:}` blocks.

## Notes

If the user says “按 Chapter3_DI.tex 中上传的格式填写”, always load `references/chapter3_di_hyperref_format.md` and mirror its LaTeX formatting exactly.
