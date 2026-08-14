---
name: zotero-identifier-importer
description: >
  使用 Zotero MCP Server 的 zotero_add_item 工具,通过标识符(arXiv ID / DOI / ISBN / URL / BibTeX)
  批量添加条目到指定 Zotero 收藏夹,添加成功后清理源文件中已入库的选中片段。
  当用户给出 arXiv_Inbox / DOI_Inbox / ISBN 等标识符片段并要求"通过标识符添加条目 / 入库到 Zotero /
  添加到 00_Inbox / import by identifier"时使用。
  触发动词: 通过标识符添加条目、入库、添加到 Zotero、identifier import。
---

# Zotero Identifier Importer

将选中片段中的标识符(arXiv ID、DOI、ISBN、URL)逐个通过 Zotero MCP Server 的
"通过标识符添加条目"功能入库到指定收藏夹(默认 `00_Inbox`),添加成功后删除
源文件中已入库的标识符行。

## 输入格式(用户粘贴的标识符片段)

```
arXiv\_Inbox

2605.28424v1
2604.03088v3

DOI\_Inbox

10.32629/mcmf.v5i4.2573
```

或纯标识符列表(每行一个,可带 v1/v2 版本后缀)。

## 执行流程

### Step1 — 检查目标收藏夹可读写

1. `zotero_search_collections(query="00_Inbox")` 确认目标收藏夹存在并获取 key。
2. 用第一个标识符执行一次 `zotero_add_item` 验证读写能力(此条目同时计入 Step2 结果)。
3. 若失败(如 local-only 只读模式)返回 `Null`,不再继续。

### Step2 — 逐个通过标识符添加条目

对每个标识符调用 `zotero_add_item`:

- **source**: arXiv ID 一律转为 `https://arxiv.org/abs/<ID>`(去掉 `v1`/`v2` 版本后缀,可拿到完整元数据 + PDF);
  DOI 直接用 DOI 字符串(走 CrossRef);ISBN 直接用 ISBN;BibTeX/CSL JSON 支持批量。
- **collections**: 目标收藏夹 key(如 `BIWJX4IB`)。
- **if_exists**: `file`(已存在时复用条目,补充缺失的收藏夹/附件,绝不删除或修改已有条目)。
- **attach_mode**: `auto`(自动附加开放获取 PDF)。
- 多个标识符可并行调用 `zotero_add_item`。
- 逐个记录成功/失败;失败的标识符收进「失败条目 list」。

### Step3 — 清理源文件已入库片段

- 全部成功后,用 Edit 从用户选中的源文件片段中删除所有**成功入库**的标识符行。
- 保留 Inbox 标题(如 `arXiv\_Inbox`、`DOI\_Inbox`)与整体文档结构,仅删条目行。
- 失败条目保留在源文件中,并向用户汇报。

### 汇报格式

- 成功条目:表格列出 # / 标识符 / 论文标题 / 状态(+PDF)。
- 「失败条目 list」:失败标识符清单;无失败则写 "空(无)"。

## 注意事项

- 需要可写的 Zotero 库(web API key 或 hybrid 模式);local-only 只读模式会失败。
- 添加完成后可提示用户运行 `zotero_update_search_database` 使新条目可被语义搜索。
- 若目标收藏夹不存在,用 `zotero_create_collection` 创建,或询问用户指定其他收藏夹。
- 关联 skill: [[github-inbox-manager]] 负责 GitHub 项目搜索 + tabularx 表格入库;
  本 skill 负责标识符直接入库 Zotero。
