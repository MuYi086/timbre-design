"""VoxCPM2 command runner for sample synthesis."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
from pathlib import Path

from timbre_design.controls import VoiceControls, default_controls_for_voice, render_voxcpm2_prompt
from timbre_design.models import Voice


def synthesize_with_voxcpm2(
    *,
    command: str | None,
    text: str,
    voice: Voice,
    output_wav: Path,
    controls: VoiceControls | None = None,
    timeout_seconds: float | None = None,
) -> Path:
    command = command or os.environ.get("TIMBRE_VOXCPM2_COMMAND")
    if not command:
        raise RuntimeError(
            "未配置 VoxCPM2 调用命令。请设置 TIMBRE_VOXCPM2_COMMAND，"
            "命令模板可使用 {text_file}、{voice_description_file}、"
            "{voice_controls_file}、{voice_controls_json}、{voice_id}、{output_wav}。"
        )
    output_wav.parent.mkdir(parents=True, exist_ok=True)
    text_file = output_wav.with_suffix(".txt")
    description_file = output_wav.with_suffix(".voice.txt")
    controls_file = output_wav.with_suffix(".controls.json")
    resolved_controls = controls or default_controls_for_voice(voice)
    prompt = render_voxcpm2_prompt(voice, resolved_controls)
    controls_payload = resolved_controls.to_dict()
    controls_json = json.dumps(controls_payload, ensure_ascii=False, sort_keys=True)
    text_file.write_text(text, encoding="utf-8")
    description_file.write_text(prompt, encoding="utf-8")
    controls_file.write_text(controls_json + "\n", encoding="utf-8")

    values = {
        "text": text,
        "text_file": str(text_file),
        "voice_id": voice.voice_id,
        "voice_description": prompt,
        "voice_description_file": str(description_file),
        "voice_controls_file": str(controls_file),
        "voice_controls_json": controls_json,
        "output_wav": str(output_wav),
    }
    args = [part.format(**values) for part in shlex.split(command, posix=os.name != "nt")]
    timeout = timeout_seconds or float(os.environ.get("TIMBRE_TTS_TIMEOUT_SECONDS", "900"))
    try:
        subprocess.run(
            args,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"VoxCPM2 命令不存在：{args[0]}。") from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(f"VoxCPM2 合成超时：超过 {timeout:.0f} 秒。") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else "无 stderr"
        raise RuntimeError(f"VoxCPM2 合成失败：{stderr}") from exc
    if not output_wav.is_file():
        raise RuntimeError(f"VoxCPM2 未生成目标 WAV：{output_wav}。")
    return output_wav
