---
name: 0115-TeXHeaderCommentFiller
description: Fill and normalize the front comment header in LaTeX .tex notes/homework (e.g. % FILE, % PATH, % AUTHOR, % LAST MODIFIED) using the actual file path and today's date. Use when the user says “填写Tex前文注释” and provides a target .tex file (especially Chapter2_OM_Hw.tex-style headers), or asks to replace placeholders like % AUTHOR: [Your Name] and update % LAST MODIFIED.
---

# TeX Fill Front Comments

## Do
- Update the header comment block (between the `% ===...` separator lines) without changing any math/content.
- Fill/refresh:
  - `% FILE:` -> basename of the file
  - `% PATH:` -> directory path of the file
  - `% AUTHOR:` -> provided author (default to system username if not given)
  - `% LAST MODIFIED:` -> today (YYYY-MM-DD), unless user specifies a date

## Use the Script
- Run:
  - `python3 skills/tex-fill-front-comments/scripts/fill_front_comments.py --file '<path/to.tex>'`
- Optional:
  - `--author 'Your Name'`
  - `--date 'YYYY-MM-DD'`
  - `--dry-run`

## Verification
- Confirm the header fields are filled (no `[Your Name]` left).
- Confirm only comment lines in the header changed.
