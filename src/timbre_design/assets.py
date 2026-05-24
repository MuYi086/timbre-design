"""Voice asset directory generation."""

from __future__ import annotations

import json
import os
import shlex
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from timbre_design.controls import VoiceControls, default_controls_for_voice, render_voxcpm2_prompt
from timbre_design.models import JsonDict, Voice
from timbre_design.voxcpm import synthesize_with_voxcpm2

DEFAULT_ASSET_ROOT = Path("samples/generated")
DEFAULT_SAMPLE_TEXT = (
    "这是一个用于锁定音色的试听片段。请保持普通话清晰自然，情绪稳定，"
    "并在长文本中保持同一 voice_id 的声音一致。"
)

TERM_LABELS_ZH = {
    "adult": "成年",
    "adventure": "冒险/探险",
    "ageless": "无年龄感",
    "aged": "年龄段",
    "ai": "人工智能",
    "airy": "气声/空灵",
    "alert": "警觉",
    "analytical": "分析型",
    "anger": "愤怒",
    "animal": "动物",
    "asmr": "近耳/助眠",
    "authoritative": "权威",
    "battle": "战场/动作",
    "bedtime": "睡前",
    "bright": "明亮",
    "broadcast": "播报",
    "calm": "平静",
    "cabin": "座舱",
    "caring": "关怀",
    "chapter": "章节",
    "cheerful": "愉悦",
    "child": "儿童",
    "children": "儿童",
    "classic": "古风/经典",
    "clean": "干净",
    "clear": "清晰",
    "cold": "冷感",
    "comic": "喜剧",
    "commander": "指挥官",
    "creature": "生物/怪物/拟人动物",
    "cyber": "赛博/电子",
    "dark": "阴暗",
    "deep": "低沉",
    "detached": "疏离",
    "dialogue": "对白",
    "documentary": "纪实",
    "driver": "司机",
    "dry": "干声/干涩",
    "eerie": "诡异",
    "elder": "长者",
    "energetic": "有活力",
    "extension": "扩展音色",
    "female": "女声",
    "female_coded": "女性化拟声",
    "field": "野外/现场",
    "functional": "功能角色",
    "general": "通用",
    "gentle": "温和",
    "ghost": "幽灵",
    "guiding": "引导",
    "high": "高",
    "human": "人类/常规人物",
    "human_fx": "带媒介效果的人声",
    "id": "编号",
    "intro": "导入/开场",
    "intimate": "亲近/贴耳",
    "kind": "亲切",
    "lead": "主角/领声",
    "low": "低",
    "male": "男声",
    "male_coded": "男性化拟声",
    "medium": "中等",
    "middle_aged": "中年",
    "monster": "怪物",
    "narration": "叙述",
    "narrator": "旁白",
    "nearfield": "近场",
    "neutral": "中性",
    "nonhuman": "非人智慧体",
    "over": "超过",
    "old": "老年/旧式",
    "oracle": "神谕",
    "pov": "视角",
    "playful": "俏皮",
    "prompt": "提示",
    "radio": "无线电/广播",
    "robot": "机器人",
    "role": "角色",
    "senior": "老年",
    "serious": "严肃",
    "service": "服务",
    "soft": "柔和",
    "spatial": "空间音频",
    "speed": "语速",
    "special": "特殊音色",
    "spirit": "灵体/超自然",
    "stage": "舞台",
    "strict": "严厉",
    "teen": "少年/少女",
    "tense": "紧张",
    "theater": "剧场",
    "timbre": "音色质感",
    "voice": "声音/音色",
    "warm": "温暖",
    "x": "倍速",
    "young": "年轻",
    "young_adult": "青年",
    "zh-CN": "中国大陆普通话",
    "1.1x": "1.1 倍速",
    "1.2x": "1.2 倍速",
}

