# 当前证据与现存例外

> 层级：L3 证据（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。复用具名参考时先核对下表：若参考存在已知缺口，新设计仍须遵守 L2 规则而不复制缺口；若属不同语义的合理实现差异，则保留差异。

## 复用时应避开的现存缺口

| 角色 / 参考 | 现存缺口 | 新设计约束 / ID |
|---|---|---|
| 通用 `showForm` Cancel | 相比 IR Import Cancel 缺按压内凹与键盘 focus 材料 | 命令内凹与 focus 须按 L2 规则补全；`PRODUCT-001` |
| Monitor Bus `Device…` | 持续按住仍缩放并留外投影 | 普通命令须走 `momentary` 内凹；`MONITOR-MOMENTARY-OBS-01` |
| Monitor Export `aria-label` | enabled 且 title 清空后 DOM `aria-label` 仍留旧禁用文案 | 可见文案、可用态与辅助名称同步更新；`MONITOR-WORKFLOW-OBS-01` |
| Host 主题切换中途切 palette | mode 动画中切 palette 时旧前景终点先完成再跳新色 | 验收核对交错中间帧；`THEME-V2-OBS-01` |
| Plugin Browser / Cheat Sheet 分段 `::before` | `transform 500ms` 压过低特异性主题过渡致材料提前跳变 | 伪元素须显式组合选择位移与 `--motion-theme-material`；`FILTER-THEME-OBS-01` |
| Strip 插件栏快捷键 `P` 反向 | 收起中途约 325ms 再按 `P` 仍发收起 | 快速反向依据逻辑目标而非未稳定 DOM class；`BROWSER-DRAWER-OBS-01` |
| IR Distance 入场途中关闭 | 入场中途关闭出现透明度不连续 | 退场从当前实时透明度起算；`IR-DISTANCE-OBS-01` |
| Align context 回读后首次输入 | 回读取消旧编辑却保留 focus 后首次新输入可能丢失 | 结束旧事务后新编辑必建新 entry；`ALIGN-READBACK-01` |
| LFE 内联 Ch 取消 | Escape 后 Tab 仍可提交（扩大窗正常） | 内联与扩大窗分测，Analyzer 不作基准；`LIBANA-SRC-02` |
| CLR Router 通道缩减时拖调 | output 6→2 后已退役 `ch6` 拖调仍发值 | 捕获身份退役即停发旧命令；`CLR-SRC-02` |
| Graph Router 按钮失焦释放 | window blur 后原按钮释放可能发反向命令 | canceled gesture 与 pointerup 分离；`GRAPH-ROUTER-FLAG-BLUR-001` |
| LFO 自定义曲线拖点 Escape | capture 将焦点移至 stage 致局部 Escape 未收到 | SVG 子控件焦点与全局快捷键协同；`LFO-CURRENT-01` |
| Group / Comment 文本编辑 | 已存文字画在透明草稿下、两行受定高裁切 | 同步验草稿、静态 copy 与多行高度；`GRAPH-ANNOTATION-EDIT-OBS-01` |
| Source Playback 缩放后 resize | 缩窗后逻辑范围保留但 canvas 右侧留白 | resize 同步核对实际绘制映射；`SOURCE-PLAYBACK-OBS-01` |
| Preset 扩大窗缩窗 | 1600→1280px 后外框未重夹取、Done 出视口 | 外框可达性与内容 camera 分离校验；`PRESET-WINDOW-OBS-01` |
| Analyzer 关闭符号 | 仍用文本 `×` 而非 Reference SVG | 公共关闭语法按 L2 规则，不抄受限现状；`LIBANA-SRC-01` |

## 已锁定结论与非缺陷边界

### COLOR-USER-API-01

现行 Approved B 色板、四主题与用户节点色保护持续有效。`COLOR-USER-API-01` **仅作底层/MCP 保护，不暴露前端右键调色盘**；`ChloraTheme.nodeColor(hue)` 为色相映射、`node.labelColor/nodeColor/color` 为底层保护链、`Jelly` 5-stop 相位色（`#E5484D/#8A8A8A/#3E8BFF`）为功能色阶，不得借此宣称右键选色存在。

- **`STRIP-EDIT-EXCEPTION-01`（锁定）**：Strip 数字编辑透明 caret、无行内 `dB`、禁数字 scrub 保持锁定；`#mixerGrid .channel-well` 已具 `role="slider"` 方向键控制，连续拖拽按 `Escape` 回滚。
- **刻意保留的作用域差异**：`IR-NATIVE-FONT-01`（原生选择器已继承用户 Title/Body 字体）；`CLR-SRC-01`/`03`（VST3 `0ms` 外观瞬切 + `"Follow Chlora"` 字体覆写）；`GUIDE-STRIP-COLOR-SCOPE-01`（共享蓝/黄/红 vs Chlora `.app #routing` 墨绿体系）；`GRO-ANCHOR-SCOPE-01`（附属 Fanout 逻辑锚共中心而端口 hit 盒在两端）。
