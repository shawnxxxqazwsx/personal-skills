# IR Loader Reverb Bank：完整规格与复现流程

本文件用于从新的 IR 数据集制作 **Stereo → 9.0.6** 或 **9.1.6 → 9.0.6**
矩阵混响，并让 Chlora 的 **IR Loader → Load Bank…** 一次加载整套矩阵。
不需要此前对话、INSPIRATA 专用生成器或现有混响库才能使用本规格。
Clara、Chlora、IRL、ILO、IRO 在这类请求中均应先核对是否指这个 IR Loader。

规格核对日期：2026-10-25。依据当前 `clara://ir-router-matrix/v1` 完整组加载器，
以及 Chlora 0.1.2.249 的内部 IR 路由实现。以后源码若改变，应重新核对本文的
“源码与验证入口”，不能仅靠产品版本标题判断二进制已经包含这些能力。

## 1. 最短可执行工作流

1. 先确定每个 IR 的 **物理声源、接收位置、声道、时间基准和来源**，列出实际
   source→receiver 覆盖。不能用“文件有16声道”推断它已经是这个矩阵。
2. 把每个实际测得的 source→receiver 传递函数准备为 **48,000 Hz、mono、
   IEEE float32 WAV**。保留原始素材，只生成新的工作副本。
3. 复制 [完整配方示例](../assets/ir-bank-recipe.example.json) 到自己的工作目录，
   修改 `profiles`、`outputs` 和 `transfers[].file`，使其准确指向自己的 IR。
   示例有15个独立 source、15个 receiver、225条完整物理传递，以及两个输入格式。
4. 运行生成器；目标目录必须是新的绝对路径：

   ```bash
   python3 "$SKILL_DIR/scripts/ir_bank.py" build /absolute/work/recipe.json --output /absolute/library/NewRoom-Array-Min
   ```

5. 分别校验两个输出入口：

   ```bash
   python3 "$SKILL_DIR/scripts/ir_bank.py" validate '/absolute/library/NewRoom-Array-Min/01_立体声输入_9.0.6输出.irmatrix.json' --profile stereo
   python3 "$SKILL_DIR/scripts/ir_bank.py" validate '/absolute/library/NewRoom-Array-Min/02_9.1.6输入_9.0.6输出.irmatrix.json' --profile 916
   ```

6. 按第9节选择匹配的单 IR Loader 节点预设，在 **Load Bank…** 中选择其中一个
   `.irmatrix.json`。等待 native `Ready`，再检查声道和音频；不能把 Python 校验
   PASS 或窗口里出现名称当作原生加载成功。

生成工具需要Python 3.10或以上，仅用标准库，无需安装pip依赖。
以上脚本路径相对仓库根目录；从别处执行时改用该脚本的实际绝对路径。
不需要构建或连接 Chlora 就能生成和离线校验 Bank。脚本不修改原始 IR、现有 Bank、
应用、声卡或正在运行的 Graph。

## 2. 固定声道合同：不要混淆载体、有效输入和物理 IR 数

| 项目 | Stereo 输入版本 | 9.1.6 输入版本 |
|---|---|---|
| 单节点预设实际外露总线 | 2输入 → 16输出 | 16输入 → 16输出 |
| manifest 的输入／输出载体 | **16 / 16** | **16 / 16** |
| 有效输入槽，manifest从1开始 | `[1,2]` | `[1,2,3,5,6,7,8,9,10,11,12,13,14,15,16]` |
| `silent_input_slots` | `[3,4,5,6,7,8,9,10,11,12,13,14,15,16]` | `[4]` |
| 有效输出槽 | 全部非4号槽，共15个 | 相同 |
| `silent_output_slots` | `[4]` | `[4]` |
| 完整逻辑 IR 路径数 | **2×15=30** | **15×15=225** |
| 空节点状态的 `internalBankInputs` | `2` | `15`，不是16 |
| 物理 lane 引用数 | `15×不同physical_source_id数量`，通常30 | 同公式，最多225 |

**manifest 两个 bus 字段始终填16**；不能因为立体声节点只有两个外露输入就把
`input_bus_channels` 改成2。输出称9.0.6，是15个有效扬声器；文件／节点使用16槽载体，
第4槽 LFE 保持静音。9.1.6 输入中的 LFE 不进入这些混响路径。

标准语义和顺序如下。UI／DSP路由数组从0开始，manifest从1开始；转换只减1一次。

| manifest槽 | UI/DSP索引 | 语义 | 常用manifest标签 |
|---:|---:|---|---|
| 1 | 0 | Left | L |
| 2 | 1 | Right | R |
| 3 | 2 | Centre | C |
| 4 | 3 | LFE，输入和输出均静音 | LFE |
| 5 | 4 | Left wide | LW / Lw |
| 6 | 5 | Right wide | RW / Rw |
| 7 | 6 | Left side | LS / Ls |
| 8 | 7 | Right side | RS / Rs |
| 9 | 8 | Left rear | LB / Lrs |
| 10 | 9 | Right rear | RB / Rrs |
| 11 | 10 | Top front left | FTL / Ltf |
| 12 | 11 | Top front right | FTR / Rtf |
| 13 | 12 | Top middle left | MTL / Ltm |
| 14 | 13 | Top middle right | MTR / Rtm |
| 15 | 14 | Top rear left | RTL / Ltr |
| 16 | 15 | Top rear right | RTR / Rtr |

