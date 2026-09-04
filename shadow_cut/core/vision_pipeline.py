"""
YOLO-World vision pipeline.
Detects props from script vocabulary on every frame.
"""
import cv2
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional
import json

class VisionPipeline:
    def __init__(self, model_path: str = "yolov8s-world.pt", device: str = "cpu"):
        try:
            from ultralytics import YOLO
            self.model = YOLO(model_path)
            self.model.to(device)
            self.device = device
            self.available = True
        except Exception as e:
            print(f"YOLO init failed: {e}")
            self.available = False

    def set_classes(self, class_names: List[str]):
        if self.available:
            try:
                self.model.set_classes(class_names)
            except Exception as e:
                print(f"Failed to set classes: {e}")

    def process_video(self, video_path: str, sample_fps: int = 1) -> dict:
        if not self.available:
            return self._fallback_process(video_path)

        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        frame_interval = int(fps / sample_fps) if fps >= sample_fps else 1

        object_tracks = {}
        anomaly_flags = []
        frame_idx = 0
        processed_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % frame_interval == 0:
                results = self.model(frame, verbose=False)
                processed_count += 1

                for r in results:
                    for box in r.boxes:
                        cls_name = self.model.names[int(box.cls)]
                        conf = float(box.conf)
                        x1, y1, x2, y2 = map(int, box.xyxy[0])

                        if cls_name not in object_tracks:
                            object_tracks[cls_name] = {
                                "class": cls_name,
                                "first_seen_frame": frame_idx,
                                "last_seen_frame": frame_idx,
                                "confidence_avg": conf,
                                "positions": [],
                                "state_changes": []
                            }

                        track = object_tracks[cls_name]
                        track["last_seen_frame"] = frame_idx
                        track["confidence_avg"] = (track["confidence_avg"] * len(track["positions"]) + conf) / (len(track["positions"]) + 1)
                        track["positions"].append({
                            "frame": frame_idx,
                            "timestamp": frame_idx / fps if fps > 0 else 0.0,
                            "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                            "state": "unknown",
                            "confidence": conf
                        })

            frame_idx += 1

        cap.release()

        for cls_name, track in object_tracks.items():
            if len(track["positions"]) >= 2:
                first = track["positions"][0]
                last = track["positions"][-1]
                dx = abs(last["bbox"]["x1"] - first["bbox"]["x1"])
                dy = abs(last["bbox"]["y1"] - first["bbox"]["y1"])
                if dx > 50 or dy > 50:
                    anomaly_flags.append({
                        "type": "prop_position_change",
                        "prop": cls_name,
                        "frame": last["frame"],
                        "timestamp": last["timestamp"],
                        "severity": "medium",
                        "confidence": last["confidence"],
                        "description": f"{cls_name} moved significantly between frames"
                    })

        return {
            "take_id": Path(video_path).stem,
            "scene": 1,
            "shot": 1,
            "take": 1,
            "duration_seconds": duration,
            "frames_analyzed": processed_count,
            "fps": sample_fps,
            "object_tracks": object_tracks,
            "anomaly_flags": anomaly_flags
        }

    def _fallback_process(self, video_path: str) -> dict:
        return {
            "take_id": Path(video_path).stem,
            "scene": 1, "shot": 1, "take": 1,
            "duration_seconds": 0,
            "frames_analyzed": 0,
            "fps": 1,
            "object_tracks": {},
            "anomaly_flags": []
        }
