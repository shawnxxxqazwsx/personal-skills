# Handoff Template

Use the language of the user's current request. Keep headings recognizable and omit truly inapplicable sections rather than filling boilerplate. If no required work remains, mark the task complete and omit `立即下一步` and `新会话首条指令`.

```markdown
# 交接 · [项目或主题] · [YYYY-MM-DD]

## 当前状态
[一段话：目标、已到达的状态、准确停点、用户最后要求]

## 目标与范围
- **目标**：
- **范围内**：
- **明确不做**：

## 已完成
- [x] [可验证结果，而不是工具调用过程]

## 进行中 / 未解决
- [ ] [现象、剩余工作、复现或验证方式]
- **阻塞**：[无 / 精确条件与所需输入]

## 关键决策
| 决策 | 原因 | 放弃或未选方案 |
|---|---|---|
| … | … | … |

## 相关文件 / 外部状态
| 路径或对象 | 当前状态 / 改动 | 注意 |
|---|---|---|
| `relative/path` | … | 未提交 / 用户原有改动 / 外部 ID 等 |

## 仓库与任务状态
- **项目 / 工作区**：
- **分支 / worktree**：
- **未提交状态**：
- **活动 Goal / 任务对象**：[无 / objective、status、证据与剩余项]

## 验证
- **已运行**：`command` → ✅ / ❌（关键结果）
- **手工验证**：
- **未运行 / 未确认**：

## 假设与风险
- **已验证事实**：
- **待验证假设**：
- **风险 / Gotchas**：

## 立即下一步
1. …
2. …
3. …

## 新会话首条指令
[一句可执行指令，包含第一步所需的项目相对路径和验收点]
```

## 可选：游戏引擎 / Unity 序列化附注（仅在改动引擎资产时追加）

- **引擎版本 / 渲染管线 / 主场景**：记录版本、管线及涉及的 Scene / Prefab / ScriptableObject / Volume。
- **序列化覆盖**：写明 Scene/Prefab 的 Inspector 覆盖值（会覆盖代码默认值），以及受影响的 `.meta` GUID 关系（勿粘贴全文）。
- **包与项目设置**：记录 `Packages/`（如 `manifest.json`）与 `ProjectSettings/` 改动。
- **验证分项**：区分编译、Edit Mode、Play Mode、手工复现与未覆盖平台/场景。