Wide 在 Side 之前。别的数据集可能以不同顺序、坐标系或缩写记录；必须实际重映射，
不能只改标签。`role` 在原生格式中只是非空显示字符串，既不会自动重排 WAV，
也不会证明其声学方向正确。Stereo 输入的 role 也可以是 `stage_source_01` 等标签。

## 3. 从其他 IR 数据集构造传递矩阵

对默认输入直通和默认输出映射，在100% wet时：

```text
wet[o,n] = Σ(active input i) gate[i,o] × convolution(x[i], h[physicalSource(i), receiver(o)])[n]
```

一条 IR 是一个 **实际物理 source→receiver 传递函数**，不是一个输出音箱的整个
16声道混音，也不是“房间只有一条IR所以复制225次就算测过225个位置”。

- 将多声道 IR 拆成mono前，要有该文件的声道→receiver对应表。接收方向未知时先
  记录未知并取得必要信息，不凭声道数猜 Ambisonics、FuMa、Atmos或音箱顺序。
- 普通 stereo reverb 的 L/R 文件不自动包含15个接收方向。资料不足不能生成一套
  冒充实测的完整空间矩阵。可在用户明确允许后制作带清楚标注的派生／近似版本。
- 保留原始增益、符号、测量延迟、相位和早期反射；不要为提高相关性、响度或某个
  验收数字而自行逐IR归一化、对齐、EQ、截头或改变极性。
- 若必须转采样，用真实采样率转换生成新的48k副本并记录方法；不能只把 WAV 头
  的采样率改为48000。若需从多声道文件取某通道，应显式选择该通道，不能盲目downmix。
- 记录坐标、单位、轴向、角度约定、声源／接收器身份、原文件通道、采样率、许可、
  实测／合成／插值／复用身份和缺失位置。这些影响声学可信度；格式PASS不证明它们。

### 允许共享物理声源时的精确 folding

同一个 `physical_source_id` 可以映射到多个逻辑输入槽。对于每个 receiver，
**只存一条物理 lane**，其 `input_slots` 列出这个source对应的所有逻辑输入。

例如逻辑槽1和11共用S01，则S01→L的lane为：

```json
{"physical_source_id":"S01","input_slots":[1,11],"output_slot":1,"receiver_id":"L"}
```

还必须对其余14个receiver各有一条相同 `input_slots` 的S01 lane。不能把同一个
S01→L拆成 `[1]` 和 `[11]` 两条lane；也不能漏掉11。其他source继续依此规则。
这样即使只有3个物理声源，也可以在用户允许位置复用时组成225条逻辑路径，
实际只需要45条物理传递引用；当前 Input Router 仍可分别关闭这两个逻辑输入的路径。

复用策略不是对所有数据集的默认许可。天空↔相应地面、地面按最近方向复用是本库
曾采用的授权策略；给新用户／新数据集制作时，按其意图和测量证据确定是否允许，
记录方向误差和复用关系。不要把不同位置仅因文件相同、曲线相似或名字接近就合并身份。

## 4. 可加载 manifest 的全部字段

文件名推荐以 `.irmatrix.json` 结尾，供 **Load Bank…** 浏览器识别。顶层为JSON对象；
原生拒绝条件来自完整组校验与文件获取校验的交集，而不是通用旧matrix导入器的宽泛上限。

| 字段 | 类型／必需值 | 含义 |
|---|---|---|
| `format` | string，`clara://ir-router-matrix/v1` | 完整Bank入口格式 |
| `version` | integer，`1` | manifest版本，不能填内部路由版本2 |
| `entry_uuid` | 非空string | 入口身份；推荐为每个入口生成并保留UUID，原生未强制UUID字面格式 |
| `label` | 非空string | 整套Bank显示名称 |
| `input_bus_channels` | integer，`16` | 包括静音槽的输入载体 |
| `output_bus_channels` | integer，`16` | 包括静音槽的输出载体 |
| `max_sample_rate` | integer，`192000` | 协议声明的准备上限，**不是WAV采样率** |
| `package_root` | 非空相对路径string | 资源包的边界目录，相对manifest所在目录 |
| `inputs` | 非空array | 每个有效输入恰一行，见下表 |
| `outputs` | 非空array | 每个有效receiver输出恰一行 |
| `silent_input_slots` | integer array | 与inputs无重复、无遗漏地覆盖1–16，包含4 |
| `silent_output_slots` | integer array | 与outputs无重复、无遗漏地覆盖1–16，目标版本为`[4]` |
| `banks` | array，1–8项 | **内部存储分块**，一次整体加载，不是多个用户Bank |
| `metadata` | 可选object | 来源、坐标、RT、族／尺度、处理和近似说明等；不参与自动补齐矩阵 |

`inputs[]` 每行必需：`slot`（integer 1–16）、`physical_source_id`（非空string）、
`role`（非空string）。`outputs[]` 每行必需：`slot`、`receiver_id`、`role`，规则相同。
input/output槽位都不能重复；4号槽不能在有效数组中。
推荐数组按slot排序，source与receiver的标识保持稳定且可追溯。

