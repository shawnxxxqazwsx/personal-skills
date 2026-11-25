# 现行实现参考：未单独批准的源码成熟模式

> 层级：L2 补充（效力低于已批准规则，冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。复用时在继承依据中标注“SP-xx 现行实现，未单独批准”并核对当前源码。
> 缩写：`H`=`host/web-shell/ui/host-surface.html`，`S`=`host/web-shell/ui/host-surface.css`，`D`=`host/web-shell/ui/host-dark-themes.css`，`P`=`draftroom/strip/ui/host-strip-patch.css`。

<a id="cu-chrome-patterns"></a>
## A. 公共 Chrome、浮层与状态（CU-CHROME）

| ID | 模式 | Owner | 继承要点 | 边界与风险 |
|---|---|---|---|---|
| SP-01 | 控件尺寸档 | S `:root` `--ctl-h`/`-sm`/`-xs`/`--ctl-pad-x`/`--ctl-radius`/`--radius`/`--gap` | 24（顶栏/搜索/开关/insert chip）、20（读数/ctx 行/span chip）、18（小号 S/M/密集过滤行）；引用 token 禁写死 px | 新增档位需用户批准 |
| SP-02 | 手势上下文守卫 | H `withSurfaceGestureContext`/`surfaceGestureContextMatches` | 记录 instance/binding/graphLifetime/mode/topology，任一变化立即作废进行中手势/表单 | 适用于全部跨异步回包手势 |
| SP-03 | 单键快捷键守卫 | H `graphShortcutTargetIsInteractive` | 焦点在 input/textarea/select/button/crosspoint/contenteditable、repeat、修饰键不符或菜单/对话框打开时不触发 | 新快捷键必经守卫并登记 Cheat Sheet |
| SP-04 | Graph 缩放与平移 | H `setGraphViewZoom`/`bindGraphZoom`/`deferGraphZoomDecorations`/`#graphZoomReset` | 指针为锚缩放（Ctrl/捏合 vs Cmd 系数不同）；普通滚轮屏幕平移；中键/Alt+左键拖移；停 180ms 更新装饰 | S 中 `.graph-zoom-chrome`/`#graphZoomLabel` 无 DOM 为死样式 |
| SP-05 | 框选 | H `#graphMarquee`/`update/finish/cancelGraphMarquee`；S/D `.graph-marquee` | 空白画布起手，Shift/Cmd/Ctrl 追加，pointer capture 丢失取消，4px 阈值，计数 `tabular-nums` + `" · "` | Preset editor 框选归父层 |
| SP-06 | 级联添加面板（Shift+A） | H `openGraphAddPalette`/`positionGraphAddPalette`；S add palette | 平面无阴影、`--ctl-h` 行高、flyout hover 桥、`.hi` 低透明 wine、打开短延迟启 hover、边缘夹取 | 排除 `repairCanvasFrame` 分支 |
| SP-07 | 资源列表行与过滤框 | S 插件 Browser 行/`#pluginFilter`；H `handlePluginBrowserShortcut` | 过滤框底边 inset 聚焦加粗；行用圆点+名称/厂商，选中=填色+左 wine 条+圆点+加粗 | D 中 `--favorite` 无 DOM，勿建收藏 UI |
| SP-08 | 拖拽标签与目标高亮 | H `#dragGhost`/`showDragGhost`；S/D `.drag-ghost`/`.drop-target` | fixed、不截 pointer、按 uiZoom 换算偏移、深底浅字；目标 2px inset wine | 区别于 Insert 移除 ghost |
| SP-09 | 插槽落点预览 | H `updateInsertDropHint` FLIP；S insert drop hint | wine 低透明 + 1px 框 + caption 粗体，FLIP 位移沿 motion-out | multiMono 不显示 |
| SP-10 | 端口可放/不可放/禁用 | D drop-ok/drop-invalid；P 端口 hover/press | 可放共发光；不可放 2px 虚线 `--state-mute`+offset；禁用半透明 scale 1 无阴影；`:not(:disabled,[aria-disabled])` | 端口专用，非普通命令 |
| SP-11 | 不可用/载入/失败/重试 | S `.graph-load-node`/去饱和/`[data-worker-retry]`/Preset 扫光 | 不可用仅去饱和；失败 1px 虚线框+卡内重试；扫光守 reduced motion | `.graph-load-node` 写死 Light 色，新设计须用主题 token |
| SP-12 | 弹层内破坏性确认 | H `#storageConfirmation`、`host/web-shell/ui/host-storage.js` | 原菜单内展开，Cancel 左/具体动作右，busy 禁用，两键 Tab 循环；全页禁 `confirm()` | Preset 删除当前无二次确认 |
| SP-13 | `showForm` 快速表单 | H `showForm`；S `.ctx-dialog` | OK/Cancel 等宽，`role=alert`+`aria-invalid/describedby`，首字段聚焦全选，关后还焦，generation+SP-02+`placePopup` | Strip 通道数不走 `showForm` |
| SP-14 | 三种滚动条策略 | S `.reference-body`、Router 侧栏、Settings、`.cheat-content` | 长文档细滚条+主题 thumb；窄侧栏隐藏仍可滚；变宽分栏 `scrollbar-gutter:stable` | 按内容选型，不强行统一 |
| SP-15 | 空状态文字 | `.instance/.node-library/.graph-presets/.graph-add/.storage/.cheat-empty` | dim caption 说明原因，无插图 | IR `display:none` 空态不作基准 |

