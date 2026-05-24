# v_zh_spatial_103

## 音色定位

- 分组：spatial（空间音频）
- 档案：female（女声） / adult（成年） / human（人类/常规人物） / zh-CN
- 声音质感：ensemble_clear（ensemble=群像合奏, clear=清晰）、responsive（响应感）
- 默认语气：alert（警觉）、lively（活泼）
- 适配角色：immersive_theater_side_actor（immersive=沉浸式, theater=剧场, side=侧方, actor=演员/角色）、crowd_lead_female（crowd=群演/人群, lead=主角/领声, female=女声）、interactive_scene_partner（interactive=互动, scene=场景, partner=搭档）
- 不推荐场景：solemn_history（solemn=庄严, history=历史）、long_main_narration（long=长篇, main=主要, narration=叙述）
- 备注：沉浸剧场侧方角色、群演领声和互动搭话，适合短句穿插。

## 文件约定

- `voice.json`：从音色库导出的锁定元数据。
- `sample.txt`：试听合成文本。
- `sample.voice.txt`：VoxCPM2 音色控制提示。
- `sample.controls.json`：结构化控制参数。
- `sample.wav`：VoxCPM2 生成的无损试听音频。
- `sample.mp3`：由 WAV 转出的便携试听音频。

## VoxCPM2 控制提示

`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。
