"""
Plot Knowledge Graph builder.
Reads script, calls Gemini Pro, validates against schema.
"""
import json
from google import genai
from google.genai import types
from pathlib import Path

class PlotGraphBuilder:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.1-pro-preview"

    def parse_script(self, script_text: str, production_title: str = "Untitled") -> dict:
        """Parse script into Plot Knowledge Graph."""
        prompt_path = Path(__file__).parent.parent / "data" / "script_extraction_prompt.txt"
        if prompt_path.exists():
            prompt_template = prompt_path.read_text(encoding="utf-8")
            prompt = prompt_template.replace("{{SCRIPT_TEXT}}", script_text)
        else:
            prompt = f"Extract plot knowledge graph JSON from this script:\n{script_text}"

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=8192,
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except Exception:
            return self._retry_parse(script_text)

    def _retry_parse(self, script_text: str) -> dict:
        strict_prompt = f"""
        Extract ONLY valid JSON from this script. No markdown, no explanations.
        The JSON must have these top-level keys: scenes, props, emotional_arcs, setups.
        Script: {script_text[:50000]}
        """
        response = self.client.models.generate_content(
            model=self.model,
            contents=strict_prompt,
            config=types.GenerateContentConfig(max_output_tokens=8192)
        )
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        return json.loads(text.strip())
