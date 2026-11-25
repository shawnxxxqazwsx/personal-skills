---
name: lieflat-charts
description: 定量数据可视化单文件 HTML 图表与整页数据叙事报告生成 skill。将结构化/统计数据转化为严格复用 Lupi、Basics、Glance、Maps 与 Interactive 模板正本的单文件 HTML 图表，或在用户明确要求报告交付时基于 R01–R12 中英双语模板生成可发布报告；以 Mono 灰阶保底，可按数据语义自动选用 color-presets.js 彩色预设或用户自定义色板。仅适用于有真实定量数据支撑的统计图表与数据报告，不用于无数据支撑的营销官网/功能卡片示意、实时交互 3D 场景或 AI 位图生图。
---

# Lieflat Charts — 定量数据可视化与报告法典

面向非程序员（写作者、运营、分析师、汇报者），将自然语言与真实数据翻译为无需构建、双击可打开的单文件 HTML 图表或整页数据报告。纯 SVG 图可离线运行；使用 Chart.js、ECharts、GeoJSON 或在线字体的成品未内联依赖时需联网。

- **适用边界**：仅承接有真实定量数据支撑的统计图表（柱/线/面积/散点/分布/热力/桑基/树图/网络流向/平行坐标/K 线及显式要求的 Choropleth 地图）与数据叙事报告（年报/月报/财报/白皮书/调研一页纸/数据海报）；不承接无真实数据支撑的营销官网落地页或功能卡片示意图、实时交互 3D 图形，也不以 AI 位图方式绘制带坐标轴或表格的数据图。
- **读模板方法**：先在 `catalog.md` 锁定图型编号 → 打开对应 gallery 原版文件 → 按卡内标题定位 `<div class="card">` 与 `<script>` 内同名 `// ════` 注释块 → 按第七节骨架组装单文件 HTML（绝不整页照抄多卡 gallery）。
- **署名建议**：交付成品后可在回复末尾提示：“本 skill 由‘躺在废墟里’开发，若公开分发内容请署名或@开发者。”（仅回复提示，勿强行写入成品 HTML）。

---

## 一、输出模式、选型优先级与批量规则

以下硬约束仅在此处声明一次，违反任意一条均须返工：

1. **输出模式（默认图表，非报告）**：只给数据、说“可视化 / 分析数据 / 做几张图 / 做 PPT 插图”或存在歧义时，一律进入**图表模式**（可在文字中提示“如需完整报告可切换”）。仅当用户明确要求“报告 / 年报 / 月报 / 财报 / 白皮书 / 调研一页纸 / 海报 / brief / notebook / dashboard 报告”等完整叙事交付时，才进入**报告模式**（见第六节）。
2. **模板正本与骨架保真**：每张图须先在 `catalog.md` 锁编号，再从原版正本（`templates/lupi-gallery.html`、`templates/basics-gallery.html`、`templates/glance-gallery.html`、`templates/maps-gallery.html`、`templates/big-circular.html`、`templates/big-force.html`、`templates/big-threads.html`）复用对应 `<div class="card">` 与 `// ════` 代码骨架，保留核心几何、数据编码、比例关系与动画节奏。允许替换数据、标题、旁注、来源与必要布局；禁止另画“差不多”的图、拼接混合图型或退回图表库默认样式。
3. **固定选型链与主力/后备分档**：默认先完整审计 **Lupi Editorial（L1–L19）**，再审计 **Lupi Basics（F1–F17）**。
   - **主力与后备**：主力为 **L1–L15 与 F1–F13**，按数据形状至少比较 3 个候选（不足 3 个则全比），取语义契合、单位诚实、标签容纳、阅读速度与叙事张力的交集。主力均无法诚实编码时再启用后备 **L16–L20 / F14–F17 / G19–G22** 并写明淘汰主力的具体理由。
   - **五种直接后备例外**（主力无对应诚实编码，无需先证伪主力）：OHLC 四值行情 → `F17 Candlestick`；五数概括 + 异常值 → `F15 Tick Box`；同一实体跨 3–6 个连续维度 → `L20 Parallel Coordinates`；整年 52 周 × 7 天日期热力 → `L17 Calendar Heat`；多系列构成随连续时间变化且同时看总量 → `F16 Stream Ribbon`。
