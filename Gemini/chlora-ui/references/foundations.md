# 布局、材料、文字和主题

> 层级：L2 规则（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。所有尺寸均为逻辑 px；新增功能可按规则扩展，不随意重画已有控件。

## 工作面组织

主界面为 `host/web-shell/ui/host-surface.html`，由 `host/web-shell/HostShell.h` 启用、`host/web-shell/HostWebChrome.h` 解析资源。独立 `host-shell.*`、`host-browser.*` 仅作兼容路径，不与主路径混用。

| 结构 | 现行基准 |
|---|---|
| 顶栏 | 44px，连续底板与区域分隔，不加浮动卡片阴影 |
| 插件栏 | 展开 `clamp(170px,18vw,280px)`，折叠 40px；进 Graph 初始折叠，回 Strip 恢复偏好 |
| Strip 三段 | Routing `minmax(140px,28%)`；Inserts `minmax(0,1fr)`；Mixer `minmax(130px,35%)` |
| 通道列距 | 默认 56（可选 48/56/64/80/96/112）；Inserts/Mixer 同轴；余白不触发 flex-grow |
| 通用控件 | 高 24/20/18（`--ctl-h`/`-sm`/`-xs`）；横 pad 9；圆角 6；连续 plate 不叠卡片 |
| 节点库 | 底部 drawer（NODES/PRESET → Routing/Modifier）；`Shift+Space` Node Lens |
| Graph | 世界坐标与 screen chrome 分离；源码节点坐标通常 `/3` 进 CSS 坐标再经 camera transform |

来源：`host/web-shell/ui/host-surface.css`、`host/web-shell/ui/host-surface.html`。端口数变化优先调整 owning layout 的内容 envelope，不留无用尾部空白；浮层须明确归属 graph-world 或 screen-fixed（后者须 clamp viewport），不得用布局换算覆盖已保存 geometry/topology。

## 角色色与批准色板

正式锁定「四层场景色域分工」：主界面暖纸（Light）/三暗色（Graphite/Slate/Carbon）+ Analyzer 零色偏灰 + DarkRoom 纯黑 + VST3（`CLR Router` / `CLR 3D Panner`）`0ms` 瞬切。

| Token / 角色 | Light | Graphite | Slate | Carbon |
|---|---|---|---|---|
| plate / bg | `#fff7e9` | `#1a1a1a` | 同 | 同 |
| raised | `#f3e8d6` | `#3d3d3d` | 同 | 同 |
| well | taupe 透明凹槽 | `#1d1d1d` | 同 | 同 |
| ink | `#342a25` | `#c5bfb5` | `#c0ccd4` | `#bbc9c3` |
| dim | `#79665a` | `#98938b` | `#98a1a8` | `#909b96` |
| mute | `#a18d80` | `#7f7a73` | `#73808a` | `#6e7d76` |
| accent / wine 映射 | `#7a2e3a` | `#c5bfb5` | `#6b89a4` | `#658c82` |
| quiet accent | `#8e4f5c` | `#938e84` | `#50667c` | `#425f57` |
| Solo | `#ffd078` | `#d4ae74` | `#d6b47b` | `#d2b37e` |
| Mute | `#b34c3f` | `#d48985` | `#df918d` | `#d58b87` |

| 节点身份（Approved B） | Light | Graphite | 说明 |
|---|---|---|---|
| Snake | `#5b5b36` | `#484723` | Slate/Carbon 完整映射见 `host-dark-themes.css` |
| Merge（internal sum） | `#634f6e` | `#493e5e` | 退役旧色（Snake `#6A6A3E`/Merge `#5A3E6A`/Fanout `#4A8080`）禁作基准 |
| Fanout | `#2e6262` | `#204f43` | 新节点颜色批准后显式登记，不按序号随机取色 |
| Router | `#6f5139` | `#593f24` | — |
| Stack | `#3c5c75` | `#294860` | — |
| Align（internal channel） | `#426147` | `#2d4e37` | — |

来源：`host/web-shell/ui/host-surface.css`、`host/web-shell/ui/host-dark-themes.css`、`draftroom/strip/ui/host-channel.css`。不要把 Light 的酒红强调误推为深色主题也必须显示酒红。

Modifier 使用低色度 OKLCH 材料：LFO hue320、IR hue15（light surface `.91 .024` / ink `.31 .012`，dark surface `.355 .002` / ink `.87 .024`）。File Source header 暖棕、surface `#e2dfd2` / dark `#252525`；Monitor Bus header `#2e587a`，body 复用 file surface；Playback 为 neutral hue85。详见 `draftroom/nodes/ui/host-lfo.css`、`draftroom/ir-loader/ui/host-ir-loader.css`、`darkroom/workspace/ui/host-file-graph.css`、`darkroom/playback-monitor/ui/host-file-monitor.css`、`darkroom/playback-monitor/ui/host-file-playback.css`。

## 电平与增益视觉分工

Light console meter 使用不透明 taupe ramp：`#7e6b59 → #9a7d63 → #af9176 → #c3a789`（相对已填充盒，无 alpha 尾羽）。Dark Strip 后置覆盖为单色 `--dark-control`、轨道 `--dark-raised`（`host-dark-themes.css`），不按彩色 ramp 覆盖深色 Strip；Graph 专用 meter 保留各自角色映射。品牌强调不代替电平/故障；S/M 用文字、位置与完整状态块补足颜色；增益设定、信号量与 pending 确认三者不混用。

## 字体、材料层级与最终 Cascade

默认 Title 为 Charm，Body 为 original（正文 Charm，detail 系统无衬线）；保留用户字体偏好不强行重置。字号阶梯：micro 12、caption/value 13、ui 14、body 15、title 16、brand 20。数字启用 `font-variant-numeric:tabular-nums` 且不省略单位。Charm 仅用 400/700；S/M 用 `--font-detail`（idle 600 / active 700）；Barlow 有真实 600 资产。来源：`host/web-shell/ui/host-typography.js`、`host-surface.css`。

连续底板、局部控件凹槽、可抓取 thumb 与细分隔线构成材料层级。**以最终 computed cascade 为准**：现行 hover/selected diffuse elevation（`host-dark-themes.css`）和深色 Strip 单色 meter 均覆盖早期源码注释（如“never halo”），不得据旧注释删改现行效果。保留用户节点色，状态识别不只靠色相。全产品不存在统一全局 tooltip delay，不编造默认延迟常数。