每个 `banks[]` 对象必需：

```json
{"id":1,"lanes":[...]}
```

`id` 从1连续；每个chunk的 `lanes` 非空，最多128条。每条lane的完整必需字段：

```json
{
  "lane": 1,
  "input_slots": [1],
  "output_slot": 1,
  "physical_source_id": "S01",
  "receiver_id": "L",
  "sample_rate": 48000,
  "frames": 48000,
  "mono_wav": "assets/S01-L.wav",
  "sha256": "这里必须填该WAV整个文件实际计算所得的64位小写SHA256"
}
```

上面的单lane是字段说明，**不是可加载的完整Bank**；完整文件必须覆盖全部30／225
逻辑cell。完整可生成示例见配方文件与生成器，不能把`...`或示意hash直接写入成品。

| lane字段 | 必须满足 |
|---|---|
| `lane` | integer，每个chunk从1重新连续编号 |
| `physical_source_id` | 必须出现在inputs，且与该lane全部input_slots的source一致 |
| `input_slots` | 非空、无重复integer array；包含该source对应的**全部**有效输入槽 |
| `output_slot` | 有效输出槽1–16，不是4 |
| `receiver_id` | 必须与outputs中该output_slot的receiver_id完全相同 |
| `sample_rate` | integer，`48000` |
| `frames` | integer，1–1,440,000，且等于WAV的实际frame数 |
| `mono_wav` | 非空相对`.wav`路径，**相对manifest目录** |
| `sha256` | WAV整个文件字节的SHA256，64位小写hex |

整数不能用字符串、小数或JSON boolean代替。所有active input×active output组合必须
恰好覆盖一次，`physical_source_id + output_slot` 也必须全局唯一；不允许有静音槽cell、
重复lane、缺少传递或用别的source的IR代替而不改清楚身份。

### 全局排序规则

source的顺序由 `inputs[]` 中 `physical_source_id` 的**首次出现顺序**决定，不是按ID
字母排序。对每个source，按 `output_slot` 数值递增列出receiver。这个顺序在所有chunk
之间连续保持；切到下一chunk只能重置 `lane` 编号，不能重排source／output。
允许在一个source的15个receiver中间切chunk。

## 5. WAV、长度、预算和分块

原生完整Bank要求每个引用文件实际是：mono、48kHz、32-bit IEEE floating-point WAV。
PCM16／24／32、float64或多声道WAV都不能直接当此处mono资源引用；先显式转换副本。
随附工具使用little-endian RIFF/WAVE，接受普通IEEE float格式标识3和正确的
WAVE_FORMAT_EXTENSIBLE IEEE float32；要求`fmt `块先于`data`块，且文件长度与RIFF声明
一致。不支持RIFX／RF64。不要只检查扩展名或JSON的frames；`data`先于`fmt `的文件
会被当前原生读取路径拒绝，工具也应提前拒绝。其他合法metadata块可保留并计入文件SHA。
样本不能含NaN／Inf。48k shared FFT另检查 `max(abs(sample)) ≤ 1e6`，
每条IR `sum(abs(sample)) ≤ 1e9`；这只是有限算术保护，不是推荐混音电平。

每条最多30秒；**每个chunk内**frame数必须完全相同，**不同chunk之间**可以不同。
生成器为简化复现，要求所有用到的WAV同长；有差异时默认报错。明确设置
`pad_to_common_frames: true` 才会在新的工作副本末尾补零到共同最大长度，
不会改源文件、增益、起点、符号或IR中已有样本。不要用截掉长IR的方式偷偷满足预算。

每个chunk同时满足：

```text
1 ≤ lane_count ≤ 128
Σ(lane.frames × 192000/48000) = Σ(4 × lane.frames) ≤ 120000000
完整Bank的chunk_count ≤ 8
```

这是192k准备的sample预算；数值上恰好等于48k float32数据字节数，**语义上不是
整个WAV文件字节数上限**，不能把RIFF头也加进公式。

若同长为F帧，单chunk容量为 `min(128, floor(120000000/(4F)))`。
225条、每条817612帧约17.03秒时，单chunk最多36条，需7个chunk；一次Load Bank即可
全部加载。225条全30秒时单chunk最多20条，需12个chunk，超过8，**当前格式拒绝**。
225条共同长度在8chunk约束下最多1034482帧，约21.551708秒。
不能仅检查“每条≤30秒”就声称整个225条矩阵可加载。

## 6. 目录、共享、命名与catalogue

推荐自包含结构；同一阵列／大小的两个格式共享assets：

```text
IR Bank Library/
  RT 01.20 s · 大厅 · Room Name/
    Array Family/
      01_Min/
        assets/                           # 实际mono WAV，只存需要的物理资源
        01_立体声输入_9.0.6输出.irmatrix.json
        02_9.1.6输入_9.0.6输出.irmatrix.json
  bank-catalog.json                       # 可选，不是供Load Bank选择的matrix
```

先写可排序的RT，再写房间类型、房间名称，之后族、大小、输入格式。推荐RT数值补齐
位数（如`RT 00.90 s`），便于按名称排序。RT60不是WAV总长度；没有测量／依据就标未知，
不能从文件尾长直接编造RT60。三种大小×两种阵列技术×两种输入格式=每空间12个入口，
这是现有库的组织约定，**不是所有新Bank必须有12个的格式限制**。

