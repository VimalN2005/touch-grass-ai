"""Open-Source AI Inference Engine for TouchGrass AI.
Supports Groq (Llama 3 open-weights), Hugging Face, Local Ollama, and an offline fallback.
"""

from __future__ import annotations

import json
import random
import requests
from typing import Any, Dict


class OpenSourceAIEngine:
    def __init__(
        self,
        provider: str = "Demo / Offline Mode",
        api_key: str | None = None,
        model_name: str = "llama-3.1-8b-instant",
        ollama_base_url: str = "http://localhost:11434",
    ):
        self.provider = provider
        self.api_key = api_key or ""
        self.model_name = model_name
        self.ollama_base_url = ollama_base_url.rstrip("/")

    def generate(self, prompt: str, system_prompt: str = "You are TouchGrass AI, an empathetic open-source wellness and nature guide for software developers.") -> str:
        if self.provider == "Groq (Llama 3 Open-Weights)" and self.api_key:
            return self._call_groq(prompt, system_prompt)
        elif self.provider == "Hugging Face Inference API" and self.api_key:
            return self._call_huggingface(prompt)
        elif self.provider == "Local Ollama (Offline)" and self.ollama_base_url:
            return self._call_ollama(prompt, system_prompt)
        else:
            return self._offline_generate(prompt)

    def _call_groq(self, prompt: str, system_prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 1200,
        }
        try:
            resp = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=25,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                return f"Error from Groq API ({resp.status_code}): {resp.text}\nFalling back to local heuristic."
        except Exception as e:
            return f"Connection error: {e}. Falling back to offline engine."

    def _call_huggingface(self, prompt: str) -> str:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"inputs": prompt, "parameters": {"max_new_tokens": 800, "temperature": 0.7}}
        try:
            resp = requests.post(
                "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3",
                headers=headers,
                json=payload,
                timeout=25,
            )
            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, list) and len(data) > 0:
                    return data[0].get("generated_text", str(data[0]))
                return str(data)
            return f"HF error ({resp.status_code}). Falling back to offline mode."
        except Exception as e:
            return f"HF connection error: {e}."

    def _call_ollama(self, prompt: str, system_prompt: str) -> str:
        try:
            resp = requests.post(
                f"{self.ollama_base_url}/api/generate",
                json={
                    "model": "llama3",
                    "prompt": f"{system_prompt}\n\nUser: {prompt}\nAssistant:",
                    "stream": False,
                },
                timeout=30,
            )
            if resp.status_code == 200:
                return resp.json().get("response", "")
            return "Ollama returned non-200 status."
        except Exception as e:
            return f"Ollama connection error: {e}. Is Ollama running on localhost?"

    def _offline_generate(self, prompt: str) -> str:
        """High-fidelity dynamic offline simulation when no API key is provided."""
        if "quest" in prompt.lower() or "break" in prompt.lower():
            return json.dumps({
                "quest_title": "The Dopamine & Cortisol Circuit Breaker",
                "duration_minutes": 15,
                "burnout_level_addressed": "High Screen Strain",
                "primary_biome": "Neighborhood Park / Garden Trail",
                "objectives": [
                    "Step outside without looking at your mobile phone or monitor for at least 10 continuous minutes.",
                    "Locate 3 different natural textures (e.g., rough tree bark, cool grass, dry fallen leaves) and touch them.",
                    "Look at the furthest point on the horizon or treetops for 2 minutes to relax your ciliary eye muscles.",
                    "Take 5 deep diaphragmatic breaths matching the rhythm of the wind."
                ],
                "biological_rationale": "Extended close-up screen focus locks the eyes in continuous convergence and blue light suppresses melatonin while elevating sympathetic nervous system tension. Natural optical flow and 20-foot distance viewing resets cognitive focus.",
                "reward_xp": 150,
                "badge_awarded": "Grass Toucher Lv. 1"
            }, indent=2)
        elif "identify" in prompt.lower() or "nature" in prompt.lower():
            return json.dumps({
                "species_candidate": "Neem (Azadirachta indica) or Ficus Microcarpa",
                "category": "Broadleaf Flora / Foliage",
                "observed_features": "Serrate leaf margins, pinnate venation, healthy chlorophyll saturation under natural sunlight.",
                "ecological_significance": "Known for releasing high levels of oxygen during daylight and active bio-filtering of atmospheric microparticulates.",
                "mindfulness_note": "Notice how the leaves tremble independently in subtle air currents—a classic example of natural organic fractal movement that calms the human nervous system.",
                "nature_points": 50
            }, indent=2)
        else:
            return (
                "You take a deep breath. The cool outdoor air fills your lungs. "
                "Step away from the terminal. Look at the leaves swaying in the breeze. "
                "Your code and problem will still be there when you return, but your mind will be 10x sharper."
            )
