---
name: web-research
description: >-
  Antigravity-only web-research (ignore .agents/skills/web-research and
  .claude/skills/web-research). Multi-source web research requiring at least
  three parallel Antigravity native Gemini 4 Hydrogen subagents
  (`invoke_subagent` `Model: "flash"` or native `swarm` `gemini-4-hydrogen-*`,
  never Magpie proxies) plus lead-agent synthesis with verified live URLs and
  papers (fetch before cite). Auto-apply for technical docs, APIs, papers,
  product compare, market pricing, policy tables, obscure-entity/media hunts, or
  @web-research / 调研 / look up sources. Consult official Anthropic docs for
  Anthropic/Claude questions.
---

# Web Research（Antigravity 版 — 原生 Gemini 4 Hydrogen）

> **独立 harness 版本**：仅限 Antigravity（`~/.gemini/config/plugins/cursor-skills/skills/web-research/`），忽略工作区 `.agents/skills/web-research/` 与 `.claude/skills/web-research/`。

目标：**准、全、可复核**——结论可跟、依据可点开、论文/链接须经抓取确认。**错误正例差过「未找到」，严禁编造 URL / DOI / 文献。** 范围：技术文档、API、学术论文、产品/政策/行情对比与冷门实体溯源。

## 原生三路并行检索与核验（强制）

任何深度（含 Standard 与单事实查询）均强制满足以下规则，不得以任务简单或主代理自行搜索为由省略：

1. **三路同轮原生 Hydrogen 派发（主代理不计入）**：
   - 先调用 `define_subagent(Name: "agy-worker-ro", EnableWriteTools: false, EnableSubagentTools: false, ...)` 建立只读防递归联网工人（确保具备 `search_web` 能力且物理禁写、禁递归）。
   - 在**同一回合**并行派发**至少 3 个**独立 Antigravity 原生 Gemini 4 Hydrogen 子代理：`invoke_subagent(TypeName: "agy-worker-ro", Model: "flash", ...)`（若已在活跃原生 `swarm` 中或需指定强度，亦可用原生 `swarm` `gemini-4-hydrogen-medium|high|xhigh`）。**先全部派发再等待**，严禁逐个串行；严禁调用 `magpie-agent` / `cursor:magpie_agent` 或任何反代路线（用户当前显式点名其他模型时从用户指定）。
2. **明确分工与完整任务包**：将任务拆成 ≥3 个明确方向（窄题可分：主来源定位 / 独立交叉核对 / 反证与版本边界冲突），不得为凑数引入无关议题。每个子代理须收到完整中文任务包（问题、实体/版本/日期、来源要求、返回格式），实际检索并打开页面，返回结论、已打开 URL、页面证据、适用时间/版本与冲突缺口（无结果时返回实际查询与失败范围）。仅做摘要或审阅的代理不计数；子代理不递归派生。主代理可同步补查但不抵扣 3 路数量。
3. **独立 `conversationId` 与合规门槛**：逐一核验宿主返回的 **至少 3 个不同 `conversationId`**（或 3 名独立原生 `swarm` Hydrogen 工人）均真实执行了 `search_web` 与只读抓取。单代理多轮检索/并发查询均不能替代 3 个独立子代理。创建失败、未检索或落入非 Hydrogen/反代路线的均不计数，须重派或用 `send_message(Recipient: "<conversationId>", ...)` 组织合规并行轮次（禁事后串行冒充）；若环境并发受限无法满足，须如实说明，不得静默降级后宣称完成。
4. **原生额度耗尽降级**：当 Antigravity 原生 `Gemini · 7 days` 或 `5 hours` 窗口为 `0%` 或 Hydrogen 不可用时，**严禁静默切往 Magpie 反代模型**；改由主代理直接用 `search_web` + 只读抓取按同等验证标准完成，并在交付中注明“因原生 Gemini 额度耗尽/Hydrogen 不可用，由主代理直查”。
5. **主代理核验与仲裁整合**：收齐 ≥3 份报告后，主代理亲自打开拟写入最终答案的全部 URL 核验是否支持主张，按实体/原始来源去重（同源转载不算独立证据）；冲突依原始证据、日期、版本、地区与口径仲裁（不按代理多数票），无法裁决时明示分歧。Anthropic/Claude 问题优先查 Anthropic 官方文档；OpenAI/Codex 查 OpenAI 官方开发者文档。

## When / Scale

| Need | Depth |
|---|---|
| 单事实、报错、官方价格、API 签名 | **Standard**：定位并抓取直接支持结论的主来源；有冲突再补检 |
| 对比、行情、政策表、全面调研 | **Deep**：按独立子问题与冲突扩展，直至证据覆盖或明确停止 |
| 论文 / 学术主张 | **Academic**：优先 DOI / arXiv / 出版社页；见 [reference.md](reference.md#academic--papers) |
| 旧应用 / 实机视频 / 下架软件 | **Obscure**：身份锚定 → 验证 → 负结论 OK；见 [reference.md](reference.md#obscure-entity--media-hunts) |

## Workflow & Stopping

1. **Classify**：时效、版本、名称撞车、论文还是产品页？
2. **Anchors & Dispatch**：实体全名 + 消歧项（开发商 / ID / 作者 / 年份），同轮并行派发 ≥3 路原生 Hydrogen。
3. **Search Rounds**：A 官方/主键（`site:`、商店 API）→ B 实务（GitHub、论坛、SO）→ C 学术（Scholar 线索 → DOI/arXiv 落地页）→ D 补洞（去过时与 SEO 污染）。
4. **Collect & Verify**：收齐 ≥3 路报告，主代理逐项抓取核验拟引用 URL，失败剔除。
5. **Synthesize**：去重、仲裁冲突、统一输出，缺口进「未覆盖」。

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

- 凭记忆答时效/需引用的问题；仅单路搜索或只贴搜索摘要；**编造** DOI/链接；未打开即引用视频/论文；用近似结果充依据；二手将比价爬虫当成交或混入未标注新价。
