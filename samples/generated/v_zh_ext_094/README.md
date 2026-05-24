# v_zh_ext_094

## 音色定位

- 分组：extension（扩展音色）
- 档案：male_coded（男性化拟声） / ageless（无年龄感） / robot（机器人） / zh-CN
- 声音质感：hard_precise（hard=硬朗, precise=精准）
- 默认语气：tactical（战术）
- 适配角色：tactical_ai（tactical=战术, ai=人工智能）、security_core（security=安防, core=核心/中控）
- 不推荐场景：lyrical_paragraph（lyrical=抒情, paragraph=段落）
- 备注：战术/指挥AI。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
