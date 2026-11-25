# 节点、图标与控件

> 层级：L2 规则（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。相似功能允许存在有结构理由的场景变体（如 Strip/Graph 插件栏模型、不同体量窗口时长、不同 gain taper、不同 selection 形态），仅同角色同状态差异进入一致性审查。

## 节点与区域语法

| 对象 | 结构与最小几何 | 继承与边界 |
|---|---|---|
| Snake | 固定 76×68（title 28 + body 40）；左右各一 aggregate jack | empty/pack/unpack 说明操作，不随通道数拉高 |
| 附着 Snake | full 宽 132；compact 最小 16×16，每 attachment lane +8px | 完整覆盖时单 external socket，不画折叠 scalar comb |
| Merge | `280×(36+44×visibleBranches+8)`；occupied banks + 1 spare | 分支 gain/S/M/Ø + output gain；按真实拓扑，不按记录顺序推断分支 |
| Fanout | loose 76×68（title 28）；单 aggregate in/out 可多连线 | 输出分发由连接表达，不堆叠多个相同 jack |
| Group/Stack Fanout | 18×18 结构节点；中 18×10 圆角 socket；10px 透明 drag rim | 共用单可见 socket；Stack 边界跟 Stack 身份色 |
| Router | 宽 ≥190，高 `30+18+16×visibleRows`；左右 scalar ports | header 含 Router/Matrix 与 expand；完整 Snake 覆盖时 compact |
| Matrix | 同 Router 节点；compact pitch 22/14/10/7（CH ≤16/32/64/>64）；宽 `max(190,48+out×pitch)`，高 `72+in×pitch` | 左输入/下输出；expanded pitch 28、880px 窗，canvas `max(220,110+out×28)×(116+in×28)`，clamp viewport |
| Align | `270×(100+40×CH)`；header 48、bottom 52；行 label 48/gain 44/toggles 78/delay 50，gap 6 | MASTER 与逐通道分开；ports 40px 节距 |
| Stack v2 | `graphGroup` + 成员 + 边界节点；紧凑卡 `min-width:228px`、header 36；Detail Editor（`.is-compact-cols`/`.is-dense-cols` + `.stack-fallback-submenu`） | **成熟参考基准**；由 `stackCount/stackWidth/stackLaneWidths/members/fanouts` 决定，非单卡 |
| Chloe Input | `.chloe-input-node`；`.chloe-input-instance-btn` + 复用 Chloe Instance 垂直 meters + 右侧 GAIN 列 | **成熟参考基准**；与普通 hosted node 参数区隔离 |
| Jelly（原 Nebula） | `min 400×280`；顶栏内联 `Detail`（`.nebula-detail-toggle`，无独立 `.nebula-editor` 浮窗）；底部 Band-Pass 色谱滑轨（`.nebula-bandpass`：`.nebula-bp-toggle`/`BP`/`.nebula-bp-track`/`.nebula-bp-window`/`[data-nebula-bp-handle]` 拖拽与双击关闭、键盘 `Enter/Space/Escape/←→/↑↓/[]/Shift`、关态 `Full`）；`#E5484D/#8A8A8A/#3E8BFF` 5-stop 相位色；全局 `Render resolution (0.5×–3×)` | **专用受限 Analyzer 表面**；`1.5px` 焦点边框；仅保留 `Speaker angles` 与 `Phase colors` 模态框 |
| Level Meter | Target 开启含 `Tol <val> dB` scrub（`[data-level-target-tolerance-control]`）与可拖公差下界线/悬浮标签（`.level-meter-tolerance-line`/`.level-meter-tolerance-label`，`>16ch` Canvas2D 禁 `shadowBlur`）；底栏同源 Jelly 联动只读徽章 `.level-meter-bandpass-badge`（`BP <lo>–<hi> Hz`，`--level-bp-hue`） | **专用受限 Analyzer 表面**；`1.5px` 焦点边框 |
| Spectrogram / LFE Spectrum | 单画布 `[data-spectrogram-canvas]` 统一绘制坐标轴（无 `.spectrogram-axes` 副 canvas）；`[data-spectrogram-tolerance-line]` 可拖；叠层复选框标签统一 `LF`（`LFE Spectrum` 独立节点标题不变） | **专用受限 Analyzer 表面**；`1.5px` 焦点边框；`Unavailable` 旧统计读数降为 `--spectrogram-dim` 半透明态 |
| Pin | cable SVG circle r5，坐标 `/3` | rest cream + wine 边，hover/selected 反转；非普通 node 存储 |
| File Source | `minW 426`，`minH=max(300,180+18×CH,50+outputRows×pitch)` | 源/播放/加载/metadata、水平 meter+S/M、右 MASTER；raw ports 或 Snake |
| Monitor Bus | `min 500×562`，header 30；spatial edge=`width−126` | workflow、downmix、spatial/bars+MASTER、footer；`listeningPorts` 真时才有 through outputs |
| Playback 兼容节点 | 无 ports 440×260；source+wrapped 440×286；header 40 | 兼容路径，非新卡片默认模板 |
| File Source Playback | 浮窗 960×400（min 380×220），clamp viewport | 可拖 header、wave/loop/ruler/transport/zoom，复用 IR handles |
| LFO | 固定 480×306（header 40、curve 180）；4 边 24px mapping hit、9px dot | 无 audio ports；custom points/tangents；disabled 非通用静音模板 |
| IR Loader | `min 400×280`（header 40、inset 47/18/10） | overview、Load WAV/Bank、三列参数（Wet/Gain/Pre-delay/Decay/Size 含单位）；WAV/Bank summary 分支不同 |
| IR expanded | 初始 1800×1240（min 640×440、max 2200×1440，screen clamp）；row 110、master 140、wave 72 | 共享 normalized time axis；普通模式 All channels master + 16 行分页/8 行视觉组，Complete Bank 为 All IRs 单 master；SVG 波形（上 fade diamonds、下 trim triangles、右 gain contour/thumb） |
| IR internal routing | 绑定同一真实 Router editor | 不另造近似 matrix |
| IR Distance | screen-space 840 宽、radius 16、plot 300；1–5m、depth 0…48dB、两 Bézier grips | Linear/Logarithmic/Inverse-exp；bypass 虚线 + `.65`；仅支持 Bank 显示 |

