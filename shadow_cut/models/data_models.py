# models/data_models.py
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import List, Dict, Optional, Literal
from enum import Enum
from datetime import datetime

class PropState(str, Enum):
    FOLDED = "folded"
    OPEN = "open"
    LEFT_WRIST = "left_wrist"
    RIGHT_WRIST = "right_wrist"
    IN_HAND = "in_hand"
    ON_TABLE = "on_table"
    MISSING = "missing"
    UNKNOWN = "unknown"

class PlotWeight(str, Enum):
    CRITICAL = "CRITICAL"
    IMPORTANT = "IMPORTANT"
    INCIDENTAL = "INCIDENTAL"

class Severity(str, Enum):
    CRITICAL = "critical"
    WARNING = "warning"
    INFO = "info"

class BoundingBox(BaseModel):
    x1: int = Field(..., ge=0)
    y1: int = Field(..., ge=0)
    x2: int = Field(..., ge=0)
    y2: int = Field(..., ge=0)

    @field_validator("x2")
    @classmethod
    def x2_greater(cls, v: int, info: ValidationInfo) -> int:
        if "x1" in info.data and v <= info.data["x1"]:
            raise ValueError("x2 must be > x1")
        return v

    @field_validator("y2")
    @classmethod
    def y2_greater(cls, v: int, info: ValidationInfo) -> int:
        if "y1" in info.data and v <= info.data["y1"]:
            raise ValueError("y2 must be > y1")
        return v

class ObjectPosition(BaseModel):
    frame: int = Field(..., ge=1)
    timestamp: float = Field(..., ge=0.0)
    bbox: BoundingBox
    state: PropState = Field(default=PropState.UNKNOWN)
    confidence: float = Field(..., ge=0.0, le=1.0)

class StateChange(BaseModel):
    from_state: PropState
    to_state: PropState
    frame: int = Field(..., ge=1)
    timestamp: float = Field(..., ge=0.0)
    confidence: float = Field(..., ge=0.0, le=1.0)

class ObjectTrack(BaseModel):
    class_name: str = Field(..., min_length=1)
    first_seen_frame: int = Field(..., ge=1)
    last_seen_frame: int = Field(..., ge=1)
    confidence_avg: float = Field(..., ge=0.0, le=1.0)
    positions: List[ObjectPosition] = Field(default_factory=list)
    state_changes: List[StateChange] = Field(default_factory=list)

class AnomalyFlag(BaseModel):
    type: Literal["prop_position_change", "prop_state_change", "prop_missing",
                   "prop_appeared", "actor_position_shift", "lighting_change", "unknown"]
    prop: Optional[str] = Field(default=None)
    from_state: Optional[PropState] = Field(default=None)
    to_state: Optional[PropState] = Field(default=None)
    frame: int = Field(..., ge=1)
    timestamp: float = Field(..., ge=0.0)
    severity: Literal["critical", "high", "medium", "low", "info"]
    confidence: float = Field(..., ge=0.0, le=1.0)
    description: str = Field(default="", max_length=500)

class YoloMathOutput(BaseModel):
    take_id: str = Field(..., pattern=r"^s[0-9]+_sh[0-9]+_t[0-9]+$")
    scene: int = Field(..., ge=1)
    shot: int = Field(..., ge=1)
    take: int = Field(..., ge=1)
    duration_seconds: float = Field(..., gt=0.0)
    frames_analyzed: int = Field(..., ge=1)
    fps: int = Field(default=30, ge=1)
    object_tracks: Dict[str, ObjectTrack] = Field(default_factory=dict)
    actor_tracks: Dict[str, List[dict]] = Field(default_factory=dict)
    anomaly_flags: List[AnomalyFlag] = Field(default_factory=list)

class PropReference(BaseModel):
    name: str = Field(..., min_length=1)
    importance: Literal["CRITICAL", "IMPORTANT", "INCIDENTAL"]
    rules: List[str] = Field(default_factory=list)
    first_scene: int = Field(default=1, ge=1)
    last_scene: Optional[int] = Field(default=None, ge=1)
    payoff_scene: Optional[int] = Field(default=None, ge=1)
    state_requirements: List[str] = Field(default_factory=list)

class SceneContext(BaseModel):
    scene_number: int = Field(..., ge=1)
    scene_title: str = Field(..., min_length=1, max_length=200)
    characters: List[str] = Field(default_factory=list)
    emotional_tone: str = Field(default="", max_length=500)
    lighting_notes: str = Field(default="", max_length=500)
    critical_props: List[PropReference] = Field(default_factory=list)
    important_props: List[PropReference] = Field(default_factory=list)
    setups: List[str] = Field(default_factory=list)
    payoffs: List[str] = Field(default_factory=list)

class FlashLiteValidationResult(BaseModel):
    take_id: str = Field(..., pattern=r"^s[0-9]+_sh[0-9]+_t[0-9]+$")
    timestamp: str = Field(...)
    verdicts: List[dict] = Field(default_factory=list)
    missed_issues: List[dict] = Field(default_factory=list)
    performance_notes: List[dict] = Field(default_factory=list)
    audio_transcript: str = Field(default="", max_length=5000)
    needs_escalation: bool = Field(default=False)
    escalation_reason: Optional[str] = Field(default=None)
    processing_time_ms: int = Field(..., ge=0)
    tokens_used: int = Field(..., ge=0)
    cost_usd: float = Field(..., ge=0.0)

class DirectorAlert(BaseModel):
    alert_id: str = Field(..., pattern=r"^alert_[a-z0-9_-]+$")
    timestamp: str
    severity: Literal["critical", "warning", "info"]
    scene: int = Field(..., ge=1)
    shot: int = Field(..., ge=1)
    take: int = Field(..., ge=1)
    title: str = Field(..., max_length=200)
    description: str = Field(..., max_length=1000)
    prop_involved: Optional[str] = Field(default=None)
    confidence: float = Field(..., ge=0.0, le=1.0)
    script_rule_violated: Optional[str] = Field(default=None)
    actions: List[str] = Field(default=["confirm", "dismiss", "dismiss_forever"])

class TakeUploadedEvent(BaseModel):
    event_id: str = Field(..., pattern=r"^[a-f0-9-]{36}$")
    timestamp: str
    type: Literal["take_uploaded"] = "take_uploaded"
    data: dict = Field(...)

class Settings(BaseModel):
    """Pydantic-settings for env vars"""
    google_cloud_project: str
    gemini_api_key: str
    firestore_project_id: str
    gcs_bucket: str
    confluent_bootstrap_servers: str
    confluent_api_key: str
    confluent_api_secret: str
    confluent_topic: str = "shadow-cut.takes.uploaded"
    pro_escalation_budget: int = 50
    env: Literal["development", "production"] = "development"
    log_level: str = "INFO"
