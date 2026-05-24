# voices_v2_106.json（106 音色库 JSON 文件）字段说明

本文档说明 `voices_v2_106.json`（106 音色库 JSON 文件）的字段含义、当前状态和维护约定。修改音色库时应同步更新本文档，避免字段语义漂移。

阅读约定：JSON 字段名、代码枚举值和程序术语保留英文原文，后面用括号补中文说明。例如 `voice_id`（音色唯一编号）、`narrator`（旁白分组）、`string`（字符串）。

## 根节点

| 字段 | 类型 | 状态 | 含义 | 当前使用 |
| --- | --- | --- | --- | --- |
| `version`（版本） | `string`（字符串） | 必填 | 音色库版本。当前为 `2.0.0`。 | 用于摘要输出和人工审计。 |
| `locale`（语言区域） | `string`（字符串） | 必填 | 音色库默认语言区域。当前为 `zh-CN`（中国大陆普通话）。 | `VoiceProfile.from_mapping()`（从 JSON 映射生成音色档案）在单条音色未声明 `locale`（语言区域）时继承该值。 |
| `total_voices`（音色总数） | `number`（数字） | 必填 | 声明的音色总数。当前为 `106`。 | `VoiceLibrary.validate()`（音色库校验方法）会校验它和 `voices.length`（音色数组长度）是否一致。 |
| `naming_rule`（命名规则） | `string`（字符串） | 必填 | `voice_id`（音色唯一编号）的命名规则说明。当前为 `v_zh_{group}_{nnn}`（中文音色 + 分组 + 三位序号）。 | 文档和人工维护使用，校验器当前只强制 `v_zh_`（中文音色前缀）前缀。 |
| `voices`（音色条目列表） | `array`（数组） | 必填 | 音色条目数组。 | 加载、校验、搜索、匹配、提示词渲染、导出 `casting`（角色配音映射）都依赖它。 |

## voice（单个音色条目）

每个 `voices[]`（音色数组中的单项）代表一个可锁定复用的音色资产。

| 字段 | 类型 | 状态 | 含义 | 当前使用 |
| --- | --- | --- | --- | --- |
| `voice_id`（音色唯一编号） | `string`（字符串） | 必填、不可变 | 音色唯一主键。示例：`v_zh_narr_001`（中文旁白第 001 号）。一旦被书籍映射使用，不应改名。 | 作为库内查找、`voice-casting.json`（配音映射文件）的 `voice_slot`（音色槽位）、资产目录名和 `provider voice id`（供应商音色编号）。 |
| `group`（业务分组） | `string`（字符串） | 必填 | 音色业务分组。见“group（业务分组）取值”。 | 匹配候选过滤、默认控制参数、空间音色特殊处理。 |
| `profile`（基础档案） | `object`（对象） | 必填 | 基础身份属性，描述性别、年龄段、物种/类型和语言。 | 匹配器用于性别、年龄、物种打分；提示词渲染会写入基础定位。 |
| `style_tags`（风格标签） | `object`（对象） | 必填 | 声音风格标签，描述音质、语速、能量、默认情绪和空间场景。 | 搜索、匹配、默认控制参数、空间场景识别。 |
| `fit_roles`（适配角色） | `array[string]`（字符串数组） | 必填、至少 1 项 | 适配的叙事角色或场景角色。 | 匹配器做角色打分；搜索文本会纳入；提示词渲染会展示。 |
| `constraints`（使用约束） | `object`（对象） | 必填，可为空对象 | 禁忌、风险和维护备注。 | 匹配器根据 `not_good_for`（不适合场景）做惩罚和复核；提示词和资产 `README`（说明文件）会展示。 |

## profile（基础档案）

| 字段 | 类型 | 状态 | 含义 |
| --- | --- | --- | --- |
| `gender`（声线性别） | `string`（字符串） | 必填 | 声线性别/拟性别。当前使用：`male`（男声）、`female`（女声）、`neutral`（中性声）、`male_coded`（男性化拟声）、`female_coded`（女性化拟声）。 |
| `age_band`（年龄段） | `string`（字符串） | 必填 | 年龄段。当前使用：`teen`（少年/少女）、`young_adult`（青年）、`adult`（成年）、`middle_aged`（中年）、`senior`（老年）、`ageless`（无年龄感）。 |
| `species`（角色/声源类型） | `string`（字符串） | 必填 | 角色类型或声源类型。当前使用：`human`（人类）、`robot`（机器人/AI）、`spirit`（灵体/超自然）、`creature`（生物/怪物/拟人动物）、`human_fx`（带媒介效果的人声）、`nonhuman`（非人智慧体）。 |
| `locale`（语言区域） | `string`（字符串） | 可选 | 单条音色语言区域。缺省时继承根节点 `locale`（语言区域）。 |

