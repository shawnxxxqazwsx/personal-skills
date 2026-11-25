# Preset 工作流

> 层级：L1 任务（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。Preset 节点投影为只读内容，父编辑器管理布局；预览内控件不得连向实时音频节点。

## 入口与 Owner

除显式公开 API 外均位于 `host/web-shell/ui/host-surface.html` 私有作用域，须沿现有 UI 绑定进入：

| 任务 | 具名 Owner / Selector | 状态与事务 |
|---|---|---|
| 库与 tab | `requestGraphPresets`、`renderGraphPresets`、`setGraphLibraryTab`；`#graphPresetsPanel`、`.graph-preset-card` | empty/list 与 inactive/inert 分离；静态缩略图不代表实时分析 |
| 请求扩大预览 | `showGraphPresetHover`、`receiveGraphPresetPreview`、`hideGraphPresetHover` | 真实菜单“Enlarge preview”进入；校验 `requestId` 匹配/过期/错误及 card 在树 |
| 布局窗口 | `openGraphPresetEditor`、`graphPresetEditorFit`、`graphPresetEditorPointerDown/Move/Up`；`.graph-preset-editor`/`.graph-preset-editor-canvas` | 新开完整 fit，父窗管 selection/pan/zoom/拖放，保留当次手动 camera（避开 `PRESET-WINDOW-OBS-01` 外框越界） |
| 只读节点投影 | `draftroom/graph/ui/host-preset-preview.js` 公开 `ChloraPresetPreview.create(model,helpers)` | 返回 `element/render/bounds/nodeRects/groupNodeKeys/setSelection/layout`；sanitize 去 id、禁内部控件/tab/pointer |
| 保存新 Preset | `saveGraphPresetAt` → `showForm` → `captureGraphPreset` | 仅 Name（trim 非空），冻结 selection/instance/binding/topology/lifetime；context 变化拒绝保存旧选择 |
| 保存编辑布局 | `closeGraphPresetEditor`、`finishGraphPresetEditCapture` | unchanged 直接关；dirty 发 capture 防重；匹配 `captureId` 成功关，失败留草稿并提供 Discard changes |
| 删除 Preset | `deleteGraphPresetMenu` → `receiveGraphPresetPreview` → `deleteGraphPreset` | 保存中阻止；取当前 editor 或请求 metadata 的 `revisionToken`；无第二层确认表单 |

## 交互、提交守门与验证

- **Escape 语义**：手势中取消手势；空闲窗调 `closeGraphPresetEditor` 保存 dirty 布局（同 Done）；Name 表单 Cancel 不 capture。勿套用数值编辑取消语义丢弃布局。
- **身份与版本守门**：`requestId`、`captureId`、`revisionToken` 各司其职。`finishGraphPresetEditCapture` 匹配后发 `cancelGraphPresetCapture`；`host/web-shell/HostShell.h` 清同 ID pending 与像素回调核验；`host/app/MainComponent.h` 交 `draftroom/graph/GraphPresetStore.h::update` 在解析与覆盖前双检版本。UI 忽略旧回包不等于后台未发生陈旧写入。
- **验证**：按需选 `tests/host_graph_presets_ui_verify.mjs`、`tests/host_preset_saved_projection_verify.mjs`，覆盖真实入口、无操作对照、A 超时/退役 → B 成功 → A 迟到顺序（双查 UI 与已提交模型/revision）、四主题、reduced 与 resize/zoom。
