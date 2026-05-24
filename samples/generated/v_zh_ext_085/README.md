# v_zh_ext_085

## 音色定位

- 分组：extension（扩展音色）
- 档案：male（男声） / adult（成年） / human（人类/常规人物） / zh-CN
- 声音质感：mid_forward（mid=中频, forward=前向）
- 默认语气：precise（精准）
- 适配角色：investigator（调查者）、strategist（谋略者）
- 不推荐场景：rough_street_role（rough=粗粝, street=市井/街头, role=角色）
- 备注：齿音清晰，信息密度高时可懂度好。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