### profile（基础档案）取值说明

| 字段 | 取值 | 含义 |
| --- | --- | --- |
| `gender`（声线性别） | `male`（男声） / `female`（女声） | 明确男声 / 女声。 |
| `gender`（声线性别） | `neutral`（中性声） | 中性声线，不强调性别。 |
| `gender`（声线性别） | `male_coded`（男性化拟声） / `female_coded`（女性化拟声） | 非人或特殊音色的男性化 / 女性化声线。 |
| `age_band`（年龄段） | `teen`（少年/少女） | 少年/少女角色。 |
| `age_band`（年龄段） | `young_adult`（青年） | 青年角色。 |
| `age_band`（年龄段） | `adult`（成年） | 成年角色。 |
| `age_band`（年龄段） | `middle_aged`（中年） | 中年角色。 |
| `age_band`（年龄段） | `senior`（老年） | 老年角色。 |
| `age_band`（年龄段） | `ageless`（无年龄感） | 无年龄感，常用于机器人、系统声、幽灵、神谕等。 |
| `species`（角色/声源类型） | `human`（人类） | 普通人物或可作为人物对白使用的自然声线。 |
| `species`（角色/声源类型） | `robot`（机器人/AI） | 机器人、AI（人工智能）、中控、系统助手等。 |
| `species`（角色/声源类型） | `spirit`（灵体/超自然） | 幽灵、神谕、精灵、古神等超自然声线。 |
| `species`（角色/声源类型） | `creature`（生物/怪物/拟人动物） | 怪物、拟人动物、非人实体。 |
| `species`（角色/声源类型） | `human_fx`（带媒介效果的人声） | 带媒介质感的人声源，如电话、无线电、广播、游戏提示。 |
| `species`（角色/声源类型） | `nonhuman`（非人智慧体） | 高维、宇宙视角、难以归类的非人智慧体。 |

## style_tags（风格标签）

| 字段 | 类型 | 状态 | 含义 | 当前使用 |
| --- | --- | --- | --- | --- |
| `timbre`（音色质感） | `array[string]`（字符串数组）或 `string`（字符串） | 必填、至少 1 项 | 音色质感标签，如 `warm`（温暖）、`dark`（阴暗）、`metallic_clean`（干净金属感）、`nearfield_soft`（近场柔和）。 | `Voice.timbre_tags`（音色质感标签属性）、搜索、匹配、提示词、校验。 |
| `pace_default`（默认语速档位） | `string`（字符串） | 推荐必填 | 默认语速档位。 | `default_controls_for_voice()`（根据音色生成默认控制参数）映射到 `speed`（语速）。缺省按 `medium`（中速）处理。 |
| `energy`（默认能量/力度） | `string`（字符串） | 推荐必填 | 默认能量/力度。 | 当前主要用于搜索和描述，后续可用于动态控制。 |
| `emotion_bias`（默认情绪倾向） | `array[string]`（字符串数组）或 `string`（字符串） | 推荐必填 | 默认情绪倾向，如 `calm`（平静）、`friendly`（亲和）、`tactical`（战术紧张）。 | `default_controls_for_voice()`（根据音色生成默认控制参数）映射到统一 `emotion`（情绪）；提示词展示。 |
| `scene_tags`（空间场景标签） | `array[string]`（字符串数组）或 `string`（字符串） | `spatial`（空间音频分组）条件必填，其他分组可选 | 高价值空间音频场景标签。 | `spatial.py`（空间音频规则模块）用于识别空间场景和默认摆位。 |

### pace_default（默认语速档位）当前取值

`controls.py`（控制参数模块）当前明确映射以下值：

| 取值 | `speed`（语速） |
| --- | --- |
| `slow`（慢速） | `0.88` |
| `medium_slow`（中慢速） | `0.94` |
| `slow_medium`（慢中速） | `0.94` |
| `medium`（中速） | `1.00` |
| `fast_medium`（快中速） | `1.04` |
| `medium_fast`（中快速） | `1.04` |
| `fast`（快速） | `1.08` |

未列出的值会按 `medium`（中速）处理。

### energy（默认能量/力度）当前状态

