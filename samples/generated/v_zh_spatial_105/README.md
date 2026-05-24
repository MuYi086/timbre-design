# v_zh_spatial_105

## 音色定位

- 分组：spatial（空间音频）
- 档案：female（女声） / young_adult（青年） / human（人类/常规人物） / zh-CN
- 声音质感：breath_active（breath=呼吸感, active=活跃）、bright_clear（bright=明亮, clear=清晰）
- 默认语气：brisk（轻快）、curious（好奇）
- 适配角色：field_explorer（field=野外/现场, explorer=探索者）、adventure_companion（adventure=冒险/探险, companion=伙伴）、moving_scene_lead（moving=移动, scene=场景, lead=主角/领声）
- 不推荐场景：static_bedtime（static=静态, bedtime=睡前）、strict_authority（strict=严厉, authority=权威）
- 备注：探险、逃离、户外移动场景，适合有呼吸感但不嘈杂的运动对白。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
