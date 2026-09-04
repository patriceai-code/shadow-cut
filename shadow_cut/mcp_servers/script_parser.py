"""
Shadow Cut MCP Server — Tool 1: parse_script
Calls Gemini 3.1 Pro Preview to extract a PlotKnowledgeGraph from a film script.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Literal

from pydantic import ValidationError

from shadow_cut.config.settings import get_settings
from shadow_cut.models.schemas import (
    EmotionalBeat,
    PlotKnowledgeGraph,
    PropDefinition,
    SceneDefinition,
    ScenePropRef,
    SetupPayoffLink,
)


# ---------------------------------------------------------------------------
# @tool decorator (watsonx Orchestrate / IBM Bob compatible)
# ---------------------------------------------------------------------------

def tool(func):  # type: ignore[no-untyped-def]
    """
    Lightweight @tool shim.
    In watsonx Orchestrate the platform replaces this with its own decorator;
    in local/test contexts it is a transparent pass-through.
    """
    return func


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

_PROMPT_PATH = Path(__file__).parent.parent / "data" / "script_extraction_prompt.txt"


def _load_prompt_template() -> str:
    if _PROMPT_PATH.exists():
        return _PROMPT_PATH.read_text(encoding="utf-8")
    return (
        "Extract a Plot Knowledge Graph JSON from this script. "
        "Keys: production_title, total_scenes, scenes, props, emotional_arcs, setups.\n"
        "Script:\n{{SCRIPT_TEXT}}"
    )


def _strip_markdown_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?", "", text)
    text = re.sub(r"```$", "", text)
    return text.strip()


def _raw_to_kg(raw: dict) -> PlotKnowledgeGraph:
    """
    Convert Gemini's raw dict output into a validated PlotKnowledgeGraph.
    Tolerates the flat scene dict (keyed by scene number) that the prompt
    template produces.
    """
    # Normalise scenes: may be a dict {"1": {...}} or a list
    scenes_raw = raw.get("scenes", [])
    if isinstance(scenes_raw, dict):
        scenes_raw = list(scenes_raw.values())

    scenes: list[SceneDefinition] = []
    for s in scenes_raw:
        # Normalise per-scene prop lists
        critical = [ScenePropRef(**p) if isinstance(p, dict) else p for p in s.get("critical_props", [])]
        important = [ScenePropRef(**p) if isinstance(p, dict) else p for p in s.get("important_props", [])]
        incidental = [ScenePropRef(**p) if isinstance(p, dict) else p for p in s.get("incidental_props", [])]

        emotional_beats_raw = s.get("emotional_beats", [])
        emotional_beats = [EmotionalBeat(**b) if isinstance(b, dict) else b for b in emotional_beats_raw]

        scene_dict = {**s, "critical_props": critical, "important_props": important,
                      "incidental_props": incidental, "emotional_beats": emotional_beats}
        scenes.append(SceneDefinition(**scene_dict))

    props_raw = raw.get("props", {})
    props: list[PropDefinition] = []
    if isinstance(props_raw, dict):
        for _key, p in props_raw.items():
            props.append(PropDefinition(**p))
    else:
        props = [PropDefinition(**p) if isinstance(p, dict) else p for p in props_raw]

    arcs_raw = raw.get("emotional_arcs", [])
    emotional_arcs = [EmotionalBeat(**a) if isinstance(a, dict) else a for a in arcs_raw]

    setups_raw = raw.get("setups", [])
    setups = [SetupPayoffLink(**su) if isinstance(su, dict) else su for su in setups_raw]

    return PlotKnowledgeGraph(
        production_title=raw.get("production_title", "Untitled"),
        total_scenes=raw.get("total_scenes", len(scenes)),
        scenes=scenes,
        props=props,
        emotional_arcs=emotional_arcs,
        setups=setups,
        extraction_warnings=raw.get("extraction_warnings", []),
    )


# ---------------------------------------------------------------------------
# MCP Tool
# ---------------------------------------------------------------------------

@tool
def parse_script(
    script_text: str,
    format: Literal["pdf", "fountain", "txt"] = "txt",
) -> PlotKnowledgeGraph:
    """
    Parse a film script into a structured Plot Knowledge Graph.

    Sends the full script text to Gemini 3.1 Pro Preview with the Shadow Cut extraction
    prompt and validates the response against the PlotKnowledgeGraph schema.

    Args:
        script_text: Full text content of the script (PDF/Fountain pre-converted to text).
        format:      Source format hint ("pdf", "fountain", or "txt"). Used for logging
                     only; the caller is responsible for text extraction from binary formats.

    Returns:
        PlotKnowledgeGraph with scenes, props, emotional_arcs, and setups.

    Raises:
        ValueError: If Gemini returns invalid JSON or schema validation fails after retry.
    """
    from google import genai  # lazy import — avoids hard dep in schema-only contexts
    from google.genai import types

    settings = get_settings()
    client = genai.Client(api_key=settings.gemini_api_key)
    model = "gemini-3.1-pro-preview"

    prompt_template = _load_prompt_template()
    prompt = prompt_template.replace("{{SCRIPT_TEXT}}", script_text)

    # ── First attempt ──────────────────────────────────────────────────────
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=8192,
                response_mime_type="application/json",
            ),
        )
        raw = json.loads(response.text)
        return _raw_to_kg(raw)
    except (json.JSONDecodeError, ValidationError, KeyError):
        pass

    # ── Retry with strict minimal prompt ──────────────────────────────────
    strict_prompt = (
        "Return ONLY valid JSON with keys: production_title, total_scenes, scenes, "
        "props, emotional_arcs, setups. No markdown, no commentary.\n\n"
        f"Script (truncated to 50 000 chars):\n{script_text[:50_000]}"
    )
    response = client.models.generate_content(
        model=model,
        contents=strict_prompt,
        config=types.GenerateContentConfig(max_output_tokens=8192),
    )
    raw = json.loads(_strip_markdown_fences(response.text))
    return _raw_to_kg(raw)