TERM_LABELS_ZH.update(
    {
        "action": "动作",
        "active": "活跃",
        "actor": "演员/角色",
        "agile": "灵活",
        "anchor": "主播/播报员",
        "ancient": "古老",
        "announcement": "公告",
        "announcer": "宣告者",
        "antagonist": "对立角色",
        "antihero": "反英雄",
        "ar": "增强现实",
        "assistant": "助手",
        "audio": "音频",
        "audiobook": "有声书",
        "authority": "权威",
        "band": "频段",
        "battlefield": "战场",
        "binaural": "双耳",
        "biography": "传记",
        "blooded": "冷血",
        "book": "书籍",
        "boss": "上司/老板",
        "boy": "男孩",
        "branching": "分支",
        "brave": "勇敢",
        "breath": "呼吸感",
        "breathy": "带气声",
        "brisk": "轻快",
        "calculating": "算计感",
        "call": "呼叫",
        "car": "车载",
        "care": "照护",
        "careful": "谨慎",
        "casual": "日常随意",
        "center": "中心",
        "ceremony": "仪式",
        "character": "角色",
        "chatty": "爱聊天",
        "childlike": "孩童感",
        "choice": "选择",
        "city": "市井/城市",
        "clan": "宗族",
        "classical": "古典",
        "clever": "聪明机敏",
        "close": "近距离",
        "cn": "中文",
        "comedic": "喜剧化",
        "comedy": "喜剧",
        "command": "命令",
        "commanding": "指挥感",
        "commands": "命令",
        "commoner": "普通人/市井人",
        "companion": "伙伴",
        "composed": "沉着",
        "conflict": "冲突",
        "conservative": "守旧",
        "content": "内容",
        "cool": "清冷",
        "core": "核心/中控",
        "cosmic": "宇宙感",
        "cozy": "舒适温馨",
        "crisp": "清脆利落",
        "crowd": "群演/人群",
        "cruel": "残酷",
        "cryptic": "隐晦神秘",
        "curious": "好奇",
        "customer": "客户",
        "cute": "可爱",
        "cynic": "讥讽者",
        "daily": "日常",
        "dated": "旧式",
        "delivery": "信息传达",
        "dense": "密集",
        "density": "密度",
        "detective": "侦探",
        "device": "设备",
        "dim": "维度",
        "disciplined": "纪律感",
        "dispatch": "调度",
        "dispatcher": "调度员",
        "distance": "远距离",
        "doctor": "医生",
        "drama": "戏剧性",
        "dream": "梦境",
        "dreamy": "梦幻",
        "dynamic": "动态",
        "ear": "耳边",
        "earthy": "朴实接地气",
        "edict": "诏令",
        "efficient": "干练高效",
        "electronic": "电子感",
        "elegant": "温雅",
        "elf": "精灵",
        "emotion": "情绪",
        "energy": "能量",
        "ensemble": "群像合奏",
        "entity": "实体",
        "epic": "史诗感",
        "ethereal": "空灵",
        "event": "活动",
        "everyday": "日常",
        "exaggerated": "夸张",
        "exploration": "探索",
        "explorer": "探索者",
        "extreme": "极端",
        "f": "女性",
        "fairy": "童话",
        "fallen": "落魄",
        "fast": "快速",
        "father": "父亲",
        "fatigue": "疲劳",
        "fight": "打斗",
        "fighter": "战士/斗士",
        "firm": "坚定",
        "focused": "专注",
        "forceful": "强势有力",
        "form": "形式",
        "formal": "正式",
        "forward": "前向",
        "fragile": "脆弱",
        "frail": "虚弱",
        "friend": "朋友",
        "friendly": "亲和",
        "front": "前方",
        "full": "完整/全量",
        "funny": "诙谐",
        "game": "游戏",
        "giant": "巨人",
        "girl": "女孩",
        "glossy": "冷亮光泽感",
        "grandfather": "祖父",
        "grandmother": "祖母",
        "gravel": "沙哑低沉",
        "grief": "悲痛",
        "guarded": "戒备",
        "guardian": "守护者",
        "guide": "引导者",
        "hard": "硬朗",
        "harsh": "严苛刺耳",
        "hazy": "朦胧",
        "headset": "头显",
        "healing": "疗愈",
        "heavy": "沉重",
        "helpful": "助人",
        "henchman": "反派副手",
        "higher": "高维",
        "historical": "历史",
        "history": "历史",
        "horror": "恐怖",
        "host": "主持",
        "house": "宅邸/家族",
        "humorous": "幽默",
        "idealistic": "理想主义",
        "ill": "病弱",
        "immersive": "沉浸式",
        "info": "信息",
        "inner": "内心",
        "intellectual": "知性",
        "interaction": "交互",
        "interactive": "互动",
        "intimidation": "威慑",
        "introvert": "内向",
        "investigator": "调查者",
        "iq": "智商",
        "judge": "法官/审判者",
        "kids": "儿童",
        "knowledge": "知识",
        "lady": "女士/闺阁女性",
        "legacy": "旧式遗留",
        "light": "轻亮",
        "literary": "文艺",
        "lively": "活泼",
        "long": "长篇",
        "loud": "大声",
        "love": "爱情",
        "lyrical": "抒情",
        "magnetic": "磁性",
        "main": "主要",
        "man": "男性",
        "manager": "管理者",
        "master": "主持/主控",
        "matriarch": "女家长",
        "medic": "医疗",
        "mentor": "导师",
        "merchant": "商人",
        "metallic": "金属感",
        "mid": "中频",
        "middle": "中年/中间",
        "military": "军警",
        "mischievous": "顽皮",
        "mission": "任务",
        "modern": "现代",
        "monologue": "独白",
        "mother": "母亲",
        "mourning": "哀悼",
        "moving": "移动",
        "mysterious": "神秘",
        "mystery": "悬疑",
        "mystic": "神秘/玄秘",
        "nasal": "鼻腔共鸣",
        "navigation": "导航",
        "near": "近",
        "neighbor": "邻里",
        "news": "新闻",
        "nimble": "灵动",
        "noble": "贵气",
        "nobleman": "贵族男性",
        "noisy": "嘈杂",
        "nurturing": "养育/母性",
        "objective": "客观",
        "of": "的",
        "office": "办公室/职场",
        "official": "官员",
        "offscreen": "画外/场外",
        "ominous": "不祥",
        "opening": "开场",
        "oppressive": "压迫感",
        "optimistic": "乐观",
        "oral": "口述",
        "outdoor": "户外",
        "overacted": "表演过度",
        "paced": "节奏",
        "paragraph": "段落",
        "partner": "搭档",
        "passage": "段落",
        "passerby": "路人",
        "phone": "电话",
        "pitch": "音高",
        "plain": "朴素",
        "poetic": "诗性",
        "police": "警察",
        "polite": "礼貌",
        "power": "权力",
        "precise": "精准",
        "pressure": "压迫",
        "professional": "职业化",
        "projected": "投射感",
        "prophet": "预言者",
        "public": "公开/公共",
        "quick": "机敏快速",
        "quiet": "安静",
        "rage": "暴怒",
        "rally": "动员",
        "rapid": "快速",
        "rational": "理性",
        "reader": "诵读者",
        "reading": "朗读",
        "reassuring": "安心",
        "recollection": "回忆",
        "reflective": "沉思",
        "reliable": "可靠",
        "reserved": "克制保留",
        "responsive": "响应感",
        "restrained": "克制",
        "retro": "复古",
        "rigid": "顽固僵硬",
        "ritual": "仪式",
        "road": "道路",
        "roadside": "路边",
        "romance": "恋爱",
        "romantic": "浪漫",
        "rough": "粗粝",
        "round": "圆润",
        "rousing": "振奋",
        "route": "路线",
        "ruthless": "狠辣",
        "scene": "场景",
        "scholar": "学者",
        "scholarly": "书卷气",
        "security": "安防",
        "sensitive": "敏感",
        "sequence": "序列/片段",
        "severe": "严厉",
        "shadow": "阴影",
        "shaman": "神婆/巫者",
        "sharp": "锐利",
        "shift": "变调",
        "ship": "飞船",
        "shopkeeper": "店主",
        "shout": "喊叫",
        "shouts": "喊叫",
        "side": "侧方",
        "sidekick": "搭档",
        "slang": "俚语",
        "slapstick": "夸张闹剧",
        "sleep": "睡眠",
        "slightly": "略微",
        "slow": "慢速",
        "smalltalk": "闲聊",
        "solemn": "庄严",
        "soothing": "安抚",
        "source": "声源",
        "speech": "演讲/语音",
        "static": "静态",
        "steady": "稳定",
        "stoic": "冷静克制",
        "story": "故事",
        "strategist": "谋略者",
        "street": "市井/街头",
        "streetwise": "市井机敏",
        "strong": "强烈",
        "stubborn": "固执",
        "student": "学生",
        "style": "风格",
        "sunny": "阳光",
        "suspense": "悬疑",
        "sweet": "甜润",
        "system": "系统",
        "tactical": "战术",
        "tale": "故事/童话",
        "talkative": "健谈",
        "teacher": "教师",
        "telephone": "电话",
        "terminal": "终端",
        "text": "文本",
        "thick": "厚实",
        "threatening": "威胁感",
        "timid": "胆怯",
        "tired": "疲惫",
        "title": "标题",
        "tone": "语气",
        "track": "音轨",
        "trickster": "狡黠角色",
        "troublemaker": "捣蛋角色",
        "tutorial": "教程",
        "ultra": "极致",
        "upbeat": "积极明快",
        "urban": "都市",
        "urgent": "紧急",
        "vehicle": "车载/车辆",
        "velvet": "丝绒感",
        "verdict": "裁决",
        "villain": "反派",
        "vintage": "复古",
        "volume": "音量",
        "vr": "虚拟现实",
        "vulgar": "粗俗",
        "war": "战争",
        "warrior": "战士",
        "weak": "虚弱",
        "weary": "疲惫",
        "whisper": "低语",
        "wise": "睿智",
        "witty": "机智",
        "woman": "女性",
        "worker": "工人",
        "youth": "青年/少年",
    }
)


