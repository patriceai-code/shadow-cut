# scripts/test_notld_yolo.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shadow_cut.core.vision_pipeline import VisionPipeline
import json

print("Initializing YOLO-World vision pipeline...")
vision = VisionPipeline(device="cpu")
vision.set_classes([
    "wooden_plank", "rifle", "shoes", "tissue_box",
    "picture_frame", "vase", "door", "window", "person"
])

print("Processing farmhouse_scene.mp4 with YOLO at 1 fps...")
result = vision.process_video("test_data/notld/farmhouse_scene.mp4", sample_fps=1)

with open("test_data/notld/yolo_result.json", "w") as f:
    json.dump(result, f, indent=2)

print(f"Analyzed {result['frames_analyzed']} frames")
print(f"Detected objects: {list(result['object_tracks'].keys())}")
print(f"Anomalies: {len(result['anomaly_flags'])}")
for a in result["anomaly_flags"]:
    print(f"  - {a['type']}: {a['prop']} ({a['severity']}, conf={a['confidence']:.2f})")
