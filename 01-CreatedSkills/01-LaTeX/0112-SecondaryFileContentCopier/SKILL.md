---
name: 0112-SecondaryFileContentCopier
description: 将指定行范围复制到新位置（可跨文件或同文件），并可在复制后删除原位置内容实现移动；支持复制到目标文件时自动补 `\\section*`（可选同步 `\\addcontentsline`）。当用户提出“粘贴到第2个文件中”“把A文件第x-y行复制到B文件第n行前”“复制到新的位置”“移动到第n行并删除原处”“复制后加 section”“复制到第2个文件后删除源文件对应行”这类请求时使用。
---

# Copy Content To Second File

## Command

```bash
python3 scripts/copy_content_to_second_file.py \
  --src '<a.tex>' --start 120 --end 180 \
  --dst '<b.tex>' --before-line 40
```

Optional:

```bash
--delete-source
--section-title '标题'
--add-contentsline
```
