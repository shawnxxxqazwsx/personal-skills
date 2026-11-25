# 公共控件：按功能选择真实入口

> 层级：L1 任务（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。精确材料/动效查 [components.md](components.md)、[motion.md](motion.md)、[webview-guardrails.md](webview-guardrails.md)。未导出函数仅作源码 owner，勿虚构公开 API。

## channel-settings

| 任务 | 具名实例与实际 Owner | 继承与禁忌 | 最小验证 |
|---|---|---|---|
| 改 Strip 通道数 | `host/web-shell/ui/host-surface.html`：`#insertChannels/#outputChannels`、`channelCountEntries`、`finishTypedChannelCount`、`syncInsOutChannelInputs` | 原生 number/change 字段（1…128 整数），focus 捕原值与 context；MultiMono Insert 由 Output 锁定；不走 `showForm` | 非法/空/未变/合法、Enter/blur 防重提、旧 context 退役、disabled |
| 改语义通道顺序 | 同文件 `createUnifiedChannelController`、`ChloraUnifiedChannels.sync/result/cancelDrag/handleKey`（多实例 `.create(options)`） | tile 身份为 `role`（非标签或当前位置），保留 current/confirmed/inFlight 与 queued save；family picker 归 `host/web-shell/ui/host-typography.js` | 拖放 Escape 恢复、键盘移动、确认/拒绝、快速 family 反向、reduced |
| 切换 RMS / Peak | 同文件 `showMeterModeMenu`（`setMixerMeterMode`/`setMasterMeterMode`） | 仅 RMS/Peak，不加 Hold；区分 SVG 可点击 stroke 与不可点中心；meter 保留信号 ballistics | 右键命中、当前项、Escape 零命令、单次意图 |

Unified native 角色来源：`draftroom/strip/HostUnifiedChannelSettings.h`、`shared/include/mc/ChannelLayoutRouting.hpp`。

## reference-and-menu

| 任务 | 入口与状态 Owner | 继承要点 |
|---|---|---|
| 公共设置 / 说明弹窗 | `host-surface.html` 私有 `openReferenceDialog/closeReferenceDialog/fitReferenceDialog`（品牌菜单进入） | 中性初始 focus、return-focus、UI zoom 与 viewport clamp；不发明通用模态 open API |
| 帮助搜索与分栏详情 | `#cheatSheetFilter`、`filterCheatSheet/selectCheatModule/setCheatView`、`#cheatSheetOverview/#cheatSheetDetail` | 无结果用 `#cheatSheetEmpty`；旧 pane 立即 inert/aria-hidden（反向时检查非终帧）；不借共享页操作 DarkRoom 或推广 Analyzer |
| 节点二级菜单 | `menuHtml/showMenu/hideCtx` + 节点 builder（LFO 另经 `draftroom/nodes/ui/host-lfo.js`） | selected/focus/disabled 分离；具名 Bridge 项为 `menuitem + .on`（非 `menuitemradio`） |
| 分段选择 | `.mode-group/.filter-row` markup、`.on` 与 CSS `::before` 共同拥有 | 现行二段由 `:has(> button:nth-child(2).on)` 驱动；多段须显式改造状态绑定并组合主题材料过渡（见 [theme-inheritance.md](theme-inheritance.md)） |

## names-and-status

- **长名称 Hint**：`host-surface.html` 的 `.cl-meter-name[data-channel-name]` 由 `graphIoBindNameHints/Show/Validate/HideNameHint` 拥有，浮层 `.chlora-io-name-hint`（完整名称、当前卡片材料、screen-space 夹取、不截 pointer），区别于 socket 原生 title 与 Spatial meter。核对 hover、出界、context 变化与边缘。
- **空 / 等待 / 错误**：按数据 owner 选型（Cheat Sheet 过滤空态、Unified `Saving`/reject、`host/web-shell/ui/host-storage.js` 的 `ChloraStorage.receive`/`#storageStatus`、Preset 保存链），不用通用 spinner 替代状态，并核对错误文案在视口内可见。
- **最终覆盖与伪元素**：普通命令沿 `host/web-shell/ui/host-dark-themes.css` 末段 `data-ui-action="momentary"` 最终 patch 继承（排除持久选择/checkbox/radio/slider/popup），实测持续按住阴影、无位移与单次执行。教学正反例：[material-composition](../assets/examples/material-composition/index.html)。
