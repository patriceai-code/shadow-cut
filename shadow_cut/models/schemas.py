"""
Shadow Cut — Pydantic v2 strict schemas.
Zero Dict[str, Any]. All tool I/O is fully typed.
"""
from __future__ import annotations

from typing import Annotated, Literal
from pydantic import BaseModel, Field, field_validator, model_validator

# ---------------------------------------------------------------------------
# Shared enumerations
# ---------------------------------------------------------------------------

PlotWeightLiteral = Literal["CRITICAL", "IMPORTANT", "INCIDENTAL"]
AlertActionLiteral = Literal["ALERT", "SILENT_LOG", "SUPPRESS", "ESCALATE"]


# ---------------------------------------------------------------------------
# TOOL 1 — parse_script  (output: PlotKnowledgeGraph)
# ---------------------------------------------------------------------------

class PropRule(BaseModel):
    """A single continuity rule for a prop, written in imperative form."""

    rule: str = Field(..., min_length=5, max_length=500)


class PropDefinition(BaseModel):
    """A physical object extracted from a film script."""

    canonical_name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1, max_length=1000)
    plot_weight: PlotWeightLiteral
    first_appears_scene: int = Field(..., ge=1)
    last_appears_scene: int | None = Field(default=None, ge=1)
    payoff_scene: int | None = Field(default=None, ge=1)
    setup_scene: int | None = Field(default=None, ge=1)
    is_character_signature: bool = False
    is_macguffin: bool = False
    state_vocabulary: list[str] = Field(default_factory=list)
    default_state: str = Field(default="unknown", max_length=100)
    continuity_rules: list[str] = Field(default_factory=list)


class ScenePropRef(BaseModel):
    """Prop reference within a scene."""

    prop_name: str = Field(..., min_length=1)
    scene_state: str = Field(..., min_length=1)
    rules: list[str] = Field(default_factory=list)
    alert_on_change: bool = True


class EmotionalBeat(BaseModel):
    """Emotional arc entry for a single character in a scene."""

    character: str = Field(..., min_length=1)
    emotion_start: str = Field(..., min_length=1, max_length=100)
    emotion_end: str = Field(..., min_length=1, max_length=100)
    intensity: Annotated[float, Field(ge=0.0, le=1.0)]


class SceneDefinition(BaseModel):
    """One scene extracted from the script."""

    number: int = Field(..., ge=1)
    title: str = Field(..., min_length=1, max_length=300)
    setting: str = Field(default="", max_length=300)
    characters_present: list[str] = Field(default_factory=list)
    plot_weight: PlotWeightLiteral
    critical_props: list[ScenePropRef] = Field(default_factory=list)
    important_props: list[ScenePropRef] = Field(default_factory=list)
    incidental_props: list[ScenePropRef] = Field(default_factory=list)
    emotional_beats: list[EmotionalBeat] = Field(default_factory=list)
    emotional_tone: str = Field(default="", max_length=500)
    lighting_notes: str = Field(default="", max_length=500)
    setups_introduced: list[str] = Field(default_factory=list)
    payoffs_delivered: list[str] = Field(default_factory=list)
    continuity_rules: list[str] = Field(default_factory=list)
    notes_for_shadow: str = Field(default="", max_length=1000)


class SetupPayoffLink(BaseModel):
    """Explicit Chekhov's Gun link between setup and payoff scene."""

    description: str = Field(..., min_length=5, max_length=500)
    setup_scene: int = Field(..., ge=1)
    payoff_scene: int = Field(..., ge=1)
    prop_involved: str | None = Field(default=None)
    status: Literal["open", "resolved", "abandoned"] = "open"


class PlotKnowledgeGraph(BaseModel):
    """
    Full structured representation of a film script.
    Output of TOOL 1 (parse_script).
    """

    production_title: str = Field(default="Untitled", max_length=200)
    total_scenes: int = Field(..., ge=1)
    scenes: list[SceneDefinition] = Field(..., min_length=1)
    props: list[PropDefinition] = Field(default_factory=list)
    emotional_arcs: list[EmotionalBeat] = Field(default_factory=list)
    setups: list[SetupPayoffLink] = Field(default_factory=list)
    extraction_warnings: list[str] = Field(default_factory=list)

    @field_validator("scenes")
    @classmethod
    def scenes_not_empty(cls, v: list[SceneDefinition]) -> list[SceneDefinition]:
        if len(v) == 0:
            raise ValueError("scenes list must not be empty")
        return v


# ---------------------------------------------------------------------------
# TOOL 2 — analyze_take  (input / output helpers + FlashLiteResult)
# ---------------------------------------------------------------------------

class BoundingBox(BaseModel):
    x1: int = Field(..., ge=0)
    y1: int = Field(..., ge=0)
    x2: int = Field(..., ge=0)
    y2: int = Field(..., ge=0)

    @model_validator(mode="after")
    def bbox_valid(self) -> BoundingBox:
        if self.x2 <= self.x1:
            raise ValueError("x2 must be > x1")
        if self.y2 <= self.y1:
            raise ValueError("y2 must be > y1")
        return self


