---
name: chlora-ui
description: 设计、实现或审查 Chlora 宿主界面（Strip、DraftRoom、公共弹层、原生文件选择器）及独立 CLR Router / CLR 3D Panner UI 的视觉语言、组件基线、色域、焦点、动效与数值交互规范。Stack v2 与 Chloe Input 为成熟参考基准；Device I/O 与 Analyzer 家族为专用受限表面。不负责 C++/CMake 构建部署或音频引擎实现，不约束第三方插件自身皮肤，不覆盖硬件 EQ DSP 拟合或通用 DAW 宿主操作。
---

# Chlora UI

让新增或修改的界面继承现行产品的布局、材料、控件语义、功能图形和运动方式。DraftRoom 指 Graph 工作区；DarkRoom / Repair 为独立工作区。

## 1. 文档分四层，按层读取

按层级从上往下查找，读到能回答当前问题的层级即停：

| 层 | 回答什么 | 文件 | 规范效力 |
|---|---|---|---|
| **L0 入口** | 任务路由、决策阶梯与全局边界 | 本文件 | 只做路由与硬边界，不存放常数 |
| **L1 任务** | 选 owner、走事务与最小验证入口 | [design-recipes](references/design-recipes.md)（六类配方）、[shared-controls](references/shared-controls.md)、[preset-workflows](references/preset-workflows.md)、[native-file-pickers](references/native-file-pickers.md)、[graph-routing-objects](references/graph-routing-objects.md)、[strip-roles](references/strip-roles.md)、[cl-router](references/cl-router.md) | 引用 L2 精确值；只给选型与流程 |
| **L2 规则** | 精确尺寸、颜色、字体、时序、状态与禁止项 | 索引 [design-navigation](references/design-navigation.md)（CU-* 卡）→ [foundations](references/foundations.md)、[components](references/components.md)、[motion](references/motion.md)、[numeric-fields](references/numeric-fields.md)、[numeric-validation](references/numeric-validation.md)、[webview-guardrails](references/webview-guardrails.md)、[theme-inheritance](references/theme-inheritance.md)；补充 [surface-patterns](references/surface-patterns.md) | 已批准规则为单一来源；`surface-patterns` 仅作现行实现参考 |
| **L3 证据** | 现存例外、源码映射、审查口径与图鉴 | [current-audit](references/current-audit.md)、[source-map](references/source-map.md)、[audit-workflow](references/audit-workflow.md)、[设计图鉴](assets/atlas/index.html#overview) | 不产生新规范；不覆盖高层规则 |

**冲突权威顺序：** 用户当前指示 → 仓库工程合同 → L2 已批准规则 → L1 配方 → 具名成熟实例当前源码 → L2 `surface-patterns` 现行实现参考 → L3 证据。低层与高层冲突时按高层执行并记录偏差。

## 2. 五步工作流与任务路由

1. **定位任务**：在下表选行；跨多家族时逐项拆开。
2. **查规则**：进入 L1 配方并沿链接读对应 L2 `CU-*` 卡与精确规则（`CU-*` 仅作定位标签，精确值以所链接规则为单一来源）。
3. **选 owner**：在当前源码核对 selector/function 与最终 cascade；查 [current-audit](references/current-audit.md) 避开已知例外。
4. **留继承依据**：写明 `任务/控件角色 → CU规则 → 具名成熟实例 → 实际owner/API/selector → 适用状态/颜色/动效 → 最小验证入口`（多家族建表；不写空泛“沿用风格”）。
5. **分层验证**：覆盖最小/默认窗口、长名、通道数、四主题、键盘 focus 及适用交互/reduced motion；组件、组合 WebKit、嵌入 WKWebView、native、DAW、音频分层报告，低层不证明高层。

| 当前任务 | L1 入口 | 主要 L2 规则 |
|---|---|---|
| 新节点卡、已有节点内增加功能 | [新节点配方](references/design-recipes.md#recipe-node) | [CU-NODE](references/design-navigation.md#cu-node)、[CU-COLOR](references/design-navigation.md#cu-color) |
| 普通按钮、持续开关、Checkbox 或 Matrix | [布尔与命令配方](references/design-recipes.md#recipe-boolean) | [CU-ACTION](references/design-navigation.md#cu-action)、[CU-SWITCH](references/design-navigation.md#cu-switch) |
| 数字拖调、推子或只点击输入 | [数值配方](references/design-recipes.md#recipe-number) | [CU-NUMBER](references/design-navigation.md#cu-number) |
| 节点库预览、功能抽象或操作图标 | [功能图形配方](references/design-recipes.md#recipe-preview) | [CU-ICON](references/design-navigation.md#cu-icon) |
| 小型参数窗、大波形窗、菜单或内联展开 | [窗口配方](references/design-recipes.md#recipe-window) | [CU-WINDOW](references/design-navigation.md#cu-window) |
| Graph Router/Matrix 或独立 CLR Router | [路由配方](references/design-recipes.md#recipe-router)；CLR Router 走 [cl-router](references/cl-router.md) | 二者不混作同一 owner |
| 波形/曲线/时间轴绘图、可拖 handle、播放头 | [窗口配方](references/design-recipes.md#recipe-window) 选容器 | [CU-PLOT](references/design-navigation.md#cu-plot) |
| 浮层、拖放、滚动条、光标、空状态、小表单 | 按所在容器选配方 | [CU-CHROME](references/design-navigation.md#cu-chrome) |
| 公共设置、通道顺序/数量、名称提示、帮助、状态 | [公共控件入口](references/shared-controls.md) | [CU-WEB](references/design-navigation.md#cu-web) |
| Preset 库、扩大预览、布局编辑、保存或删除 | [Preset 工作流](references/preset-workflows.md) | [CU-WINDOW](references/design-navigation.md#cu-window) |
| Strip 端口身份色与跨产品同步 | [Strip 角色与作用域](references/strip-roles.md) | [CU-COLOR](references/design-navigation.md#cu-color) |
| Chlora 自有原生文件选择与 IR 导入/mapping | [原生文件选择导览](references/native-file-pickers.md) | — |
| Graph 连线、端口、Cable Pin、Snake/Merge/Fanout | [Graph 路由对象](references/graph-routing-objects.md) | [CU-MOTION](references/design-navigation.md#cu-motion) |
| 主题、文字、布局、配色或动效 | 直接进入 L2 | [规则导航](references/design-navigation.md)（按语义选，不按截图相似度） |
| 核对现存例外 / 盘点与对比审查 | [当前证据与例外](references/current-audit.md) / [审查口径](references/audit-workflow.md) | 局部修改不升级为全产品审计 |

## 3. 找不到规则时的决策阶梯

依次停在首个可回答台阶并在继承依据中写明：1) **已批准 L2 规则** → 直接执行；2) **同语义具名成熟实例** → 继承完整 owner、事务与运动；3) **[surface-patterns](references/surface-patterns.md)** → 可复用并标注“现行实现，未单独批准”；4) **最近家族有依据扩展** → 写清差异与选用 token；5) **新身份、新颜色、新全局常数或改规则** → 停下交由用户决定。

## 4. 必须保持的设计与证据边界

- **范围与成熟度分开**：主 `host-surface.html`、Strip、Graph、插件/Node 栏、Routing/Modifier、宿主插件外壳、Group/`Stack v2`/`Chloe Input`/Comment/Pin 及公共弹层是成熟参考基准；File Source / Monitor Bus 不是 Device I/O。Device I/O 与 Analyzer 家族（`Jelly`（原 Nebula）、`Spectrogram`、`LFE Spectrum`、`Level Meter`）为专用受限表面，可复用公共 chrome 与自身 `1.5px` 焦点边框，但其专用材料、16px 窄轨、仪器画布与预览不反向推广。旧 Clone I/O、隐藏 Monitor 与独立 shell/browser 仅作兼容路径。第三方插件内部皮肤不受约束（宿主边框与开关方式仍属宿主）。
- **四层色域与色板保护**：主界面暖纸（Light）/三暗色（Graphite/Slate/Carbon）+ Analyzer 零色偏灰 + DarkRoom 纯黑 + VST3（`CLR Router` / `CLR 3D Panner`）`0ms` 瞬切。保持 Approved B 色板、四主题与用户节点色（`COLOR-USER-API-01` 仅作底层/MCP 保护，不暴露右键调色盘），不恢复退役历史色值，不从 candidate 重建期待色板。Strip Inserts/Mixer 同轴，Graph 表达真实拓扑。
- **交互、图形、运动与 WebView**：复用含解析、fine drag、归零、preview/commit/cancel 的完整 owner；命令与参数即时，装饰动效不延迟操作。preview07 为统一尺度功能抽象图而非缩略图。动效按用途继承，禁止无依据统一时长或 `transition:all`。WebView 禁用浏览器默认 outline/皮肤/蓝链/无意选中与 Reload/Inspect 菜单，保留合法语义装饰与四轨 `:focus-visible`。新开编辑器默认完整视图，回读/resize 不重置手动缩放。
- **工程与证据边界**：本指南不授权改产品、部署、重启或操作运行会话。图鉴与隔离 WebKit 仅验证前端组件/样式层，不证明嵌入 WKWebView、native、DAW、音频或运行二进制身份。旧行号仅作线索，验证以当前源码 selector/function 为准。

## 5. 图鉴预览

```sh
python3 scripts/serve_atlas.py --port 17869
```

打开 `http://127.0.0.1:17869/index.html#overview` 查看组件与时序示意（仅记录实验命令，不连接生产宿主；`scripts/build_atlas.py` 仅供显式维护，不得在测试中重建期待值）。