@dataclass(frozen=True)
class VoiceAssetPaths:
    """Conventional files for one voice asset directory."""

    root: Path
    voice_id: str

    @property
    def directory(self) -> Path:
        return self.root / self.voice_id

    @property
    def voice_json(self) -> Path:
        return self.directory / "voice.json"

    @property
    def readme(self) -> Path:
        return self.directory / "README.md"

    @property
    def sample_text(self) -> Path:
        return self.directory / "sample.txt"

    @property
    def prompt_text(self) -> Path:
        return self.directory / "sample.voice.txt"

    @property
    def controls_json(self) -> Path:
        return self.directory / "sample.controls.json"

    @property
    def wav(self) -> Path:
        return self.directory / "sample.wav"

    @property
    def mp3(self) -> Path:
        return self.directory / "sample.mp3"

    def metadata_files(self) -> tuple[Path, ...]:
        return (
            self.voice_json,
            self.readme,
            self.sample_text,
            self.prompt_text,
            self.controls_json,
        )


@dataclass(frozen=True)
class VoiceAssetBundle:
    voice_id: str
    paths: VoiceAssetPaths
    files: tuple[Path, ...]

    @property
    def directory(self) -> Path:
        return self.paths.directory

    def to_dict(self) -> JsonDict:
        return {
            "voice_id": self.voice_id,
            "directory": str(self.directory),
            "files": [str(path) for path in self.files],
        }