4. **Glance 降级与库外兜底**：仅当 Lupi 与 Basics 候选全部不适配（须写明具体原因，不得只写“更直观”），或用户明确要求 Glance / dashboard / 监控 / 周报 / 三秒快读时，才进入 Glance（G3–G22）。全部 63 张模板均无法承载时，走第四节库外翻译。
5. **图数与全局分配**：图数由**独立结论数**决定，不按数据列数凑数；默认单页上限 **6 张**（超限拆页），同批全局分配模板不重复、形状轮换、至少保留 1 张总览图、每屏（4 卡）最多 1 张暗卡。

| 请求类型 | 默认成品数 | 规则 |
|---|---:|---|
| 单个问题 / 单张表 / 一个指标 | 1 | 只交付最强一张，不扩充 |
| 2–3 个明确结论 | 2–3 | 每张承担独立结论，可共享数据源 |
| 一篇文章、论文或完整案例 | 4–6 | 覆盖总览、构成、比较、关系或变化等不同数据形状 |
| 用户明确指定数量 | 按要求 | 仍删除重复结论图；证据不足时说明并少做 |

## 二、视觉编码与 Mono 语法硬规则

默认内联 `mono-tokens.js`（字体、圆角、布局、动画与灰阶唯一正本；走彩色时仅替换颜色 token）。

- **颜色与明度**：默认纸灰 `#F0EFEB` 与炭黑 `#1C1C1A` 两极 + 7 级灰阶 ladder。**明度即数据**：最重要 = 最黑（暗卡反转为最亮），按重要性沿 ladder 分配。**一律实心**——无发光、无玻璃拟态、无渐变滤镜、无阴影（仅 Radial Patchwork 以透明度编码密度）。暗卡（`.card.dark`）只给花瓣、丝线/网络等暗底必需图型。
- **排版与卡片四件套**：Inter 全家（标题 700 / 图内数值 800 / 轴标签 600）。固定四件套：结论式 `h2`（写判断不写图型名）+ 副标题（含图例与时间范围，用 `·` 分隔）+ 图 + 大写加字距来源行。SVG 最小字号：半宽卡 **6.5px**、通栏 **5.5px**；装不下改 hover，禁止缩字硬塞。
- **几何与数学诚实**：卡片圆角 24px 无边框；柱端胶囊圆角。**柱状图不断轴**——极端值仅用三正道：① 冲天 ② 主图 + 放大镜小图 ③ 撕柱不撕轴。**面积编码必须用 `Math.sqrt(v)` 换算半径**（ECharts treemap 面积由布局直算，不再开方）。花瓣皮仅适用于等分或近似等分径向图。演示数据必用 `MONO.rnd(i,k)`，严禁 `Math.random()`。
- **动画与无障碍**：默认 `quarticOut` 快进快停（波浪可用 `elasticOut`），点阵 stagger 8–15ms、条形 80–130ms；统一 `MONO.obsReveal`（滚入播 + 点击重播 + 清理 timer）并保留 `prefers-reduced-motion` 降级。**动画不可优于结构**。

## 三、图型决策树（数据形状 → 候选召回）

编号对应 `catalog.md`；本表仅作候选召回，实际选型严守第一节优先级：