- **光标与层级现状**：S 末尾 `:root *{cursor:default !important}` 令局部 cursor 失效，新控件勿靠光标表达状态；z-index（20–100000）与阴影无统一 scale，参照同类 owner 取值。

<a id="cu-plot-patterns"></a>
## B. 绘图、时间轴与可拖 Handle（CU-PLOT）

Source Playback 均指 `darkroom/playback-monitor/ui/host-file-playback.js` 的 `ChloraSourcePlaybackUI`（非 legacy `ChloraFilePlaybackUI`）。

| ID | 模式 | Owner | 继承要点 | 边界与风险 |
|---|---|---|---|---|
| SP-20 | HiDPI 画布与像素预算 | Source Playback `draw`；`draftroom/nodes/ui/host-lfo.js`；`draftroom/ir-loader/ui/host-ir-loader.js` | backing store = CSS × dpr（上限 2），大画布按面积/宽度设预算 | 选最接近一处并写明，不自创第四种 |
| SP-21 | 波形包络 | Source Playback `paintWave`/`buildSourceIndex`/`ChloraSourceWaveModel` | 每像素列 min/max 包络，索引查极值，采样级绘精确采样点，绘制签名跳重绘 | 适用单源深缩放；IR 多通道为 SVG |
| SP-22 | Worker 准备与清理 | Source Playback `prepareWave`/`close` | 分块并发 + AbortController + token 校验；关时 abort/terminate/revoke Blob URL | 仅限真正含 Worker 路径（IR 无 Worker） |
| SP-23 | 时间轴缩放与平移 | Source Playback `setZoom` / wheel | Ctrl/Cmd+滚轮指针锚缩放（deltaMode 归一+rAF 合并），Shift+滚轮平移，`0` 归全貌，`+/-` 每步 √2 | 系数区别于 SP-04 |
| SP-24 | 虚拟化横向滚动 | Source Playback `windowFrames` | 轨宽设上限，scrollLeft↔首帧双向映射，canvas sticky，隐藏滚条 + `overscroll-behavior:contain` | 仅深缩放超布局上限时使用 |
| SP-25 | 播放头外推 | Source Playback `transportPosition`/`updateRealtime` | 按回包外推设上限、指数平滑纠偏、loop 取模、仅播放期 rAF、出视窗隐藏 | 估计值不代 native 时钟验收 |
| SP-26 | 选区与端点 Handle | Source Playback `bindWave`；IR `.ir-wave-handle` | 超阈值建选区否则 seek；命中区>线宽；`role=slider`+时钟 `aria-valuetext`；Shift/方向键/Home/End；屏外禁点；pointercancel 回滚 | 复用 IR handles 的完整交互基准 |
| SP-27 | 共享时间导航条 | `host-ir-loader.js` 缩放 slider/自制 scrollbar/标尺 | 对数 `role=slider` 双击全貌；`role=scrollbar` 记 thumb 偏移+PageUp/Down；标尺起中止三刻度自适应小数 | 适用多行共享时间轴 |
| SP-28 | 非等比 SVG 曲线编辑 | `host-lfo.js` `circleGeometry` | `preserveAspectRatio=none` 用椭圆 rx/ry 补形变+`non-scaling-stroke`；屏像素命中；点优先于切线；两端 x 锁；右键删/切型 | 避开 `LFO-CURRENT-01` 拖点 Escape 缺口 |
| SP-29 | SVG 坐标与手势失效 | `draftroom/ir-loader/ui/host-ir-distance.js` `gestureSignature`/`readGeometry` | `getScreenCTM().inverse()` 换算；zoom/视口/dpr 签名变化即取消重测；纵轴步长取整+短过渡+rAF 合并 | 适用缩放环境小 SVG 图 |
| SP-30 | 缓存光晕与共享帧循环 | `host-lfo.js` `sweepPaint`/`scheduleRuntime` | 预渲染光晕缓存（key 含主题变量），每帧仅移遮罩，共用限速 rAF 失活移出 | 避开每帧 blur |
| SP-31 | 选择弹层（listbox） | `host/web-shell/ui/host-typography.js` vs `darkroom/playback-monitor/ui/host-file-monitor.js` | Typography：combobox+`aria-activedescendant`+隐 select+typeahead+上翻；Monitor：roving focus+首次 Escape 关列表 | 无批准基准，新增写明选型理由 |
| SP-32 | 树形列表与滑动选中块 | `host/web-shell/ui/host-storage.js` `selectionPaint`/`setGroupOpen`/`render` | `role=treeitem`+`aria-selected`、独立选中层 `translateY`+ResizeObserver、busy 禁用、`storage-badge`、展开错开设上限 | 适用带元数据资源列表 |
| SP-33 | 浮窗几何与视图记忆 | Source Playback `clampBox`、`.is-narrow/.is-compact`、localStorage 视图偏好 | 边缘留距、容器断点类、监听 body zoom 重夹取、偏好带 schema 版本与条数上限 | localStorage 禁存项目状态 |

- **Canvas 主题重绘**：`ChloraTheme` 不派发事件；新画布将 computed style 纳入绘制签名/缓存 key，不得假设自动重绘。`darkroom/sources/ui/host-file-analysis-packet.js` 仅作 legacy 协议账本，不作 UI 基准。

## C. 源码中不存在的模式

无 toast、banner、通知、minimap、splitter/resizer、收藏夹、撤销历史面板与通用进度条（Monitor 导出进度仅一行 `role=status`，撤销/重做仅快捷键）。需用时走 [SKILL.md](../SKILL.md#3-找不到规则时的决策阶梯) 第 4–5 级，不宣称沿用现有组件。
