# scripts/forensic_audit_notld_20min.py
"""
Forensic 20-Minute Continuity Audit on Night of the Living Dead (1968).
Analyzes the entire farmhouse boarding-up sequence (~25:00 to 45:00)
to identify documented continuity goofs (like 'upper right corner' plank)
and uncover brand-new, uncatalogued continuity errors across cutaways.
"""
import sys
import time
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from google import genai
from google.genai import types
from shadow_cut.config.settings import get_settings

settings = get_settings()
client = genai.Client(api_key=settings.gemini_api_key)

video_path = "test_data/notld/farmhouse_scene_full.mp4"
print(f"Uploading {video_path} (123.6 MB) to Gemini Files API...")

video_file = client.files.upload(file=video_path)
print(f"File uploaded: {video_file.name}. Waiting for processing...")

# Poll until ACTIVE
while video_file.state.name == "PROCESSING":
    print("Video is processing in Google Cloud, waiting 10 seconds...")
    time.sleep(10)
    video_file = client.files.get(name=video_file.name)

if video_file.state.name != "ACTIVE":
    raise RuntimeError(f"Video file processing failed with state: {video_file.state.name}")

print(f"Video is ACTIVE: {video_file.uri}")

prompt = """
You are SHADOW, an elite film script supervisor AI performing a forensic continuity analysis on this 20-minute sequence (approx. minutes 25:00 - 45:00) of George A. Romero's 1968 classic film 'Night of the Living Dead'.

This sequence covers the desperate farmhouse boarding-up, searching the upstairs rooms, finding the rifle and ammunition, and fortifying against the living dead.

Analyze all shots, camera setups, and cutaways across the full 20 minutes with extreme precision.

Specifically investigate:

1. BARRICADE PLANKS & SET CONSTRUCTION MARKINGS:
   - Track every board nailed to the front door and windows.
   - Look for the famous production easter egg: the board with "UPPER RIGHT CORNER" (or similar wording) written in dark marker/pencil/chalk on the wood by the crew. State the exact timestamp (mm:ss relative to this video clip and relative to the 25:00 offset), which board it is, and how visible it is.
   - Look for board orientation or nail position discrepancies before and after reverse cuts.

2. WEAPONS & PROPS CONTINUITY:
   - The Winchester lever-action rifle (handling, leaning against walls/couch/table, orientation between angle reversals).
   - The ammunition / bullet box.
   - Kerosene lamp, matches, fireplace tools, hammer, nails.

3. ACTORS, WARDROBE & PHYSICAL CONTINUITY:
   - Barbra: Footwear continuity (barefoot on the couch vs. slippers/shoes between cuts), hair dishevelment, dress state.
   - Ben: Sweat patterns, jacket/shirt state, tool holding hand.

4. DEBRIS & FURNITURE:
   - The dismantled dining chairs and tables: layout of broken wood pieces on the floor changing between angles.

5. BRAND-NEW / UNDISCOVERED CONTINUITY ERRORS:
   - Identify any subtle micro-continuity lapses in this 1968 indie production that are NOT widely catalogued on trivia sites (e.g. background door ajar angles, window latch positions, objects on shelves shifting, shadow angles from artificial lights).

Provide your response in valid JSON with this exact schema:
{
  "sequence_summary": "Brief summary of the 20-minute sequence analyzed",
  "catalogued_errors": [
    {
      "timestamp_in_clip": "mm:ss",
      "timestamp_film": "mm:ss",
      "category": "prop | wardrobe | set_marking | lighting",
      "title": "Short title",
      "description": "Detailed explanation of the error",
      "visual_evidence": "Exact description of what is seen on screen across the cut",
      "confidence": 0.95
    }
  ],
  "novel_undiscovered_errors": [
    {
      "timestamp_in_clip": "mm:ss",
      "timestamp_film": "mm:ss",
      "category": "prop | wardrobe | set_construction | lighting | blocking",
      "title": "Short title",
      "description": "Detailed explanation of the newly discovered error",
      "visual_evidence": "Exact description of what is seen on screen",
      "confidence": 0.90
    }
  ],
  "director_trust_report": {
    "total_cuts_analyzed": 0,
    "continuity_score": 0.85,
    "reshoot_risk_level": "CRITICAL | MODERATE | LOW",
    "summary_verdict": "Executive summary for the director"
  }
}
"""

print("Submitting 20-minute video to Gemini 3.5 Flash-Lite...")
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=[video_file, prompt],
    config=types.GenerateContentConfig(
        max_output_tokens=8192,
        response_mime_type="application/json"
    )
)

out_path = "test_data/notld/forensic_20min_report.json"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"\nForensic analysis complete! Saved to {out_path}")
try:
    data = json.loads(response.text)
    print("\n" + "=" * 60)
    print("CATALOGUED ERRORS FOUND:")
    for err in data.get("catalogued_errors", []):
        print(f"[{err.get('timestamp_film', '??')}] {err.get('title')}: {err.get('description')}")
    print("\n" + "=" * 60)
    print("NOVEL / UNDISCOVERED ERRORS FOUND:")
    for err in data.get("novel_undiscovered_errors", []):
        print(f"[{err.get('timestamp_film', '??')}] {err.get('title')}: {err.get('description')}")
    print("=" * 60)
except Exception as e:
    print(f"Raw output:\n{response.text[:500]}...")