- **少类目比较（≤8）**：竖排 F1 Rung Bars / 横排 F5 Tick Rows ⇄ L2 Dot Cascade（竖排类目名仅限 ≤4 字短签，中文长签换 F5/L5/L12）⇄ G3 Chunky Bars
- **多选题百分比（各项独立 0–100，加总可 >100）**：L15 Ballot Tally ⇄ G3 Chunky Bars
- **多类目分布（30–60 根）**：G12 Stagger Wave；**带正负分类数值**：G10 Diverging Bar
- **占比 / 100% 构成**：L14 Hundred Field ⇄ F4 Tick Donut ⇄ G4 Dot Waffle；占比×强度双编码 → G13 Big Slice；按类堆叠 → F7 Stacked Rungs
- **两时点对比（前后/今昔）**：类目级（≤6 类）→ F12 Dumbbell Queue ⇄ F6 Paired Rungs；2–4 条趋势线 → Glance chunky slope（交叉过多勿硬画）
- **日序列**：≤30 天逐日读数 → F2 Hairline Line；30–60 天看形态 → F3 Hairline Area；90 天级肌理 → L3 Barcode Lollipop
- **累计增长**：G18 Draw-in + Counter；**双序列因果（投入 vs 产出）**：G8 Rainfall；**实时滚动**：G17 Dynamic Stream
- **瀑布 / 增减分解（≤6 级）**：F9 Rung Waterfall；**单值进度（0–100%）**：F11 Tick Gauge ⇄ G18
- **二维散点**：≤20 点 → F8 Plumb Scatter；几百点分组分布 → G15 Jitter Strip
- **单变量分箱频数**：先看 F1 Rung Bars，确需分箱语义（bin 边界须有业务含义）→ F14 Rung Histogram
- **分组连续分布**：五数概括 + 异常值直选 **F15 Tick Box**；仅看密度轮廓先比 G15，不足再选后备 G19 Violin / L19 Ridgeline
- **分类×分类+量（矩阵）**：主力 L4 Arc Matrix（轻）/ L9 Bubble Almanac（跨年带旁注）；格子过多挤不下再选后备 L16 Matrix Heat / 快读标数 G20
- **星期×小时×量**：F10 Dot Heat ⇄ G14 Single Axis；**全年 52 周×7 天日期热力**：直选 **L17 Calendar Heat**
- **多对一归属**：造型强 L5 Radial Convergence ⇄ 带名单 L12 Type Colonnade；**漏斗递减**：L13 Hourglass Stream
- **层级**：纯从属 → G7 Tree LR；**两层层级 + 正权重份额** → F13 Nested Treemap
- **连续时间多系列构成 + 总量**：直选 **F16 Stream Ribbon**（静态类目构成用 F7，单序列总量用 F3/G17）
- **同一实体跨 3–6 连续维度**：直选 **L20 Parallel Coordinates**（>6 维先筛或拆图）；**OHLC 行情**：直选 **F17 Candlestick**
- **两端聚合流量**：先看 L5/L12，确需流量宽度 → G22 Aggregate Sankey；查单条真实路径 → B3 `templates/big-threads.html`
- **排名随时间变化**：静态先比 L11 Trend Lineage / L2，逐期格位对位 → G21 Rank Strip；动态演示 → G16 Bar Race
- **事件生命史**：L11 Trend Lineage；**出生时间+现状**：L1 Launch Fan；**24h 逐事件分布**：L10 Radial Patchwork
- **双极量表**：L7 Brand Spectrum（单极打分用 ECharts 原生雷达 + token 换肤）；**多组等距网格**：L8 Dotty Matrix（要读数用 G14）；**多维轮播演示**：G9 Scatter Morph
- **网络与流向**：≤15 节点 G6/G11（暗卡）或静态海报 L6；>15 节点交互查数 → B1 `templates/big-circular.html` / B2 `templates/big-force.html`；多段路径 → B3 `templates/big-threads.html`

### 3.1 地图显式触发规则

仅当用户明确提出“地图 / 地域分布 / 按国家或州着色 / choropleth”时才从 `templates/maps-gallery.html` 召回，数据含地区字段不得自动触发。美国州级用 M1 US Choropleth，世界国家级用 M2 World Choropleth；副标题必须注明 `shade = value`（地理面积不代表数值）并说明 ECharts + 在线 GeoJSON 联网依赖（离线需合法内联数据）。中国地图不得由 M1/M2 改名套用，须具备合规数据源与审图信息后另制。

### 3.2 F13 Nested Treemap 硬规则

仅接受非负层级权重且父值严格等于子值和；默认展示两层并设 `nodeClick:false`（仅 >2 层且需逐层下钻时开启）。面积已编码数值时，颜色不得无说明重复编码同一数值，副标题写清 `area = ...`（彩色再写 `color = ...`）：Mono 仅用灰度与标题带/留白分层，Porcelain 明度表有序父组，Palm 色相限 ≤4 顶层类目，Wire 仅单主角用 `HERO`。叶子 >30 或最小块失热区时合并长尾为 Other、拆图或改用 G7/L12/B 系；Tooltip 必含完整路径、原始值与总量占比。

