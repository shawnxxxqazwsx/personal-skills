# 动效与反馈

> 层级：L2 规则（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。按最近语义继承；持续信号与弹簧保留其数学模型，禁止统一全局时长或 `transition:all`。

## 局部材料、命令与状态色

- **材料反馈**：hover/focus 背景与材料内缘统一 `--motion-material:180ms`、`--motion-material-easing:ease` 双向，写在 idle/base selector（hover/focus 仅写目标值），中途反转从当前值继续。保留各 owner 原有非材料时序（如 Node tabs 500ms、IR row lift 140ms、Playback transform 90ms）。
- **普通瞬时命令与 DarkRoom**：`data-ui-action="momentary"` 采用 Browser 式稳定内凹（`inset 0 2px 3px`、本地 ink 12%，180ms ease），按下无位移/缩放（不再 Y+1 / scale .94 / scale .96）。DarkRoom 按钮/divider/Display summary 已接入 180ms 材料并保留各自专用 dark 配色与尾项时序；Instance 列表未选/已选/project 行 hover 背景/字色 180ms ease。
- **成熟文字 S/M 与 Ø**：Strip、Align、File Source、Merge、Router/Matrix、IR Solo 的背景与字色双向 180ms ease（Merge 独立 hover 层 opacity 与 Router/Merge Ø 同 180ms）；`.on`/`aria-pressed` 与参数命令即时更新，不等待动画。
- **直接拖调数字**：Align/Graph/LFO/IR/IR Distance/Remote 统一 180ms ease 背景与框阴影（IR 去原 120ms text-shadow，保留 color 120ms 等非材料时序；Distance depth 窄覆写 `!important` 并在 owning reduced 分支取消）。详见 [numeric-fields.md](numeric-fields.md)。
- **主题与 Reduced Motion**：主题切换 320ms `cubic-bezier(.4,0,.2,1)`；shadow-only owner 用 `--motion-theme-material` 保持平时 0ms 与切主题 320ms。`prefers-reduced-motion` 将材料与 theme-only token 置 0，JS/WAAPI/native 均走 snap 分支，保留信号 ballistics 与状态含义。回归入口：`tests/host_material_feedback_motion_webkit_verify.mjs`。

## 公共 Chrome、窗口与库栏

| 场景 | 时序 / 曲线 / 模型 | Owner |
|---|---|---|
| 普通 context/submenu | 140ms `cubic-bezier(.16,1,.3,1)`，opacity `.35→1`；close 立即 hidden（禁 transform） | `host-surface.css` |
| brand / LFO menu | 220ms 同 motion-out、Y −4→0、alpha 0→1 | `host-surface.css`、`host-lfo.css` |
| segmented switch | 500ms `cubic-bezier(.4,0,.2,1)`，滑块 transform + text | `host-surface.css` |
| 插件组 / 插件行 | 组 chevron/grid 500ms（展开分摊 delay、折叠归零）；行 bg/shadow 180ms ease、color 180ms motion-out | `host-surface.{css,html}` |
| Instance popup | open 320 / close 220ms motion-out，scale `.975↔1` + alpha；close 立即 inert 结束 hidden 并归还 focus | `host-surface.html` |
| Settings / Reference | open/close 500ms ease，Y +8↔0 + alpha，backdrop 同步 | `host-surface.{css,html}` |
| Settings choice / Cheat | choice open 160ms ease-out Y +3→0（close 立即 hidden）；Cheat 320ms Y +8↔0 | `host-surface.css`、`host-typography.js` |
| 主题 / Ink reveal | 主题材料 320ms + 固定终点 WAAPI 前景 320ms（380ms 清理）；reveal 750ms（首 layout 前禁 transition） | `host-theme.js`、`host-surface.{css,html}` |
| Strip / Graph 插件栏 | Strip 500ms rAF smoothstep `t²(3−2t)` 实改 width；Graph 500ms `.4,0,.2,1` translate+clip 完后 commit（勿互换） | `host-surface.{html,css}` |
| Node drawer / family | 500ms `.4,0,.2,1` 揭示与 tabs，family opacity 500ms ease-in-out | `host-surface.{html,css}` |
| 选择 / hover 弹簧 | Strip 选择 / Instance / native file-list：pos/size/alpha 临界阻尼 `ω30 ζ1`，scale `ω32 ζ.72`（初 `.94`/Y+2/α0），无固定时长 | `host-surface.html` |
| Insert 生命周期 | birth 220ms motion-out；reorder 180ms；remove inert ghost 180ms `.4,0,1,1`（Y−2/scale.985）；drop 提示 180ms | `host-surface.{html,css}` |