`package_root` 相对manifest目录解析；`mono_wav`也相对manifest目录解析，**不是**
相对package_root。两者canonical后，manifest和全部WAV都必须位于canonical package_root
内；符号链接也不能逃出。自包含文件夹用`package_root: "."`。
跨多个阵列共享原资源时可以使用`../..`等相对root，但它必须是真实共同祖先，且移动
整库时保留相对结构。运行时保存的group state还绑定manifest绝对路径；移动以后应
从新位置明确重新加载，不能承诺旧工程会自动定位。

manifest最大16MiB。`entry_uuid`保持稳定，内容修订后重新算外部catalogue hash。
WAV的SHA必须是完整文件字节SHA，增加一个metadata chunk也会变；manifest的外部SHA
同样受JSON排版影响。加载过程中不能改manifest或WAV；旧工程引用不匹配时可能成为
Missing IR并静音，而不是自动接受修改过的文件。

可选catalogue格式如下，其中path相对**配置的Bank库根目录**：

```json
{
  "schema":"clara://ir-bank-catalog/v1",
  "banks":[
    {"room":"Room Name","label":"RT 01.20 s · 大厅 · Room Name · Array · Min · 立体声 → 9.0.6",
     "path":"Room-Array-Min/01_立体声输入_9.0.6输出.irmatrix.json",
     "sha256":"填manifest整个文件的实际64位小写SHA256","active_inputs":2}
  ]
}
```

916的 `active_inputs` 为15，不是16。当前native读取catalogue要求文件≤1MiB、最多4096项；
schema／path／SHA决定匹配校验，room、label、active_inputs是有用的索引信息，不能代替
manifest本身的有效输入检查。生成可用索引：

```bash
python3 "$SKILL_DIR/scripts/ir_bank.py" catalog /absolute/library --output /absolute/library/bank-catalog.json
```

脚本拒绝覆盖已有索引；更新现有库时先生成新文件、审核diff和hash，再在该次任务
授权内替换。不要为新房间覆盖别人的全库索引。

## 7. 生成配方：与manifest不是同一个schema

生成器命令读取：

```json
{
  "schema":"chlora-ir-bank-recipe/v1",
  "label":"RT unknown · Unclassified · Custom Room · Array · Min",
  "room":"Custom Room",
  "profiles":{
    "stereo":[{"slot":1,"physical_source_id":"S01","role":"L"},{"slot":2,"physical_source_id":"S02","role":"R"}],
    "916":["此处必须是完整15行；直接使用完整配方示例，不要保留这个说明字符串"]
  },
  "outputs":["完整15行slot/receiver_id/role，见完整示例"],
  "transfers":[{"physical_source_id":"S01","receiver_id":"L","file":"raw/S01/L.wav"}],
  "pad_to_common_frames":false,
  "metadata":{"measurement_kind":"由实际来源填写","coordinate_convention":"由来源填写或明确unknown"}
}
```

此片段只解释schema；[完整示例JSON](../assets/ir-bank-recipe.example.json) 没有省略的输入、
输出或transfer行。它引用的`raw/S01/L.wav`等是应由用户提供的实际资源路径，不是自带的
真实房间音频。复制模板后必须核对身份映射，不能把示例S01等名称当作测量证据。

- profile key只用`stereo`或`916`；可只生成其中一种或同时生成两种。
- 每个profile的inputs遵守第2节槽位集合。input `role`可省略，工具填标准标签；显式
  role是非空显示字符串。outputs始终完整15行，`receiver_id`应稳定，recipe工具要求
  outputs中15个receiver ID唯一，以使transfer的(source,receiver)键无歧义。
  原生manifest解析器本身不强制这个ID唯一，不能把工具的配方限制误写成原生限制。
- `transfers`必须覆盖所选profile用到的不同source×15个receiver，不多不少、不重复。
  `file`可为绝对路径或相对recipe目录的路径；**成品manifest**使用相对资源路径。
- 工具只接受已经准备好的mono48kfloat32 WAV；不盲猜输入文件中应拆哪一声道，也不
  内置重采样／归一化。缺少测量时会报错，不能生成假的传递函数补数。
- 同物理资源可以被Stereo和916入口引用；工具保留source/lane身份。即使对完全相同
  字节进行文件存储去重，也不能据此宣称两个不同物理source测量身份相同。
- 成品名称在base `label`后追加输入格式，便于加载时辨识；RT、房型、房名仍在前。
- `build`和`catalog`成功向stdout输出JSON receipt，失败向stderr输出错误并返回非0；
  build拒绝已存在的输出目录。保留receipt和输入来源表作为交付证据。

## 8. 不要混用四种文件／版本

| 文件／层 | 格式与版本 | 应由谁生成 |
|---|---|---|
| 可选全库索引 `bank-catalog.json` | schema `clara://ir-bank-catalog/v1` | catalog helper／维护流程 |
| **Load Bank选择的 `.irmatrix.json`** | format `clara://ir-router-matrix/v1`，`version:1` | 本规范生成器 |
| 已加载节点的持久状态 | kind `clara://ir-loader-group/v1`，state `version:2`（原始）／`3`（整体编辑） | IR Loader原生保存 |
| 空的typed单节点预设中的IR状态 | kind `clara://ir-loader/v1`，state `version:5` | 原生节点／预设作者 |

