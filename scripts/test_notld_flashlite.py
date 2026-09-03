# scripts/test_notld_flashlite.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shadow_cut.core.bridge import FlashLiteBridge
from shadow_cut.config.settings import get_settings
import json

settings = get_settings()
print(f"Connecting to Gemini Flash-Lite with project: {settings.google_cloud_project}...")
bridge = FlashLiteBridge(api_key=settings.gemini_api_key)

with open("test_data/notld/yolo_result.json", "r", encoding="utf-8") as f:
    yolo_math = json.load(f)

with open("test_data/notld/plot_graph.json", "r", encoding="utf-8") as f:
    plot_graph = json.load(f)

scene_context = plot_graph["scenes"]["farmhouse_interior"]
scene_context["scene_number"] = 1
scene_context["scene_title"] = scene_context["title"]
scene_context["characters"] = scene_context["characters_present"]
scene_context["critical_props"] = scene_context["critical_props"]

print("Uploading farmhouse_scene.mp4 and running multimodal validation...")
result = bridge.validate_take(
    video_path="test_data/notld/farmhouse_scene.mp4",
    yolo_math=yolo_math,
    scene_context=scene_context,
    script_summary="Survivors barricade themselves in a farmhouse during a zombie outbreak. Continuity of barricades, weapons, and props is critical."
)

with open("test_data/notld/flashlite_result.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2)

print("Flash-Lite Results:")
print(f"Needs escalation: {result.get('needs_escalation')}")
for v in result.get("verdicts", []):
    print(f"  Verdict: {v.get('verdict')} | Conf: {v.get('confidence')} | {v.get('explanation', '')[:100]}")
for m in result.get("missed_issues", []):
    print(f"  Missed: {m.get('description', '')[:100]}")
