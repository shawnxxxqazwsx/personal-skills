# WebView 禁止项与焦点规则

> 层级：L2 规则（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。去除浏览器默认装饰时不得破坏键盘可达性与辅助语义。

## WebView 禁止项

| 禁止项 | 正确处理 |
|---|---|
| 浏览器默认蓝/黑 focus 框或按下突现的 UA outline | 全局 reset（`host-surface.css`）+ 按四轨显式设计 `:focus-visible`，区分指针与键盘 focus；禁止取消 outline 后无任何可见 focus |
| 默认链接蓝、链接下划线、以焦点下划线表达强调 | 成熟参考范围禁用焦点下划线，使用局部材料填色/内缘；保留有语义的负号/`−∞`、LFO disabled 删除线与 Remote invalid 波浪线 |
| 原生按钮白板、select 皮肤、checkbox 蓝底、number spinner | 复用现行自绘控件与 appearance reset，保留真实表单值源、role、name、min/max、disabled 与 change |
| 拖节点/推子无意选中文本、touch-callout、网页拖影 | 非编辑区 `user-select/user-drag/touch-callout:none`，真实输入与说明文档放行（复核 `contenteditable` 的 `selectstart` whitelist） |
| 系统 Reload/Inspect/context menu、重复 native title 气泡 | capture 阻断默认 contextmenu 交现有菜单；decorative `title` 转 `aria-label` |
| hover / selected / roving active-target 混为同态 | 真实 selected/checked 与当前 hover/焦点分离 |
| 搜索框隐式夺焦拦截快捷键；关闭菜单/退出 ghost 仍可命中 | 仅显式编辑动作聚焦，退出归还焦点；关闭立即 `inert`/`aria-hidden` 或 `pointer-events:none`；高 specificity `[hidden]{display:none}` |
| 调参触发页面滚动、游标乱闪、普通菜单加 transform | gesture owner 接管 capture/缩放；全局 `:root *{cursor:default !important}` 下不靠光标表达状态；普通 context/submenu 仅动画 opacity 防 fixed 子菜单错位 |

## 四轨 `:focus-visible` 分治与局部表达

正式锁定**四轨 `:focus-visible` 分治体系**，不得全局 `text-decoration:none!important` 或 `box-shadow:none!important`：
1. **宿主成熟命令 / 列表 / 导航 / S/M**：局部材料填色或 `2px` 内缘 + `180ms ease`（无焦点下划线）。
2. **直接拖调数值字段（含 Remote range）**：本地 ink `12%` 填色 + `3px` 圆角（hover 不覆写，详见 [numeric-fields.md](numeric-fields.md)）。
3. **Analyzer 家族**（`Jelly`、Spectrogram、LFE Spectrum、Level Meter）：统一 `1.5px` 外框线宽（专用受限表面，不外溢）。
4. **DarkRoom / 独立表单 / 特殊 SVG 控件**：保留各自语义焦点环与自绘 focus（推子 cap 提亮、LFO 曲线、Router 等）。

| 焦点 Owner（宿主成熟参考） | 批准的局部表达 |
|---|---|
| 直接拖调数字字段（含 Remote range） | 本地 ink `12%` 填色 + `3px` 圆角（不改 padding/height） |
| 其他裸数值、picker、LFO wave/tempo | `color-mix(in srgb,currentColor 12%,transparent)` + `3px` 圆角 |
| Reference 普通字段 / 动作按钮 | 当前文字色 `12%` 混合 `--flat-fill`（排除 close/picker option/checkbox） |
| Strip/File Source、Merge/Align S/M | `2px` 内缘 `currentColor 55%`（on 背景/字色不变；File Source Solo 仅清除额外 outline，不推广至 Mute） |
| Node 库 preview07 卡片 | `2px` `--ink` 内缘（身份底色与预览不变） |
| Settings checkbox 旁文字 | 无额外装饰，焦点由 Matrix 方格底格 marker 表达 |

- Graph 数值的 neutral reset 与主题后置 hover 不得覆盖键盘焦点填色；鼠标悬停在聚焦元素上时，focus selector 优先抑制普通 hover underline。
- **Settings 隐藏滚动条**：Settings 作用域（含嵌套列表）同时设 `scrollbar-width:none` 与 `::-webkit-scrollbar` 隐藏原生滚动条，保留 overflow 与滚轮/触控板/键盘滚动（不推广到其他窗口）。
- **真实 Checkbox**：仅 unchecked/checked/disabled（Matrix 方格，无勾号/滑钮/mixed），键盘 focus/hover 由底格 marker 表达，保留 native input/label/Space/change。
- **快捷键与文本上下文**：真实文本编辑态不触发节点删除或快捷创建；Node Lens 快捷键为 `Shift+Space`。

## 交付前最小检查

在组合 WebKit 页面执行 `click → Tab → Enter/Space → Escape`、拖动后 `pointercancel/window blur`、空新建与空编辑、四主题及 `reduced-motion`，确认无残余编辑器、悬挂手势、隐藏可点区或 UA 装饰。回归入口：`tests/host_keyboard_focus_no_underline_webkit_verify.mjs`。
