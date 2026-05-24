# v_zh_spec_070

## 音色定位

- 分组：special（特殊音色）
- 档案：male_coded（男性化拟声） / ageless（无年龄感） / robot（机器人） / zh-CN
- 声音质感：metallic_hard（metallic=金属感, hard=硬朗）
- 默认语气：guarded（戒备）
- 适配角色：security_robot（security=安防, robot=机器人）
- 不推荐场景：warm_bedtime_narration（warm=温暖, bedtime=睡前, narration=叙述）
- 备注：无

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
