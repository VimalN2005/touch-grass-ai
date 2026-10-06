"""Outdoor Quest Generator for Developers."""

from __future__ import annotations

import json
from typing import Any, Dict
from .ai_engine import OpenSourceAIEngine


class QuestGenerator:
    def __init__(self, engine: OpenSourceAIEngine):
        self.engine = engine

    def generate_quest(
        self,
        screen_hours: float,
        task_type: str,
        fatigue_symptoms: list[str],
        available_environment: str,
        available_time_minutes: int = 15,
    ) -> Dict[str, Any]:
        prompt = f"""
You are TouchGrass AI, an expert neuro-wellness and open-source nature companion for programmers.
A software developer has been coding and needs to step away to 'touch grass' and rejuvenate.

Developer Details:
- Hours staring at code today: {screen_hours} hours
- Work context: {task_type}
- Physical/Mental Symptoms: {", ".join(fatigue_symptoms) if fatigue_symptoms else "General fatigue"}
- Available outdoor environment: {available_environment}
- Target break duration: {available_time_minutes} minutes

Generate a custom, gamified 'Touch Grass Quest' formatted strictly as JSON with the following keys:
- "quest_title": string (an inspiring, fun name for the quest)
- "duration_minutes": integer
- "burnout_level_addressed": string
- "primary_biome": string
- "objectives": list of 4 concrete, actionable outdoor steps
- "biological_rationale": string (neuroscience/health explanation of why this outdoor exercise resets attention and dopamine)
- "reward_xp": integer (between 100 and 300)
- "badge_awarded": string (e.g. "Sunlight Synthesizer", "Mindful Stroller", "Nature Debugger")

Output ONLY valid JSON.
"""
        raw_response = self.engine.generate(prompt)
        return self._parse_json(raw_response)

    def _parse_json(self, raw: str) -> Dict[str, Any]:
        cleaned = raw.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json")[1].split("```")[0].strip()
        elif "```" in cleaned:
            cleaned = cleaned.split("```")[1].split("```")[0].strip()
        try:
            return json.loads(cleaned)
        except Exception:
            # Fallback robust parse
            return {
                "quest_title": "The Sunlight Reset & Grounding Quest",
                "duration_minutes": 15,
                "burnout_level_addressed": "Cognitive & Ocular Fatigue",
                "primary_biome": "Open Air Space",
                "objectives": [
                    "Step away from all screens and remove blue-light glasses.",
                    "Walk outdoors for 10 minutes, observing 3 distinct shades of green foliage.",
                    "Look into the distance (20+ feet) to relieve focal convergence strain.",
                    "Take 5 deep breaths feeling the ambient temperature against your skin."
                ],
                "biological_rationale": "Direct natural sunlight stimulates dopamine release in the retina, while optic flow from walking suppresses the brain's default mode network, dissolving debugging fixation.",
                "reward_xp": 175,
                "badge_awarded": "Sunlight Healer"
            }
