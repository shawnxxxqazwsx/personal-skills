# 数值字段：直接拖调的统一反馈

> 层级：L2 规则（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。本规则仅统一**既有可直接拖动数字字段**的视觉反馈与居中契约，不给推子、旋钮、只读值或只点击输入字段新增 scrub，不改变各 owner 的范围、步长、方向或事务。非法键入恢复编辑前完整原值见 [numeric-validation.md](numeric-validation.md)。

## 材料与交互规则

| 状态 | 材料与反馈 |
|---|---|
| Idle / 离开后 | 透明背景，`box-shadow:none`，`text-shadow:none`，`outline:none`，圆角 5px |
| 可用字段 hover | 本地 ink 7% 背景；框阴影 `0 2px 7px`（ink 16%），圆角 5px |
| 键盘 `focus-visible` | 本地 ink 12% 背景，圆角 3px；无普通外框或下划线（四轨 `:focus-visible` 第 2 轨，与 Analyzer `1.5px` 外框分治） |
| hover + `focus-visible` | 保持 12% 焦点背景与 hover 框阴影（不被 hover 覆回 7%） |
| Disabled | 无 hover/focus 材料，保留各 owner 原 disabled 语义 |
| 进出与主题 | `--motion-material:180ms ease` 双向声明在 base；theme-changing 320ms `cubic-bezier(.4,0,.2,1)`；reduced snap |

- **本地 ink**：Graph 节点用 `--graph-node-ink`，IR 扩展/Distance 用 `--ir-ink`，Graph 外 Remote 用 `--ink`；不为字面 RGB 一致修改字色或节点色。
- **拖拽取消与符号**：所有连续拖拽（含 `Merge` scrub、Strip/Master 指针拖拽）按 `Escape` 统一取消回滚。宿主 Strip `#mixerGrid .channel-well` 具 `role="slider"` 方向键推推子，同时锁定 `STRIP-EDIT-EXCEPTION-01`（透明光标/无行内 `dB`/禁数字 scrub）。Analyzer 与插件静态数值框统一使用真负号 `U+2212` `−`。
- **Merge 特殊说明**：Merge 的指针 focus/active/inline entry 同样采用 12% 材料与 7%/16% hover 框阴影（180ms 双向）；数字下方框阴影与按钮外投影分属不同属性，S/M/Ø 按钮（24×24、去向下外投影、独立 hover 层 180ms、亮灭 180ms、2px inset focus）的处理不得扩至数值框。

## 数字与材料框居中

所有直接拖调数字字段的文字排版中心须与自身材料/焦点框水平中心一致（label/unit 与外层网格保留原排版）：

- **Merge（固定宽 280px）**：高/行高 24px、左右 pad 3px + 2px 原生 caret 余量，按实际字体 logical DOM advance 测宽在列内居中；输入列中心 54px、S/M/Ø 区间 96–172px、输出列中心 `width−62px`（两数字列各 60px，合法已格式化值完整显示，超长未提交草稿列内滚动）。只读 preset 预览复用同列位置不加交互。
- **Align / LFO / IR 节点 / Remote / IR Gain / IR Distance depth**：自身框内 `text-align:center`，保留原宽度与单位位置。
- **IR 扩展 Time（收框保右锚）**：短 IR 保留 56px 列轨道与数字右锚，input 框宽 = 实际 DOM 文字 advance + 对称 pad（3px/3px）+ `--ir-time-caret-room:2px` 原生编辑余量，以 `−1px` 结束边距补偿扩张使文字与框共居中；长 IR 按最大合法秒数预留共享 Time 列（≥56px），不随当前值抖动列宽。测宽使用 editor-local `aria-hidden` DOM sizer（复制实际字体、`tabular-nums`、font-feature、字距，缓存上限 256，随值/字体/resize 刷新，禁 Canvas 猜宽或 `length*ch`）。验收须核对长→短切换后真实 `scrollLeft` 与首帧/稳定态居中。

## 生产覆盖与排除

共享规则位于 `host/web-shell/ui/host-dark-themes.css` 末尾，按明确 scrub 属性匹配以下七类 owner：

| Owner | 匹配选择器 / 目标 |
|---|---|
| Merge | `#graphCanvas .graph-node.is-sum input[data-graph-sum-gain="1"]`（分支/输出 gain） |
| Align | `#graphCanvas .graph-node.is-channel input[data-channel-field]`（gain/delay 及 MASTER） |
| LFO 连续数字 | phase、smoothMs、非 `role="button"` 的 free rateHz |
| IR Loader 节点 | `.graph-ir-loader-controls input[data-ir-field]` |
| LFO Remote | `.graph-lfo-wire-hint .graph-lfo-range input`（min/max） |
| IR 扩展编辑器 | `.ir-editor input[data-ir-direct-value]`（gain/time/fade 等） |
| IR Distance | `.ir-distance-dialog input[data-ir-distance-depth]`（depth） |

**严格排除**：禁止用 `.graph-sum-gain` 或全局 `input` 批量匹配（Device 复用 class 但无 scrub）。LFO sync rate（菜单）、depth caption（旋钮）、Strip/File Source/Monitor 点击编辑值、IR 导入、DarkRoom、普通表单及 Device/Analyzer 均不自动接入。保留各 owner 非材料时序（IR color 120ms / row lift 140ms、Distance color/opacity 120ms）与 Remote 非法范围语义波浪线。参考对照：[Merge 居中与动效](../assets/atlas/merge-reference.html)、[居中逐项对照](../assets/atlas/numeric-center.html)。