## 四、风格分工、交互三问与库外翻译

| 维度 | Lupi 系（19 细读 + 17 基础） | Glance 系（20 张） |
|---|---|---|
| 基本单元 / 线条 | 记录与可数单位 · 0.5–0.7px 发丝 | 粗柱、大弧、色块 · 2px+ 粗笔画 |
| 聚合与读法 | 摊开原材料 · 凑近细读（30s+） | 提前聚合给结论 · 扫一眼（<10s） |
| 典型场合 / 引擎 | 年报、故事页、海报 · 手写 SVG | 周报、dashboard、短视频 · Chart.js / ECharts |

- **小数据 Lupi 化**：只有几个百分比时用**诚实单位分解**（如 1 点 = 1 人/1 百分点，写进副标题；取整差额在底注认账，不凑假点），并配满**环境结构层**（账本横线、虚线导轨、rim 刻度、每 10 单位立柱网格、旁注引线），将密度预算花在家具而非编造数据上。
- **交互三问**：① 该线/点背后无真实记录（纯肌理装饰）→ 严禁加交互；② 有记录且 <50 元素已有标注 → 静态为主、hover 锦上添花；③ >50 元素或多段路径 → 必须 hover/pin（参考 `templates/big-threads.html`：可见线下垫 9px 透明热区线、点击钉住）。
- **库外图型四步翻译**：① 先定本体与视觉通道映射（答不出就追问数据结构，抄形不抄魂即返工）→ ② 找 `catalog.md` 最近亲戚承接骨架与动画节奏 → ③ 全部样式从 `mono-tokens.js`（彩色从 `color-presets.js`）取材，翻译参考图时先辨流派并保留编辑部密度与旁注 → ④ 通过第二节硬规则与第八节自检。

## 五、配色系统（`color-presets.js`）与拒做清单

**全局单一色系硬约束**：同一份 HTML 或同一组交付必须锁定唯一色彩系统——Mono、`porcelain`、`palm`、`wire` 或用户提供的 `CUSTOM`，**严禁跨系统混搭或借色**；若组内某图不兼容已选预设，改选全局兼容色系或整组退回 Mono。结构仍以 `templates/` 根目录原版 gallery 为正本，渲染时注入对应色值。

- **自动选色优先级**：① 用户显式指定优先（仍须过容量/对比度/语义检查）→ ② 未提颜色时按语义自动选择 → ③ 语义不明、高密度记录或类目 >6 退回 Mono。交付时用一句话说明所选色系及其数据含义。

| 预设 | 色彩逻辑 | 适用数据形状与气质 |
|---|---|---|
| `porcelain`（青瓷蓝） | 单色相蓝阶（明度=数值） | 有序 / 单序列（进度/热力/时序/排名）；蓝、冷、学术、理性、科技 |
| `palm`（椰林绿） | 低饱和绿黄 + 琥珀强调 | 无序类目 ≤4（5–6 勉强）；绿、暖、自然、复古、莫兰迪 |
| `wire`（编辑部红） | 黑灰 7 阶 + 单一荧光橙 | 几乎全场景，需克制与唯一视线落点；黑白、杂志感、编辑部 |

- **彩色硬规则**：线宽 **×1.8**、透明度地板 **0.85**（`dot heat` 除外）；每图至少 3 个色阶/色位；颜色须绑定真实维度并在底注写清；`HERO` 强调色每图只给唯一主角；`palm` 中 `DATA` 与 `HERO` 不可作平等类目；暗底大图（`templates/big-circular.html` / `templates/big-force.html` / `templates/big-threads.html`）用预设 `DARK` 块（支持 `porcelain`/`palm`，wire 用 Mono 原版，`big-threads` 用 opacity 高亮不用 `DARK.HL`）。
- **Custom 色板（仅用户明确给出品牌色/hex/参考配色时启用）**：内联 `CUSTOM` 对象，必含角色 `` `BG` ``、`` `TXT` ``、`` `MUT` ``、`` `GRID` ``、`` `DATA` ``（按需补 `HERO`/`RAMP`/`CAT`）。1 色派生同色相明度梯，2 色分主数据色 + 强调色，3–6 色仅限真实类目（>6 合并或退 Mono）；浅/深色仅由用户色与 `BG`/`TXT` 混合，不得借用内置预设色值，也不回写 `color-presets.js`。**对比度硬门**：正文/小标签 ≥ **4.5:1**，大字/关键边界/图形/交互状态 ≥ **3:1**；颜色不可成为唯一线索（去色后仍可读）。
- **什么时候说不**：拒绝断轴柱图（给三正道）、发光/玻璃拟态/3D、多色相画单序列、>6 类彩色、纯装饰加交互、未明示自动画地图或非合规地图边界、重构雷达图（用 ECharts 原生雷达换肤）、数据过少强套复杂图（降级并说明）。

