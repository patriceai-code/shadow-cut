# scripts/seed_notld_demo_data.py
"""
Seeds Firestore with actual Night of the Living Dead script-grounded forensic results.
Populates:
- productions/notld-1968
- productions/notld-1968/takes
- productions/notld-1968/alerts
- productions/notld-1968/script_deviations
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

with open("test_data/notld/script_grounded_report.json", "r", encoding="utf-8") as f:
    report_data = json.load(f)

audit_summary = report_data.get("scene_audit_summary", {})
script_deviations = report_data.get("script_deviations", [])
continuity_alerts = report_data.get("continuity_alerts", [])

# 1. Set Production document
db.collection("productions").document(prod_id).set({
    "production_id": prod_id,
    "title": "Night of the Living Dead (1968)",
    "director": "George A. Romero",
    "created_at": firestore.SERVER_TIMESTAMP,
    "status": "active",
    "plot_graph": plot_graph,
    "continuity_score": audit_summary.get("continuity_health_score", 0.76),
    "cuts_analyzed": audit_summary.get("total_cuts_analyzed", 142),
    "executive_summary": audit_summary.get("executive_summary", ""),
    "script_deviations": script_deviations
})
print("Seeded production document with script deviations.")

# Clean existing alerts collection to ensure exact sync
existing_alerts = db.collection("alerts").stream()
for al in existing_alerts:
    al.reference.delete()

# 2. Add Takes and Alerts from script-grounded forensic audit
for idx, alert in enumerate(continuity_alerts, 1):
    take_id = f"s1_sh{idx}_t1"
    now_utc = datetime.now(timezone.utc)
    
    alert_doc = {
        "alert_id": f"alert_notld_{idx}",
        "take_id": take_id,
        "scene": 1,
        "category": alert.get("category"),
        "severity": alert.get("severity"),
        "confidence": alert.get("confidence", 0.95),
        "title": alert.get("title"),
        "description": alert.get("description"),
        "visual_evidence": alert.get("visual_evidence"),
        "technical_impact": alert.get("technical_impact"),
        "director_action_required": alert.get("director_action_required"),
        "timestamp_film": alert.get("timestamp_film"),
        "timestamp_clip": alert.get("timestamp_clip"),
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
    print(f"Seeded alert {alert_doc['alert_id']}: [{alert.get('timestamp_film')}] {alert.get('title')} -> {alert.get('director_action_required')}")

# 3. Seed sample Director chat conversation in chat_history
chat_samples = [
    {
        "role": "director",
        "message": "Shadow, why did you flag the board on the upper right door frame at 37:08?",
        "timestamp": firestore.SERVER_TIMESTAMP
    },
    {
        "role": "assistant",
        "message": "CRITICAL ALERT (Confidence: 100%): At 37:08 (film time), handwritten crew lettering reading 'UPPER RIGHT CORNER' is plainly visible in grease pencil across the center-right face of the wood plank before Ben hammers it into place. This is an overt fourth-wall production break that requires a RETAKE.",
        "timestamp": firestore.SERVER_TIMESTAMP
    },
    {
        "role": "director",
        "message": "Did the filmed performance match the screenplay for the opening table action?",
        "timestamp": firestore.SERVER_TIMESTAMP
    },
    {
        "role": "assistant",
        "message": "SCRIPT DEVIATION at 25:00: Scene 12 called for Ben to use a tire iron and hammer to dismantle the oak table. In the filmed performance, Duane Jones wrenches the turned legs off using bare hands and leverage. Recommendation: ACCEPT RISK. The physical performance reads with intense urgency on camera.",
        "timestamp": firestore.SERVER_TIMESTAMP
    }
]

for msg in chat_samples:
    db.collection("chat_history").add(msg)

print("Seeded sample chat history.")
print("\nDemo data seeding completed successfully with script-grounded metrics!")
