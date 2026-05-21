from __future__ import annotations

from timbre_design.library import load_voice_library


def test_bundled_library_validates() -> None:
    library = load_voice_library()

    assert library.validate() == []
    assert library.summary()["total_voices"] == 96
    assert library.get("v_zh_narr_001").profile.gender == "male"


def test_search_finds_robot_voice() -> None:
    library = load_voice_library()

    results = library.search("robot service", limit=3)

    assert results
    assert any(voice.profile.species == "robot" for voice in results)
