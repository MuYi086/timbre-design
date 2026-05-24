# v_zh_spatial_097

## 音色定位

- 分组：spatial（空间音频）
- 档案：female（女声） / adult（成年） / human（人类/常规人物） / zh-CN
- 声音质感：nearfield_soft（nearfield=近场, soft=柔和）、breathy_clean（breathy=带气声, clean=干净）
- 默认语气：intimate（亲近/贴耳）、soothing（安抚）
- 适配角色：asmr_close_whisper_female（asmr=近耳/助眠, close=近距离, whisper=低语, female=女声）、bedtime_nearfield_guide（bedtime=睡前, nearfield=近场, guide=引导者）、sleep_story_soft_lead（sleep=睡眠, story=故事, soft=柔和, lead=主角/领声）
- 不推荐场景：loud_action（loud=大声, action=动作）、public_announcement（public=公开/公共, announcement=公告）、high_anger（high=高, anger=愤怒）
- 备注：近耳低声与助眠场景优先，保持低齿噪和低疲劳。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
