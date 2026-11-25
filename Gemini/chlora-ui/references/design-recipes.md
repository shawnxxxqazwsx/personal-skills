# 从任务到实施的六类配方

> 层级：L1 任务（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。精确值链接至 L2 规则不重复抄写。多家族变更用下表留存继承依据（单局部改写用一行）：

| 任务 / 角色 | CU 规则与具名实例 | 实际 owner / API / selector | 状态、颜色与 motion | 最小验证与未测层 |
|---|---|---|---|---|
| 受影响项 | 选规则与成熟实例 | 源码路径及函数/selector（复用或扩展） | 仅列适用项；N/A 写原因 | 专项与真实事件；分层报告 |

<a id="recipe-node"></a>
## 1. 新节点卡或节点内新功能
- **选身份与规则**：优先扩展已有身份；新身份须列功能差异、库分类、批准色与预览。读 [CU-NODE](design-navigation.md#cu-node)、[CU-COLOR](design-navigation.md#cu-color)、[CU-ICON](design-navigation.md#cu-icon)。按内容选几何（Align 逐通道行+MASTER / Router 路由 / File Source 源+meter / Stack 组合边界），不套 Device/Analyzer 专用样式。
- **实施与验证**：列 renderer、CSS、后置主题与生命周期，复用 `ChloraChannelUI` 等完整 API 与删除 cancel；不把附属 handles 当独立可 group 节点。核对多通道、长名、Snake 附着、min/default 窗、zoom、用户色与持久化拓扑/几何。**反例**：用营销卡片替代拓扑、加大外壳掩盖裁切、随机选色。

<a id="recipe-boolean"></a>
## 2. 普通按钮、Boolean 或 Checkbox
- **按语义分支**：一次性命令走 [CU-ACTION](design-navigation.md#cu-action)（正向标记 `data-ui-action="momentary"`，Browser 内凹）；真实 Checkbox 走 [CU-SWITCH](design-navigation.md#cu-switch)（native input/label + `ChloraCheckboxUI.sync()`，不发假 change）；S/M/Ø、radio、模式按钮、Play/Pause toggle、Matrix 选通各保原角色。
- **状态与验证**：区分 idle/hover/pressed/focus/on-off/disabled/pending；Checkbox 白内方仅表 checked、按住改底板，实际值与命令即时。验证真实 pointer/Space/Enter/label 点击、程序回读、disabled、反向与 reduced。**反例**：用白方闪动表按压、普通按钮时长代 Checkbox 模型、仅凭 `aria-pressed` 判 transport。

<a id="recipe-number"></a>
## 3. 数字拖调、推子或只点击输入
- **分能力**：拖调数字继承 Align/Graph 材料与居中；只点击输入不新增 scrub；推子保原 taper 与直跟手。读 [CU-NUMBER](design-navigation.md#cu-number)、[numeric-fields.md](numeric-fields.md)、[numeric-validation.md](numeric-validation.md)。
- **事务与回读**：入口捕获完整原值（非显示文本）；非法 Enter/change/blur 恢复原值并清 preview；Escape 与迟到 ACK 沿 owner。若同 context 回读结束旧事务但保留 focus，下次编辑须从当前完整参数建新 entry（不在 `input` 改完后才捕获），旧 blur/ACK 禁写新身份。
- **验证**：原值 0/非零、非法串、typed 越界拒绝 vs drag clamp、Shift/双击/Escape/失焦、长值 `scrollLeft`、迟到 ACK，以及“保留 focus 回读 → 单次完整替换 → Enter/blur”与旧 blur 对照。**反例**：`parseFloat` 接前缀、非法归零、relative fader 改点击跳值。

<a id="recipe-preview"></a>
## 4. 抽象功能 Preview 或操作图标
- **先写功能句**：描述汇聚/分发/选通/对齐/时变关系，再按 [CU-ICON](design-navigation.md#cu-icon) 与 [components.md](components.md) preview07 三层语法绘制（不从 Device/Analyzer 反推）。
- **落点与验证**：节点库 SVG decorative、不截 pointer/Tab；accent 与 node fill 分别查冻结基准 `tests/fixtures/host_node_preview_v7.json`（不从 fill 反算）；Snake mask/Expand/Add/关闭/删除/回到起点互不混用。验证四主题/scale、原按钮命中包络与单次 payload。**反例**：缩略面板、全图发光、照抄隐藏 `≋`。

<a id="recipe-window"></a>
## 5. 小型专用参数窗与大波形窗
读 [CU-WINDOW](design-navigation.md#cu-window)，按内容与坐标空间选型：

| 内容 / 位置 | 合适 Owner | 避免的误用 |
|---|---|---|
| 节点内少量参数 | 本节点 layout/envelope（Align 优先内联） | 仅因“expanded”套 IR 大窗 |
| Graph 路由浮窗 | Router Stage portal（`#graphRouterWindows`） | 挂缩放节点下再用 inverse scale |
| 小型专用参数 plot | Distance 式 screen-fixed（`ChloraIrDistanceUI.markup/update/dispose` + `[data-ir-distance-open]`） | 臆造公开 `ChloraIrDistanceUI.open()` |
| 多行 IR 波形与大通道 | 已挂载 `ChloraIrLoaderUI.openEditor(nodeKey)` / `[data-ir-expand]`（普通分页 vs Complete Bank 单 master） | 所有通道压一屏、直接调私有 openDetails |
| 单 File Source 播放/波形 | `ChloraSourcePlaybackUI.open(row,owner)` / `[data-fg-source-playback]` | 误选 legacy `ChloraFilePlaybackUI` |
| Chlora 自有原生文件选择 | [native-file-pickers.md](native-file-pickers.md) 具名 chooser 与模式 | 误认系统 OpenPanel 或用 Web 替代原生验收 |

- **实施与验证**：列父级、坐标空间、viewport clamp、close/dispose、focus return；IR 为 SVG（浏览器侧无 Worker），Source companion 为 canvas+Worker，不互套。新开默认完整范围，回读/resize 保留手动缩放，关闭用 Reference SVG 但保原命中与生命周期。验证首开/重开、缩放后 resize（核对可见绘图/刻度/handle 坐标）、快速反向、关闭 inert、节点删除与 reduced。

<a id="recipe-router"></a>
## 6. Graph Router/Matrix 与独立 CLR Router
- **Chlora Graph Router/Matrix**：读 [components.md](components.md)、[motion.md](motion.md)、[CU-ACTION](design-navigation.md#cu-action)、[CU-SWITCH](design-navigation.md#cu-switch)、[CU-WINDOW](design-navigation.md#cu-window)。Owner：`host/web-shell/ui/host-surface.html` 的 `graphRouterMountWindow`、`graphRouterPanel`/`Owner`、`graphRouterDisposeWindow`、`graphRouterCrosspointPaint`。主 Graph 走 Stage portal，IR adapter 保自身 inline/bounds（禁 `closest('.graph-node')`）。route ACK 改 topology token、flags ACK 不改；通道强调不缩放端口。回归：`tests/host_router_flags_ack_webkit_verify.mjs`、`tests/host_router_window_portal_webkit_verify.mjs`。
- **独立 CLR Router**：`cl-utilities` 插件，原生窗由 `McRouterEditor` 拥有，完整契约见 [cl-router.md](cl-router.md)（五层 CSS、不同推子律、选中组 gain/delay、S/M 刷选、`0ms` 外观瞬切）。不将其重写成 Graph Matrix，也不因共享主题文件推定交互一致。
