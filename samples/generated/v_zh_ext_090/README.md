# v_zh_ext_090

## 音色定位

- 分组：extension（扩展音色）
- 档案：female（女声） / young_adult（青年） / human（人类/常规人物） / zh-CN
- 声音质感：clear（清晰）、gentle（温和）
- 默认语气：kind（亲切）
- 适配角色：kids_narrator_female（kids=儿童, narrator=旁白, female=女声）、bedtime_story（bedtime=睡前, story=故事）
- 不推荐场景：oppressive_villain（oppressive=压迫感, villain=反派）
- 备注：儿童向高可懂旁白女。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