源码 owner 分布于 `host/web-shell/ui/host-surface.{html,css}`、`draftroom/strip/ui/host-channel.js`、`draftroom/nodes/ui/host-{lfo,stack}.{js,css}`、`draftroom/ir-loader/ui/host-ir-{loader,distance}.{js,css}`、`darkroom/playback-monitor/ui/host-file-{monitor,playback}.{js,css}`、`audio-bridge/chloe-host/ui/host-chloe-input.{js,css}`。Group frame、Comment、hosted plugin exposed params 与附着 ports 不得被框选误认作独立可 group 节点。

### Router / Matrix 落点、选中、标签与 Stage Portal

- **落点与选中**：Node 栏拖入时节点左上角对齐鼠标 world 坐标（参与 camera pan、Graph zoom、UI zoom），保留有限带符号坐标，不夹入旧 Input/Output 或强设 `y≥20`。折叠背景与 Matrix 预览空白继承普通节点选中/拖动及 Shift/Meta 增减选中；模式/展开按钮与有效单元格点击选中所属卡片但不拖动节点，已选中时连续操作不反向取消选中。预览 canvas 仅放行左键空白路径，截住非左键/不可用手势防止中键平移卡死。Owner：`graphAddDropEngineXY`、`selectGraphRouterControlOwner`、`bindGraphRouterCrosspoints`、`bindGraphNodeActions`、`host/engine/PluginHostEngine.h::addRouterNodeLocked`。
- **标签、模式材料与通道控制**：Graph 端口与附着 Snake 范围仅用数字（`1-2`、`1-16`），展开 Router 行用 `Channel 1/2`，不拼原生 UID 方括号或完整布局名（真实名留数据层，scalar socket 空白面 + tooltip）。折叠 Router 标题 30px，模式按钮高 26px / line-height 20px / 上下 pad 3px，hover/focus 用 10% `currentColor`；expanded 标题按钮 30px。展开 Matrix 左侧输入 S/M、下方输出 S/M/Ø（22px，共用原生通道命令），底部状态行固定 37px 单行 ellipsis（文案变化不改窗高/居中）。S/M 支持按住刷选：首个按钮决定目标态、快速跨行填补中间通道、重入不反转、输出保留多选批量，Ø 仅单输出；pending 回读不重置目标，取消/失焦/关闭/上下文变化立即终止。
- **Stage Portal**：主 Graph 浮动窗挂在 `#graphStage` 内、`#graphWorld` 外的 `#graphRouterWindows`（不含相机变换，仍受 UI zoom 约束），IR 内部 Router 保留自身 inline/bounds。通过 `graphRouterPanel` / `graphRouterPanelOwner` 解析归属（禁 `closest('.graph-node')`）；普通关闭立即 inert 并隐藏、重开复用；节点替换/删除/lifetime 变化走 `graphRouterDisposeWindow` 清理。每个请求保留独立到期时间，快捷 ACK 同步浮动窗按钮。

