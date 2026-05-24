# v_zh_spec_069

## 音色定位

- 分组：special（特殊音色）
- 档案：neutral（中性） / ageless（无年龄感） / robot（机器人） / zh-CN
- 声音质感：metallic_clean（metallic=金属感, clean=干净）
- 默认语气：helpful（助人）
- 适配角色：service_robot（service=服务, robot=机器人）、system_assistant（system=系统, assistant=助手）
- 不推荐场景：strong_human_emotion（strong=强烈, human=人类/常规人物, emotion=情绪）
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