group state v3另外保存`bankEdit`：`master`（start/end/fadeIn/fadeOut/gainDb/muted）、`sizePercent`、`decaySeconds`和兼容用`decayPercent`；不修改manifest版本。旧v1/v2按未编辑原始Bank恢复，空节点预设仍为scalar v5。

后两者内部还有 `internalRouting.version:2`，其中：

- `kernelRoutes` 是 **0-based** `{input,output}` 数组，控制实际IR路径，默认30／225全开。
  `[]`明确表示全关，不能当成“未设置所以用默认值”。
- `outputRoutes` 是receiver→host输出映射，默认15个非LFE对角映射。
- `inputRoutes` 是旧工程保留的前级premix兼容状态，默认输入直通。
  **它不是本轮Input Router展示的30／225条IR路径。**不要把225个cell写入这里。

这些状态字段不应塞入Bank manifest当作版本升级，也不能用手工伪造的processor state
替代完整manifest。旧内部路由v1状态迁移时默认打开全部真实IR路径。

## 9. 原生加载、单节点预设和后续切换

1. 读取当前Host状态、实际通道顺序和节点身份。按 [layout.md](layout.md) 留出无遮挡
   的位置。查找并取得两个现有单IR节点预设的原生预览；名称只是选择线索，核对它们
   实际仅有一个IR Loader、Stereo外露2→16或916外露16→16、`internalBankInputs`为2／15。
2. 如果本机缺少这两个预设，可用本skill的原生生成的
   [Stereo模板](../assets/ir-bank-presets/INSPIRATA%20Stereo%20to%209.0.6.clara-preset) 和
   [9.1.6模板](../assets/ir-bank-presets/INSPIRATA%209.1.6%20to%209.0.6.clara-preset)。
   两者IR引用为空，没有绑定INSPIRATA音频，名称不限制新数据集。仅在用户要求安装／
   使用时，放入其Settings配置的Graph Presets目录；已有相同ID／文件时先比较并复用，
   不覆盖不同内容、不创建重名副本。之后刷新库并用原生list/get核对实际预览。
3. 在 **Settings → IR Banks** 选择共同Bank库根目录。现有本机示例库在
   `/Volumes/HUB_SSD/INSPIRATA_9.0.6_Arrays_20261023/01_Banks_按混响时间`；这是本机
   位置示例，新的数据集和其他机器应使用实际路径，不必仿造这个路径。
4. 通过原生Preset库加载匹配的单节点预设。按实际源宽度和输出映射连接
   `Source → IR Loader → Monitoring Output`，优先两条完整Snake；无需外部两个Router。
   将完整16槽输出接到支持该布局的下游；声卡监听设备和1–16物理输出映射另行核实。
5. 点击 **Load Bank…**，选择对应profile的**一个**`.irmatrix.json`入口。
   原生后台准备其中全部内部chunks；不要逐chunk选择、逐WAV导入，也不要再创建225个节点。
   这一步是Bank加载，不是`Load WAV`／普通单IR导入，也不是旧的外部Router矩阵创建菜单。
6. 等待加载完成，核对 `status=Ready`、`groupManifest`、`groupLabel`、资源revision，
   `internalRouting.kernelRoutes`默认30／225条，输出非LFE15条和实际总线宽度。
   预览的“available”、`No IR`、准备中、Missing IR或名称出现都不算Ready。
7. 打开右上角 **Routing**：原版Advanced的Input窗口显示并控制真实IR路径；Output
   窗口控制receiver→host映射。第4槽禁用，任意窗口关闭或Esc应同步关闭两窗。
   原版 **1:1** 按钮会只保留对应对角IR路径，**不是恢复默认全30／225开通**。
8. 同格式换Bank不改跳线。**当前自定义kernel开关和Output映射会保留**；如果先前
   使用过1:1／全关，换Bank不会替用户自动打开它们。要默认全矩阵效果，可明确恢复
   全部路径或重新加载干净的匹配节点预设。错格式选择应被拒绝且不改原Bank。
9. 另存工程并验证恢复；路径和SHA绑定必须保持可访问。不要在运行中重写已引用WAV。

`.clara-preset` 是原生Graph预设XML容器，内含节点及编码后的processor state；它不是
Bank JSON，也不能直接交给Load Bank。使用随附完整文件和原生预设库，避免自行拼写
编码state、总线描述或Snake字段。空节点预设只确定路由和输入规格，仍需加载实际Bank。

### 9.0 原生 MCP / `clara` CLI 全程控制 Reverb Bank

现在可通过原生 MCP / `clara` CLI 完成 IR Bank 库目录配置、`.irmatrix.json` 加载与全部内部路由/编辑控制（不再依赖原生 Load Bank 文件浏览器）：