`energy`（默认能量/力度）是描述性标签，目前没有强枚举。JSON（结构化数据文件）中常见取值包括：

- `low`（低能量）
- `low_medium`（低到中等能量）
- `medium_low`（中等偏低能量）
- `medium`（中等能量）
- `medium_high`（中等偏高能量）
- `high`（高能量）

维护时建议优先复用以上取值，避免同义词过多导致搜索和后续控制规则变复杂。

### emotion_bias（默认情绪倾向）当前状态

`emotion_bias`（默认情绪倾向）是描述性标签，`controls.py`（控制参数模块）会把部分标签映射到 `provider-neutral emotion`（供应商无关的统一情绪标签）：

| 标签示例 | 映射结果 |
| --- | --- |
| `calm`（平静）、`soothing`（安抚）、`guiding`（引导） | `calm`（平静） |
| `kind`（亲切）、`gentle`（温和）、`warm`（温暖） | `warm`（温暖） |
| `bright`（明亮）、`energetic`（有活力）、`brisk`（轻快） | `bright`（明亮） |
| `lively`（活泼）、`cheerful`（愉悦）、`playful`（俏皮） | `happy`（愉悦） |
| `serious`（严肃）、`authoritative`（权威）、`strict`（严厉）、`cold`（冷感）、`focused`（专注） | `serious`（严肃） |
| `mysterious`（神秘）、`suspense`（悬疑）、`eerie`（诡异）、`threatening`（威胁感）、`tactical`（战术紧张） | `tense`（紧张） |
| `intimate`（亲近/贴耳） | `whispering`（低声耳语） |
| `weak`（虚弱）、`fragile`（脆弱） | `sad`（悲伤） |

未映射的标签仍会进入搜索文本和提示词，但默认 `emotion`（情绪）会回退到分组/物种逻辑。

## constraints（使用约束）

| 字段 | 类型 | 状态 | 含义 | 当前使用 |
| --- | --- | --- | --- | --- |
| `not_good_for`（不适合场景） | `array[string]`（字符串数组） | 推荐必填，可为空 | 不推荐使用的场景、情绪、角色或参数风险。 | 匹配器会根据角色上下文命中禁忌，降低分数并输出复核标记；提示词和资产 `README`（说明文件）会展示。 |
| `notes`（备注） | `string`（字符串） | 推荐必填，可为空 | 人类可读备注，说明风险、最佳用途或维护原因。 | 搜索文本、提示词和资产 `README`（说明文件）会展示。 |

### not_good_for（不适合场景）维护规则

- 使用稳定的英文 `snake_case key`（小写下划线键名），例如 `high_anger`（高怒情绪）、`speed_over_1.2x`（语速超过 1.2 倍）、`long_main_narration`（长篇主旁白）。
- 不要直接写长中文句子作为 `key`（键名）；中文说明放到 `notes`（备注）。
- 若新增 `key`（键名）希望被中文角色提示自动命中，应同步更新 `matcher.py`（匹配器模块）的 `CONSTRAINT_KEYWORDS`（约束关键词表）。
- `not_good_for`（不适合场景）是约束，不是绝对禁用。命中后会降分并进入复核，最终仍可人工确认使用。

## group（业务分组）取值

| `group`（业务分组） | 当前数量 | 含义 | 使用建议 |
| --- | ---: | --- | --- |
| `narrator`（旁白） | 10 | 旁白和章节叙述。 | 优先给全书旁白、章节标题、纪实叙述。 |
| `human`（常规人物） | 48 | 常规人物池。 | 高频人物和低频人物分组的主力。 |
| `functional`（功能角色） | 10 | 功能角色，如播报、客服、路人、喜剧、阴沉耳语。 | 适合短句、群像、功能性对白。 |
| `special`（特殊音色） | 12 | 机器人、非人、超自然、媒介质感声线。 | 适合科幻、童话、神怪、电话/广播等片段。 |
| `extension`（扩展音色） | 16 | 80 音色基础库后的扩展池。 | 补古风、防撞声、儿童友好、机器人/非人细分。 |
| `spatial`（空间音频） | 10 | 空间音频高价值场景专用声源。 | 只在 ASMR（近耳/助眠）、车载、VR/AR（虚拟现实/增强现实）、剧场、战场、探险、互动游戏等场景使用。 |

## spatial（空间音频）专用字段

`group == "spatial"`（业务分组为空间音频）的音色必须在 `style_tags.scene_tags`（风格标签里的空间场景标签）中覆盖至少一个高价值空间场景。校验器会检查 `spatial`（空间音频）分组整体是否覆盖全部高价值场景。

