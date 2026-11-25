# 原生文件选择：模式、外观与生命周期

> 层级：L1 任务（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。此处的 Browser 是 Chlora 自绘 JUCE `PickerWindow` / `HostIrFileBrowser`，不是 macOS `NSOpenPanel`，也不是旧 `host/web-shell/ui/host-browser.html`。

## 按任务选 Owner 与模式

| 任务 | 入口与模式 | 禁止套用 |
|---|---|---|
| IR Bank 导入 | `ChloraIrLoaderUI.beginGroupImport` → `requestGraphIRGroupImport` → `MainComponent::openIrBankMenu` → `openIrMatrixPicker(...,"group")` | 非多选 WAV；不保留窗口进逐通道 mapping |
| IR WAV 导入与 mapping | `HostFilePickerOptions` 默认 WAV 模式可多选并保留窗口；`ThemedIrFileChooser::showImport` 检 retain/window/active 后转交 `PickerWindow::showImport` | 禁止跳过前置门槛直接以同名 `PickerWindow::showImport` 为入口 |
| 项目 / File Source / 插件 / 目录 / 导出 | 核对各调用点 `HostFilePickerOptions` 工厂、过滤、回调与 `paletteRole` | 共享窗口类不代表过滤、多选、保存或流程相同 |

Bank 由 `HostFilePickerOptions::project(bankRoot)` 建立，配置 `*.irmatrix.json`、单选、`rememberSelection=false`、`retainForIrImport=false` 与 `irLoader` `paletteRole`。源码：`draftroom/ir-loader/HostIrFileChooser.{h,cpp}`、`draftroom/ir-loader/HostIrFileChooser_mac.mm`、`draftroom/ir-loader/IrRouterMatrixMain.inc`、`host/app/MainComponent.h`、`draftroom/ir-loader/ui/host-ir-loader.js`。

## 设计角色、窗口链与验证

- **材料与颜色**：`HostIrBrowserTheme::fromOwner(origin,paletteRole)` 读取宿主主题与 dark palette 交本窗 LookAndFeel；`irLoader` 与 `audioSource` 分离；不把 Web Graph 节点色直接作原生列表选中色。
- **字体**：原生文件选择器已继承用户 Title/Body 字体偏好（`IR-NATIVE-FONT-01`），文件名/路径细节按系统可读字体渲染。
- **选择、键盘与运动**：`HostIrFileBrowser::updateSelection` 管 Open 可用态，`complete` 仅消费一次；`navigationKey/keyPressed`、FileList 与 PathEditor 各管键盘范围。运动按 [motion.md](motion.md) 与 `draftroom/ir-loader/HostIrBrowserMotion.h` 执行（open 320ms / close 220ms / scan dissolve 200ms / 列表弹簧 `ω30/32`）。绘制归 `draftroom/ir-loader/HostIrFileBrowser.{h,cpp}`、`host/app/HostLookAndFeel.h`，属性同步归 `host/web-shell/HostShell.h`。
- **事务链**：`createHostIrFileChooser` → `ThemedIrFileChooser::open` → `PickerWindow` → `HostIrFileBrowser`；WAV 转 mapping 保留窗口 bounds 并 dissolve 内容。关闭/Escape/取消须移除 peer、清 callback、消费 serial、清 busy 并发布回读，过期目标必须拒绝。
- **原生验证入口**：`tests/host_ir_file_browser_verify.cpp`、`tests/host_ir_picker_lifecycle_verify.cpp`、`tests/host_ir_group_main_verify.inc`（核四主题、边缘、长路径、键盘、取消/目标替换与回调一次性；HTML 不可代原生验收）。
