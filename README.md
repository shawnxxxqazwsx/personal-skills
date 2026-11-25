# Personal Skills

个人 Antigravity (Gemini) Skills 同步仓库（原 `codex-skills` 更名并重构）。

## 目录结构

- `Gemini/`：仅同步 **Antigravity (Gemini)** 使用的 15 个 Skills，所有符号链接均已解引用为真实文件，可直接检出或链接到 Antigravity 的本地 skills 目录。

## 同步边界与安全策略

- **平台限定**：本仓库 `Gemini/` 仅面向 Antigravity (Gemini) 环境；不混入其他 harness 的重复副本。
- **永久排除项**：永久排除任何服务器运维类 Skill、主机/公网 IP、SSH 配置、环境变量文件（`.env` / `*.env`），以及一切含凭证、私钥、Token 或个人隐私路径的私有文件。
- **体积与卫生控制**：同步时自动跳过 `.DS_Store`、`__pycache__/`、`*.pyc`、符号链接等本地缓存垃圾；`chlora-ui` 省略约 116 MB 的本地历史图鉴快照（`assets/atlas/`），并对示例 provenance 记录中的本机主目录前缀做了 `$HOME` 脱敏。

## `Gemini/` Skills 清单（共 15 项）

### 编排、检索与会话记忆（4 项）

| Skill | 简介 |
|---|---|
| [`orchestrator`](Gemini/orchestrator/SKILL.md) | Antigravity 专属多代理编排与 Swarm 调度（Pure Dispatcher Primary、原生 Gemini 配额调度、UI 双模式协作与公开发布安全门控）。 |
| [`web-research`](Gemini/web-research/SKILL.md) | Antigravity 原生 Gemini 4 Hydrogen 多路并行联网调研与主代理交叉核验，所有 URL 与论文先抓取后引用。 |
| [`memory`](Gemini/memory/SKILL.md) | 基于 `~/.mnemon-mcp/memory.db`（SQLite + FTS5）的跨模型、跨会话长期记忆读写（程序性偏好、项目里程碑与稳定架构事实）。 |
| [`session-handoff`](Gemini/session-handoff/SKILL.md) | 单任务或跨窗口切换时的临时工作态交接摘要与新会话续跑上下文生成。 |

### 音频工程、Chlora 与宿主控制（6 项）

| Skill | 简介 |
|---|---|
| [`chlora-development`](Gemini/chlora-development/SKILL.md) | Chlora 跨平台（macOS / Windows）代码开发、架构、CMake 构建、测试与部署规范（Host、DraftRoom、DarkRoom、Audio Bridge、Network Audio、Meris、CLI/MCP）。 |
| [`chlora-operation`](Gemini/chlora-operation/SKILL.md) | 通过 MCP、原生 `clara` CLI 或受控 UI 回退实时操控运行中的 Chlora 宿主（Graph、Strip、IR Loader、Analyzers、FileGraph、DarkRoom）。 |
| [`chlora-ui`](Gemini/chlora-ui/SKILL.md) | Chlora 宿主界面（Strip、DraftRoom、公共弹层、原生文件选择器）及独立 CLR Router / CLR 3D Panner UI 的视觉与交互规范（公开版省略本地百兆图鉴快照 `assets/atlas/`）。 |
| [`daw-control`](Gemini/daw-control/SKILL.md) | REAPER、Nuendo/Cubase、Pro Tools、Logic Pro、Ableton Live 等常见 DAW 的实时检查、多通道路由、插件重载、导出与落盘信号验证。 |
| [`immersive-audio`](Gemini/immersive-audio/SKILL.md) | 通道/对象/声场/WFS 空间音频格式、心理声学、双耳与扬声器渲染 DSP、房间声学校准、编解码交付标准与论文语料分析。 |
| [`pigora-eq`](Gemini/pigora-eq/SKILL.md) | Pigora 硬件 EQ 模块的公开资料提取、滤波器与控制律拟合、编译后频响验证与上线后审计。 |

### 网页设计、数据可视化与创意媒体（5 项）

| Skill | 简介 |
|---|---|
| [`web-craft`](Gemini/web-craft/SKILL.md) | 全栈网页视觉设计、交互动效编排与无头浏览器门控验证（显式分流 Track A `commerce` 商业站与 Track B `showcase` 创意动效站）。 |
| [`lieflat-charts`](Gemini/lieflat-charts/SKILL.md) | 面向真实定量数据的单文件 HTML 统计图表与 R01–R12 中英双语数据叙事报告生成（严格复用 Lupi/Basics/Glance/Maps/Interactive 原版模板）。 |
| [`threejs`](Gemini/threejs/SKILL.md) | 基于 three.js r185（`WebGPURenderer` + 自动 WebGL2 回退）、TSL 节点材质、物理与后处理的实时 3D 场景构建与排障。 |
| [`onetake`](Gemini/onetake/SKILL.md) | 基于单文件确定性 HTML 合成（`window.__seek(t)`）的 10–60 秒产品动效短片与多语配音功能演示渲染（`.mp4`）。 |
| [`imagegen`](Gemini/imagegen/SKILL.md) | 独立位图素材（`.png` / `.jpg` / `.webp`）的生成与参考图编辑（摄影视觉、插画、概念图、贴图与透明背景抠图）。 |