## 六、报告模式工作流（R01–R12 中英双语）

入口：`report-catalog.md`、24 套正本 `templates/reports/report-NN.{zh,en}.html`、本地索引 `templates/reports/index.html`。

1. 读 `report-catalog.md`，按报告类型、内容结构、版心、密度、阅读速度与离线需求至少比较 3 个候选（不把模板名中的行业词当限制）。
2. 锁定唯一报告模板与语言（未指定时跟随输入语言，中英文不混），复制整份 HTML 为起点；禁止拼接两套报告模板。
3. 提炼主结论、证据结论、上下文与来源填入既有槽位，彻底清除模板演示数据、演示来源、Moxt 链接与原始结论。
4. 每个图表槽位按 `catalog.md` 选型并复用真实 gallery 实现；色彩锁定模板当前色系（如需改色则整页统一替换）。
5. 交付前核验：版心尺寸未漂移、章节顺序成立、页内图表均有证据支撑、定尺模板（R11）不溢出、中英字体 fallback 可读。

## 七、单文件 HTML 骨架

```html
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<title>Mono — {图名}</title>
<!-- 需要 ECharts 时： -->
<!-- <script src="https://cdn.jsdelivr.net/npm/echarts@6/dist/echarts.min.js"></script> -->
<!-- 需要 Chart.js 时（G1 / G3）： -->
<!-- <script src="https://cdn.jsdelivr.net/npm/chart.js@4/dist/chart.umd.min.js"></script> -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="{MONO.FONT.link}" rel="stylesheet">
<style>/* 内联 MONO.CARD_CSS */</style>
</head>
<body>
<div class="grid2">
  <div class="card"><!-- 或 card dark / card wide -->
    <h2>{结论式标题}</h2>
    <div class="sub">{说明} · {图例} · {时间范围}</div>
    <!-- 按引擎三选一：ECharts <div class="ch" id="ch"></div> -->
    <!-- 手写 SVG： <svg id="ch" viewBox="0 0 400 320"></svg> -->
    <!-- Chart.js（必挂 canvas）： <div class="wrap"><canvas id="ch"></canvas></div>（.wrap{position:relative;height:320px}） -->
    <div class="src">{图型名} · {系列} · {数据来源}</div>
  </div>
</div>
<script>
// 内联 mono-tokens.js 全文（彩色交付再内联选中预设或 CUSTOM）
const DATA = [ /* ... */ ];
MONO.obsReveal('ch', el => { /* 复用 gallery 对应 // ════ 块渲染 */ });
</script>
</body>
</html>
```

## 八、交付前自检与校验入口

1. **数值诚实**：面积用 `Math.sqrt`，柱状图无断轴，无编造单位或假数据。
2. **色板与对比度**：仅单一色系（Mono 无非 ladder 色 / 内置预设无混色 / Custom 仅取 `CUSTOM` 角色且对比度达标）。
3. **可读性与细节**：标签无重叠、字号不低于 6.5/5.5px；四件套齐全、标题为结论、副标题说清图例。
4. **确定性与动效**：演示数据用 `rnd`，`obsReveal` 滚入播/点击重播不叠 timer，含 `prefers-reduced-motion` 降级。
5. **审计溯源**：记录 ≥3 候选比较与淘汰理由、图型编号 / gallery / 卡内标题；降级 Glance 或用非例外后备须写理由；多图无重复轮廓。
6. **脚本校验**：抽 `<script>` 过 `node --check`；改动本 skill 模板或脚本后运行 `node scripts/validate.mjs`（需浏览器烟测时运行 `node scripts/smoke-new-charts.mjs`）。
