---
name: web-research
description: >-
  Antigravity-only web-research (ignore .agents/skills/web-research and
  .claude/skills/web-research). Multi-source web research requiring at least
  three parallel Antigravity native swarm Gemini 4 Hydrogen workers
  (`gemini-4-hydrogen-medium|high|xhigh`, never Magpie proxies) plus lead-agent
  synthesis with verified live URLs and papers (fetch before cite). Auto-apply
  for technical docs, APIs, papers, product compare, market pricing, policy
  tables, obscure-entity/media hunts, or @web-research / 调研 / look up sources.
  Consult official Anthropic docs for Anthropic/Claude questions.
---

# Web Research（Antigravity 版 — Swarm 原生 Gemini 4 Hydrogen）

> **独立 harness 版本**：仅限 Antigravity（`~/.gemini/config/plugins/cursor-skills/skills/web-research/`），忽略工作区 `.agents/skills/web-research/` 与 `.claude/skills/web-research/`。

目标：**准、全、可复核**——结论可跟、依据可点开、论文/链接须经抓取确认。**错误正例差过「未找到」，严禁编造 URL / DOI / 文献。** 范围：技术文档、API、学术论文、产品/政策/行情对比与冷门实体溯源。

## 原生 Swarm 三路并行检索与协作（强制）

任何深度（含 Standard 与单事实查询）均强制使用 Antigravity 原生 `swarm` 派发 Hydrogen 工人，**禁止走 `invoke_subagent` / `define_subagent`**，**严禁 Magpie 反代**（用户显式指定其他模型除外），不得以任务简单或主代理自查为由省略：

1. **建/复看板与同轮分片派发（≥ 3 路）**：
   - 若当前会话尚无活动 swarm，先调 `swarm(action: "title", title: "...")`，并向用户展示 `open_board` 链接；若已有活动 swarm，直接复用当前看板。
   - 同一回合通过 `tasks` 分片派发 **至少 3 个**独立 `research-1..k` worker（默认 `gemini-4-hydrogen-medium`，深挖/复杂溯源可选 `high|xhigh`；复杂主题按需扩至 5–10+ 路）：
     ```text
     swarm(action: "add", name: "research", model: "gemini-4-hydrogen-medium",
           workspace: "inherit", tasks: ["<角度1>", "<角度2>", "<角度3>", ...],
           brief: "<共享目标、实体/版本/日期锚点、只读核验纪律与返回格式>")
     ```
     异构角度可同轮并行多次 `swarm(action: "add", ...)`；**先全部派发再等待**，严禁串行凑数。
