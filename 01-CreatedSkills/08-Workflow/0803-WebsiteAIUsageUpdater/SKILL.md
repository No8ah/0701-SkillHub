---
name: 0803-WebsiteAIUsageUpdater
description: Update AI usage statistics across AIUsage.jsx and AI使用水平.jsx. Use when the user asks to update token consumption, cost data, cache metrics, request counts, or provider stats for the AI usage dashboard.
---

# update-ai-usage

## Workflow

The user will upload screenshots of the AI Usage dashboard (one per provider card + aggregate card). Follow these steps:

1. **Read screenshots** — identify which screenshot corresponds to Claude Code, Codex, and 汇总 (aggregate). The Claude Code card has a yellow accent (`#f7bf16`), the Codex card has a green accent (`#32d7a0`), and the aggregate card shows 总请求数/总成本/总 Token 数/缓存 Token.

2. **Extract data from screenshots** — read every visible number from each card. Extract: `totalTokens`, `compactTokens`, `requests`, `actualCost`, `cost`, `cacheRate`, `bar`, and all four `stats` values (新增输入, Output, 创建, 命中). For the aggregate card, extract: 总请求数, 总成本, 理论成本, 总 Token 数, Input, Output, 缓存 Token, 创建, 命中.

3. **Update Card 2 (Claude Code)** in [AIUsage.jsx](personal_website_react/src/pages/AIUsage.jsx) lines 6–20.

4. **Update Card 3 (Codex)** in [AIUsage.jsx](personal_website_react/src/pages/AIUsage.jsx) lines 23–37.

5. **Update Card 1 (汇总)** in [AI使用水平.jsx](personal_website_react/src/components/AI使用水平.jsx) lines 6–44 — re-derive from Card 2 + Card 3.

6. **Verify consistency** — confirm Card 1 values match the derivation rules below.

## Card 1 — 汇总卡片

[personal_website_react/src/components/AI使用水平.jsx](personal_website_react/src/components/AI使用水平.jsx) lines 6–44, the `metrics` array.

**Derivation** — every field in Card 1 is derived from Card 2 + Card 3:

| Card 1 field | Source |
|-------------|--------|
| `总请求数` `value` | `sum(requests)` from both providers |
| `总成本` `value` | `sum(actualCost)` — **do NOT change unless actualCost changes** |
| `总成本` `lines[0][1]` (理论成本) | `sum(cost)` from both providers |
| `总 Token 数` `value` | `sum(totalTokens)` |
| `总 Token 数` `lines[0][1]` (Input) | sum of `stats[新增输入]` |
| `总 Token 数` `lines[1][1]` (Output) | sum of `stats[Output]` |
| `缓存 Token` `value` | `stats[命中] + stats[创建]` summed across providers |
| `缓存 Token` `lines[0][1]` (创建) | sum of `stats[创建]` |
| `缓存 Token` `lines[1][1]` (命中) | sum of `stats[命中]` |

## Card 2 — Claude Code 卡片

[personal_website_react/src/pages/AIUsage.jsx](personal_website_react/src/pages/AIUsage.jsx) lines 6–20.

**Updatable fields on this card:**

| Field | When to update | Unit |
|-------|---------------|------|
| `totalTokens` | Always when tokens change | comma-separated integer string |
| `compactTokens` | Match `totalTokens` in human form | `≈ X 亿 tokens` |
| `requests` | New request count available | integer string |
| `actualCost` | **NEVER CHANGE** — stable historical cost | `$X.XX` |
| `cost` | Recomputed from tokens × rate | `$X.XXXX` |
| `cacheRate` / `bar` | Recomputed as `命中 ÷ (命中 + 新增输入)` | percent string / number |
| `stats[新增输入]` | Cache-miss input tokens | `万` abbreviated |
| `stats[Output]` | Output tokens | `万` abbreviated |
| `stats[创建]` | Cache writes (usually 0) | integer string |
| `stats[命中]` | Cache-hit tokens | `亿` / `万` abbreviated |

## Card 3 — Codex 卡片

[personal_website_react/src/pages/AIUsage.jsx](personal_website_react/src/pages/AIUsage.jsx) lines 23–37.

Same structure as Card 2, with `name: 'Codex'` and `accent: '#32d7a0'`.

Same updatable fields as Card 2.

## Consistency Rule

`actualCost` on **both** Card 2 and Card 3 is **stable historical data**. When token counts, cache rates, or theoretical costs change, update all other fields — but leave `actualCost` untouched.

## Non-updatable sections

- AIUsage.jsx lines 41–49 (`coreLogic`) — architectural concepts
- AIUsage.jsx lines 51–136 (`architectureLayers`) — eight-layer system description
- AIUsage.jsx lines 138–151 (`finalPipeline`) — pipeline chain
- AIUsage.jsx lines 153–166 (`capabilityGroups`) — skill boundaries per tool
