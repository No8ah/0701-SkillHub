---
name: 0118-TeXStructureCreator
description: 在指定目录下按课程笔记结构创建 `Section*/Set/*.tex` 与主 tex 文件（例如 `ChapterN_ScM_COURSE_标题.tex`）。用于“在该目录下创建.tex文件及其文件夹”“在路径下创建tex文件”这类请求，并可复用填写文件头注释的技能。
---

# Create TeX Folder Scaffold

参考：
- `tools/skills_example/Example_在该目录下创建.tex文件及其文件夹(文件夹关键词).md`
- `tools/skills_example/Example_在路径(路径名)下创建tex文件.md`

## Command

```bash
python3 scripts/create_tex_scaffold.py \
  --base '<Notes目录>' \
  --section-name 'Section3_线性系统的相容性' \
  --main-tex 'Chapter2_Sc3_OM_线性系统的相容性.tex'
```
