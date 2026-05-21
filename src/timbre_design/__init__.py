"""Chinese timbre library and VoxCPM2 voice-design helpers."""

from timbre_design.library import VoiceLibrary, load_voice_library
from timbre_design.matcher import CharacterProfile, MatchResult, match_voice

__all__ = [
    "CharacterProfile",
    "MatchResult",
    "VoiceLibrary",
    "load_voice_library",
    "match_voice",
]

__version__ = "0.1.0"
