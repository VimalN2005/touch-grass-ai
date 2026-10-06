"""Unit tests for TouchGrass AI core engines."""

import pytest
from PIL import Image
from touchgrass.ai_engine import OpenSourceAIEngine
from touchgrass.quest_generator import QuestGenerator
from touchgrass.nature_identifier import NatureIdentifier
from touchgrass.audio_guide import AudioStrollGuide


def test_ai_engine_offline_fallback():
    engine = OpenSourceAIEngine(provider="Demo / Offline Mode")
    res = engine.generate("Generate a quest")
    assert "quest_title" in res
    assert "objectives" in res


def test_quest_generator_structure():
    engine = OpenSourceAIEngine(provider="Demo / Offline Mode")
    gen = QuestGenerator(engine)
    quest = gen.generate_quest(
        screen_hours=7.0,
        task_type="Debugging",
        fatigue_symptoms=["Dry eyes"],
        available_environment="Park",
        available_time_minutes=15,
    )
    assert "quest_title" in quest
    assert isinstance(quest["objectives"], list)
    assert len(quest["objectives"]) >= 3
    assert "biological_rationale" in quest
    assert quest["duration_minutes"] == 15


def test_nature_identifier():
    engine = OpenSourceAIEngine(provider="Demo / Offline Mode")
    identifier = NatureIdentifier(engine)
    img = Image.new("RGB", (100, 100), color="green")
    res = identifier.identify_finding(img, notes="Found near my front porch")
    assert "species_candidate" in res
    assert "ecological_significance" in res
    assert res["nature_points"] > 0


def test_audio_stroll_guide():
    engine = OpenSourceAIEngine(provider="Demo / Offline Mode")
    guide = AudioStrollGuide(engine)
    res = guide.generate_stroll_script(mood="High eye strain", walk_style="Slow walk")
    assert "title" in res
    assert len(res["script"]) > 20
