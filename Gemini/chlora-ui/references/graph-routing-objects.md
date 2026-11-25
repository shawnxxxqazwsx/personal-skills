# Graph 路由对象

> 层级：L1 任务（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。用于连线、端口、Cable Pin、Snake/Merge/Fanout 与 Group/Router 附属对象；Router/Matrix 控件见 [design-recipes.md](design-recipes.md#recipe-router)，独立插件见 [cl-router.md](cl-router.md)。

## 三种位置与源码 Owner

**语义端点**（连谁）、**绘制锚点**（画到哪）、**DOM 命中区**（从哪操作）须分别沿真实 owner 维护，不得用可见圆心或 DOM 序号代替完整语义 tuple。下列函数位于 `host/web-shell/ui/host-surface.html` 私有作用域：

| 对象 / 任务 | 具名源码入口 | 必须保留的身份与状态 |
|---|---|---|
| 端口与连接捕获 | `graphNodePinItems`、`updateGraphPinElement`、`bindGraphPinActions`、`finishGraphPinDrag`；`button.graph-pin[data-pin-kind/role/ch]` | 起终 node、role、channel、bundle、branch；held preview、合法/无效目标、取消与提交 |
| 线绘制与选择 | `normalizeGraphWire`、`graphPortXY`、`graphLiveWirePath`、`graphWireRoutePointsWithPins`、`graphWireLifecycle`；`.graph-wire`/`.wire-under`/`.wire-over` | 核心线、背景线、hover hit 与选择分离；按完整语义 tuple 定位 |
| Cable Pin 与拖动 | `createGraphCablePinIndex`、`graphCablePinsForWire`、`addGraphCablePinAtClient`、`selectGraphCablePin`；`begin/apply/cancel/finishGraphCablePinDrag`；`svg .graph-cable-pin` | `pinId`、所属 wire 完整 tuple、`order` 与 parent；Pin 即时跟手，线缆走自身收敛模型 |
| Snake / Fanout / Merge | `graphNodePinItems`、`graphNodeMetrics`、`graphSumVisibleBranches` | aggregate 端口非单通道；空态与已接线区分；Merge 显示 lane 与真实 bank 身份分离（如稀疏 `[0,2,1]` 中 spare 不重编号已占 bank） |
| Group 附属 Fanout | `graphGroupFanoutLayout`、`graphGroupFanoutForNode`、`graphGroupFanoutWorldCenter`、`refreshGraphGroupAttachedFanouts`；`.is-group-fanout` | group/member/附属 node 身份与边；`graphPortXY` 共中心逻辑锚，端口 hit 盒在两端为中间 grip 留空间（勿强行统一圆心） |
| Router 附属 Snake | `graphRouterAttachmentMarkup`、`refreshGraphRouterSidecars`、`graphPortSnakeOwner`；`.graph-router-sidecar-channels`、`[data-graph-snake-sidecars]` | 遵守 sidecar 与 hidden topology 合同 |

## 运动、事务与验证

- 线缆选中、Pin 跟随、路径趋近（`τ75ms`）与出入场沿 [motion.md](motion.md) 各自继承，不改 180ms 材料动画；取消须撤回手势并清理捕获/preview。
- 用真实指针事件核对命中与坐标，禁 forced click 或扩 hitbox 凑绿；保存/恢复须满足完整拓扑与几何持久化合同（含逆序/乱序记录恢复与完整端点/branch/Pin 比对）。
