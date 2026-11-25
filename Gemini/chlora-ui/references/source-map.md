# 源码映射、图鉴与验证入口

> 层级：L3 证据（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。路径以仓库 `~/Projects/mc-patcher/` 为根；查实现以 selector/function 为准。

## 现行文件结构映射

| 领域 / 模块 | 拥有文件 |
|---|---|
| 主 Surface 路由与资源解析 | `host/web-shell/HostShell.h`、`host/web-shell/HostWebChrome.h` |
| 主页面、基础 Token、Strip/Graph/Node/Router/Preview07 | `host/web-shell/ui/host-surface.html`、`host/web-shell/ui/host-surface.css` |
| 后置主题、Selection/Elevation、共享 Scrub/S/M/Momentary | `host/web-shell/ui/host-dark-themes.css` |
| 字体、主题切换、Storage、兼容 Shell/Browser | `host/web-shell/ui/host-typography.js`、`host-theme.js`、`host-storage.js`、`host-shell.*`、`host-browser.*` |
| Strip 共享 Patch 与 Align（Channel） | `draftroom/strip/ui/host-strip-patch.css`、`draftroom/strip/ui/host-channel.{js,css}`、`draftroom/strip/HostUnifiedChannelSettings.h` |
| Preset 只读投影与存储 | `draftroom/graph/ui/host-preset-preview.js`、`draftroom/graph/GraphPresetStore.h` |
| LFO 与 Stack v2 | `draftroom/nodes/ui/host-lfo.{js,css}`、`draftroom/nodes/ui/host-stack.{js,css}` |
| IR Loader、IR Distance 与原生 IR 文件选择器 | `draftroom/ir-loader/ui/host-ir-loader.{js,css}`、`host-ir-distance.{js,css}`、`draftroom/ir-loader/HostIrFileChooser.{h,cpp}`、`HostIrFileChooser_mac.mm`、`HostIrFileBrowser.{h,cpp}`、`HostIrBrowserMotion.h`、`IrRouterMatrixMain.inc` |
| Chloe Input 与 Device I/O（后者受限） | `audio-bridge/chloe-host/ui/host-chloe-input.{js,css}`、`audio-bridge/device-io/ui/host-device-io.{js,css}` |
| Analyzer 家族（专用受限表面） | `draftroom/analyzers/nebula/ui/host-nebula.{js,css}`（Jelly）、`spectrogram/ui/host-spectrogram.{js,css}`、`level-meter/ui/host-level-meter.{js,css}` |
| File Source / Monitor Bus / Playback / Repair | `darkroom/workspace/ui/host-file-graph.{js,css}`、`darkroom/playback-monitor/ui/host-file-monitor.{js,css}`、`host-file-playback.{js,css}`、`darkroom/repair/ui/host-file-repair.{js,css}`、`darkroom/sources/ui/host-file-analysis-packet.js` |
| 原生宿主入口与 LookAndFeel | `host/app/MainComponent.h`、`host/app/HostLookAndFeel.h`、`host/engine/PluginHostEngine.h`、`shared/include/mc/ChannelLayoutRouting.hpp` |
| 独立 CLR Router / CLR 3D Panner | `~/Projects/cl-utilities/`（详见 [cl-router.md](cl-router.md)） |

## 易混淆工作流与原生边界

| 任务 | 实际 Owner | 边界提醒 |
|---|---|---|
| 编辑 IR 源文件通道映射 | `draftroom/ir-loader/ui/host-ir-loader.js`：`ChloraIrLoaderUI.openChannelMapping(nodeKey, expectedRevision)` → `editGraphIRChannelMapping`（原生优先，HTML fallback 走 `receiveImport`/`renderChannelMap`） | 非 IR 内部 Input/Output Router；保留既有 mapping 顺序/数量/锁定与 `expectedRevision` 校验 |
| Monitor 路径、导出与进度 | `darkroom/workspace/ui/host-file-graph.js`：`output-workflow-v1`、`fileGraphSetOutputPath`/`fileGraphExport`、`targetSourceBindings`/`targetExportReady`/`workflowActionStamp` | 独立于 Monitor gain/Device/Reference；记录 bridge 不执行真实文件导出 |
| 打开宿主插件编辑器 | `host/app/MainComponent.h::openEditor` → `host/engine/PluginHostEngine.h::showEditorOnChannel`/`openOrFocusEditorWindow`（`prepareParameterHistoryEditorAdmission` 可拒入） | 区分 in-process 与 sandbox 窗口；仅审宿主 chrome，第三方内部皮肤排除 |

## 图鉴工具与常用回归入口

- **图鉴资产**：`assets/atlas/source-ui/` 保存冻结 UI 副本与字体，`assets/atlas/provenance.json` 记录 SHA-256；`scripts/serve_atlas.py` 本地预览，`scripts/check_atlas.mjs` 做隔离 WebKit 挂载与截图核验，`scripts/build_atlas.py` 仅供显式基准刷新。
- **常用仓库回归（按受影响 owner 选跑）**：`tests/host_node_library_preview_webkit_verify.mjs`（配 `tests/fixtures/host_node_preview_v7.json`）、`tests/host_keyboard_focus_no_underline_webkit_verify.mjs`、`tests/host_material_feedback_motion_webkit_verify.mjs`、`tests/host_checkbox_theme_webkit_verify.mjs`、`tests/host_channel_button_history_webkit_verify.mjs`、`tests/host_source_monitor_fader_style_verify.mjs`、`tests/host_ir_distance_interaction_webkit_verify.mjs`、`tests/host_router_card_selection_webkit_verify.mjs`、`tests/host_router_controls_paint_webkit_verify.mjs`、`tests/host_router_flags_ack_webkit_verify.mjs`、`tests/host_router_window_motion_webkit_verify.mjs`、`tests/host_router_window_portal_webkit_verify.mjs`、`tests/host_graph_presets_ui_verify.mjs`、`tests/host_preset_saved_projection_verify.mjs`。