class AnomalyVerdict(BaseModel):
    anomaly_index: int = Field(..., ge=0)
    verdict: Literal["real_issue", "false_alarm", "uncertain"]
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    severity: Literal["critical", "warning", "info"]
    explanation: str = Field(..., min_length=1, max_length=1000)


class PerformanceNote(BaseModel):
    character: str = Field(..., min_length=1)
    note: str = Field(..., min_length=1, max_length=500)
    matches_required_tone: bool


class MissedIssue(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)
    severity: Literal["critical", "warning", "info"]
    prop_involved: str | None = Field(default=None)


class AnomalyFlag(BaseModel):
    """Single YOLO-detected anomaly passed from vision pipeline."""

    anomaly_type: Literal[
        "prop_position_change",
        "prop_state_change",
        "prop_missing",
        "prop_appeared",
        "actor_position_shift",
        "lighting_change",
        "unknown",
    ]
    prop: str | None = Field(default=None)
    frame: int = Field(..., ge=1)
    timestamp: Annotated[float, Field(ge=0.0)]
    severity: Literal["critical", "high", "medium", "low", "info"]
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    description: str = Field(default="", max_length=500)


class YoloMath(BaseModel):
    """Structured YOLO output — replaces Dict[str, Any]."""

    take_id: str = Field(..., pattern=r"^s[0-9]+_sh[0-9]+_t[0-9]+$")
    scene: int = Field(..., ge=1)
    shot: int = Field(..., ge=1)
    take: int = Field(..., ge=1)
    duration_seconds: Annotated[float, Field(gt=0.0)]
    frames_analyzed: int = Field(..., ge=1)
    fps: int = Field(default=30, ge=1)
    anomaly_flags: list[AnomalyFlag] = Field(default_factory=list)
    tracked_objects: list[str] = Field(default_factory=list)


class PropReference(BaseModel):
    name: str = Field(..., min_length=1)
    importance: PlotWeightLiteral
    rules: list[str] = Field(default_factory=list)
    first_scene: int = Field(default=1, ge=1)
    last_scene: int | None = Field(default=None, ge=1)
    payoff_scene: int | None = Field(default=None, ge=1)
    state_requirements: list[str] = Field(default_factory=list)


class SceneContext(BaseModel):
    """Scene metadata passed to analyze_take."""

    scene_number: int = Field(..., ge=1)
    scene_title: str = Field(..., min_length=1, max_length=200)
    characters: list[str] = Field(default_factory=list)
    emotional_tone: str = Field(default="", max_length=500)
    lighting_notes: str = Field(default="", max_length=500)
    critical_props: list[PropReference] = Field(default_factory=list)
    important_props: list[PropReference] = Field(default_factory=list)
    setups: list[str] = Field(default_factory=list)
    payoffs: list[str] = Field(default_factory=list)


class FlashLiteResult(BaseModel):
    """
    Structured output of Gemini Flash-Lite validation.
    Output of TOOL 2 (analyze_take).
    """

    take_id: str = Field(..., pattern=r"^s[0-9]+_sh[0-9]+_t[0-9]+$")
    verdicts: list[AnomalyVerdict] = Field(default_factory=list)
    missed_issues: list[MissedIssue] = Field(default_factory=list)
    performance_notes: list[PerformanceNote] = Field(default_factory=list)
    audio_transcript: str = Field(default="", max_length=5000)
    needs_escalation: bool = False
    escalation_reason: str | None = Field(default=None, max_length=500)
    processing_time_ms: int = Field(default=0, ge=0)
    tokens_used: int = Field(default=0, ge=0)
    cost_usd: Annotated[float, Field(default=0.0, ge=0.0)]


# ---------------------------------------------------------------------------
# TOOL 3 — check_continuity  (input: Take; output: ContinuityReport)
# ---------------------------------------------------------------------------

class PropStateSnapshot(BaseModel):
    prop_name: str = Field(..., min_length=1)
    observed_state: str = Field(..., min_length=1)
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    frame: int = Field(default=1, ge=1)
    timestamp: Annotated[float, Field(default=0.0, ge=0.0)]


class Take(BaseModel):
    """Minimal take record for continuity comparison."""

    take_id: str = Field(..., pattern=r"^s[0-9]+_sh[0-9]+_t[0-9]+$")
    scene: int = Field(..., ge=1)
    shot: int = Field(..., ge=1)
    take_number: int = Field(..., ge=1)
    prop_states: list[PropStateSnapshot] = Field(default_factory=list)
    emotional_tone: str = Field(default="", max_length=500)
    notes: str = Field(default="", max_length=1000)


class ContinuityMatch(BaseModel):
    prop_name: str
    current_take_id: str
    previous_take_id: str
    state: str
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]


