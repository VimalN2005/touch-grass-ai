"""Mindful Nature Stroll Script & Guide."""

from __future__ import annotations

from typing import Dict, Any
from .ai_engine import OpenSourceAIEngine


class AudioStrollGuide:
    def __init__(self, engine: OpenSourceAIEngine):
        self.engine = engine

    def generate_stroll_script(self, mood: str = "Tense / High Screen Overload", walk_style: str = "Slow Garden Walk") -> Dict[str, Any]:
        prompt = f"""
You are TouchGrass AI's mindfulness and nature guide.
A developer is taking a walking break outside to reset from coding.
Current State: {mood}
Style of Walk: {walk_style}

Write a peaceful, calming 4-phase walking meditation script:
Phase 1: Leaving the desk and feeling the ground under feet.
Phase 2: Opening the senses (listening to wind, birds, rustling trees).
Phase 3: Deep breathing and dissolving mental bug loops.
Phase 4: Returning with renewed mental clarity.

Include a title, estimated duration (3-5 minutes), and the narration text for each phase.
"""
        raw = self.engine.generate(prompt)
        return {
            "title": "5-Minute Code Dissolution Stroll",
            "duration": "5 Minutes",
            "script": raw
        }
