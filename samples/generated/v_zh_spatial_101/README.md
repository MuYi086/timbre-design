# v_zh_spatial_101

## 音色定位

- 分组：spatial（空间音频）
- 档案：neutral（中性） / ageless（无年龄感） / robot（机器人） / zh-CN
- 声音质感：ultra_clear（ultra=极致, clear=清晰）、spatial_anchor（spatial=空间音频, anchor=主播/播报员）
- 默认语气：focused（专注）、helpful（助人）
- 适配角色：vr_ar_guide（vr=虚拟现实, ar=增强现实, guide=引导者）、headset_system_voice（headset=头显, system=系统, voice=声音/音色）、spatial_interaction_tutorial（spatial=空间音频, interaction=交互, tutorial=教程）
- 不推荐场景：warm_bedtime（warm=温暖, bedtime=睡前）、ancient_style（ancient=古老, style=风格）
- 备注：VR/AR 头显里的空间引导与交互教程，需稳定、短句、方向感明确。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
