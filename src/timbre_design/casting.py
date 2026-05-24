"""Build audio-3d-sdd compatible voice-casting payloads."""

from __future__ import annotations

from timbre_design.controls import default_controls_for_voice, render_voxcpm2_prompt
from timbre_design.library import VoiceLibrary
from timbre_design.matcher import (
    DEFAULT_CHARACTER_REVIEW_CONFIDENCE,
    CharacterProfile,
    MatchResult,
    match_voice,
)
from timbre_design.models import JsonDict, Voice
from timbre_design.spatial import default_spatial_placement_for_voice

LOW_FREQUENCY_GROUPS = (
    "青年男",
    "中年男",
    "老年男",
    "青年女",
    "中年女",
    "老年女",
    "儿童",
    "群像",
)

LOW_GROUP_CHARACTERS = {
    "青年男": CharacterProfile("group_young_male", "低频青年男", "male", "young", "human"),
    "中年男": CharacterProfile("group_middle_male", "低频中年男", "male", "middle", "human"),
    "老年男": CharacterProfile("group_old_male", "低频老年男", "male", "old", "human"),
    "青年女": CharacterProfile("group_young_female", "低频青年女", "female", "young", "human"),
    "中年女": CharacterProfile("group_middle_female", "低频中年女", "female", "middle", "human"),
    "老年女": CharacterProfile("group_old_female", "低频老年女", "female", "old", "human"),
    "儿童": CharacterProfile("group_child", "低频儿童", "neutral", "child", "human"),
    "群像": CharacterProfile("group_crowd", "低频群像", "neutral", "unknown", "human"),
}