## 功能预览图标（preview07）

统一 **148×88** 逻辑卡（title 28 + body 60，drawer scale `.7`），为抽象功能图解而非面板缩略图。普通 SVG 48×48（绘 46×46），LFO/IR 72×48（绘 68×46）。三层语法：结构线 `currentColor` stroke 1.8 round；次级结构 opacity `.42`、wash fill `.12`、少量 solid 信号点；活动路径单部位独立 accent stroke 3.1（IR 3.6）+ 同底色 clearance stroke 6.1（IR 6.6）。SVG 为 decorative、不截 pointer、不加 tab stop。

| 类型 | 功能语义 | Light accent | Dark accent |
|---|---|---|---|
| File Source | 发出点与传播弧 | `#a1d9ff` | 同 |
| Snake | 束内独立弯曲 lanes | `#aea3ff` | `#aca3ff` |
| Merge | 左到右汇聚 + 单路输出 | `#9de663` | `#c0de3e` |
| Fanout | 左到右分发至三端点 | `#ff939c` | `#ff8dbe` |
| Monitor Bus | 汇入中心 | `#ffbf81` | 同 |
| Router | 3×3 crosspoint 三选通格 | `#4fbcff` | `#65b8ff` |
| Align | 两对应瞬态峰对齐 | `#f3abee` | `#f6aae9` |
| Stack | 叠层模块前沿 | `#fc9400` | 同 |
| Pin | 曲线固定锚点环 | `#70c1bf` | 同 |
| LFO | 双相位正弦与周期强调 | `#2a8f00` | `#62c24c` |
| IR | 首脉冲峰与衰减轮廓 | `#008a8b` | `#4cbbbb` |

来源：`host/web-shell/ui/host-surface.{html,css}`、冻结基准 `tests/fixtures/host_node_preview_v7.json`（仅非排除项）；preview accent 与 node fill 分别冻结，不互推。

## Ports 与线缆

scalar pin 12×12 圆、bundle 18×10 r3、sidechain 方角 r2；输出透明 hit disk `55.4256px`。色阶（node accent）：deep 82%、mid 58%、soft 24%、pale 14%、halo 34%。scalar wire under/top `4.5/2.25`（selected `5.5/2.6` opacity `.95`）；bundle `10/6`（selected `12/7`）；preview dashed `5/4`。线从 jack 中心连续到 jack 中心，fan-in/out 离开一 jack 半径内可分辨；curve/straight/orthogonal 保持完整端点与 Pin 语义。

## 按钮、开关、参数与关闭/Transport

