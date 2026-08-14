# Lecture6 拆解样式锚点

用于对齐“拆解为 N 个部分”的结构与排版风格时，直接对照下面这个真实样例：

- 源片段：`Lecture/Stochastic Process/Lecture Notes/Lecture6/Notes/Lecture6_SP.tex` 的 `Line20-133`
- 拆解结果：同一文件的 `Line135-285`

该样例体现了典型拆解方式：

- 将一个包含多个结论的 `\\customproblem{...}{...}` 拆成 `... (1) / (2) / ...`
- 每个 part 都有自己的 `\\addcontentsline`、`\\label`、`\\textbf{引用:}`/`\\textbf{注:}` 与 `Proof:`/`Step` 结构