def build_voice_casting(
    characters: list[CharacterProfile],
    library: VoiceLibrary,
    *,
    provider: str = "voxcpm2-local",
    dedicated_limit: int = 12,
    min_score: float = 0.45,
    min_character_confidence: float = DEFAULT_CHARACTER_REVIEW_CONFIDENCE,
) -> JsonDict:
    used: set[str] = set()
    degradation_notes: list[str] = []
    review_items: list[JsonDict] = []
    match_audit: JsonDict = {
        "policy": {
            "dedicated_limit": dedicated_limit,
            "min_score": min_score,
            "min_character_confidence": min_character_confidence,
        },
        "narrator": {},
        "low_frequency_groups": {},
        "high_frequency_slots": {},
    }

    narrator = _pick_fixed_or_match(
        library,
        preferred_id="v_zh_narr_001",
        character=CharacterProfile("narrator", "旁白", "neutral", "adult", "human", ("narrator",)),
        used=used,
    )
    used.add(narrator.voice_id)
    match_audit["narrator"] = {
        "voice_id": narrator.voice_id,
        "assignment_type": "fixed_preferred_or_best_match",
    }

    low_frequency_groups: dict[str, str] = {}
    selected_voices: dict[str, Voice] = {narrator.voice_id: narrator}
    for group in LOW_FREQUENCY_GROUPS:
        result = match_voice(LOW_GROUP_CHARACTERS[group], library, exclude_voice_ids=used, top_k=1)
        voice = result[0].voice if result else narrator
        low_frequency_groups[group] = voice.voice_id
        selected_voices[voice.voice_id] = voice
        used.add(voice.voice_id)
        match_audit["low_frequency_groups"][group] = (
            _match_audit_entry(LOW_GROUP_CHARACTERS[group], result[0], "low_frequency_group")
            if result
            else {
                "character_id": LOW_GROUP_CHARACTERS[group].character_id,
                "display_name": LOW_GROUP_CHARACTERS[group].display_name,
                "voice_id": narrator.voice_id,
                "assignment_type": "low_frequency_group",
                "score": 0.0,
                "reasons": ["fallback_to_narrator"],
                "review_required": True,
            }
        )

    high_frequency_slots: dict[str, str] = {}
    high_frequency = []
    low_confidence_high_frequency: set[str] = set()
    for character in _dedicated_characters(characters):
        if character.confidence < min_character_confidence:
            low_confidence_high_frequency.add(character.character_id)
            degradation_notes.append(
                f"{character.display_name} 角色抽取置信度 {character.confidence:.2f} "
                f"低于 {min_character_confidence:.2f}，暂不分配独立音色。"
            )
            review_items.append(
                _review_item(
                    character,
                    "low_character_confidence",
                    suggested_slot=_fallback_slot_for_character(
                        character,
                        threshold=min_character_confidence,
                    ),
                )
            )
            continue
        high_frequency.append(character)
    for character in high_frequency[:dedicated_limit]:
        result = match_voice(character, library, exclude_voice_ids=used, top_k=1)
        if not result:
            degradation_notes.append(f"{character.display_name} 未找到可用独立音色，降级为低频分组。")
            review_items.append(_review_item(character, "no_dedicated_voice_available"))
            continue
        match = result[0]
        if match.score < min_score:
            degradation_notes.append(
                f"{character.display_name} 独立音色匹配置信度偏低："
                f"{match.voice.voice_id} score={match.score:.2f}。"
            )
            review_items.append(
                _review_item(
                    character,
                    "low_match_score",
                    suggested_voice_id=match.voice.voice_id,
                    score=match.score,
                )
            )
        if match.review_flags:
            review_items.append(
                _review_item(
                    character,
                    ",".join(match.review_flags),
                    suggested_voice_id=match.voice.voice_id,
                    score=match.score,
                )
            )
        high_frequency_slots[character.character_id] = match.voice.voice_id
        selected_voices[match.voice.voice_id] = match.voice
        used.add(match.voice.voice_id)
        match_audit["high_frequency_slots"][character.character_id] = _match_audit_entry(
            character,
            match,
            "dedicated",
            min_score=min_score,
            min_character_confidence=min_character_confidence,
        )
    for character in high_frequency[dedicated_limit:]:
        degradation_notes.append(
            f"{character.display_name} 超过独立音色上限 {dedicated_limit}，降级为低频分组。"
        )
        review_items.append(_review_item(character, "dedicated_limit_exceeded"))

    fallback_slots = {
        "未识别男声": low_frequency_groups["青年男"],
        "未识别女声": low_frequency_groups["青年女"],
        "旁白": narrator.voice_id,
    }
    review_reasons_by_character = _review_reasons_by_character(review_items)
    character_assignments = _build_character_assignments(
        characters,
        high_frequency_slots=high_frequency_slots,
        low_frequency_groups=low_frequency_groups,
        fallback_slots=fallback_slots,
        low_confidence_character_ids=low_confidence_high_frequency,
        min_character_confidence=min_character_confidence,
        review_reasons_by_character=review_reasons_by_character,
    )
    character_voice_slots = {
        assignment["character_id"]: assignment["voice_id"] for assignment in character_assignments
    }
    voice_descriptions = {
        voice_id: render_voxcpm2_prompt(voice)
        for voice_id, voice in sorted(selected_voices.items())
    }
    voice_controls = {
        voice_id: default_controls_for_voice(voice).to_dict()
        for voice_id, voice in sorted(selected_voices.items())
    }
    spatial_placements: dict[str, JsonDict] = {}
    for voice_id, voice in sorted(selected_voices.items()):
        placement = default_spatial_placement_for_voice(voice)
        if placement is not None:
            spatial_placements[voice_id] = placement
    return {
        "schema_version": "1.3-timbre-design",
        "provider": provider,
        "narrator_voice_slot": narrator.voice_id,
        "high_frequency_slots": high_frequency_slots,
        "low_frequency_groups": low_frequency_groups,
        "fallback_slots": fallback_slots,
        "character_voice_slots": character_voice_slots,
        "character_assignments": character_assignments,
        "voice_descriptions": voice_descriptions,
        "voice_controls": voice_controls,
        "spatial_placements": spatial_placements,
        "provider_voice_ids": {voice_id: voice_id for voice_id in sorted(selected_voices)},
        "degradation_notes": degradation_notes,
        "review_items": _dedupe_review_items(review_items),
        "match_audit": match_audit,
    }


def low_frequency_group(gender_group: str, age_group: str) -> str:
    if age_group in {"child", "teen", "儿童", "少年", "少女"}:
        return "儿童"
    if gender_group in {"male", "男", "男性"}:
        if age_group in {"old", "senior", "老年"}:
            return "老年男"
        if age_group in {"middle", "middle_aged", "中年"}:
            return "中年男"
        return "青年男"
    if gender_group in {"female", "女", "女性"}:
        if age_group in {"old", "senior", "老年"}:
            return "老年女"
        if age_group in {"middle", "middle_aged", "中年"}:
            return "中年女"
        return "青年女"
    return "群像"


def fallback_speaker_slot(
    confidence: float,
    gender_hint: str | None,
    threshold: float = 0.6,
) -> str | None:
    if confidence >= threshold:
        return None
    normalized_gender = _normalize_gender_for_fallback(gender_hint)
    if normalized_gender == "male":
        return "未识别男声"
    if normalized_gender == "female":
        return "未识别女声"
    return "旁白"


def _dedicated_characters(characters: list[CharacterProfile]) -> list[CharacterProfile]:
    candidates = [
        character
        for character in characters
        if character.frequency_class == "high_frequency"
        or character.dialogue_count >= 20
        or character.appearance_count >= 30
    ]
    return sorted(
        candidates,
        key=lambda character: (
            -character.appearance_count,
            -character.dialogue_count,
            character.character_id,
        ),
    )


