# scripts/test_notld_pipeline.py
"""
End-to-end pipeline test on Night of the Living Dead.
This is the make-or-break test.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shadow_cut.core.vision_pipeline import VisionPipeline
from shadow_cut.core.bridge import FlashLiteBridge
from shadow_cut.core.confidence import ConfidenceEngine, Anomaly, PlotWeight
from shadow_cut.config.settings import get_settings
import json

settings = get_settings()

print("=" * 60)
print("SHADOW CUT — Night of the Living Dead Pipeline Test")
print("=" * 60)

# Step 1: YOLO
print("\n[1/4] Running YOLO-World...")
vision = VisionPipeline(device=settings.yolo_device)
vision.set_classes(["wooden_plank", "rifle", "shoes", "person", "door", "window"])
yolo_result = vision.process_video("test_data/notld/farmhouse_scene.mp4", sample_fps=1)
print(f"  - {yolo_result['frames_analyzed']} frames analyzed")
print(f"  - Objects: {list(yolo_result['object_tracks'].keys())}")
print(f"  - Anomalies flagged: {len(yolo_result['anomaly_flags'])}")

# Step 2: Flash-Lite
print("\n[2/4] Running Gemini Flash-Lite...")
bridge = FlashLiteBridge(api_key=settings.gemini_api_key)

with open("test_data/notld/plot_graph.json", "r", encoding="utf-8") as f:
    plot_graph = json.load(f)

scene_ctx = plot_graph["scenes"]["farmhouse_interior"]
scene_ctx["scene_number"] = 1
scene_ctx["scene_title"] = scene_ctx["title"]
scene_ctx["characters"] = scene_ctx["characters_present"]

flash_result = bridge.validate_take(
    "test_data/notld/farmhouse_scene.mp4",
    yolo_result,
    scene_ctx,
    "Survivors barricade themselves in a farmhouse during a zombie outbreak."
)
print(f"  - Verdicts: {len(flash_result.get('verdicts', []))}")
print(f"  - Missed issues: {len(flash_result.get('missed_issues', []))}")
print(f"  - Needs escalation: {flash_result.get('needs_escalation')}")

# Step 3: Confidence Engine
print("\n[3/4] Running Confidence Engine...")
engine = ConfidenceEngine(pro_budget=50)

for verdict in flash_result.get("verdicts", []):
    anomaly = Anomaly(
        category=verdict.get("type", "unknown"),
        prop_name=verdict.get("prop"),
        scene=1
    )
    conf = engine.calculate_technical_confidence(anomaly)
    weight = PlotWeight.CRITICAL if verdict.get("severity") == "critical" else PlotWeight.IMPORTANT
    action = engine.decide_action(anomaly, conf, weight)
    print(f"  - {verdict.get('prop', 'unknown')}: conf={conf:.2f} -> {action.value}")

# Step 4: Results
print("\n[4/4] Results Summary")
print("-" * 60)

found_plank_text = False
for v in flash_result.get("verdicts", []):
    if "plank" in v.get("explanation", "").lower() or "upper right" in v.get("explanation", "").lower():
        found_plank_text = True
        print(f"  FOUND: {v['explanation'][:120]}")

for m in flash_result.get("missed_issues", []):
    if "plank" in m.get("description", "").lower() or "text" in m.get("description", "").lower():
        found_plank_text = True
        print(f"  FOUND (missed): {m['description'][:120]}")

if not found_plank_text:
    print("  Did not detect plank text anomaly")
    print("  -> For demo: use controlled phone clips with OBVIOUS errors")

print("\n" + "=" * 60)
print("Test complete. Check test_data/notld/ for full outputs.")
print("=" * 60)
