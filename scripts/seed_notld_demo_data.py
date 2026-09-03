# scripts/seed_notld_demo_data.py
"""
Seeds Firestore with actual Night of the Living Dead forensic results.
Populates:
- productions/notld-1968
- productions/notld-1968/takes
- productions/notld-1968/alerts
- chat_history
"""
import sys
import json
from pathlib import Path
from datetime import datetime, timezone

sys.path.insert(0, str(Path(__file__).parent.parent))

from google.cloud import firestore
from shadow_cut.config.settings import get_settings

settings = get_settings()
print(f"Connecting to Firestore for project: {settings.google_cloud_project}...")

sa_path = Path("service-account.json")
if sa_path.exists():
    db = firestore.Client.from_service_account_json(
        str(sa_path),
        project=settings.google_cloud_project,
        database=settings.firestore_database
    )
else:
    db = firestore.Client(
        project=settings.google_cloud_project,
        database=settings.firestore_database
    )

prod_id = "notld-1968"

with open("test_data/notld/plot_graph.json", "r", encoding="utf-8") as f:
    plot_graph = json.load(f)

with open("test_data/notld/forensic_20min_report.json", "r", encoding="utf-8") as f:
    forensic_data = json.load(f)

# 1. Set Production document
db.collection("productions").document(prod_id).set({
    "production_id": prod_id,
    "title": "Night of the Living Dead (1968)",
    "director": "George A. Romero",
    "created_at": firestore.SERVER_TIMESTAMP,
    "status": "active",
    "plot_graph": plot_graph,
    "continuity_score": forensic_data.get("director_trust_report", {}).get("continuity_score", 0.82),
    "cuts_analyzed": forensic_data.get("director_trust_report", {}).get("total_cuts_analyzed", 142)
})
print("Seeded production document.")

# 2. Add Takes and Alerts from forensic audit
all_errors = forensic_data.get("catalogued_errors", []) + forensic_data.get("novel_undiscovered_errors", [])

for idx, err in enumerate(all_errors, 1):
    take_id = f"s1_sh{idx}_t1"
    is_critical = err.get("category") in ["set_marking", "prop"]
    severity = "critical" if is_critical else "warning"

    now_utc = datetime.now(timezone.utc)
    alert_doc = {
        "alert_id": f"alert_notld_{idx}",
        "take_id": take_id,
        "scene": 1,
        "category": err.get("category"),
        "severity": severity,
        "confidence": err.get("confidence", 0.90),
        "title": err.get("title"),
        "description": err.get("description"),
        "visual_evidence": err.get("visual_evidence"),
        "timestamp_film": err.get("timestamp_film"),
        "timestamp_clip": err.get("timestamp_in_clip"),
        "timestamp": now_utc.isoformat(),
        "status": "pending_review"
    }

    # Write alert document in top-level alerts collection
    db.collection("alerts").document(alert_doc["alert_id"]).set(alert_doc)

    # Write take document
    db.collection("productions").document(prod_id).collection("takes").document(take_id).set({
        "take_id": take_id,
        "scene": 1,
        "shot": idx,
        "take": 1,
        "status": "flagged",
        "uploaded_at": firestore.SERVER_TIMESTAMP,
        "alerts": [alert_doc]
    })
    print(f"Seeded take {take_id}: [{err.get('timestamp_film')}] {err.get('title')}")

# 3. Seed sample Director chat conversation in chat_history
chat_samples = [
    {
        "role": "director",
        "message": "Shadow, why did you flag the board on the upper right door frame at 37:08?",
        "timestamp": firestore.SERVER_TIMESTAMP
    },
    {
        "role": "assistant",
        "message": "At 37:08 (film time), handwritten crew lettering reading 'UPPER RIGHT CORNER' is faintly legible in grease pencil across the center-right face of the wood plank before Ben nails it into place. This is a visible set construction prop marking that should be retaken or digitally painted out.",
        "timestamp": firestore.SERVER_TIMESTAMP
    },
    {
        "role": "director",
        "message": "Did you catch anything the online forums missed in this scene?",
        "timestamp": firestore.SERVER_TIMESTAMP
    },
    {
        "role": "assistant",
        "message": "Yes. At 33:01, the Charcoal Lighter fluid box on the hearth flips brand label orientation between cuts. At 36:32, the closet shoe box jumps from horizontal to tilted. And at 41:11, the key-light on Harry Cooper reverses shadow direction from screen-right to screen-left across dialogue cuts.",
        "timestamp": firestore.SERVER_TIMESTAMP
    }
]

for msg in chat_samples:
    db.collection("chat_history").add(msg)

print("Seeded sample chat history.")
print("\nDemo data seeding completed successfully!")
