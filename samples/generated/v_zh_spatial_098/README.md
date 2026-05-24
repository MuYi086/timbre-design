# v_zh_spatial_098

## 音色定位

- 分组：spatial（空间音频）
- 档案：male（男声） / adult（成年） / human（人类/常规人物） / zh-CN
- 声音质感：nearfield_low（nearfield=近场, low=低）、velvet（丝绒感）
- 默认语气：intimate（亲近/贴耳）、calm（平静）
- 适配角色：asmr_close_whisper_male（asmr=近耳/助眠, close=近距离, whisper=低语, male=男声）、bedtime_story_male（bedtime=睡前, story=故事, male=男声）、nearfield_inner_monologue（nearfield=近场, inner=内心, monologue=独白）
- 不推荐场景：battle_command（battle=战场/动作, command=命令）、comic_fast（comic=喜剧, fast=快速）、children_main（children=儿童, main=主要）
- 备注：低频近讲男声，适合睡前、私语、内心独白。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
