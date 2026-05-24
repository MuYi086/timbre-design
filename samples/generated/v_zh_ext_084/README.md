# v_zh_ext_084

## 音色定位

- 分组：extension（扩展音色）
- 档案：neutral（中性） / ageless（无年龄感） / human（人类/常规人物） / zh-CN
- 声音质感：neutral_clean（neutral=中性, clean=干净）
- 默认语气：objective（客观）
- 适配角色：edict_reader（edict=诏令, reader=诵读者）、ritual_announcer（ritual=仪式, announcer=宣告者）
- 不推荐场景：romantic_monologue（romantic=浪漫, monologue=独白）
- 备注：古风中性诵读官。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