## Graph 节点、连线与 Matrix 开关方格

| 场景 | 现行模型 | Owner |
|---|---|---|
| node / group / comment | node 入 250ms ease-out / 出 140ms ease-in；comment 入 180ms；实时读当前 `opacity` | `host-surface.html` |
| elevation（独立预绘层） | node / socket 入 140 / 出 480ms `.2,.7,.2,1`；Group 入 360 / 出 600ms | `host-dark-themes.css` |
| Router / Matrix | Router↔Matrix 240ms smoothstep（内容 220ms Y+3→0）；通道强调 bg/color/border/shadow 180ms（scale 恒 1、字重固定）；行列号固定字号字重仅 alpha `.8→1`；Stage 窗口层不含相机变换 | `host-surface.{html,css}`、`host-dark-themes.css` |
| Snake / Merge / Align / Stack | Snake wrap/expand 180ms；Merge 分支 300ms `.42,0,.58,1`（controls 250ms）；Align/Stack 高度指数 `τ60ms`（无 overshoot） | `host-surface.{html,css}` |
| wire reflow / reveal | reflow `τ75ms` 指数（速度上限 `.75 px/ms`、inertia `τ95ms`，端点/Pin 即时）；reveal 180ms；Merge inspection 1150 world-u/s | `host-surface.html` |

**Matrix 开关方格与 Checkbox（250ms 真实时钟 smoothstep）**：共用 `switchPaintValue`，按 `(now-start)/250` 采样 smoothstep（无 4% kick、无 20ms 帧钳制、无 330ms 强截止）；反向从当前真实时间进度继续，同目标回读不重置。白内方块占控件高 64% 且仅表示 checked（scale `.92→1` + opacity 随进度）；底板 opacity 进退 130ms：off `.13` / hover-focus `.20` / press `.28`，on `.48` / on+hover-focus `.54` / on+press `.62`（disabled 无 hover/press）。Matrix 绘制时 hover marker 位置直跟手（平时 transform 95ms `.2,.7,.2,1`，opacity/bg 130ms）。reduced/hidden 直接 settle，无活动动画停 rAF。`ChloraCheckboxUI.sync()` 仅同步绘制，不发 change。

## Modifier、播放、连续信号与原生窗口

| 场景 | 现行模型 | Owner |
|---|---|---|
| LFO | 波形换形 280ms smoothstep raster crossfade；radio border 180ms/shadow 220ms/dot 150ms+scale 240ms；mapping hint 220ms | `draftroom/nodes/ui/host-lfo.{js,css}` |
| IR expanded / controls | 窗入 320ms `.22,.61,.36,1` / 出 280ms；row lift 140ms Y−2；color/contour/handles 120ms | `draftroom/ir-loader/ui/host-ir-loader.css` |
| IR Distance | scrim 160ms；panel 入 180ms `.2,.7,.3,1` Y+6 / 出 140ms Y+4；color/opacity 120ms | `draftroom/ir-loader/ui/host-ir-distance.css` |
| Playback / Source companion | full 入 280ms `.16,1,.3,1` Y+12/scale.97 / 出 160ms；compact bg 180ms/alpha 160ms/transform 90ms；companion 入 220ms/出 160ms | `darkroom/playback-monitor/ui/host-file-playback.{js,css}` |
| 原生 IR Browser | open 320ms Y+6 / close 220ms Y+4 smoothstep；scan dissolve 200ms；scrollbar 停 650ms 后 200ms 淡出；列表弹簧同 `ω30/32` | `draftroom/ir-loader/HostIrBrowserMotion.h`、`HostIrFileChooser.cpp` |

- **推子与 Meter**：推子直跟 rAF 与手势（无 CSS easing，native preview ≤24ms，release 先 flush 再 commit，cancel/blur/删除必终止）；Meter 为测量 ballistics（amp→dB `−60…0`，attack `τ12ms`、release `τ280ms` EMA、epsilon `.00025`、hidden 停 rAF 并归零），非装饰动画。

## 动效验收要点

- `prefers-reduced-motion` 关闭装饰动效且保留信号 ballistics；反向/快速重复从当前可见位置继续；退出 ghost 不可命中不可聚焦；dense meters 禁动态 blur；`will-change` 按需挂卸。
- 覆盖 press/drag/release/pending/ACK/settle 及延迟/拒绝/超时/context cancel；Router route ACK 改 topology token 而 flags ACK 不改，模拟器须分别覆盖；定位函数不得引入“归零→强测→恢复”同步布局瞬态。
- 异步 Worker 携带 context/revision 仅接纳当前结果，fallback 不证明 Worker 通过。