class ContinuityMismatch(BaseModel):
    prop_name: str
    current_state: str
    expected_state: str
    current_take_id: str
    previous_take_id: str
    plot_weight: PlotWeightLiteral
    severity: Literal["critical", "warning", "info"]
    rule_violated: str | None = Field(default=None)


class CrossSceneIssue(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)
    scenes_involved: list[int] = Field(..., min_length=2)
    prop_name: str | None = Field(default=None)
    severity: Literal["critical", "warning", "info"]


class ContinuityReport(BaseModel):
    """
    Output of TOOL 3 (check_continuity).
    """

    current_take_id: str
    matches: list[ContinuityMatch] = Field(default_factory=list)
    mismatches: list[ContinuityMismatch] = Field(default_factory=list)
    cross_scene_issues: list[CrossSceneIssue] = Field(default_factory=list)
    total_props_checked: int = Field(default=0, ge=0)
    issues_found: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def sync_issues_count(self) -> ContinuityReport:
        self.issues_found = len(self.mismatches) + len(self.cross_scene_issues)
        return self


# ---------------------------------------------------------------------------
# TOOL 4 — flag_alert  (input: Anomaly; output: AlertDecision)
# ---------------------------------------------------------------------------

class Anomaly(BaseModel):
    """Anomaly payload for the Decision Matrix."""

    category: str = Field(..., min_length=1, max_length=200)
    prop_name: str | None = Field(default=None)
    scene: int = Field(..., ge=1)
    is_cross_scene: bool = False
    is_novel: bool = False
    evidence_source_count: int = Field(default=1, ge=0)
    description: str = Field(default="", max_length=500)


class AlertDecision(BaseModel):
    """
    Output of TOOL 4 (flag_alert).
    """

    action: AlertActionLiteral
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    plot_weight: PlotWeightLiteral
    reasoning: str = Field(..., min_length=5, max_length=1000)
    should_escalate_to_pro: bool = False
    escalation_reason: str | None = Field(default=None, max_length=500)


# ---------------------------------------------------------------------------
# TOOL 5 — query_memory  (output: MemoryQueryResult)
# ---------------------------------------------------------------------------

class MemoryChunk(BaseModel):
    chunk_id: str = Field(..., min_length=1)
    source_collection: Literal["takes", "alerts", "plot_graph", "reports"]
    scene: int | None = Field(default=None, ge=1)
    take_id: str | None = Field(default=None)
    text: str = Field(..., min_length=1, max_length=2000)
    relevance_score: Annotated[float, Field(ge=0.0, le=1.0)]
    timestamp: str = Field(default="", max_length=50)


class MemoryQueryResult(BaseModel):
    """
    Output of TOOL 5 (query_memory).
    """

    question: str
    chunks: list[MemoryChunk] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    total_found: int = Field(default=0, ge=0)
    scene_filter_applied: int | None = Field(default=None)

    @model_validator(mode="after")
    def sync_total(self) -> MemoryQueryResult:
        self.total_found = len(self.chunks)
        return self


# ---------------------------------------------------------------------------
# TOOL 6 — generate_report  (output: DailyReport)
# ---------------------------------------------------------------------------

class TakeAccuracyRow(BaseModel):
    scene: int = Field(..., ge=1)
    takes_analyzed: int = Field(..., ge=0)
    alerts_generated: int = Field(..., ge=0)
    confirmed_alerts: int = Field(..., ge=0)
    false_positives: int = Field(..., ge=0)
    accuracy: Annotated[float, Field(ge=0.0, le=1.0)]


class CostBreakdown(BaseModel):
    flash_lite_calls: int = Field(default=0, ge=0)
    pro_escalations: int = Field(default=0, ge=0)
    flash_lite_cost_usd: Annotated[float, Field(default=0.0, ge=0.0)]
    pro_cost_usd: Annotated[float, Field(default=0.0, ge=0.0)]
    total_cost_usd: Annotated[float, Field(default=0.0, ge=0.0)]


class DailyReport(BaseModel):
    """
    Output of TOOL 6 (generate_report).
    """

    production_id: str = Field(..., min_length=1)
    date_from: str = Field(..., min_length=8, max_length=20)
    date_to: str = Field(..., min_length=8, max_length=20)
    takes_analyzed: int = Field(..., ge=0)
    alerts_generated: int = Field(..., ge=0)
    confirmed_alerts: int = Field(..., ge=0)
    false_positives: int = Field(..., ge=0)
    accuracy: Annotated[float, Field(ge=0.0, le=1.0)]
    cost: CostBreakdown
    savings_estimate_usd: Annotated[float, Field(default=0.0, ge=0.0)]
    scene_breakdown: list[TakeAccuracyRow] = Field(default_factory=list)
    top_alert_categories: list[str] = Field(default_factory=list)
    notes: str = Field(default="", max_length=2000)

    @field_validator("accuracy", mode="before")
    @classmethod
    def clamp_accuracy(cls, v: float) -> float:
        return max(0.0, min(1.0, float(v)))
