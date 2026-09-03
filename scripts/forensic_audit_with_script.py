import os
import sys
import time
import json
from pathlib import Path
from dotenv import load_dotenv

# Load environment
load_dotenv()

from google import genai
from google.genai import types

def run_audit():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        sys.exit(1)

    client = genai.Client(api_key=api_key)

    video_path = Path("test_data/notld/farmhouse_scene_full.mp4")
    script_path = Path("test_data/notld/farmhouse_scene_script.txt")

    if not video_path.exists():
        print(f"Error: {video_path} not found.")
        sys.exit(1)
    if not script_path.exists():
        print(f"Error: {script_path} not found.")
        sys.exit(1)

    screenplay_text = script_path.read_text(encoding="utf-8")

    file_size_mb = video_path.stat().st_size / (1024 * 1024)
    print(f"Uploading {video_path} ({file_size_mb:.1f} MB) to Gemini Files API...")

    video_file = client.files.upload(file=str(video_path))
    print(f"File uploaded: {video_file.name}. Waiting for processing...")

    while video_file.state.name == "PROCESSING":
        print("Video is processing in Google Cloud, waiting 10 seconds...")
        time.sleep(10)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name != "ACTIVE":
        print(f"File processing failed: {video_file.state.name}")
        sys.exit(1)

    print(f"Video is ACTIVE: {video_file.uri}")
    print("Running Script-Grounded Forensic Audit with Gemini 3.5 Flash-Lite...")

    prompt = f"""You are Shadow, an elite Hollywood script supervisor and cinematic continuity engineer.
You have been provided with:
1. The SHOOTING SCREENPLAY for the scene.
2. The FULL 20-MINUTE VIDEO of the scene as filmed (Minutes 25:00 to 45:00 of Night of the Living Dead 1968).

=== SHOOTING SCREENPLAY ===
{screenplay_text}
===========================

Perform an exhaustive, rigorous, frame-by-frame script supervisor audit comparing what is WRITTEN in the screenplay against what is ACTUALLY VISIBLE on camera across all 142 cuts.

CRITICAL RULES FOR ACCURACY (ZERO-HALLUCINATION POLICY):
1. STRICT VISUAL ANCHORING:
   - ONLY report objects, props, wardrobe, or body parts that are PHYSICALLY VISIBLE inside the camera frame.
   - If an actor's lower body, feet, or shoes are cropped out of frame by the camera angle (e.g. bust or medium close-ups), DO NOT infer, guess, or report on them. Never hallucinate off-camera details.
   - DO NOT regurgitate online film trivia unless you can verify it directly in the video pixels.
2. SCRIPT DEVIATIONS (PERFORMANCE VS TEXT):
   - Note where actor performance or physical blocking deviated from written action descriptions (e.g., Ben dismantling the table by bare hands instead of the scripted tire iron).
3. CONTINUITY CLASSIFICATION:
   - 'RETAKE REQUIRED': Fourth-wall breaches, crew construction notes on camera (e.g. handwritten text on wood planks), or major production blunders.
   - 'DIRECTOR REVIEW REQUIRED': Clear, visually verified prop or lighting discrepancies between cuts that require the director's artistic judgment.
   - 'LOG ONLY': Natural actor movement, posture shifts during dialogue, or subtle coverage lighting adjustments.

Check specifically:
- Living room door barricade: Inspect the lumber planks for visible crew handwriting or carpenter marks.
- Hearth and mantelpiece: Track the 'Charcoal Lighter' fluid container placement and orientation.
- Hallway closet: Inspect the Winchester rifle retrieval, ammunition box, and shelf contents.
- Basement confrontation: Inspect the lighting contrast and key-light shadows on Harry Cooper and Ben.

Return your findings in pure, strictly valid JSON matching this schema:
{{
  "scene_audit_summary": {{
    "total_cuts_analyzed": 142,
    "critical_errors_found": integer,
    "warnings_found": integer,
    "minor_variations_found": integer,
    "continuity_health_score": 0.0 to 1.0,
    "executive_summary": "string"
  }},
  "script_deviations": [
    {{
      "timestamp_film": "MM:SS",
      "timestamp_clip": "MM:SS",
      "scripted_element": "string",
      "filmed_reality": "string",
      "severity": "warning" | "minor",
      "objective_impact": "string"
    }}
  ],
  "continuity_alerts": [
    {{
      "timestamp_film": "MM:SS",
      "timestamp_clip": "MM:SS",
      "category": "set_marking" | "prop" | "wardrobe" | "lighting" | "blocking",
      "title": "string",
      "severity": "critical" | "warning" | "minor",
      "director_action_required": "RETAKE REQUIRED" | "DIRECTOR REVIEW REQUIRED" | "LOG ONLY",
      "confidence": 0.0 to 1.0,
      "description": "string",
      "visual_evidence": "string",
      "technical_impact": "string"
    }}
  ]
}}
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[video_file, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            temperature=0.1
        )
    )

    output_path = Path("test_data/notld/script_grounded_report.json")
    clean_text = response.text.strip()
    if clean_text.startswith("```json"):
        clean_text = clean_text[7:]
    if clean_text.endswith("```"):
        clean_text = clean_text[:-3]

    output_path.write_text(clean_text, encoding="utf-8")
    print(f"\nAudit complete! Saved to {output_path}")

    # Print summary
    try:
        data = json.loads(clean_text)
        print("\n" + "="*60)
        print(f"CRITICAL ERRORS: {data.get('scene_audit_summary', {}).get('critical_errors_found')}")
        print(f"WARNINGS: {data.get('scene_audit_summary', {}).get('warnings_found')}")
        print(f"CONTINUITY HEALTH SCORE: {data.get('scene_audit_summary', {}).get('continuity_health_score')}")
        print("="*60)
        print("\nCONTINUITY ALERTS:")
        for alert in data.get("continuity_alerts", []):
            print(f"[{alert.get('timestamp_film')}] {alert.get('title')} [{alert.get('severity').upper()}] -> {alert.get('director_action_required')}")
            print(f"   Evidence: {alert.get('visual_evidence')}")
        print("\nSCRIPT DEVIATIONS:")
        for dev in data.get("script_deviations", []):
            print(f"[{dev.get('timestamp_film')}] Scripted: {dev.get('scripted_element')} -> Filmed: {dev.get('filmed_reality')} [{dev.get('severity').upper()}]")
        print("="*60)
    except Exception as e:
        print(f"Failed to pretty print: {e}")
        print(clean_text[:500])

if __name__ == "__main__":
    run_audit()
