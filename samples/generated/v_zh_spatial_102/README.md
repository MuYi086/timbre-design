# v_zh_spatial_102

## 音色定位

- 分组：spatial（空间音频）
- 档案：male（男声） / adult（成年） / human（人类/常规人物） / zh-CN
- 声音质感：projected（投射感）、stage_bright（stage=舞台, bright=明亮）
- 默认语气：immersive（沉浸式）、serious（严肃）
- 适配角色：immersive_theater_announcer（immersive=沉浸式, theater=剧场, announcer=宣告者）、stage_narrator（stage=舞台, narrator=旁白）、ceremony_lead（ceremony=仪式, lead=主角/领声）
- 不推荐场景：near_ear_asmr（near=近, ear=耳边, asmr=近耳/助眠）、casual_smalltalk（casual=日常随意, smalltalk=闲聊）
- 备注：沉浸式剧场、开场宣告、仪式感旁白，适合前方舞台定位。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