def voice_asset_paths(root: str | Path, voice_id: str) -> VoiceAssetPaths:
    _validate_voice_id_for_path(voice_id)
    return VoiceAssetPaths(root=Path(root), voice_id=voice_id)


def write_voice_asset_bundle(
    voice: Voice,
    root: str | Path = DEFAULT_ASSET_ROOT,
    *,
    sample_text: str | None = None,
    controls: VoiceControls | None = None,
    overwrite: bool = True,
) -> VoiceAssetBundle:
    """Write deterministic metadata files for a single voice directory."""

    paths = voice_asset_paths(root, voice.voice_id)
    paths.directory.mkdir(parents=True, exist_ok=True)
    resolved_controls = controls or default_controls_for_voice(voice)
    text = sample_text or DEFAULT_SAMPLE_TEXT
    prompt = render_voxcpm2_prompt(voice, resolved_controls)
    files = [
        _write_text(
            paths.voice_json,
            json.dumps(voice.to_dict(), ensure_ascii=False, indent=2) + "\n",
            overwrite=overwrite,
        ),
        _write_text(paths.sample_text, text.rstrip() + "\n", overwrite=overwrite),
        _write_text(paths.prompt_text, prompt.rstrip() + "\n", overwrite=overwrite),
        _write_text(
            paths.controls_json,
            json.dumps(resolved_controls.to_dict(), ensure_ascii=False, indent=2) + "\n",
            overwrite=overwrite,
        ),
        _write_text(
            paths.readme,
            render_voice_asset_readme(voice, prompt=prompt, controls=resolved_controls),
            overwrite=overwrite,
        ),
    ]
    return VoiceAssetBundle(voice_id=voice.voice_id, paths=paths, files=tuple(files))


