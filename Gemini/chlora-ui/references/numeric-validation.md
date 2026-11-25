# 数值校验：非法输入保留编辑前原值

> 层级：L2 规则（冲突顺序见 [SKILL.md](../SKILL.md#1-文档分四层按层读取)）。适用于所有可自由键入的参数（含点击输入与直接拖调数字的编辑态）；不为只读值新增编辑，不改变推子、旋钮、拖动或方向键的原有范围与夹值律。

## 提交契约

1. **完整捕获原值**：进入编辑时保存真实参数原值、完整快照及对象/会话身份，不得从 `toFixed` 显示文本反解；`0`、小数与 `−∞` 领域值均须保真。
2. **完整 token 校验**：仅接受完整合法 token，按字段声明校验有限性、范围、整数或 step；保留 owner 已定义的单位与静音别名（如 Merge 的 bare `inf/Infinity/∞`、Strip 的负 `∞` 别名），不跨 owner 扩大合法语法。
3. **非法恢复原值**：空串、混入字符、非法格式、溢出/越界或不合法 step 在 Enter/change/blur 时一律不提交，显示恢复编辑前原值；禁止归零、取边界、取最后合法中间值或发同值 commit/undo。
4. **清除脏 preview**：输入中允许未完成草稿；若已有合法中间 preview 而最终非法，取消整次 entry、回退原快照并清除该 owner 的 preview。
5. **未改动不量化**：未修改显示文本的 click→Enter/blur 不得量化完整原值；合法输入沿用各参数精度/单位（如 DarkRoom 秒数采样点量化 vs Hz 声明 step）。
6. **上下文守卫**：会话切换、源替换、节点删除或迟到回包不得把旧参数写入新对象。

禁止用 `parseFloat('1abc')`、`Number('')`、`Number(value)||0` 或 truthy/falsy 做提交判定；typed 越界输入不得交给 drag/readback clamp。

## 表单、错误反馈与最小验证

- 通道数、Router/Align/Stack 尺寸、IR 导入、Device 及选区范围等自由数值表单同守此契约：非法字段恢复编辑前值、保留其余编辑内容、拒绝 OK/Apply，不得静默填默认值。Device/Analyzer 适用本功能契约，但其视觉不作成熟基准。
- 使用现有文案或语义错误标记（保留 LFO Remote 非法范围波浪线）；不引入浏览器默认 validation 气泡、焦点框或下划线强调。
- 最小验证：原值 `0` 与非零、Enter 与 blur、先合法 preview 再非法、未编辑不量化、合法相邻输入、旧 context 拒绝；注意避开 IR/Merge 双击归零误触发，并区分原生 `type="number"` 拦截字符。对照样本：[数值校验前后对照](../assets/atlas/numeric-validation.html)。
