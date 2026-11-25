# CLR Router / CLR 3D Panner：独立产品复用入口

> 层级：L1 任务（独立产品，冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。用于维护独立 `CLR Router` / `CLR 3D Panner` 或与 Chlora Strip 同角色对照；源码位于 `~/Projects/cl-utilities`，原生 editor 为 `McRouterEditor`，与 Graph Router/Matrix 及 IR 内部路由窗隔离。

## 资源与五层 CSS Cascade

| 层 | 实际入口（`cl-utilities/`） |
|---|---|
| 产品与打包 | `CMakeLists.txt`（`PRODUCT_NAME "CLR Router"`、`McRouterAssets`） |
| 原生窗口与外观 | `plugins/utilities/gain/McRouterEditor.cpp`（`syncWindowGeometry`、`resource`、`event`、`refreshAppearance`） |
| 页面、控件与共享函数 | `plugins/utilities/gain/ui/cl-router.{html,js}`、`cl-router-shared.js`（冻结模块） |
| 主题/字体副本 | `vendor/host-ui/`（独立副本，非 `mc-patcher` 直接引用） |

**五层加载顺序**：`vendor/host-ui/host-surface.css → cl-router.css → vendor/host-ui/host-dark-themes.css → cl-router-sm.css → cl-strip-patch.css`。最后两层拥有现行 S/M、端口与选择表现，禁止摘取前层已被覆盖的样式。

## 任务 Owner 与关键契约

| 任务 | 源码 Owner 与语义 | 禁止误用 |
|---|---|---|
| 端口、线缆与多选路由 | `layout/drawRoutes/selectPort/patchPairs/changeRoutes/cancelRouting` + `cl-strip-patch.css`；批量越界整组拒绝 | 把选择当连线；把 Strip 端口缩放套至 Graph Router |
| Input / Master 推子 | `startFader/moveFader` + `dbToPreGainT/dbToFaderPos`（Input −30…+30 dB 线性；Master −100…+12 dB 非线性） | 合并 taper；给参数跟手加装饰 easing |
| Mixer gain/delay 选中组 | `commitChannelGain`（相对差值）/ `commitChannelDelay`（绝对值） | 混用相对/绝对规则；把选择染色当 Solo |
| 直接数字输入 / 拖调 | `editNumber/startNumberDrag/endNumberDrag`；静态框统一真负号 `U+2212` `−`；完整原值捕获与校验 | 取整文本当原值；`parseFloat` 接前缀 |
| 数字右键与剪贴板 | `openNumberMenu/numberClipboard/receiveNumberClipboard`（绑定请求/编辑身份/revision） | 弹菜单或迟到回复直接提交参数 |
| S/M 刷选 | `beginSmPaint` + `cl-router-sm.css`；首目标定态，状态/ARIA/命令即时 | 当作 momentary/Checkbox；混干湿 Solo |
| 设置 / Order / 字体覆写 | `menuItems/closeMenu`；`CLR Router` 与 `CLR 3D Panner` 对称支持 `"Follow Chlora"` 字体覆写菜单 | 把菜单触发器当音频开关；误删作者下缘 |
| Spatial meter | `renderSpatial/updateSpatialLevels/spatialAction` + `graphSpatialMarkup`（按真实布局显示已知/推断/unavailable） | 按声道数编造扬声器；替代 `Jelly` 规范 |
| 原生窗口 | `McRouterEditor` 逻辑几何 + 宿主尺寸协调 | 套用 Graph world/screen-fixed 定位 |

- **MASTER 专项**：鼠标命中 SVG `[data-fader="master"]`，键盘归 `#masterFader[role="slider"]`，数字为 `#masterValue`。`moveFader` 经 UI 缩放与曲线几何反解 taper（Shift fine 作用于物理位移）；指针实时发 `begin/value/end`，键盘走 `complete` 等回读更新。
- **动画与 `0ms` 主题瞬切**：端口材料/缩放读最终 patch；S/M 与数字材料各自进退；Mixer 选择保留弹簧，meter 保留信号 attack/release（reduced 仍响应信号）。`applyAppearance` 不调 `ChloraTheme.apply`，按四层场景色域分工锁定 VST3 **`0ms` 瞬切**。

## 最小验证与现存缺口

离线完整页面必须装齐全部五层 CSS、脚本与字体；`cl-utilities/tests/` 可选入口：`cl_router_sm_paint_webkit_verify.mjs`、`cl_router_multiselect_composed_browser_verify.mjs`、`cl_router_numeric_menu_verify.mjs`（注意该旧测试资源表曾漏后两层 CSS，不可直接作完整视觉验收）、`cl_router_fader_edit_verify.mjs`、`cl_router_port_labels_verify.mjs`。

**避免复制的已知缺口（`CLR-SRC-02`）**：输出由 6 缩至 2 后，持有已退役 `ch6` 的 fader/gain/delay 拖调仍会发旧通道值；新增交互须在身份退役时立即终止手势。
