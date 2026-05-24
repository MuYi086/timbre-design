# v_zh_spatial_106

## 音色定位

- 分组：spatial（空间音频）
- 档案：neutral（中性） / ageless（无年龄感） / human_fx（带媒介效果的人声） / zh-CN
- 声音质感：game_master（game=游戏, master=主持/主控）、clean_dynamic（clean=干净, dynamic=动态）
- 默认语气：guiding（引导）、alert（警觉）
- 适配角色：interactive_game_master（interactive=互动, game=游戏, master=主持/主控）、mission_prompt_voice（mission=任务, prompt=提示, voice=声音/音色）、branching_story_host（branching=分支, story=故事, host=主持）
- 不推荐场景：serious_documentary（serious=严肃, documentary=纪实）、sleep_story（sleep=睡眠, story=故事）
- 备注：游戏化互动音频、任务提示、分支选择主持，可放在稳定中心声像。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
