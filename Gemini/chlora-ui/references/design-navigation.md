# 按语义找到规则与生产 Owner

> 层级：L2 索引（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。`CU-*` 仅作定位标签，精确常数以所链接 L2 规则为单一来源。

## 范围与成熟度

| 对象 | 范围 | 参考资格 |
|---|---|---|
| Strip、Graph、公共 chrome、Routing/Modifier、宿主插件外壳、Group / `Stack v2` / `Chloe Input` / Comment / Pin | 纳入 | 成熟参考基准（组合节点不简化为单卡） |
| File Source、Monitor Bus、Source Playback | 纳入 | 成熟布局与参数 owner（非 Device I/O） |
| Device I/O、Analyzer 家族（`Jelly`、Spectrogram、LFE Spectrum、Level Meter） | 专用受限表面 | 仅借公共 chrome 与 `1.5px` 焦点边；专用材料/16px 窄轨/画布/预览不外溢 |
| 独立 CLR Router / CLR 3D Panner | 纳入 | 独立产品，入口见 [cl-router.md](cl-router.md)（不套 Graph Router） |
| DarkRoom / Repair、第三方插件皮肤、旧 Clone I/O / 独立 shell/browser | 排除 / 兼容路径 | 第三方仅审宿主边框与开关；兼容路径不作新模板 |

## CU-NODE
新节点、布局、分区、端口、Group/Stack 或选中反馈。默认扩展已有身份，确需新身份须记录差异与颜色批准。
- **规则与入口**：[components.md](components.md) 节点/端口章、[foundations.md](foundations.md) 布局章；源码 `host/web-shell/ui/host-surface.html`（节点 renderer、`graphAddDropEngineXY`）、`draftroom/strip/ui/host-channel.js`（`ChloraChannelUI`），其余见 [source-map.md](source-map.md)。
- **状态与验证**：核对 empty/ready/hover/focus/selected/bypass/disabled/pending/error、多通道、附着 Snake、Graph/UI zoom 与窗口边缘；路由/几何变更按持久化合同验证完整端点与几何。

