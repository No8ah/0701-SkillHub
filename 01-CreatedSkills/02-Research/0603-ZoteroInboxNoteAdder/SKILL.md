---
name: zotero-inbox-note-adder
description: >
  使用 Zotero MCP Server 打开 我的文库-00_Inbox,遍历其中所有标题,在每个标题下添加一条
  内容为空的笔记。当用户要求"为 00_Inbox 所有条目添加笔记 / 打开 00_Inbox 并添加笔记 /
  inbox 批量加笔记"时使用。
  触发动词: 添加笔记、批量笔记、inbox 笔记。
---

# Zotero Inbox Note Adder

遍历 00_Inbox 中的全部条目,在每个标题下添加一条内容为空的笔记。

## 执行流程

### Step1 — 打开 00_Inbox

1. `zotero_search_collections(query="00_Inbox")` 获取收藏夹 key。
2. `zotero_get_collection_items(collection_key=<key>, detail="summary")` 获取全部条目标题与 key。
3. 失败(收藏夹不存在 / 只读模式)则返回 `Null`,不再继续。

### Step2 — 为每个标题添加空笔记

对每个条目调用 `zotero_manage_note`:

- **action**: `create`
- **item_key**: 条目 key
- **note_title**: 省略或使用默认名(如 `测试笔记`)
- **note_text**: 空字符串(笔记内容为空)

逐个记录成功/失败。

### 汇报格式

- 成功:表格列出 标题 / 笔记 key / 状态。
- 失败:未添加成功的标题清单;无失败写 "空(无)"。

## 注意事项

- 需要可写的 Zotero 库(web API key 或 hybrid 模式);local-only 只读模式会失败。
- 笔记是独立子条目,创建后挂在父条目标题下,可用 `zotero_get_notes(item_key=<key>)` 验证。
- 若某标题已存在笔记,直接再创建一条即可(本 skill 不做去重)。
- 关联 skill: [[zotero-inbox-filer]] 负责 Inbox 条目按路径归档;本 skill 负责批量加空笔记。
