---
name: 0111-MathStatementInserter
description: Convert raw definition/theorem/lemma/proposition/corollary statements (often copied from PDF/notes, Chinese text + math) into the project’s LaTeX format using \\customproblem{...}{...} + \\addcontentsline{toc}{subsubsection}{...} + \\phantomsection\\label{...} placeholders. Use when the user asks “将定义(定理、引理、命题)输入到这里”, provides a “之前/之后” example, or wants to standardize math statements into the same structure as references/Example.md.
---

# Statement To Customproblem

参考 `tools/skills_example/Example_将定义(定理、引理、命题)输入到这里.md`。

## Command

```bash
python3 scripts/statement_to_customproblem.py --input raw.txt --output out.tex
```

or

```bash
cat raw.txt | python3 scripts/statement_to_customproblem.py
```