## CU-COLOR
布局材料、文字、节点身份色与状态色。先判语义角色再选批准 token。
- **规则与入口**：[foundations.md](foundations.md) 角色色与电平章、[theme-inheritance.md](theme-inheritance.md)、[strip-roles.md](strip-roles.md)、[components.md](components.md) preview 表。源码 `host/web-shell/ui/host-surface.css`、`host/web-shell/ui/host-dark-themes.css`、`draftroom/strip/ui/host-strip-patch.css`、`host/web-shell/ui/host-theme.js`、`host/web-shell/ui/host-typography.js`。
- **关键约束**：四层场景色域分工（暖纸/三暗色 + Analyzer 零色偏灰 + DarkRoom 纯黑 + VST3 `0ms` 瞬切）；保留 Approved B 与用户节点色（[COLOR-USER-API-01](current-audit.md#color-user-api-01) 仅底层/MCP 保护，不暴露右键调色盘；`Jelly` 5-stop 相位色为功能色阶）。验证沿元素及祖先查最终 computed style；preview 回归 `tests/host_node_library_preview_webkit_verify.mjs`。

## CU-ACTION
普通瞬时命令与持续状态控件（Browser Scan 为命令参考；成熟 S/M 为状态参考）。
- **规则与入口**：[components.md](components.md)、[motion.md](motion.md)。正向标记 `data-ui-action="momentary"`，Graph 归 `#graphStage`；排除状态控件（`aria-pressed/checked/selected`、S/M/Ø、Play/Pause、slider/handles）。
- **状态与验证**：命令按压 180ms 内凹无位移；成熟 S/M 亮灭 180ms，实际状态与命令即时。回归：`tests/host_material_feedback_motion_webkit_verify.mjs`、`tests/host_channel_button_history_webkit_verify.mjs`。

## CU-SWITCH
Host 真实 Checkbox（含 `role=switch`）或 Matrix 选通格。
- **规则与入口**：[components.md](components.md)、[motion.md](motion.md)、[六状态四主题图鉴](../assets/atlas/checkbox-refine.html)。源码 `host/web-shell/ui/host-surface.html` 的 `switchPaintValue`、`ChloraCheckboxUI.sync()`、`graphRouterCrosspointPaint`。
- **状态与验证**：native `checked` 为唯一值源，白内方仅表 checked、按住仅改底板（250ms 真实时钟 smoothstep，无 mixed）。回归：`tests/host_checkbox_theme_webkit_verify.mjs`。

## CU-NUMBER
直接拖调数字、推子、只点击输入与数值表单（不因视觉统一新增 scrub）。
- **规则与入口**：[numeric-fields.md](numeric-fields.md)、[numeric-validation.md](numeric-validation.md)、[components.md](components.md)。共享材料位于 `host/web-shell/ui/host-dark-themes.css` 明确 scrub 属性选择器；Strip 通道数量 `#insertChannels/#outputChannels` 见 [shared-controls.md](shared-controls.md#channel-settings)。
- **状态与验证**：Align/Graph 材料 7%/12%/16% + 居中（IR Time 收框保右锚）；连续拖拽 `Escape` 回滚；`STRIP-EDIT-EXCEPTION-01` + `#mixerGrid .channel-well` `role="slider"`；静态框真负号 `U+2212` `−`；非法键入恢复完整原值。回归：`tests/host_source_monitor_fader_style_verify.mjs`、`tests/host_ir_distance_interaction_webkit_verify.mjs`。

## CU-ICON
preview07 抽象功能图解与操作符号（互不混用）。
- **规则与入口**：[components.md](components.md)；源码 `host/web-shell/ui/host-surface.{html,css}`（`.graph-snake-wrap-icon`、`.chlora-window-close`）、冻结基准 `tests/fixtures/host_node_preview_v7.json`。
- **判定与验证**：先写一句话功能关系，再以三层语法绘制；SVG decorative 不截 pointer/Tab；删除/清除 × 非窗口关闭。回归：`tests/host_node_library_preview_webkit_verify.mjs`。

## CU-WINDOW
内联展开、Graph 路由窗、小参数窗、大波形窗、菜单与原生 Browser。
- **规则与入口**：[components.md](components.md)、[motion.md](motion.md)、[design-recipes.md](design-recipes.md#recipe-window)、[preset-workflows.md](preset-workflows.md)、[native-file-pickers.md](native-file-pickers.md)。生产入口：`draftroom/ir-loader/ui/host-ir-distance.js`（`ChloraIrDistanceUI` + `[data-ir-distance-open]`）、`draftroom/ir-loader/ui/host-ir-loader.js`（`ChloraIrLoaderUI.openEditor`）、`darkroom/playback-monitor/ui/host-file-playback.js`（`ChloraSourcePlaybackUI.open`）。
- **状态与验证**：fresh-open 完整范围、回读/resize 保留手动缩放、关闭 Reference SVG、长内容分页/滚动。回归：`tests/host_router_window_portal_webkit_verify.mjs`、`tests/host_router_window_motion_webkit_verify.mjs`。

## CU-MOTION
材料、按钮、开关、窗口、库栏、弹簧、线缆、meter 与连续手势（完整参数查 [motion.md](motion.md)）。
- **入口与路由**：[graph-routing-objects.md](graph-routing-objects.md) 区分 Pin 即时坐标与线缆收敛；`--motion-material` / `--motion-theme-material` 仅管各自职责，不覆写 owner 完整 transition。
- **验证**：覆盖进退、途中反向、快速重复、normal/reduced、hidden/移除、延迟/过期 ACK 与真实 Worker 路径。

## CU-WEB
focus、表单、菜单、键盘、文字选择、WebView 禁用项与公共控件。
- **规则与入口**：[webview-guardrails.md](webview-guardrails.md)、[shared-controls.md](shared-controls.md)。锁定四轨 `:focus-visible` 分治（成熟材料内缘 180ms / 拖调数值 12% 3px / Analyzer 1.5px 外框 / DarkRoom 与独立表单自绘焦点环）；原生选择器已继承用户 Title/Body 字体；`CLR Router` 与 `CLR 3D Panner` 对称支持 `"Follow Chlora"` 字体覆写。
- **验证**：真实 Tab/Shift+Tab、Space/Enter/Escape、blur 与菜单焦点归还；回归 `tests/host_keyboard_focus_no_underline_webkit_verify.mjs`。

## CU-PLOT
波形、曲线、时间轴、标尺、可拖 handle、播放头与 canvas/SVG 生命周期。先用 [CU-WINDOW](#cu-window) 选容器。
- **规则与入口**：[components.md](components.md)、[motion.md](motion.md)、[surface-patterns.md](surface-patterns.md#cu-plot-patterns)（SP-20…SP-33）。生产入口：`ChloraSourcePlaybackUI`（`ChloraSourceWaveModel`）、`host-ir-loader.js`（SVG）、`host-lfo.js`、`host-ir-distance.js`（legacy `ChloraFilePlaybackUI` 与 Analyzer 不作基准）。
- **要点**：backing store dpr≤2、rAF 合并+绘制签名、handle 命中大于视觉线宽且具 `role=slider`、pointercancel 回滚、切主题确认重绘、resize 核对可见绘图与 handle 坐标。

## CU-CHROME
浮层、拖放、快捷键、框选/缩放、滚动条、空状态、载入/失败/重试、破坏性确认、小表单与尺寸档。
- **规则与入口**：[foundations.md](foundations.md)、[webview-guardrails.md](webview-guardrails.md)、[shared-controls.md](shared-controls.md)、[surface-patterns.md](surface-patterns.md#cu-chrome-patterns)（SP-01…SP-15）。源码 `host/web-shell/ui/host-surface.html`、`host/web-shell/ui/host-storage.js`。
- **判定**：新快捷键走 SP-03、跨异步手势走 SP-02、破坏性操作弹层内确认禁 `confirm()`、空状态用 dim caption。无 toast/进度条/splitter 组件，全局 `cursor:default !important` 下不靠光标表达状态。
