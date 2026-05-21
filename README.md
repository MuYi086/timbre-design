# timbre-design

基于 VoxCPM2 的中文公版书音色设计库。这个仓库负责维护可复用音色资产、角色到音色的匹配规则，以及导出 `audio-3d-sdd` 可消费的 `voice-casting.json`。

## 当前能力

- 内置 `voices_v2_96.json`：96 个中文音色，覆盖旁白、常规人物、功能角色、机器人/非人等特殊音色。
- 校验音色库结构、数量、重复 `voice_id` 和基础字段。
- 根据角色的性别、年龄、物种/类型、性格和音色提示匹配音色。
- 渲染 VoxCPM2 控制提示，输出稳定的 `voice_description`。
- 从 `characters.json` 导出兼容 `audio-3d-sdd/config/voice-casting.json` 的映射文件。
- 可通过本地命令模板调用 VoxCPM2 生成样例音频。

## 快速使用

开发态未安装包时，先把 `src` 加到 `PYTHONPATH`：

```powershell
$env:PYTHONPATH = (Resolve-Path .\src)
python -m timbre_design validate
python -m timbre_design list --group narrator
python -m timbre_design match --name 林黛玉 --gender female --age young --hint "清冷、敏感、诗性"
python -m timbre_design prompt v_zh_narr_001
```

生成 `audio-3d-sdd` 可用的音色映射：

```powershell
python -m timbre_design cast `
  --characters D:\github\audio-3d-sdd\jobs\book\work\characters.json `
  --output D:\github\audio-3d-sdd\jobs\book\config\voice-casting.json
```

生成结果中的 `voice_slot` 直接使用 `voice_id`，并在 `voice_descriptions` 中写入 VoxCPM2 控制提示；`audio-3d-sdd` 的 TTS provider 会按该描述合成。

## VoxCPM2 样例合成

设置命令模板后可生成单个音色样例：

```powershell
$env:TIMBRE_VOXCPM2_COMMAND = "voxcpm design --text-file {text_file} --control-file {voice_description_file} --output {output_wav}"
python -m timbre_design synthesize --voice-id v_zh_narr_001 --text-file .\sample.txt --output-wav .\samples\generated\v_zh_narr_001.wav
```

模板可用变量：

- `{text}` / `{text_file}`
- `{voice_id}`
- `{voice_description}` / `{voice_description_file}`
- `{voice_controls_json}` / `{voice_controls_file}`
- `{output_wav}`

## 开发验证

```powershell
python -m pytest
```
