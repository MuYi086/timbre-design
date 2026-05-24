"""Rule-based voice matching for book characters."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from timbre_design.library import VoiceLibrary
from timbre_design.models import JsonDict, Voice
from timbre_design.spatial import (
    SPATIAL_ROLE_TAGS,
    SPATIAL_SCENE_KEYWORDS,
    scene_matches_voice,
    spatial_scene_score,
)

AGE_ALIASES = {
    "child": {"child", "children", "儿童", "男孩", "女孩"},
    "teen": {"teen", "teenager", "少年", "少女"},
    "young_adult": {"young", "young_adult", "青年", "年轻", "adult_young"},
    "adult": {"adult", "成年", "成人"},
    "middle_aged": {"middle", "middle_aged", "中年"},
    "senior": {"old", "senior", "elder", "老年", "老人", "年长"},
    "ageless": {"unknown", "neutral", "ageless", "未知", "无年龄"},
}

GENDER_ALIASES = {
    "male": {"male", "man", "男", "男性", "男声"},
    "female": {"female", "woman", "女", "女性", "女声"},
    "neutral": {"neutral", "unknown", "中性", "未知"},
    "male_coded": {"male_coded", "男性感", "男拟声"},
    "female_coded": {"female_coded", "女性感", "女拟声"},
}

SPECIES_KEYWORDS = {
    "robot": {"robot", "机器人", "ai", "AI", "系统", "机械", "头显", "VR", "AR"},
    "spirit": {"spirit", "幽灵", "神谕", "精灵", "鬼", "神秘", "古神"},
    "creature": {"creature", "怪物", "动物", "狐狸", "猫", "熊", "牛", "拟人"},
    "nonhuman": {"nonhuman", "非人", "高维", "宇宙"},
    "human_fx": {"电话", "广播", "收音机", "梦境", "电子", "无线电", "车机", "任务提示"},
}

ROLE_KEYWORDS = {
    "narrator": {"旁白", "叙述", "narrator"},
    "villain": {"反派", "狠", "冷酷", "威压", "villain"},
    "official": {"官", "法官", "司令", "命令", "权威", "official", "commander"},
    "scholar": {"书生", "学者", "教师", "医生", "智者", "scholar"},
    "comic": {"喜剧", "滑稽", "机灵", "顽皮", "comic"},
    "kids": {"儿童", "童话", "睡前", "kids", "fairy"},
    "mystery": {"悬疑", "侦探", "神秘", "mystery", "detective"},
    **SPATIAL_SCENE_KEYWORDS,
    "robot": SPECIES_KEYWORDS["robot"],
    "creature": SPECIES_KEYWORDS["creature"],
}

DEFAULT_CHARACTER_REVIEW_CONFIDENCE = 0.6

CONSTRAINT_KEYWORDS = {
    "high_anger": {"愤怒", "暴怒", "高怒", "怒吼", "吼叫", "angry", "rage"},
    "rage_shout": {"暴怒", "怒吼", "吼叫", "rage", "shout"},
    "fight_shouts": {"打斗", "喊叫", "怒吼", "战斗呼喊", "fight", "shout"},
    "battle_shout": {"战斗", "打斗", "喊叫", "battle", "shout"},
    "loud_action": {"大喊", "喊叫", "动作戏", "战斗", "loud", "action"},
    "high_volume_speech": {"高音量", "大声演讲", "高声", "loud", "speech"},
    "speed_over_1.2x": {"快语速", "超快", "1.2x", "speed over 1.2"},
    "speed_over_1.1x": {"快语速", "1.1x", "speed over 1.1"},
    "rapid_high_density": {"快嘴", "高密度", "信息密集", "rapid", "dense"},
    "high_density_info": {"高密度信息", "信息密集", "知识密集", "dense info"},
    "knowledge_dense_content": {"知识密集", "信息密集", "dense content"},
    "hard_info_delivery": {"硬信息", "科普", "法规", "知识密集"},
    "children_friendly": {"儿童", "孩子", "童话", "儿童友好", "children", "kids"},
    "children_friendly_long": {"儿童", "孩子", "儿童长篇", "children", "kids"},
    "long_children_content": {"儿童长篇", "儿童", "童话", "children"},
    "child_dialogue": {"儿童角色", "孩子对白", "child dialogue"},
    "child_role": {"儿童角色", "孩子", "child role"},
    "kids_friendly": {"儿童友好", "儿童", "kids"},
    "kids_story_main_narration": {"儿童故事", "童话主旁白", "kids story"},
    "children_main": {"儿童主角", "儿童主线", "children main"},
    "dark_horror": {"恐怖", "惊悚", "黑暗", "horror"},
    "horror_scene": {"恐怖", "惊悚", "horror"},
    "horror_whisper": {"恐怖低语", "恐怖", "惊悚", "horror"},
    "light_comedy": {"轻喜剧", "喜剧", "comedy"},
    "slapstick": {"滑稽", "闹剧", "夸张喜剧", "slapstick"},
    "overacted_comedy": {"夸张搞笑", "夸张喜剧", "overacted comedy"},
    "over_comedic": {"夸张搞笑", "过度喜剧", "comedic"},
    "comic_fast": {"快嘴喜剧", "喜剧快节奏", "comic fast"},
    "romance_soft": {"温柔恋爱", "柔情", "恋爱", "romance"},
    "soft_romance": {"温柔恋爱", "柔情", "恋爱", "romance"},
    "soft_love_scene": {"温柔恋爱", "柔情", "爱情", "love scene"},
    "news_reading": {"新闻播报", "播报", "news"},
    "news_broadcast": {"新闻播报", "播报", "news"},
    "modern_clean_anchor": {"现代播报", "新闻播报", "anchor"},
    "full_book_main_track": {"全书主轨", "长篇主轨", "主旁白", "full book"},
    "long_main_narration": {"长篇主旁白", "主旁白", "long narration"},
    "long_high_energy": {"长篇高能", "高能演说", "long high energy"},
    "warm_bedtime": {"睡前", "助眠", "温暖睡前", "bedtime"},
    "warm_bedtime_narration": {"睡前旁白", "助眠", "bedtime narration"},
}


@dataclass(frozen=True)
class CharacterProfile:
    character_id: str
    display_name: str
    gender_group: str = "unknown"
    age_group: str = "unknown"
    species: str = "human"
    role_tags: tuple[str, ...] = ()
    appearance_count: int = 0
    dialogue_count: int = 0
    frequency_class: str = "low_frequency"
    confidence: float = 1.0
    personality_summary: str = ""
    voice_style_hint: str = ""
    raw: JsonDict = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, data: JsonDict) -> "CharacterProfile":
        display_name = str(data.get("display_name") or data.get("name") or "").strip()
        character_id = str(data.get("character_id") or data.get("id") or display_name).strip()
        if not character_id:
            raise ValueError("角色缺少 character_id/display_name")
        role_tags = data.get("role_tags", [])
        if isinstance(role_tags, str):
            role_tags = [role_tags]
        if not isinstance(role_tags, list):
            role_tags = []
        text = " ".join(
            str(data.get(key, ""))
            for key in ("display_name", "personality_summary", "voice_style_hint", "summary")
        )
        return cls(
            character_id=character_id,
            display_name=display_name or character_id,
            gender_group=str(data.get("gender_group") or data.get("gender") or "unknown"),
            age_group=str(data.get("age_group") or data.get("age_band") or "unknown"),
            species=str(data.get("species") or _infer_species(text) or "human"),
            role_tags=tuple(str(tag) for tag in role_tags),
            appearance_count=int(data.get("appearance_count", 0)),
            dialogue_count=int(data.get("dialogue_count", 0)),
            frequency_class=str(data.get("frequency_class", "low_frequency")),
            confidence=float(data.get("confidence", 1.0)),
            personality_summary=str(data.get("personality_summary", "")),
            voice_style_hint=str(data.get("voice_style_hint", "")),
            raw=dict(data),
        )

    def to_context(self) -> str:
        parts = [
            self.display_name,
            self.gender_group,
            self.age_group,
            self.species,
            *self.role_tags,
            self.personality_summary,
            self.voice_style_hint,
        ]
        return " ".join(part for part in parts if part)

    def review_flags(
        self,
        *,
        confidence_threshold: float = DEFAULT_CHARACTER_REVIEW_CONFIDENCE,
    ) -> tuple[str, ...]:
        flags: list[str] = []
        if self.confidence < confidence_threshold:
            flags.append("low_character_confidence")
        gender_text = self.gender_group.strip().lower()
        age_text = self.age_group.strip().lower()
        if gender_text in {"", "unknown", "未知"}:
            flags.append("unknown_gender")
        if age_text in {"", "unknown", "未知"}:
            flags.append("unknown_age")
        return tuple(flags)


@dataclass(frozen=True)
class MatchResult:
    voice: Voice
    score: float
    reasons: tuple[str, ...]
    constraint_hits: tuple[str, ...] = ()
    review_flags: tuple[str, ...] = ()

    def to_dict(self) -> JsonDict:
        return {
            "voice_id": self.voice.voice_id,
            "score": round(self.score, 4),
            "reasons": list(self.reasons),
            "constraint_hits": list(self.constraint_hits),
            "review_flags": list(self.review_flags),
            "voice": self.voice.to_dict(),
        }


def match_voice(
    character: CharacterProfile,
    library: VoiceLibrary,
    *,
    exclude_voice_ids: set[str] | None = None,
    top_k: int = 1,
) -> list[MatchResult]:
    exclude = exclude_voice_ids or set()
    results = [
        _score_voice(character, voice)
        for voice in library.voices
        if voice.voice_id not in exclude and _candidate_allowed(character, voice)
    ]
    results.sort(key=lambda result: (-result.score, result.voice.voice_id))
    return results[:top_k]


def _score_voice(character: CharacterProfile, voice: Voice) -> MatchResult:
    reasons: list[str] = []
    score = 0.0
    gender_score = _gender_score(character.gender_group, voice.profile.gender)
    score += 0.22 * gender_score
    if gender_score >= 0.9:
        reasons.append("gender")
    age_score = _age_score(character.age_group, voice.profile.age_band)
    score += 0.20 * age_score
    if age_score >= 0.9:
        reasons.append("age")
    species_score = _species_score(character.species, voice.profile.species)
    score += 0.23 * species_score
    if species_score >= 0.9:
        reasons.append("species")
    role_score = _role_score(character, voice)
    score += 0.20 * role_score
    if role_score >= 0.5:
        reasons.append("role")
    style_score = _style_score(character, voice)
    score += 0.15 * style_score
    if style_score >= 0.5:
        reasons.append("style")
    spatial_score = spatial_scene_score(set(_derived_role_tags(character)), voice)
    score += 0.24 * spatial_score
    if spatial_score >= 0.75:
        reasons.append("spatial_scene")
    constraint_hits = voice_constraint_hits(character, voice)
    penalty = _constraint_penalty(constraint_hits)
    score -= penalty
    if penalty:
        reasons.append("constraint_penalty")
    review_flags = list(character.review_flags())
    if len(constraint_hits) >= 2:
        review_flags.append("multiple_constraint_hits")
    return MatchResult(
        voice=voice,
        score=max(0.0, min(score, 1.0)),
        reasons=tuple(reasons),
        constraint_hits=constraint_hits,
        review_flags=tuple(review_flags),
    )


def _candidate_allowed(character: CharacterProfile, voice: Voice) -> bool:
    role_tags = set(_derived_role_tags(character))
    spatial_role_tags = role_tags & SPATIAL_ROLE_TAGS
    if voice.group == "spatial":
        return bool(spatial_role_tags) and any(
            scene_matches_voice(scene, voice) for scene in spatial_role_tags
        )
    if _is_narrator(character):
        if role_tags & SPATIAL_ROLE_TAGS:
            return voice.group in {"narrator", "spatial"}
        return voice.group == "narrator"
    if character.species == "human" and voice.profile.species not in {"human", "human_fx"}:
        return False
    if character.species != "human" and voice.profile.species == "human":
        return False
    return True


def _gender_score(character_gender: str, voice_gender: str) -> float:
    normalized = _normalize_alias(character_gender, GENDER_ALIASES)
    if normalized in {"unknown", "neutral"}:
        return 0.75 if voice_gender in {"neutral", "male", "female"} else 0.45
    if normalized == voice_gender:
        return 1.0
    if normalized == "male" and voice_gender == "male_coded":
        return 0.85
    if normalized == "female" and voice_gender == "female_coded":
        return 0.85
    if voice_gender == "neutral":
        return 0.65
    return 0.1


def _age_score(character_age: str, voice_age: str) -> float:
    normalized = _normalize_alias(character_age, AGE_ALIASES)
    if normalized in {"unknown", "ageless"}:
        return 0.75 if voice_age in {"adult", "ageless"} else 0.45
    if normalized == voice_age:
        return 1.0
    adjacent = {
        "young_adult": {"adult", "teen"},
        "adult": {"young_adult", "middle_aged"},
        "middle_aged": {"adult", "senior"},
        "senior": {"middle_aged"},
        "teen": {"young_adult", "child"},
        "child": {"teen"},
    }
    return 0.65 if voice_age in adjacent.get(normalized, set()) else 0.2


def _species_score(character_species: str, voice_species: str) -> float:
    if character_species == voice_species:
        return 1.0
    if character_species == "human" and voice_species == "human_fx":
        return 0.45
    if character_species in {"spirit", "nonhuman"} and voice_species in {"spirit", "nonhuman"}:
        return 0.7
    if character_species in {"creature", "nonhuman"} and voice_species == "creature":
        return 0.75
    if character_species == "robot" and voice_species == "human_fx":
        return 0.35
    return 0.0


def _role_score(character: CharacterProfile, voice: Voice) -> float:
    role_tags = set(_derived_role_tags(character))
    if not role_tags:
        return 0.35
    fit_text = " ".join(voice.fit_roles)
    matched = sum(1 for tag in role_tags if tag in fit_text)
    if matched:
        return min(1.0, 0.35 + matched * 0.3)
    if "narrator" in role_tags and voice.group == "narrator":
        return 1.0
    if "robot" in role_tags and voice.profile.species == "robot":
        return 0.85
    if "creature" in role_tags and voice.profile.species == "creature":
        return 0.8
    return 0.2


def _style_score(character: CharacterProfile, voice: Voice) -> float:
    context = character.to_context().lower()
    text = voice.search_text().lower()
    tokens = _style_tokens(context)
    if not tokens:
        return 0.35
    matched = sum(1 for token in tokens if token.lower() in text)
    return min(1.0, matched / max(2, len(tokens)))


def voice_constraint_hits(character: CharacterProfile, voice: Voice) -> tuple[str, ...]:
    """Return voice constraint keys that appear in the character context."""

    context = character.to_context().lower()
    compact_context = "".join(context.replace("_", " ").split())
    not_good_for = voice.constraints.get("not_good_for", [])
    if not isinstance(not_good_for, list):
        return ()
    hits: list[str] = []
    for item in not_good_for:
        key = str(item).strip()
        if not key:
            continue
        terms = _constraint_terms(key)
        if any(_term_in_context(context, compact_context, term) for term in terms):
            hits.append(key)
    return tuple(hits)


def _constraint_penalty(hits: tuple[str, ...]) -> float:
    return min(len(hits) * 0.14, 0.35)


def _derived_role_tags(character: CharacterProfile) -> tuple[str, ...]:
    tags = set(character.role_tags)
    context = character.to_context()
    if _is_narrator(character):
        tags.add("narrator")
    for tag, keywords in ROLE_KEYWORDS.items():
        if any(keyword in context for keyword in keywords):
            tags.add(tag)
    return tuple(sorted(tags))


def _style_tokens(context: str) -> set[str]:
    tokens: set[str] = set()
    for keywords in ROLE_KEYWORDS.values():
        tokens.update(keyword for keyword in keywords if keyword.lower() in context)
    for keywords in SPECIES_KEYWORDS.values():
        tokens.update(keyword for keyword in keywords if keyword.lower() in context)
    return tokens


def _normalize_alias(value: str, aliases: dict[str, set[str]]) -> str:
    text = value.strip().lower()
    for normalized, candidates in aliases.items():
        if text in {candidate.lower() for candidate in candidates}:
            return normalized
    return text or "unknown"


def _constraint_terms(key: str) -> set[str]:
    normalized = key.lower().strip()
    terms = {
        normalized,
        normalized.replace("_", " "),
        normalized.replace("_", ""),
    }
    terms.update(term.lower() for term in CONSTRAINT_KEYWORDS.get(normalized, set()))
    return {term for term in terms if term}


def _term_in_context(context: str, compact_context: str, term: str) -> bool:
    normalized = term.lower().replace("_", " ").strip()
    compact_term = "".join(normalized.split())
    return bool(normalized) and (normalized in context or compact_term in compact_context)


def _infer_species(text: str) -> str | None:
    for species, keywords in SPECIES_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            return species
    return None


def _is_narrator(character: CharacterProfile) -> bool:
    if character.frequency_class == "narrator":
        return True
    text = f"{character.character_id} {character.display_name}".lower()
    return "narrator" in text or "旁白" in text


def load_character_profiles(payload: Any) -> list[CharacterProfile]:
    if isinstance(payload, dict):
        if isinstance(payload.get("characters"), list):
            payload = payload["characters"]
        else:
            payload = [payload]
    if not isinstance(payload, list):
        raise ValueError("角色输入必须是数组、单个对象，或包含 characters 数组的对象")
    return [CharacterProfile.from_mapping(item) for item in payload if isinstance(item, dict)]
