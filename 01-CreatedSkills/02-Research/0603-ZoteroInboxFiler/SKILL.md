---
name: zotero-inbox-filer
description: >
  使用 Zotero MCP Server 将 00_Inbox 中的存量条目按「文献标题 → 入库路径」映射归档到 Zotero 目录树收藏夹,
  归档成功后仅将条目移出 00_Inbox(条目保留在文库与新目录树中,不删除)。
  当用户给出 tabularx 文献表格(文献标题 + 推荐指数 + 入库路径)与目录树,并要求
  "归档 00_Inbox / 按标题入库 / 按路径入库 / inbox 归档"时使用。
  触发动词: 归档、入库到路径、inbox filer、按标题入库。
---

# Zotero Inbox Filer

将 00_Inbox 中的存量条目按「文献标题 → 入库路径」映射归档到 Zotero 目录树收藏夹;
成功后仅移出 00_Inbox 归属(条目保留在文库中,新目录树下的条目不删除)。

## 输入格式(用户提供的两个部分)

### 1. 目录树

```
02_Research/
├── 01_AI_Systems/
│   ├── Agent_Harness
│   ├── Inference_Systems
│   ├── Serving
│   └── Evaluation
...
```

### 2. 文献标题-入库路径映射(tabularx 或表格)

```
#  Paper  主入库路径
1  DistilVDR  09_Document_Processing/Multimodal_Document
2  Self-Knowledge RAG  08_RAG/Agentic_RAG
```

## 执行流程

### Step1 — 校验目标收藏夹

1. `zotero_search_collections(query="00_Inbox")` 确认 Inbox 存在并获取 key。
2. `zotero_get_collection_items(collection_key=<00_Inbox key>)` 获取 Inbox 全部条目(key + 标题)。
3. 若收藏夹缺失或读取失败,返回 `Null`,不再继续。

### Step2 — 遍历标题并匹配

对映射表中的每一行,用 文献标题 在 Inbox 条目中匹配:

- 优先精确子串匹配;含特殊字符的标题(如 `τ₀`、`$...$`、引号)按关键词拆解匹配。
- 匹配到 → 记录条目 key;未匹配 → 记入「失败条目 list」。

### Step3 — 按入库路径归档

1. 根据目录树将入库路径(如 `02_Research/08_RAG/Agentic_RAG`)解析为收藏夹 key:
   - `zotero_search_collections(query=路径末级名)` 查 key;不存在则 `zotero_create_collection` 按树逐级创建(先父后子)。
2. `zotero_set_item_collections(item_keys=[...], add_to=[目标 key])` 批量归档,按目标收藏夹分组减少调用。

### Step4 — 移出 00_Inbox

- 对成功归档条目:`zotero_set_item_collections(item_keys=[...], remove_from=[00_Inbox key])`。
- **只移出归属,不删除条目**(新目录树下的条目保持不动)。
- 若 Inbox 中含附件成员且 MCP 工具拒绝附件 key:改用 Web API `PATCH /items/<key>` 清空 `collections` 数组(必须带 `If-Unmodified-Since-Version` 头,否则 428)。

### 汇报格式

- 成功条目:表格列出 # / 文献标题 / 入库路径 / 状态。
- 「失败条目 list」:未匹配或归档失败的标题;无失败写 "空(无)"。

## 注意事项

- 需要可写的 Zotero 库(web API key 或 hybrid 模式);local-only 只读模式会失败。
- 标题匹配优先精确子串;模糊匹配时需人工确认避免错归档。
- 关联 skill: [[zotero-identifier-importer]] 负责按标识符(arXiv/DOI/ISBN)入库新论文;
  本 skill 负责 Inbox 存量条目按路径归档,两者互补。