- **库目录配置 (`chlora_manage_system`)**：`action="setIrBankFolder" | "addIrBankFolder" | "removeIrBankFolder"`，传入绝对 `path`；`action="getLibraries"` 回读当前 `irBankFolder` / `irBankFolders`。目录变更会自动持久化落盘至宿主首选项，首次 `addIrBankFolder` 也会自动容忍尚未创建的默认空目录。
- **Bank 枚举、取消导入与高级矩阵控制 (`chlora_graph_ir_advanced`)**（均需完整 Graph 绑定；`listBanks` 与 `cancelImport` 允许省略 `nodeKey`，其余 8 项动作必填 IR `nodeKey`）：
  - **`listBanks`**（只读，`nodeKey` 可选）：枚举全部已配置 `irBankDirectories()` 下的 `*.irmatrix.json`，返回 `folders` / `banks` / `count` / `truncated`。
  - **`cancelImport`**（`nodeKey` 可选）：取消进行中的文件选择器、Web 导入弹窗、排队编辑、`IrImportControl`（含 `loadBankFile`）及非控制态 WAV 导入作业，并释放 `pendingIsolatedLoads_ > 0` 门控。
  - **`expectedRevision` 双令牌严格拆分（切勿混用！）**：
    - **`setInternalRoute`、`resetInternalRoutes`、`setDistance`、`clearDistancePreview`**：校验的是 **`node.irLoader.internalRouting.topologyRevision`**（绝不是 `waveformRevision`！）。
    - **`setGains`、`audition`、`getWaveform`**：校验的是 **`node.irLoader.waveformRevision`**。
    - **`loadBankFile`**：`expectedRevision` 可省略或留空（未传时默认回退当前 `node.irLoader.waveformRevision`）。
    - （对比：`chlora_graph_set_ir_*` 如 `import_ir`、`retry_ir` 在空节点未加载时接受 `expectedRevision: ""`，加载后校验 `node.irLoader.waveformRevision`。）
  - **`loadBankFile` 同步回包 + 后台互斥门控（无 `operationId`！）**：
    - 传入绝对 `path`（`.irmatrix.json`）后，**`loadBankFile` 立即同步返回当前 `state()`，不生成 `operationId`，切勿调用 `chlora_get_operation`**！
    - 后台准备期间宿主置位 `pendingIsolatedLoads > 0`，此时发起任何非只读 MCP 写入都会被拒绝并报 `"Plugin load is pending; poll its operation before another write"`。
    - **正确等待方式**：轮询 **`chlora_get_state`** 直至 **`node.irLoader.preparing == false && node.irLoader.busy == false && node.irLoader.status == "Ready"`**（且 `error` 为空），随后从该最新 state 分别读取 `node.irLoader.waveformRevision` 与 `node.irLoader.internalRouting.topologyRevision`。
  - **Stereo Profile 拓扑与上游 `irBankLogicalInputs` / `Chloe Input` 前置条件**：
    - `ir_bank.py` 的 `stereo` profile 生成的是 **`2 → 16`（9.0.6，30 个脉冲通道，LFE slot 4 静音，`01_立体声输入_9.0.6输出.irmatrix.json`）**，不存在 `2 → 2` Bank。
    - 若使用 Standalone FileGraph 预置或新建的 **`Chloe Input`** 连向 `2ch Router` 再接 IR Loader，注意 **`Chloe Input` 默认也是 `snakeWrapped: true`**！若要用 `chlora_graph_connect_channel` 按离散通道连接 `2ch Router`，必须先调用 `chlora_graph_set_snake(nodeKey=<chloeKey>, wrapped=false)` 解包（或改用 Snake 连线），否则 `connect_channel` 会报 `"Graph channel transaction was rejected"`。
    - 仅当新建空 IR 节点的上游接入了**挂载在 `Router` 输出侧的 `PortSnake`** 时，才会触发 `irBankLogicalInputs` 格式校验（`2ch Router` → `2` / Stereo Bank；**`16ch Router`** → `15` / 9.1.6 Bank）。
    - 加载 `2 → 16` Stereo Bank 前，不可在 IR 输入通道 `>= 2` 留有直连线，否则会报 `"Disconnect cables on removed IR channels before loading this group"`。
    - 若同目录或库内存在 `bank-catalog.json`，会强校验其中的文件 SHA-256。
  - **`setInternalRoute` / `resetInternalRoutes`**（传 `internalRouting.topologyRevision`）：`side` 取 `"input" | "output" | "matrix"`，其中 `setInternalRoute` 指定 `input` (`0..15`)、`output` (`0..15`) 与布尔 `on`。**注意**：`resetInternalRoutes(side="matrix")` 会将矩阵内部路由重置为 **1:1 对角路由**（例如 Stereo `2 → 16` Bank 重置为 `[(0,0), (1,1)]` 共 2 条），而非恢复 Bank 清单初始的全交叉矩阵（30 条；如需恢复完整清单默认态请重新调用 `loadBankFile`）。
  - **`setDistance` / `clearDistancePreview` 仅支持 `9.1.6` Bank**（传 `internalRouting.topologyRevision`）：要求 `internalProfile == 15` / `distanceCurve.supported == true`；对 Stereo Bank 或普通 WAV 调用会报错 `"IR Distance Curve is only supported on 9.1.6 Reverb Banks"`。`distanceSettings` 包含 `enabled`、`depthDb` (`0..48`)、`control1X/Y`、`control2X/Y` (`0..1`)。
  - **IR Loader 电平、Bank 主波形与核参数编辑分工**：
    - **最轻量零重建调节输出电平**：直接通过 `chlora_graph_set_parameter` 写入节点 hosted 参数 **`Gain`**（以及 `Wet` / `Pre-delay`），或调用 `chlora_graph_set_ir_controls`。
    - **`setGains` 仅限独立 WAV 模式**：`setGains` 仅适用于通过 `import_ir` 导入的独立 WAV 模式；对任何 Reverb Bank 调用都会报 `"Grouped IR kernel/mapping edits require reloading its matrix manifest"`。
    - **Reverb Bank `All IRs` 主波形编辑与核重建（`chlora_graph_set_ir_edits` / `chlora_graph_set_ir_kernel`）**：传入 `expectedRevision = node.irLoader.waveformRevision`。`set_ir_edits` 可修改 `edits.master` 的 `gainDb` / `start` / `end` / `fadeIn` / `fadeOut`（**`master.muted` 须保持 `false`**，`channels` 与 `routeSources` 传空数组 `[]` 或保持 `node.irLoader.edits` 原值不变）；`set_ir_kernel` 可修改 `sizePercent`、`decayPercent`、`decaySeconds`。两者均通过 `prepareIrGroup` 在后台异步重建卷积核并返回 **`operationId`**，轮询 `chlora_get_operation` 直至 `status == "succeeded"` 后读取新的 `waveformRevision`！
  - **`audition` / `getWaveform`**（传 `node.irLoader.waveformRevision`）：`auditionCommand` 取 `"begin" | "set" | "end"`，`"set"` 时传 `outputs` (`0..127`)；`getWaveform` 读取当前包络波形数据。
