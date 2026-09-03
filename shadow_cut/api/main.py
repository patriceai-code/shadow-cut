"""
FastAPI backend for Shadow Cut.
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os
import tempfile
from pathlib import Path

from shadow_cut.config.settings import get_settings
from shadow_cut.core.plot_graph import PlotGraphBuilder
from shadow_cut.core.vision_pipeline import VisionPipeline
from shadow_cut.core.bridge import FlashLiteBridge
from shadow_cut.core.confidence import ConfidenceEngine, Anomaly, PlotWeight
from shadow_cut.stream.confluent_consumer import ShadowConsumer, register_webhook

settings = get_settings()

pipeline_state = {
    "plot_graph": None,
    "vision": None,
    "bridge": None,
    "confidence": None,
    "consumer": None
}

async def process_take(data: dict):
    print(f"Processing take: {data.get('take_id')}")

    if pipeline_state["vision"]:
        yolo_result = pipeline_state["vision"].process_video(data["video_path"])
    else:
        yolo_result = {"take_id": data["take_id"], "object_tracks": {}, "anomaly_flags": []}

    yolo_result["take_id"] = data["take_id"]
    yolo_result["scene"] = data["scene"]
    yolo_result["shot"] = data["shot"]
    yolo_result["take"] = data["take"]

    scene_context = {"scene_number": data["scene"], "scene_title": "Test", "characters": [], "critical_props": []}
    if pipeline_state["plot_graph"]:
        scene_ctx = pipeline_state["plot_graph"].get("scenes", {}).get(str(data["scene"]), {})
        scene_context = {
            "scene_number": data["scene"],
            "scene_title": scene_ctx.get("title", "Unknown"),
            "characters": scene_ctx.get("characters_present", []),
            "critical_props": scene_ctx.get("critical_props", [])
        }

    flash_result = {}
    if pipeline_state["bridge"]:
        flash_result = pipeline_state["bridge"].validate_take(
            data["video_path"], yolo_result, scene_context, ""
        )

    for verdict in flash_result.get("verdicts", []):
        anomaly = Anomaly(
            category=verdict.get("type", "unknown"),
            prop_name=verdict.get("prop"),
            scene=data["scene"]
        )
        if pipeline_state["confidence"]:
            conf = pipeline_state["confidence"].calculate_technical_confidence(anomaly)
            action = pipeline_state["confidence"].decide_action(
                anomaly, conf, PlotWeight.CRITICAL if verdict.get("severity") == "critical" else PlotWeight.IMPORTANT
            )
            print(f"Alert: {verdict} -> Confidence: {conf:.2f} -> Action: {action}")

    print(f"Completed take: {data.get('take_id')}")

@asynccontextmanager
async def lifespan(app: FastAPI):
    pipeline_state["vision"] = VisionPipeline(device=settings.yolo_device)
    pipeline_state["bridge"] = FlashLiteBridge(api_key=settings.gemini_api_key)
    pipeline_state["confidence"] = ConfidenceEngine(pro_budget=settings.pro_escalation_budget)

    if not settings.use_confluent_fallback and settings.confluent_bootstrap_servers:
        try:
            consumer = ShadowConsumer(
                settings.confluent_bootstrap_servers,
                settings.confluent_api_key,
                settings.confluent_api_secret,
                settings.confluent_topic
            )
            import threading
            t = threading.Thread(target=consumer.start, args=(process_take,), daemon=True)
            t.start()
            pipeline_state["consumer"] = consumer
        except Exception as e:
            print(f"Confluent consumer init failed: {e}")

    yield

    if pipeline_state["consumer"]:
        pipeline_state["consumer"].stop()

app = FastAPI(title="Shadow Cut", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_webhook(app, process_take)

@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

@app.post("/api/takes/upload")
async def upload_take(
    video: UploadFile = File(...),
    scene: int = Form(...),
    shot: int = Form(...),
    take: int = Form(...)
):
    take_id = f"s{scene}_sh{shot}_t{take}"
    tmp_dir = Path(tempfile.gettempdir()) / "shadow_cut"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    video_path = str(tmp_dir / f"{take_id}.mp4")

    with open(video_path, "wb") as f:
        f.write(await video.read())

    await process_take({
        "take_id": take_id,
        "scene": scene,
        "shot": shot,
        "take": take,
        "video_path": video_path,
        "duration": 0
    })

    return {"take_id": take_id, "status": "processing"}

@app.get("/api/alerts/latest")
async def get_latest_alerts():
    return {"alerts": []}

@app.post("/api/chat/query")
async def chat_query(question: str):
    return {"answer": "Chat query received", "question": question}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
