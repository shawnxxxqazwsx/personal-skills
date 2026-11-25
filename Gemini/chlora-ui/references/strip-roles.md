# Strip 角色与作用域

> 层级：L1 任务（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。材料、端口身份、选择与信号分别定位；CSS custom property 按实际元素及祖先逐层解析，后加载 `:root` 不覆盖子树局部声明。

## 最终 Owner 与作用域边界

| 层级 | 实际 Owner | 复用边界 |
|---|---|---|
| 共享默认材料与端口角色 | `draftroom/strip/ui/host-strip-patch.css`（根 tokens 与端口规则） | 共享蓝（Input）/黄（Process）/红（Output）适用于无局部覆盖的消费者 |
| Chlora 墨绿主题端口 | `host/web-shell/ui/host-surface.css` 的 `.app #routing` | 闲置墨绿；Input 青绿、Process 鼠尾草绿、Output 暖陶褐，三 rail 内 active ink 各有局部声明（保留冻结值） |
| 点按与选择反馈 | `host-strip-patch.css`（端口 hover/press 与 Mixer 轮廓）；`host-surface.html`（`stripSelectionGroups`、`stepStripSelectionSpring`） | 端口按压缩放 ≠ 普通命令内凹；Mixer 仅细轮廓无整列填色；Inserts 不复制 Mixer 线宽 |
| 独立 CLR Router | `cl-utilities/plugins/utilities/gain/ui/cl-router.html`（`main#routerApp.cl-router`） | 无 `.app` 祖先，沿用共享根色与独立状态 owner，见 [cl-router.md](cl-router.md) |

## 行为与验证

- **端口连线**：沿 `host-surface.html` 的 `routePorts`、`updateRouteDragPreview`、`finishRouteDrag` 与 `#routing .port` 绑定；分测 held preview、Escape 清理与有效 drop 命令。
- **Insert 槽与 Mixer 选择**：Insert 菜单走 `bindInsertChipActions(root,channel)`，保持 worker 身份独立于显示 index，拖放提交与菜单 Move later 分开验证；Mixer 选择保留 exclusive / modifier toggle / range 及弹簧进退与 reduced。
- **正反例**：Chlora 新 routing 端口从 `.app #routing` 继承身份色同时复用共享 patch 材料；禁以“最后加载”刷回蓝/黄/红，或将 Chlora 局部墨绿外溢到 CLR Router。
