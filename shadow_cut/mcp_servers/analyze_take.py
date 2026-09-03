"""
Shadow Cut MCP Server — Tool 2: analyze_take
Sends raw video + YOLO math + scene context to Gemini Flash-Lite for validation.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Literal

from shadow_cut.config.settings import get_settings
from shadow_cut.models.schemas import (
    AnomalyVerdict,
    FlashLiteResult,
    MissedIssue,
    PerformanceNote,
    SceneContext,
    YoloMath,
)


def tool(func):  # type: ignore[no-untyped-def]
    return func


# ---------------------------------------------------------------------------
# Prompt builder
# ---------------------------------------------------------------------------

def _build_prompt(yolo: YoloMath, ctx: SceneContext) -> str:
    critical_props_json = json.dumps(
        [p.model_dump() for p in ctx.critical_props], indent=2
    )
    anomalies_json = json.dumps(
        [a.model_dump() for a in yolo.anomaly_flags], indent=2
    )
    return f"""You are SHADOW, a film script supervisor AI. Validate this take.

=== SCENE CONTEXT ===
Scene: {ctx.scene_number} — {ctx.scene_title}
Characters: {", ".join(ctx.characters) or "Not specified"}
Required emotional tone: {ctx.emotional_tone or "Not specified"}
Setups active: {", ".join(ctx.setups) or "None"}
Payoffs due: {", ".join(ctx.payoffs) or "None"}

=== CRITICAL PROPS ===
{critical_props_json}

=== YOLO DETECTION DATA ===
Take: {yolo.take_id}
Duration: {yolo.duration_seconds}s  |  Frames analysed: {yolo.frames_analyzed}  |  FPS: {yolo.fps}
Objects tracked: {", ".join(yolo.tracked_objects) or "None"}

=== YOLO ANOMALY FLAGS ===
{anomalies_json}

=== YOUR TASK ===
For EACH anomaly flag (use its list index as anomaly_index):
  - "verdict": "real_issue" | "false_alarm" | "uncertain"
  - "confidence": 0.0–1.0
  - "severity": "critical" | "warning" | "info"
  - "explanation": brief reason (≤ 200 chars)

Also report:
  - missed_issues: critical props in wrong state that YOLO did not flag
  - performance_notes: one entry per character — does tone match required?
  - audio_transcript: verbatim dialogue if you can hear it, else ""
  - needs_escalation: true only if you are uncertain and stake is CRITICAL
  - escalation_reason: short reason if needs_escalation is true

Return ONLY valid JSON:
{{
  "take_id": "{yolo.take_id}",
  "verdicts": [...],
  "missed_issues": [...],
  "performance_notes": [...],
  "audio_transcript": "",
  "needs_escalation": false,
  "escalation_reason": null
}}"""


# ---------------------------------------------------------------------------
# MCP Tool
# ---------------------------------------------------------------------------

@tool
def analyze_take(
    video_path: str,
    yolo_math: YoloMath,
    scene_context: SceneContext,
) -> FlashLiteResult:
    """
    Validate a take using Gemini Flash-Lite multimodal analysis.

    Builds a structured prompt from YOLO anomaly data and scene context, then sends
    it to Gemini Flash-Lite together with the raw video file (if available) for
    cross-modal validation.

    Args:
        video_path:    Filesystem path or GCS URI of the proxy video.
        yolo_math:     Structured YOLO output for this take.
        scene_context: Scene metadata (props, characters, tone) from the plot graph.

    Returns:
        FlashLiteResult with per-anomaly verdicts, missed issues, performance notes,
        audio transcript, and an escalation flag.
    """
    from google import genai
    from google.genai import types

    settings = get_settings()
    client = genai.Client(api_key=settings.gemini_api_key)
    model = "gemini-3.5-flash-lite"

    prompt = _build_prompt(yolo_math, scene_context)

    # ── Try to upload video to Gemini Files API ───────────────────────────
    video_file = None
    local_path = Path(video_path)
    if local_path.exists():
        try:
            video_file = client.files.upload(file=str(local_path))
        except Exception:
            pass  # fall back to text-only

    contents: list = [prompt]
    if video_file:
        contents.insert(0, video_file)

    # ── Call model ────────────────────────────────────────────────────────
    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=types.GenerateContentConfig(
                max_output_tokens=4096,
                response_mime_type="application/json",
            ),
        )
        raw: dict = json.loads(response.text)
    except Exception as exc:
        # Graceful degradation: return empty result flagged for escalation
        return FlashLiteResult(
            take_id=yolo_math.take_id,
            needs_escalation=True,
            escalation_reason=f"Flash-Lite call failed: {exc}",
        )

    # ── Map raw dict → typed result ───────────────────────────────────────
    verdicts = [AnomalyVerdict(**v) for v in raw.get("verdicts", [])]
    missed = [MissedIssue(**m) for m in raw.get("missed_issues", [])]
    perf = [PerformanceNote(**p) for p in raw.get("performance_notes", [])]

    return FlashLiteResult(
        take_id=yolo_math.take_id,
        verdicts=verdicts,
        missed_issues=missed,
        performance_notes=perf,
        audio_transcript=raw.get("audio_transcript", ""),
        needs_escalation=bool(raw.get("needs_escalation", False)),
        escalation_reason=raw.get("escalation_reason"),
        cost_usd=0.002,  # Flash-Lite per-call estimate
    )
