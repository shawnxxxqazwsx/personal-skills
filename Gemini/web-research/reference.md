# Web Research — Reference

原生 `swarm` 调研的拆片模式、看板交叉核验与领域检索速查（配合 `SKILL.md` 使用）。

## Swarm Sharding & Cross-Check Patterns

按独立证据维度拆分 `tasks: [...]`（3–8 路，不重叠、不凑数），每片只跑对应来源并带回已打开 URL 与原页证据：

| 场景 | 建议路数 | `tasks: [...]` 拆片角度 |
|---|---|---|
| 技术文档 / API | 3–5 路 | ① 官方文档与符号签名（`site:` 官域）；② Changelog / Release Notes / Migration 变更边界；③ Maintainer GitHub Issues / PR 反证与已知限制；④ 平台/版本差异或竞品对照（按需） |
| 学术论文 / 标准 | 3–6 路 | ① 论文主键页（arXiv / DOI / 出版社 PDF，核对题名/作者/年份）；② 复现代码、勘误与 OpenReview 审稿讨论；③ 同主题综述与反例/后续对比；④ 行业标准 / RFC / W3C 规范条款（按需） |
| 产品对比 / 行情定价 | 4–8 路 | ① 型号谱系与改款矩阵（mkI/mkII、规格、年份）；② 官方 MSRP / 订阅定价页（币种、单只/一对、日期）；③–⑤ 分区二手成交/挂牌（按国行/港台/欧美/日区拆片）；⑥–⑧ 参数横评、保修政策与通病（按维度拆） |
| 冷门实体 / 媒体溯源 | 3–6 路 | ① 注册表与商店 API（App Store lookup、SteamDB、Wayback）；② 原语种/英文开发者与发布史；③ 中/日/韩跨语种别名与社区线索（附排除词）；④ 实机视频/截图帧验证（YouTube / B站 / archive.org） |

### 看板交叉核验与热复用

- **冲突定向复核**：发现 `#12` 与 `#15` 口径/价格/版本矛盾时，直接点名原工人复查，例如 `@research-2 复核 #12 与 #15 的币种、单只/一对与生效日期，打开原页确认`；严禁仅凭多数票裁决。
- **追问热复用**：`waiting` 状态的工人保留检索上下文，追加细化直接 `@research-3 基于 #18 补查 v2.4 迁移破坏性变更`，无需重建工人；仅在新增独立维度时追加 `tasks`。
- **去重与收口**：合并前按原始主键去重（同源转载只计 1 条独立证据）；无法消除的分歧并列列出并注明日期与适用条件。

---

## Query Templates

```text
{Product} {Version} {Feature} official documentation site:{official-domain}
{Product} {Version} {Feature} changelog OR "release notes" {Year}
"{Error message exact string}" {Product} {Version}
{Product} vs {Alternative} {Year} comparison {specific criterion}
"{Paper title}" {First author} {Year} (site:arxiv.org OR DOI)
{Topic} review OR survey {Year} filetype:pdf site:arxiv.org
site:github.com {org}/{repo} {issue keyword}
site:scholar.google.com {topic}  → 从命中结果跳转并抓取真实 DOI / arXiv 页
```

### Technical / API / Pricing

| Topic | Example query |
|---|---|
| API / Docs | `{Product} {Version} {SymbolOrAPI} site:{official-docs-domain}` |
| Plan / Pricing | `{Provider} {PlanOrModel} pricing per million tokens site:{official-domain}` |
| Breaking changes | `{Framework} {Version} "migration guide" OR "breaking changes" site:{official-domain}` |

### Academic

| Topic | Example query |
|---|---|
| Known paper | `"{Exact title}" {author} {year} site:arxiv.org` |
| By DOI | `https://doi.org/{doi}` → 直接抓取落地页 |
| Survey | `{field} survey OR "systematic review" {year}` → 落地出版社/arXiv |

### Consumer / Second-Hand (Audio Example)

| Topic | Example query |
|---|---|
| 国行 MSRP | `{Model} site:store.kef.cn OR site:kef.com` |
| 港台二手 | `{Model} 二手 site:post76.hk OR site:review33.com` |
| 欧美/日二手 | `{Model} used pair site:audiogon.com OR site:ebay.com OR site:hifido.co.jp` |

---

## Academic & Papers

```text
[ ] Primary first: arXiv abs/pdf, doi.org, ACM/IEEE/ACL Anthology, publisher page
[ ] Fetch landing page — verify exact title, authors, year
[ ] Citation format: Title (Authors, Year) + URL + DOI or arXiv ID
[ ] Never invent citations; reject broken DOI / SEO paper farms
[ ] Label preprints explicitly; never invent peer-reviewed venues
[ ] Quote from full text when possible; if abstract-only, state so
```

Trusted domains: `arxiv.org/abs/`, `arxiv.org/pdf/`, `doi.org/`, `aclanthology.org/`, `openreview.net/`.

---

## Market & Second-Hand Pricing

```text
[ ] Model matrix first (revisions, mkI/mkII, active/passive)
[ ] Anchor official MSRP (unit vs pair, currency, date)
[ ] Split regional + global listings; tag sold | asking | dealer | MSRP
[ ] Reject price-aggregator scrapers (BigGo/Feebee/ZOL) as 成交; reject search-summary prices
[ ] Report range band (low–high) + condition/month, not false precision
```

| Region | Domains |
|---|---|
| CN / HK | `erji.net`, `post76.hk`, `review33.com`, `dcfever.com` |
| JP | `hifido.co.jp`, `auctions.yahoo.co.jp`, `mercari.jp` |
| Global | `audiogon.com`, `ebay.com`, `hifizero.com` |

---

## Official Domains

| Area | Domains |
|---|---|
| AI APIs | `docs.anthropic.com`, `platform.openai.com`, `ai.google.dev` |
| Web / Standards | `developer.mozilla.org`, `w3.org`, `ietf.org`, `datatracker.ietf.org` |
| Papers | `arxiv.org`, `doi.org`, `aclanthology.org`, `openreview.net` |

---

## Obscure Entity & Media Hunts

```text
[ ] Anchor multi-language titles (EN/CN/JP/KR), developer, App ID, release year, platform
[ ] Pair unique tokens with explicit `-lookalike` exclusion terms
[ ] Run registry/API/Wayback lookup before media & regional forum rounds
[ ] Inspect actual video/image frames; unverified or mismatched title → 排除 / 未找到
```

```text
"{Exact Title}" (gameplay OR trailer OR 实机) {Developer} -{Lookalike}
("{EN Title}" OR "{原语种译名}") {Developer} {Year}
https://itunes.apple.com/lookup?id={AppID}
"{Exact Title}" site:archive.org {Developer}
```