def synthesize_voice_asset(
    voice: Voice,
    root: str | Path = DEFAULT_ASSET_ROOT,
    *,
    sample_text: str | None = None,
    controls: VoiceControls | None = None,
    command: str | None = None,
    make_mp3: bool = False,
    mp3_command: str | None = None,
    overwrite: bool = True,
) -> VoiceAssetBundle:
    """Write the asset directory, synthesize sample.wav, and optionally make sample.mp3."""

    bundle = write_voice_asset_bundle(
        voice,
        root,
        sample_text=sample_text,
        controls=controls,
        overwrite=overwrite,
    )
    text = sample_text or DEFAULT_SAMPLE_TEXT
    synthesize_with_voxcpm2(
        command=command,
        text=text,
        voice=voice,
        output_wav=bundle.paths.wav,
        controls=controls,
    )
    files = list(bundle.files)
    files.append(bundle.paths.wav)
    if make_mp3:
        convert_wav_to_mp3(
            bundle.paths.wav,
            bundle.paths.mp3,
            command=mp3_command,
            voice_id=voice.voice_id,
        )
        files.append(bundle.paths.mp3)
    return VoiceAssetBundle(voice_id=voice.voice_id, paths=bundle.paths, files=tuple(files))


def convert_wav_to_mp3(
    input_wav: str | Path,
    output_mp3: str | Path,
    *,
    command: str | None = None,
    voice_id: str = "",
) -> Path:
    input_path = Path(input_wav)
    output_path = Path(output_mp3)
    if not input_path.is_file():
        raise RuntimeError(f"找不到待转换 WAV：{input_path}")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    args = _audio_convert_args(
        command or os.environ.get("TIMBRE_AUDIO_CONVERT_COMMAND"),
        input_wav=input_path,
        output_mp3=output_path,
        voice_id=voice_id,
    )
    try:
        subprocess.run(
            args,
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
    except FileNotFoundError as exc:
        raise RuntimeError(f"音频转换命令不存在：{args[0]}。") from exc
    except subprocess.CalledProcessError as exc:
        stderr = exc.stderr.strip() if exc.stderr else "无 stderr"
        raise RuntimeError(f"音频转换失败：{stderr}") from exc
    if not output_path.is_file():
        raise RuntimeError(f"音频转换未生成目标 MP3：{output_path}。")
    return output_path


def render_voice_asset_readme(
    voice: Voice,
    *,
    prompt: str | None = None,
    controls: VoiceControls | None = None,
) -> str:
    resolved_controls = controls or default_controls_for_voice(voice)
    constraints = voice.constraints
    not_good_for = constraints.get("not_good_for", [])
    if isinstance(not_good_for, list) and not_good_for:
        not_good_for_text = "、".join(str(item) for item in not_good_for)
    else:
        not_good_for_text = "无"
    notes = str(constraints.get("notes", "")).strip() or "无"
    return (
        f"# {voice.voice_id}\n\n"
        "## 音色定位\n\n"
        f"- 分组：{_describe_term(voice.group)}\n"
        f"- 档案：{_describe_term(voice.profile.gender)} / "
        f"{_describe_term(voice.profile.age_band)} / "
        f"{_describe_term(voice.profile.species)} / {voice.profile.locale}\n"
        f"- 声音质感：{_join_described_values(voice.timbre_tags)}\n"
        f"- 默认语气：{_join_described_values(voice.emotion_biases)}\n"
        f"- 适配角色：{_join_described_values(voice.fit_roles)}\n"
        f"- 不推荐场景：{_join_described_values(tuple(str(item) for item in not_good_for)) if isinstance(not_good_for, list) and not_good_for else not_good_for_text}\n"
        f"- 备注：{notes}\n\n"
        "## 文件约定\n\n"
        "- `voice.json`：从音色库导出的锁定元数据。\n"
        "- `sample.txt`：试听合成文本。\n"
        "- `sample.voice.txt`：VoxCPM2 音色控制提示。\n"
        "- `sample.controls.json`：结构化控制参数。\n"
        "- `sample.wav`：VoxCPM2 生成的无损试听音频。\n"
        "- `sample.mp3`：由 WAV 转出的便携试听音频。\n\n"
        "## VoxCPM2 控制提示\n\n"
        "`sample.voice.txt` 保存本音色实际用于 VoxCPM2 合成的原始控制提示。"
        "该文件面向程序调用，人工阅读优先看上面的中英对照音色定位。\n"
    )


def _audio_convert_args(
    command: str | None,
    *,
    input_wav: Path,
    output_mp3: Path,
    voice_id: str,
) -> list[str]:
    if command:
        values = {
            "input_wav": str(input_wav),
            "output_mp3": str(output_mp3),
            "voice_id": voice_id,
        }
        return [part.format(**values) for part in shlex.split(command, posix=os.name != "nt")]
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise RuntimeError(
            "未找到 ffmpeg。请安装 ffmpeg，或设置 TIMBRE_AUDIO_CONVERT_COMMAND，"
            "模板可使用 {input_wav}、{output_mp3}、{voice_id}。"
        )
    return [
        ffmpeg,
        "-y",
        "-i",
        str(input_wav),
        "-codec:a",
        "libmp3lame",
        "-q:a",
        "2",
        str(output_mp3),
    ]


def _write_text(path: Path, content: str, *, overwrite: bool) -> Path:
    if path.exists() and not overwrite:
        return path
    path.write_text(content, encoding="utf-8")
    return path


def _join_values(values: tuple[str, ...]) -> str:
    return "、".join(values) if values else "无"


def _join_described_values(values: tuple[str, ...]) -> str:
    return "、".join(_describe_term(value) for value in values) if values else "无"


def _describe_term(value: str) -> str:
    if value in TERM_LABELS_ZH:
        return f"{value}（{TERM_LABELS_ZH[value]}）"
    parts = [part for part in value.replace("-", "_").split("_") if part]
    translated = [f"{part}={TERM_LABELS_ZH[part]}" for part in parts if part in TERM_LABELS_ZH]
    if translated:
        return f"{value}（{', '.join(translated)}）"
    return f"{value}（待补充中文说明）"


def _validate_voice_id_for_path(voice_id: str) -> None:
    if not voice_id or voice_id in {".", ".."}:
        raise ValueError("voice_id 不能为空或相对目录")
    if any(separator in voice_id for separator in ("/", "\\")):
        raise ValueError(f"voice_id 不能包含路径分隔符：{voice_id}")