- **标量、核参数与完整编辑**：
  - `chlora_graph_set_ir_controls`：`wet` (`0..1`)、`gainDb` (`-60..12`)、`preDelayMs` (`0..500`)。
  - `chlora_graph_set_ir_kernel`：`decayPercent` (`10..100`)、`sizePercent` (`25..400`)、`decaySeconds` (`>= 0`)（Reverb Bank 与 WAV 均支持，Bank 异步走 `prepareIrGroup` 并返回 `operationId`）。
  - `chlora_graph_set_ir_edits`：设置 `master` / `channels` / `routeSources`（Reverb Bank 改 `All IRs` 主增益/裁剪/淡入淡出时 `master.muted` 保持 `false`、`channels`/`routeSources` 传 `[]` 或原值；`expectedRevision = waveformRevision`，返回异步 `operationId`）。
  - `chlora_graph_retry_ir`：仅在 `Missing IR` 时按原保存路径与哈希重新获取。
- **与普通单/多 WAV 导入的分工**：加载整套 `.irmatrix.json` 矩阵混响包前可用 `chlora_graph_ir_advanced(action="listBanks")` 枚举并调用 `action="loadBankFile"`（需要中止进行中的加载/导入时调用 `action="cancelImport"`）；直接导入 1–128 个原始本地 WAV/RF64 文件并设置 `linked`/`mono`/`diagonal`/`matrix` 与 `channels`/`ambix`/`n3d`/`fuma` 约定使用 `chlora_graph_import_ir`。Preset list/get/load 参见 [presets.md](presets.md)。

### 9.1 整组 IR 编辑（All IRs）

加载Ready的Bank后，打开原有波形编辑器。Bank只显示 **All IRs** 总控行，不暴露逐
传递／逐声道映射、Solo或局部编辑。可统一调整Start、End、Fade In、Fade Out、总编辑
Gain，并使用卡片上的Decay（秒）和Size。手势释放／数值提交后在后台准备整组新内核，
成功才作一次可Undo的替换；准备中使用原已加载内核，失败保留原状态与外部跳线。

- 时间值使用**整组最长原始IR经Size缩放后的完整时间轴**；各IR共同起终点，不各自
  按首达自动对齐。Start剪去前段但保留原样本时间位置；不会把保留部分移到0秒。
- End与Decay会减少实际有效内核长度和卷积分区；缩短到同一分区内部时，内存／CPU
  不一定逐样本线性减少。单改Start且保留End，主要改变前段声音，不承诺同比省CPU。
- Decay是长度上限，不是RT60；Size是播放速度／时间伸缩，200%为半速，不等同裁尾。
  Size或非48k转换保留重采样滤波尾；不能为了节约资源再阈值截断有效样本。
- 波形是全部物理IR的**逐时刻峰值汇总**，用来统一编辑，不是单个输出的真实混合波形。
  原始与处理后的包络均保留，编辑后仍能在完整时间轴查看并恢复被裁去的区间。
- 原WAV、manifest、entry UUID、来源SHA与路由保持原身份；编辑参数作为节点group
  state v3的`bankEdit`保存。没有改写Bank文件，其他使用同一Bank的节点不受影响。
  重新Load Bank加载新入口时从其原始IR开始；想保留编辑请保存工程／节点预设。
- 整体编辑后的节点预设需支持group state v3的新版Host；旧Host不能保证读取。
  `.irmatrix.json`资源格式仍是v1，现有Bank生成／校验工具的输入格式无需改变。

