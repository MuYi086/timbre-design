# v_zh_spatial_099

## 音色定位

- 分组：spatial（空间音频）
- 档案：female（女声） / adult（成年） / human（人类/常规人物） / zh-CN
- 声音质感：clear（清晰）、low_fatigue（low=低, fatigue=疲劳）
- 默认语气：guiding（引导）、friendly（亲和）
- 适配角色：vehicle_cabin_host_female（vehicle=车载/车辆, cabin=座舱, host=主持, female=女声）、navigation_voice（navigation=导航, voice=声音/音色）、car_audiobook_guide（car=车载, audiobook=有声书, guide=引导者）
- 不推荐场景：horror_whisper（horror=恐怖, whisper=低语）、high_drama（high=高, drama=戏剧性）
- 备注：车载座舱前方定位，句子短、指令清晰，适合导航/车载有声剧提示。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
