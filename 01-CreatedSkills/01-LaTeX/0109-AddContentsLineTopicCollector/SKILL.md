---
name: 0109-AddContentsLineTopicCollector
description: 从 LaTeX 文件中收集并规范化 addcontentsline 的考点条目；也可从作业目录项的行区间提取匹配名称，进入 Notes 主文件指定行区间的 subfile，在匹配的 customproblem 前补/规范 purple star 考点标题。
---

# Addcontentsline 收集考点

## 目标
- 从正文中的 `\addcontentsline{toc}{subsubsection}{...}` 收集考点。
- 清理标记：删除 `\surd`。
- 统一前缀：可将 `第*次作业 - Exercise *` 替换为目标章节前缀。
- 去重并按出现顺序输出。
- 可选：把结果回写到“考点”小节。
- 可选：根据作业文件中指定行区间的目录项 `<匹配名称>`，遍历 Notes 主文件指定行区间内的 `\subfile{...}`，在 subfile 中匹配 `* - * - Content - <匹配名称> - *` 的定义项，并在其 `\customproblem` 前补/规范：
```tex
\subsection*{\textcolor{purple}{<匹配名称> $\star \star \star$}}
\addcontentsline{toc}{subsection}{\textcolor{purple}{<匹配名称> $\star \star \star$}}
```

## 使用步骤
### A. 收集/回写考点小节

1. 先预览收集结果（不改文件）：
```bash
python scripts/collect_addcontentsline_topics.py \
  --input /abs/path/file.tex \
  --prefix "Chapter6 - Section1 - 线性共轭方向法"
```

2. 将结果回写到文件“考点”小节：
```bash
python scripts/collect_addcontentsline_topics.py \
  --input /abs/path/file.tex \
  --prefix "Chapter6 - Section1 - 线性共轭方向法" \
  --rewrite
```

3. 仅去除 `\surd` 和空尾缀，不做前缀替换：
```bash
python scripts/collect_addcontentsline_topics.py --input /abs/path/file.tex
```

### B. 根据作业目录项标记 Notes 考点

适用场景：
- 作业文件中已有拆分后的：
```tex
\addcontentsline{toc}{subsubsection}{Page * - Content - <匹配名称> - *}
```
或：
```tex
\addcontentsline{toc}{subsubsection}{Page * - T* - <匹配名称> - *}
```
- Notes 主文件某段包含若干：
```tex
\subfile{...}
```
- 需要进入这些 subfile，查找：
```tex
\addcontentsline{toc}{subsubsection}{* - * - Content - <匹配名称> - *}
```
并给对应 `\customproblem` 补 purple star 标题。

1. 先检查会修改哪些 subfile：
```bash
python scripts/collect_addcontentsline_topics.py \
  --input /abs/path/Hw/Chapter*_Hw_*.tex \
  --source-lines 28:66 \
  --source-lines 271:315 \
  --notes-main /abs/path/Notes/Chapter*_*.tex \
  --notes-lines 25:65 \
  --mark-notes-headers \
  --check
```

2. 确认 `[CHANGE]` 列表后原地写入：
```bash
python scripts/collect_addcontentsline_topics.py \
  --input /abs/path/Hw/Chapter*_Hw_*.tex \
  --source-lines 28:66 \
  --source-lines 271:315 \
  --notes-main /abs/path/Notes/Chapter*_*.tex \
  --notes-lines 25:65 \
  --mark-notes-headers
```

3. 再次运行 `--check`，期望退出码为 `0`，输出只剩 `Topics: ...` 和 `Subfiles: ...`。

## 规则
- 默认只收集“考点”小节之前的 `subsubsection` 目录项，避免把历史“考点”再次采集。
- 清理 `\surd` 后若出现尾部 `- $$`、`- $ $` 会自动去掉。
- 输出项统一为：
```tex
\addcontentsline{toc}{subsubsection}{...}
```
- 去重保留首次出现顺序。
- `--source-lines START:END` 可重复传入；只从这些行中提取作业目录项。
- `--notes-lines START:END` 可重复传入；只从这些行中提取 Notes 主文件的 `\subfile{...}`。
- 匹配名称提取规则：
  - 作业目录项按顶层 ` - ` 拆分，忽略 `$...$` 内部的分隔符。
  - `Page * - Content - <匹配名称> - *` 和 `Page * - T* - <匹配名称> - *` 都取第三段为 `<匹配名称>`。
  - Notes 目录项取 `Content` 后一段为 `<匹配名称>`。
- 标记 Notes 时：
  - 若 `\customproblem` 前没有 subsection header，则插入 purple star header。
  - 若已有 red/blue/black/purple subsection header，则规范化为 purple star header。
  - 若普通 header 紧挨 purple star header，自动删除普通重复项。
  - 不修改 `\customproblem` 正文和原 `subsubsection` 目录项。

## 脚本
- `scripts/collect_addcontentsline_topics.py`