## 10. 验收与排错：交付到哪一层，就证明到哪一层

- **文件层**：运行helper validate，核对profile、30／225完整cell、physical lane数、
  每chunk预算、全部实际WAV形状与SHA、root confinement。保留receipt。
- **原生处理器层**：让当前IR Loader实际prepare/install这个入口；用已知带符号、
  分时脉冲逐输入验证输出与原始FIR直接卷积一致、LFE为零。Python validator不能取代此层。
- **Graph／界面层**：核对实际2／16输入和16输出、Snake端点、Input30／225开关确实
  改变音频、Output映射、Undo/Redo、同格式Bank切换不改外部线。保存并正常退出重启，
  比较完整路由、节点身份／几何、Pin和group；不能仅比较数量。
- **性能／试听层**：48kHz／512 samples为当前验证目标，每callback预算约10.667ms。
  总文件大小、IR条数、离线平均CPU或一次无声播放都不能证明真实声卡实时稳定。
  重Bank测稳态和切换，区分离线DSP、实际Host、声卡回调和DAW wet return的证据。

IR路径开关只控制wet；Wet=0时仍有dry。48k shared FFT按job冻结mask，改变路径后
旧的已调度湿声贡献最多残留98304 samples，即**2.048秒**，不是即时截尾或自然send尾音
承诺。未编辑Bank在其他采样率使用既有重采样输入gate兼容路径，
静态映射相同而切换尾音语义不同。整体编辑后的Bank使用宿主采样率的共享分区；
不能把48k的2.048秒上界直接套用到其他采样率。完整Bank支持第9.1节的整体非破坏编辑；逐通道编辑与IR来源映射继续保持固定。
若要把编辑结果作为新的可分发资源库，需要另行显式导出／生成新Bank，不能把节点state当作manifest。

常见失败先检查对应层，不能把所有无声都归为IR文件问题：

| 症状 | 首先检查 |
|---|---|
| 浏览不到入口 | 扩展名`.irmatrix.json`、Settings库根目录、文件权限；别选catalogue |
| 输入格式不匹配 | Stereo active仅1/2、916 active15槽、节点intent2/15；carrier仍16 |
| incomplete／duplicated cells | active+silent覆盖、folding全部input_slots、source×receiver完整且唯一 |
| lane order错误 | inputs首次source顺序、跨chunk全局output升序、chunk内lane重置 |
| 超预算 | 每chunk128、4Σframes≤120M、最多8chunks；225条30s不满足 |
| missing／hash changed | 所选manifest与WAV实际存在、全文件SHA、catalogue SHA、canonical root |
| float／rate错误 | 必须真实mono48kfloat32，不能仅改JSON／文件头 |
| Ready但无wet | Input kernel全关／被1:1限制、Output路由、Wet值、来源／输出实际连接 |
| Ready但完全听不到 | Source播放、Monitoring Output设备／physical mapping、mute/solo、总线宽度 |
| 换Bank后效果不符 | 自定义kernel mask保留、source位置近似／复用和通道顺序；不是仅看Bank名字 |

## 11. 维护与原生验证入口

无需查源码即可依本文和helper制作Bank。维护本规格时，源码的以下交集为依据：

- `apps/host/juce/AdvancedIrLoaderProcessor.cpp`：`groupReferenceShape`、
  `prepareGroupFile`、`internalProfile`、`internalRoutingState`及state恢复。
- `apps/host/juce/IrRouterMatrix.h`：完整文件、全局顺序、folding、WAV／SHA／root绑定。
- `apps/host/juce/StaticIrMatrixConvolver.h`：共享频谱、数值上限、真实IR gate调度。
- `apps/host/juce/IrRouterMatrixMain.inc`：完整组选择、catalogue SHA和目标／格式guard。
- `tests/host_ir_group_dsp_verify.cpp`：`--actual MANIFEST NEW_REPORT_JSON`可对实际生成的
  Stereo或916入口作原生加载和完整PCM脉冲oracle，不使用声卡／现有工程。
- `tests/host_ir_bank_presets_verify.cpp`：在明确拥有的空目录中原生生成两个空typed
  单节点预设，检查30／225默认路径、重排记录恢复及同格式Bank切换。

需要本地构建时按仓库build-lane规则使用本任务专用目录，例如：

```bash
python3 tools/mc_build_lane.py run --lane ir-bank-DISTINCT_TASK --build-dir build-lane-ir-bank-DISTINCT_TASK -- cmake --build build-lane-ir-bank-DISTINCT_TASK --target mc_host_ir_group_dsp_verify mc_host_ir_bank_presets_verify -j4
/absolute/owned-build/mc_host_ir_group_dsp_verify --actual /absolute/new/Bank.irmatrix.json /absolute/evidence/new-native-oracle.json
/absolute/owned-build/mc_host_ir_bank_presets_verify /absolute/evidence/new-empty-preset-directory
```

已有兼容专用lane可复用；未配置时先按仓库CMake说明配置。不要使用其他任务的build
目录，不为离线Bank生成执行Host部署、重启用户工程或修改声卡。
当native格式／通道顺序／state版本改变时，同步修订本reference、脚本和例子，
重新跑文件校验、冷启动复现和原生PCM验证后，才宣称新版本规格可复现。
