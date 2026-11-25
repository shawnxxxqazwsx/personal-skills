# 主题继承：真实 Owner、四层色域与中间帧

> 层级：L2 规则（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。离线正反例：[theme-owner](../assets/examples/theme-owner/index.html)、[material-composition](../assets/examples/material-composition/index.html)。

## 真实 Owner 与四层色域分工

- **Host 主题链**：材料过渡由 `host/web-shell/ui/host-surface.css`（`.theme-changing`、`--motion-theme-material`）拥有；前景过渡由 `host/web-shell/ui/host-theme.js` 的 `ChloraTheme.apply` 拥有——先采样当前可见色、切主题收齐目标，再建固定终点 WAAPI（320ms）。仅复制 `color 320ms` 会导致嵌套继承色拖尾；仅复制 `--motion-*` token 不会让未声明 transition 的材料运动。
- **触发分支**：Light ↔ Dark 的 mode 切换走 320ms 材料与前景动画；稳定 Graphite / Slate / Carbon 互切不新启该前景动画；`animate:false` 立即收尾。
- **四层场景色域分工**：
  1. 主界面暖纸（Light）/ 三暗色（Graphite / Slate / Carbon）：mode 切换走 320ms 链。
  2. Analyzer 家族（`Jelly`、Spectrogram、LFE Spectrum、Level Meter）：零色偏灰专用表面。
  3. DarkRoom：纯黑专用工作区。
  4. VST3（`CLR Router` / `CLR 3D Panner`）：`applyAppearance` `0ms` 瞬切（详见 [cl-router.md](cl-router.md)）。

## 分段标记与最终 Cascade 组合

二段 `.filter-row::before` 同时绘制选中位置、填充与底边阴影；`host-surface.css` 中该伪元素的 `transition: transform 500ms …` 特异性高于 `:where(:root.theme-changing …)`，导致现有 Plugin Browser / Cheat Sheet 的 `::before` 主题材料提前跳变（见 `FILTER-THEME-OBS-01`）。新设计复用时须在最终有效规则中显式组合选择位移与 `--motion-theme-material` 主题材料属性，并用 `getComputedStyle(el, '::before')` 检查中间帧，禁止用 `transition:all` 或全改 500ms 替代。

## 验证要点

核对实加载 CSS 与真实调用链；从稳定初态分别测正常 mode 切换、快速反向、稳定 palette-only、mode 动画中途切 palette（防 `THEME-V2-OBS-01` 跳变）及 reduced-motion，同时观察底板、控件、伪元素边框/阴影与前景的中间帧，不凭终帧截图判定通过。
