# v_zh_spec_078

## 音色定位

- 分组：special（特殊音色）
- 档案：neutral（中性） / ageless（无年龄感） / human_fx（带媒介效果的人声） / zh-CN
- 声音质感：radio_vintage（radio=无线电/广播, vintage=复古）
- 默认语气：broadcast_old（broadcast=播报, old=老年/旧式）
- 适配角色：radio_scene（radio=无线电/广播, scene=场景）
- 不推荐场景：modern_clean_anchor（modern=现代, clean=干净, anchor=主播/播报员）
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
