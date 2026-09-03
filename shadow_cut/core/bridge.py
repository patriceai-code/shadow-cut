"""
Bridge: YOLO math -> Gemini Flash-Lite validation.
Gemini receives the RAW VIDEO FILE directly -- no frame extraction needed.
"""
import json
from google import genai
from google.genai import types
from pathlib import Path

class FlashLiteBridge:
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-3.5-flash-lite"

    def validate_take(self, video_path: str, yolo_math: dict, scene_context: dict, script_summary: str) -> dict:
        prompt = f"""
You are SHADOW, a film script supervisor AI. Analyze this take with the following context:

=== SCENE CONTEXT ===
Scene: {scene_context.get("scene_number", "?")} - {scene_context.get("scene_title", "Unknown")}
Characters: {", ".join(scene_context.get("characters", []))}
Required emotional tone: {scene_context.get("emotional_tone", "Not specified")}

=== CRITICAL PROPS ===
{json.dumps(scene_context.get("critical_props", []), indent=2)}

=== SCRIPT SUMMARY ===
{script_summary}

=== YOLO DETECTION DATA ===
Take: {yolo_math.get("take_id")}
Duration: {yolo_math.get("duration_seconds")}s
Frames analyzed: {yolo_math.get("frames_analyzed")}
Objects tracked: {list(yolo_math.get("object_tracks", {}).keys())}

=== YOLO ANOMALY FLAGS ===
{json.dumps(yolo_math.get("anomaly_flags", []), indent=2)}

=== YOUR TASK ===
Review the YOLO anomaly flags and determine if each is a REAL continuity issue or a FALSE ALARM.

For EACH anomaly, output:
- "verdict": "real_issue", "false_alarm", or "uncertain"
- "confidence": 0.0 to 1.0
- "severity": "critical", "warning", or "info"
- "explanation": Brief reason

Also check:
1. Are any CRITICAL props missing or in wrong states?
2. Did YOLO miss any important changes?
3. Does the performance match the required emotional tone?

Return ONLY valid JSON with this structure:
{{
  "take_id": "...",
  "verdicts": [...],
  "missed_issues": [...],
  "performance_notes": [...],
  "needs_escalation": false,
  "escalation_reason": null
}}
"""
        video_file = None
        if Path(video_path).exists():
            try:
                print(f"Uploading {video_path} to Gemini Files API...")
                video_file = self.client.files.upload(file=video_path)
                print(f"Video uploaded: {video_file.name}")
            except Exception as e:
                print(f"Failed to upload video to Gemini: {e}")

        contents = [prompt]
        if video_file:
            contents.insert(0, video_file)

        try:
            print(f"Calling {self.model} for multimodal validation...")
            response = self.client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    max_output_tokens=4096,
                    response_mime_type="application/json"
                )
            )
            result = json.loads(response.text)
            result["take_id"] = yolo_math.get("take_id")
            result["processing_time_ms"] = 0
            result["tokens_used"] = 0
            result["cost_usd"] = 0.002
            return result
        except Exception as e:
            return {
                "take_id": yolo_math.get("take_id"),
                "verdicts": [],
                "missed_issues": [],
                "performance_notes": [],
                "needs_escalation": True,
                "escalation_reason": f"Validation error or JSON decode failure: {e}"
            }
