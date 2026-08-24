# Chapter3_DI.tex Hyperref 格式参考

目标：在 `\textbf{引用:}` 列表中，填写/修正 `\hyperref[...]{...}`，使其与对应定义处的 `\phantomsection\label{...}` 一一对应，并让显示文本统一为“定义名称 - 数学表达式”的绿色框格式。

## 参考片段（来自 Chapter3_DI.tex）

定义处（标签来源）：

```tex
\phantomsection\label{def:<DI>:<chap3>:<补充 - 定义 - Content - 卷积意义下的可分离核>}
```

引用处（超链接格式）：

```tex
\hspace*{2em} 1. \hyperref[def:<DI>:<chap3>:<补充 - 定义 - Content - 二维离散卷积>]{\colorbox{green!20}{$\displaystyle \text{二维离散卷积} - \left(\omega \bigstar f\right)(x, y) = \sum\limits_{i=-\infty}^{+\infty} \sum\limits_{j=-\infty}^{+\infty} \omega(i, j) \cdot f(x - i, y - j)$}}
```

## 填写规则（强约束）

1. `\hyperref[...]` 的 `[...]` 必须 **完全等于** 被引用定义处 `\phantomsection\label{...}` 的花括号内容（逐字符一致）。
2. 显示文本（`{...}` 内）使用绿色框：`\colorbox{green!20}{...}`。
3. 显示文本的数学内容使用：`$\displaystyle \text{<定义名称>} - <数学表达式>$`。
4. `<定义名称>` 使用文档中的定义名（与标题/目录项一致）。
5. `<数学表达式>` 使用该定义最核心的“定义式/关键式”（优先用定义正文中的表达式；过长时可用目录项中的较短表达式替代）。
