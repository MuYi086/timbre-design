from __future__ import annotations

from timbre_design.library import load_voice_library
from timbre_design.matcher import CharacterProfile, match_voice


def test_match_young_female_character_prefers_human_female() -> None:
    library = load_voice_library()
    character = CharacterProfile(
        character_id="char_001",
        display_name="女主角",
        gender_group="female",
        age_group="young",
        personality_summary="清冷、聪慧、敏感",
        voice_style_hint="清晰、略冷、诗性",
        frequency_class="high_frequency",
    )

    result = match_voice(character, library, top_k=1)[0]

    assert result.voice.profile.gender == "female"
    assert result.voice.profile.species == "human"
    assert result.score > 0.5


def test_match_robot_character_prefers_robot_voice() -> None:
    library = load_voice_library()
    character = CharacterProfile(
        character_id="ai",
        display_name="中控AI",
        gender_group="neutral",
        age_group="ageless",
        species="robot",
        voice_style_hint="高智能 AI，冷静清晰，系统提示",
        frequency_class="high_frequency",
    )

    result = match_voice(character, library, top_k=1)[0]

    assert result.voice.profile.species == "robot"