2. **只读分工与 Swarm 协作**：
   - 拆分为 ≥ 3 个不重叠方向（窄题拆：主来源定位 / 独立交叉核对 / 反证与版本边界冲突；分片与交叉核验模板见 [reference.md](reference.md#swarm-sharding--cross-check-patterns)）。
   - worker 均为只读 `workspace: "inherit"`，仅执行 `search_web` 与只读抓取，**严禁改文件、严禁再派生子代理**；须返回结论、已打开 URL、页面证据、适用时间/版本与缺口（无结果写明已试查询与失败范围）。
   - 发挥看板协作优势：**`#seq` 去重引用**（避免重复贴源）；出现来源/结论冲突时允许 peer 间直接 `@research-<k>` 交叉核验；后续追问直接 `@research-<k>` 热复用 `waiting` worker（零空闲 Token 消耗）。
3. **独立 `conversation_id` 门槛与唯一兜底**：
   - 逐一核验 **至少 3 个独立 `conversation_id`** 真实执行了检索与抓取（主代理不计入 3 路；仅摘要/审阅、失败或未实检者不计数，须重派补齐）。
   - **唯一兜底**：仅当原生 Gemini 池归零（`7d == 0%` 或 `5h == 0%`）或原生 `swarm` 工具故障时，由主代理直接调用 `search_web` + 只读抓取按同等标准完成，并在交付中如实告知原因；严禁回退 Magpie 反代。
4. **主代理核验与证据仲裁**：
   - 收齐 ≥ 3 份报告后，主代理亲自打开拟写入最终答案的全部 URL 核验主张，按原始来源去重（同源转载不算独立证据）；冲突依原始证据、日期、版本、地区与口径仲裁（不按代理多数票），无法裁决时明示分歧。
   - Anthropic / Claude 产品问题优先直查官方 Anthropic 文档（`docs.anthropic.com`）；OpenAI / Codex 查 OpenAI 官方开发者文档。

## When / Scale

| Need | Depth |
|---|---|
| 单事实、报错、官方价格、API 签名 | **Standard**：定位并抓取直接支持结论的主来源；有冲突再补检 |
| 对比、行情、政策表、全面调研 | **Deep**：按独立子问题扩至 5–10+ 路，直至证据覆盖或明确停止 |
| 论文 / 学术主张 | **Academic**：优先 DOI / arXiv / 出版社页；见 [reference.md](reference.md#academic--papers) |
| 旧应用 / 实机视频 / 下架软件 | **Obscure**：身份锚定 → 验证 → 负结论 OK；见 [reference.md](reference.md#obscure-entity--media-hunts) |

## Workflow & Stopping

1. **Classify**：时效、版本、名称撞车、论文还是产品页？
2. **Anchors & Swarm Dispatch**：实体全名 + 消歧项（开发商 / ID / 作者 / 年份），新建或复用 swarm 看板，同轮 `tasks` 分片并行派发 ≥ 3 路 `research-1..k`。
3. **Search Rounds & Cross-Check**：A 官方/主键（`site:`、商店 API）→ B 实务（GitHub、论坛、SO）→ C 学术（Scholar 线索 → DOI/arXiv 落地页）→ D 补洞；冲突用 `#seq` / `@research-<k>` 交叉核验。
4. **Collect & Verify**：核验 ≥ 3 个独立 `conversation_id` 报告，主代理逐项抓取核验拟引用 URL，失败剔除。
5. **Synthesize**：去重、仲裁冲突、统一输出，缺口进「未覆盖」；后续追问 `@research-<k>` 热复用。

**停止条件**：子问题已答，或两个独立权威来源在同口径下一致；锚点穷尽仍无结果 → **未找到**（不塞近似结果）。停止条件仅控深度，不跳过 3 路派发与收集。

## Query Craft

| Bad | Good |
|---|---|
| `WebAudio worklet` | `AudioWorkletProcessor process 128 frames site:developer.mozilla.org` |
| `transformer paper` | `"Attention Is All You Need" Vaswani 2017 site:arxiv.org` |
| `末日列车 视频` | `"Doomsday Express HD" Warp Dreams gameplay` + App ID |

规则：产品+版本+年份；官方用 `site:`；报错用原文；撞名用引号+开发商/ID；英文扩召回，用用户语言作答。更多模板见 [reference.md](reference.md)。

## Verify Before Cite（强制）

| 类型 | 最低验证 |
|---|---|
| 任意 URL 进「依据」 | **Fetch 成功**；404/空页/拦访 → **不引用** |
| 数字 / 政策 / 价格 | 抓取主键页；禁止仅信搜索摘要 |
| 论文 | 打开 **DOI / arXiv / 出版社页**；核对题名、作者、年份 |
| 软件是否在架 | 商店 / API lookup；0 结果 = 已下架 |
| 视频 / 实机 | 打开媒体；标题 ≠ 内容时排除 |
| 身份同一产品 | ≥ 2 锚点；仅标题不够 |

未抓取通过的不得写入「依据」；无法验证时标「未验证」或移出。

## Source Hierarchy

1. 官方文档 / changelog / 标准与法规 → 2. 官方博客、商店页、机构发布 → 3. 论文（DOI / arXiv / 学会与出版社）→ 4. Maintainer GitHub → 5. 员工论坛回复 → 6. 社区长文（须用 1–4 核对）→ 7. SEO 聚合（**最低**，不作唯一依据）。技术实现主张仅依赖 1–3；社区来源只作线索。

## Output & Market Pricing

```markdown
## 结论
[直接回答；对比可用表；否定结论说明已试范围]

## 依据（均已抓取确认）
- [标题](完整URL) — 支持要点（论文附：作者, 年份, DOI/arXiv）

## 易混淆 / 已排除（撞名或假阳性时必填）
- [标题](URL) — 排除原因

## 未覆盖 / 不确定
- …
```

**行情 / 二手**（详见 [reference.md](reference.md#market--second-hand-pricing)）：型号谱系先于价格 → 官零售价锚定+日期 → 按地区搜成交/挂牌 → 标清 `Sold / Asking / Dealer / MSRP`、单只 vs 一对、货币+月份、成色；无列表 URL 不引用。

## Anti-Patterns

- 凭记忆答时效/需引用的问题；绕开原生 `swarm` 走 `invoke_subagent` / `define_subagent` 或 Magpie 反代；仅单路搜索或只贴搜索摘要；**编造** DOI/链接；未打开即引用视频/论文；用近似结果充依据；二手将比价爬虫当成交或混入未标注新价。