| 空间场景 | 识别入口 | 默认后处理意图 |
| --- | --- | --- |
| `asmr`（近耳/助眠） | `asmr`（近耳放松音频）、`bedtime`（睡前）、`near_ear`（近耳）、`binaural_close`（近距离双耳）、`inner_monologue`（内心独白） | 近耳/助眠/私语，TTS（文本转语音）仍输出干声，后处理做双耳空间化。 |
| `vehicle`（车载座舱） | `vehicle_cabin`（车载座舱）、`navigation`（导航）、`route_prompt`（路线提示）、`driver`（司机）、`dispatch`（调度） | 车载座舱前方或侧方定位。 |
| `vr_ar`（虚拟现实/增强现实） | `vr`（虚拟现实）、`ar`（增强现实）、`headset`（头显）、`interactive_guide`（交互引导）、`spatial_anchor`（空间锚点） | 头显系统声、空间引导、方向提示。 |
| `theater`（沉浸式剧场） | `immersive_theater`（沉浸式剧场）、`stage`（舞台）、`front_stage`（前方舞台）、`side_stage`（侧方舞台）、`crowd`（群演/人群） | 舞台前方、侧方角色、群演领声。 |
| `battle`（战场/动作） | `battlefield`（战场）、`radio`（无线电）、`war`（战争）、`offscreen`（画外/场外）、`distance`（远距离） | 战场无线电、远端通讯、侧后方命令。 |
| `adventure`（探险/移动） | `adventure`（冒险）、`exploration`（探索）、`outdoor`（户外）、`moving_source`（移动声源） | 户外探险、移动伙伴、逃亡追踪。 |
| `game`（游戏化互动） | `interactive_audio`（互动音频）、`game`（游戏）、`mission`（任务）、`choice_prompt`（选择提示） | 任务提示、分支选择、互动主持。 |

重要约定：空间音色的 TTS（文本转语音）提示词会要求生成干净人声干声，不把声像、距离、移动、混响、无线电或车厢空间感烘焙进 TTS（文本转语音）；这些由下游后处理完成。

## 字段状态总览

| 状态 | 字段 |
| --- | --- |
| 强校验必填 | 根节点 `total_voices`（音色总数）、`voices`（音色条目列表）；音色条目 `voice_id`（音色唯一编号）、`group`（业务分组）、`profile`（基础档案）、`style_tags`（风格标签）、`fit_roles`（适配角色）、`constraints`（使用约束）；`style_tags.timbre`（音色质感）。 |
| 推荐必填 | `style_tags.pace_default`（默认语速档位）、`style_tags.energy`（默认能量/力度）、`style_tags.emotion_bias`（默认情绪倾向）、`constraints.not_good_for`（不适合场景）、`constraints.notes`（备注）。 |
| 条件必填 | `style_tags.scene_tags`（空间场景标签）对 `group == "spatial"`（业务分组为空间音频）必填。 |
| 可选 | `profile.locale`（单条音色语言区域）。 |
| 当前未使用但可后续扩展 | `quality`（质量评分）、`engine_binding`（引擎绑定信息）、`samples`（样例音频）、`status`（生命周期状态）、`version`（单条音色版本）等生产字段尚未进入当前 JSON（结构化数据文件）。若新增，需要同步模型、校验器和本文档。 |

## 维护检查清单

1. 新增或删除音色后，同步更新根节点 `total_voices`（音色总数）。
2. 新增 `voice_id`（音色唯一编号）必须唯一，且以 `v_zh_`（中文音色前缀）开头。
3. 每条音色至少要有 `fit_roles`（适配角色）和 `style_tags.timbre`（音色质感）。
4. `spatial`（空间音频）音色必须带 `scene_tags`（空间场景标签），且整体仍覆盖 `asmr`（近耳/助眠）、`vehicle`（车载座舱）、`vr_ar`（虚拟现实/增强现实）、`theater`（沉浸式剧场）、`battle`（战场/动作）、`adventure`（探险/移动）、`game`（游戏化互动）。
5. 新增禁忌 `key`（键名）后，若希望自动命中中文角色提示，同步更新 `matcher.py`（匹配器模块）的 `CONSTRAINT_KEYWORDS`（约束关键词表）。
6. 修改字段结构后，运行：

```bash
PYTHONPATH=src python -m timbre_design validate --json
python -m pytest
```
