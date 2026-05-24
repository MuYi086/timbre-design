# v_zh_spatial_100

## 音色定位

- 分组：spatial（空间音频）
- 档案：male（男声） / middle_aged（中年） / human（人类/常规人物） / zh-CN
- 声音质感：steady（稳定）、low_mid（low=低, mid=中频）、road_clear（road=道路, clear=清晰）
- 默认语气：calm（平静）、reliable（可靠）
- 适配角色：vehicle_driver_voice（vehicle=车载/车辆, driver=司机, voice=声音/音色）、road_dispatcher（road=道路, dispatcher=调度员）、car_cabin_side_character（car=车载, cabin=座舱, side=侧方, character=角色）
- 不推荐场景：soft_romance（soft=柔和, romance=恋爱）、child_role（child=儿童, role=角色）
- 备注：车内司机、调度、路况播报型男声，抗噪环境下保持可懂度。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
