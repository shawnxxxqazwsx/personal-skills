# Web Research — Reference

专业检索补充材料（配合 `SKILL.md` 使用）。

## Query Templates

```
{Product} {Version} {Feature} official documentation site:{official-domain}
{Product} {Version} {Feature} changelog OR release notes {Year}
"{Error message exact string}" {Product} {Version}
{Product} vs {Alternative} {Year} comparison {specific criterion}
"{Paper title}" {First author} {Year} (site:arxiv.org OR DOI)
{Topic} review OR survey {Year} filetype:pdf site:arxiv.org
site:github.com {org}/{repo} {issue keyword}
site:scholar.google.com {topic}  → then open the real DOI/arXiv from the hit
```

### Technical / Pricing / API

| Topic | Example query |
|---|---|
| API / Docs | `{Product} {Version} {SymbolOrAPI} site:{official-docs-domain}` |
| Plan / Pricing | `{Provider} {PlanOrModel} pricing per million tokens site:{official-domain}` |
| Breaking changes | `{Framework} {Version} migration guide OR breaking changes site:{official-domain}` |

### Academic

| Topic | Example query |
|---|---|
| Known paper | `"{Exact title}" {author} {year} site:arxiv.org` |
| By DOI | `https://doi.org/{doi}` then fetch |
| Survey | `{field} survey OR "systematic review" {year}` then land on publisher/arXiv |

### Consumer / Second-Hand (Audio Example)

| Topic | Example query |
|---|---|
| 国行 MSRP | `{Model} site:store.kef.cn OR site:kef.com` |
| 港二手 | `{Model} 二手 site:post76.hk OR site:review33.com` |
| 欧美二手 | `{Model} used pair site:audiogon.com OR site:ebay.com` |

---

## Academic & Papers

```
[ ] Prefer primary: arXiv abs/pdf, doi.org, ACM/IEEE/ACL Anthology, journal page
[ ] Fetch landing page — confirm title, authors, year
[ ] In 依据: Title (Authors, Year) + URL + DOI or arXiv id
[ ] Never invent citations; reject broken DOI / SEO paper farms
[ ] Preprints: label preprint; don't invent venue
[ ] Quotes: prefer full text; else verified abstract only + say so
```

Trusted domains: `arxiv.org/abs/`, `arxiv.org/pdf/`, `doi.org/`, `aclanthology.org/`, `openreview.net/`.

---

## Market & Second-Hand Pricing

```
[ ] Model matrix first (revisions, mkI/mkII, active/passive)
[ ] Official MSRP (unit vs pair, currency, date)
[ ] Regional + global listings; classify sold | asking | dealer | MSRP
[ ] Reject price-aggregator scrapers (BigGo/Feebee/ZOL) as 成交; reject search-summary prices
[ ] Report band (low–high), not false precision
```

| Region | Domains |
|---|---|
| CN / HK | `erji.net`, `post76.hk`, `review33.com`, `dcfever.com` |
| Global audio | `audiogon.com`, `ebay.com`, `hifizero.com` |

---

## Official Domains

| Area | Domains |
|---|---|
| Anthropic / OpenAI | `docs.anthropic.com`, `platform.openai.com` |
| Web / Standards | `developer.mozilla.org`, `w3.org`, `ietf.org` |
| Papers | `arxiv.org`, `doi.org`, `aclanthology.org`, `openreview.net` |

---

## Obscure Entity & Media Hunts

```
[ ] Anchor EN/CN title, developer, App ID, year, platform
[ ] Unique tokens + explicit exclusion list for lookalikes
[ ] Registry/API lookup; media + regional search rounds
[ ] Verify actual video/image frames; none → 未找到
```

```
"{Exact Title HD}" (gameplay OR trailer) {Developer}
itunes.apple.com/lookup?id={AppID}
"{Exact Title}" (archive.org) {Developer}
```
