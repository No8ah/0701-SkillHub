---
name: 0116-AnalogousDerivationGenerator
description: 补全 LaTeX 中“同理进行推导/同理补全”的对称推导段落，常见于有限体积/有限差分笔记中把“第一对偶单元”的积分守恒关系与离散守恒方程，按同样结构补齐“第二对偶单元”（右端点 b、索引 N、系数 beta 等）。用于用户给出已完成的左端推导与右端占位（只有标题/Proof 开头）时，生成右端的缺失定义块（\\customproblem + \\addcontentsline + \\label）与 Proof 推导步骤，保持原有排版风格与数学内容一致。
---

# LaTeX Tongli Derive

参考 `tools/skills_example/Example_同理进行推导.md`，为右端对称推导补全标准 Step 结构。

## Workflow

1. 识别 `$Proof:$` 后仅有占位 Step 的段落。
2. 插入 Step1-Step8 模板，保留原缩进风格。
3. 仅改空白推导，不改已有完整证明。

## Command

```bash
python3 scripts/tongli_derive.py --file <file.tex>
```
