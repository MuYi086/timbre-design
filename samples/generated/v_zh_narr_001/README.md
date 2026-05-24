# v_zh_narr_001

## 音色定位

- 分组：narrator（旁白）
- 档案：male（男声） / adult（成年） / human（人类/常规人物） / zh-CN
- 声音质感：warm（温暖）
- 默认语气：calm（平静）
- 适配角色：narrator_general（narrator=旁白, general=通用）、chapter_intro（chapter=章节, intro=导入/开场）
- 不推荐场景：high_anger（high=高, anger=愤怒）、speed_over_1.2x（speed=语速, over=超过, 1.2x=1.2 倍速）
- 备注：高怒情绪与超快语速易失真。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
