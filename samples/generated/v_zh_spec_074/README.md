# v_zh_spec_074

## 音色定位

- 分组：special（特殊音色）
- 档案：male_coded（男性化拟声） / ageless（无年龄感） / creature（生物/怪物/拟人动物） / zh-CN
- 声音质感：low_monster（low=低, monster=怪物）
- 默认语气：threatening（威胁感）
- 适配角色：monster_voice（monster=怪物, voice=声音/音色）
- 不推荐场景：high_density_info（high=高, density=密度, info=信息）
- 备注：无

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