def _pick_fixed_or_match(
    library: VoiceLibrary,
    *,
    preferred_id: str,
    character: CharacterProfile,
    used: set[str],
) -> Voice:
    try:
        voice = library.get(preferred_id)
        if preferred_id not in used:
            return voice
    except KeyError:
        pass
    result = match_voice(character, library, exclude_voice_ids=used, top_k=1)
    if not result:
        raise ValueError(f"无法为 {character.display_name} 匹配音色")
    return result[0].voice


def _build_character_assignments(
    characters: list[CharacterProfile],
    *,
    high_frequency_slots: dict[str, str],
    low_frequency_groups: dict[str, str],
    fallback_slots: dict[str, str],
    low_confidence_character_ids: set[str],
    min_character_confidence: float,
    review_reasons_by_character: dict[str, list[str]],
) -> list[JsonDict]:
    assignments: list[JsonDict] = []
    for character in characters:
        review_reasons = list(review_reasons_by_character.get(character.character_id, []))
        if character.character_id in high_frequency_slots:
            slot = character.character_id
            voice_id = high_frequency_slots[character.character_id]
            assignment_type = "dedicated"
        elif character.character_id in low_confidence_character_ids:
            slot = _fallback_slot_for_character(character, threshold=min_character_confidence)
            voice_id = fallback_slots[slot]
            assignment_type = "fallback_low_confidence"
            if "low_character_confidence" not in review_reasons:
                review_reasons.append("low_character_confidence")
        else:
            slot = low_frequency_group(character.gender_group, character.age_group)
            voice_id = low_frequency_groups[slot]
            assignment_type = "low_frequency_group"
        assignments.append(
            {
                "character_id": character.character_id,
                "display_name": character.display_name,
                "voice_id": voice_id,
                "slot": slot,
                "assignment_type": assignment_type,
                "confidence": round(character.confidence, 4),
                "review_required": bool(review_reasons),
                "review_reasons": review_reasons,
            }
        )
    return assignments


def _match_audit_entry(
    character: CharacterProfile,
    match: MatchResult,
    assignment_type: str,
    *,
    min_score: float = 0.0,
    min_character_confidence: float = DEFAULT_CHARACTER_REVIEW_CONFIDENCE,
) -> JsonDict:
    review_reasons = list(match.review_flags)
    if match.score < min_score:
        review_reasons.append("low_match_score")
    if character.confidence < min_character_confidence:
        review_reasons.append("low_character_confidence")
    return {
        "character_id": character.character_id,
        "display_name": character.display_name,
        "voice_id": match.voice.voice_id,
        "assignment_type": assignment_type,
        "score": round(match.score, 4),
        "reasons": list(match.reasons),
        "constraint_hits": list(match.constraint_hits),
        "review_required": bool(review_reasons),
        "review_reasons": sorted(set(review_reasons)),
    }


def _review_item(
    character: CharacterProfile,
    reason: str,
    *,
    suggested_voice_id: str | None = None,
    suggested_slot: str | None = None,
    score: float | None = None,
) -> JsonDict:
    item: JsonDict = {
        "character_id": character.character_id,
        "display_name": character.display_name,
        "reason": reason,
        "confidence": round(character.confidence, 4),
    }
    if suggested_voice_id:
        item["suggested_voice_id"] = suggested_voice_id
    if suggested_slot:
        item["suggested_slot"] = suggested_slot
    if score is not None:
        item["score"] = round(score, 4)
    return item


def _dedupe_review_items(items: list[JsonDict]) -> list[JsonDict]:
    seen: set[tuple[str, str]] = set()
    deduped: list[JsonDict] = []
    for item in items:
        key = (str(item.get("character_id", "")), str(item.get("reason", "")))
        if key in seen:
            continue
        seen.add(key)
        deduped.append(item)
    return deduped


def _review_reasons_by_character(items: list[JsonDict]) -> dict[str, list[str]]:
    reasons: dict[str, list[str]] = {}
    for item in items:
        character_id = str(item.get("character_id", ""))
        reason = str(item.get("reason", ""))
        if not character_id or not reason:
            continue
        character_reasons = reasons.setdefault(character_id, [])
        if reason not in character_reasons:
            character_reasons.append(reason)
    return reasons


def _fallback_slot_for_character(
    character: CharacterProfile,
    *,
    threshold: float = DEFAULT_CHARACTER_REVIEW_CONFIDENCE,
) -> str:
    return fallback_speaker_slot(character.confidence, character.gender_group, threshold) or "旁白"


def _normalize_gender_for_fallback(gender_hint: str | None) -> str:
    text = (gender_hint or "").strip().lower()
    if text in {"male", "man", "男", "男性", "男声"}:
        return "male"
    if text in {"female", "woman", "女", "女性", "女声"}:
        return "female"
    return "unknown"