- **瞬时命令与 S/M**：普通瞬时命令正向标记 `data-ui-action="momentary"`，采用 Browser 式稳定内凹（双向 180ms bg/box-shadow，无位移/缩放，已移除 `.graph-node button:active { scale: .96 }` 兜底与 IR Load WAV 悬停下划线）；Graph 规则归 `#graphStage`。必须排除带状态语义控件（`aria-pressed/checked/selected`、radio/switch/tab/slider、S/M/Ø、拖调数字、波形/loop handles、resize、Play/Pause toggle）。成熟文字 S/M（Strip/Align/Source/Merge/Router/Matrix/IR Solo）亮灭背景/字色双向 180ms ease，实际状态与命令即时；Merge S/M/Ø 24×24 去向下外投影，保留独立 hover 层 180ms 与 2px inset focus，数值框仍保留下方框阴影。File Source Solo 键盘焦点复用 Strip 2px 材料内缘（`currentColor` 55%，仅 `[data-fg-source-solo]:focus-visible` 清除额外 outline，不推广到 Mute）。Snake 操作用 `.graph-snake-wrap-icon`（16×16 三线汇聚 SVG mask、stroke 1.5、`aria-pressed=false` 旋 180° 180ms；HTML `≋` 为隐藏 fallback 非最终图标）。
- **Matrix 开关方格**：Host 全部真实 `input[type=checkbox]`（含 `role=switch`，涵盖 Settings、IR 导入、Jelly Phase/Outline、Spectrogram `LF`）共用 Matrix 背景 cell + 白色内方块（仅 unchecked/checked/disabled，无勾号/滑钮/mixed）；按真实经过时间 250ms smoothstep（详见 [motion.md](motion.md)），native `checked` 为唯一值源，程序赋 `.checked` 须调 `ChloraCheckboxUI.sync()`，不发假 change 或闲置轮询。
- **直接拖调数字与校验**：统一采用 Align/Graph 材料（hover 7% + `0 2px 7px` 16% 阴影，focus 12% 3px 圆角，180ms ease，文字与材料框居中，IR Time 收框保右锚）；非法键入恢复编辑前完整原值且不 commit。详见 [numeric-fields.md](numeric-fields.md)、[numeric-validation.md](numeric-validation.md)。

| 参数 / 手势 | 现行契约（勿强行合并差异） |
|---|---|
| Strip 输出 gain | −100…+12 dB（≤−99.5 显示 −∞）；unity `.716`、−60 在 `.08`、−18 在 `.5`（非线性） |
| Strip input trim | −30…+30 dB 线性 |
| Mixer fader | relative drag（3px 阈值、点击不跳）、rAF 显示、native preview ≤24ms、release flush 后 commit、双击 unity；`#mixerGrid .channel-well` 具 `role="slider"` 方向键控制（保持 `STRIP-EDIT-EXCEPTION-01`）；连续拖拽 `Escape` 取消回滚 |
| Inline editor | click 进透明 text input，下 rAF focus+select；Enter/blur 完整合法且有变化才 commit，Escape/非法恢复原值；typed 越界拒绝，拖动 clamp 独立 |
| Merge gain | 垂直 `.25 dB/px`（Shift `.05`），计 UI/Graph zoom；preview ≤24ms；双击 0；方向键 `.5/.1`、Page ±3；拖拽 `Escape` 回滚 |
| Align | gain −100…12 dB / delay 0…500 ms；垂直 `clientY` `.1 dB/px` 或 `.1 ms/px`（Shift `.01`，3px 阈值，不照搬 Merge zoom 补偿）；方向键 `.5/.1 dB` / `.1/.01 ms`；MASTER 复用 gain |
| File Source gain | −100…12 dB，pointer 绝对位置 preview，up commit / cancel 回滚，方向键 `1/.1`，loading 禁用 |

- **关闭符号与默认完整视图**：编辑窗关闭统一 SVG（20×20、`viewBox="0 0 24 24"`、`M5 5l14 14M19 5L5 19"`、`currentColor`、stroke 1.8 round、`aria-hidden`/`focusable="false"`；动态用 `.chlora-window-close`，保留原按钮命中包络，不套用于 clear-loop/删除 slot）。所有编辑器（IR/Source Playback/Playback/DarkRoom fresh-open/Preset）新开默认完整视图且无 Fit 按钮，同窗回读/resize 保留当前手动 zoom，长内容用分页/滚动保证可达。
- **顶栏项目入口与 Transport**：`#instanceToggle` 恒定 `inset 0 -2px 0 var(--wine)`（empty/linked/project 同框，保留实际 `.on/.live`/长名 ellipsis）。New/Open/Cancel/Create 接入 `momentary`；`.topbar button.instance-item` 180ms ease 材料。File Source Playback / Full Playback / DarkRoom 回到起点统一 SVG（`viewBox="0 0 16 16"`、`M4 3v10m8-9L6 8l6 4z"`、stroke 1.5 round、CSS 14×14 居中、`.chlora-transport-home-space` 保原命中包络）；Full Playback 与 DarkRoom 播放/暂停统一 Chlora SVG 播放图标（不再用文本 `▶`/`Ⅱ`）。
