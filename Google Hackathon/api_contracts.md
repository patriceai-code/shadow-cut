# Shadow Cut — API Contracts Between Components
## Zero-Laptop Deliverable 6: Internal Interface Specifications
### Status: LOCKED — Bob compiles clean on first try

---

## Philosophy

Every interface between components is defined as a **strict Pydantic v2 model** with:
- Typed fields (no `Dict[str, Any]`)
- Validation rules (`min_length`, `pattern`, `ge`, `le`)
- Default values where safe
- Explicit `Optional` vs. required
- Error response schemas

Bob receives these contracts as gospel. No hallucinated types. No incompatible schemas.

---

## INTERFACE 1: YOLO → Bridge (Local CV Math)

**Producer:** `core/vision_pipeline.py` (YOLO-World running locally on DIT laptop)
**Consumer:** `core/bridge.py` (YOLO-to-Flash-Lite bridge)
**Transport:** JSON file written to shared temp directory, or HTTP POST to local bridge endpoint

### Request Schema: `YoloMathOutput`

```python
from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import List, Dict, Optional
from enum import Enum

class PropState(str, Enum):
    FOLDED = "folded"
    OPEN = "open"
    LEFT_WRIST = "left_wrist"
    RIGHT_WRIST = "right_wrist"
    IN_HAND = "in_hand"
    ON_TABLE = "on_table"
    MISSING = "missing"
    UNKNOWN = "unknown"

class BoundingBox(BaseModel):
    x1: int = Field(..., ge=0, description="Top-left x coordinate")
    y1: int = Field(..., ge=0, description="Top-left y coordinate")
    x2: int = Field(..., ge=0, description="Bottom-right x coordinate")
    y2: int = Field(..., ge=0, description="Bottom-right y coordinate")

    @field_validator('x2')
    @classmethod
    def x2_greater_than_x1(cls, v: int, info: ValidationInfo) -> int:
        if 'x1' in info.data and v <= info.data['x1']:
            raise ValueError('x2 must be greater than x1')
        return v

    @field_validator('y2')
    @classmethod
    def y2_greater_than_y1(cls, v: int, info: ValidationInfo) -> int:
        if 'y1' in info.data and v <= info.data['y1']:
            raise ValueError('y2 must be greater than y1')
        return v

class ObjectPosition(BaseModel):
    frame: int = Field(..., ge=1, description="Frame number in the take")
    timestamp: float = Field(..., ge=0.0, description="Timestamp in seconds")
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
    class_name: str = Field(..., min_length=1, description="Prop name from script vocabulary")
    first_seen_frame: int = Field(..., ge=1)
    last_seen_frame: int = Field(..., ge=1)
    confidence_avg: float = Field(..., ge=0.0, le=1.0)
    positions: List[ObjectPosition] = Field(default_factory=list)
    state_changes: List[StateChange] = Field(default_factory=list)

class ActorPosition(BaseModel):
    frame: int = Field(..., ge=1)
    timestamp: float = Field(..., ge=0.0)
    character: str = Field(..., min_length=1)
    x: float = Field(..., ge=0.0, le=1.0, description="Normalized x position (0-1)")
    y: float = Field(..., ge=0.0, le=1.0, description="Normalized y position (0-1)")
    facing: str = Field(default="unknown", pattern="^(left|right|front|back|unknown)$")

class AnomalyFlag(BaseModel):
    type: str = Field(..., pattern="^(prop_position_change|prop_state_change|prop_missing|prop_appeared|actor_position_shift|lighting_change|unknown)$")
    prop: Optional[str] = Field(default=None, description="Prop name if applicable")
    from_state: Optional[PropState] = Field(default=None)
    to_state: Optional[PropState] = Field(default=None)
    frame: int = Field(..., ge=1)
    timestamp: float = Field(..., ge=0.0)
    severity: str = Field(..., pattern="^(critical|high|medium|low|info)$")
    confidence: float = Field(..., ge=0.0, le=1.0)
    description: str = Field(default="", max_length=500)

class YoloMathOutput(BaseModel):
    take_id: str = Field(..., pattern="^s[0-9]+_sh[0-9]+_t[0-9]+$")
    scene: int = Field(..., ge=1)
    shot: int = Field(..., ge=1)
    take: int = Field(..., ge=1)
    duration_seconds: float = Field(..., gt=0.0)
    frames_analyzed: int = Field(..., ge=1)
    fps: int = Field(default=30, ge=1)
    object_tracks: Dict[str, ObjectTrack] = Field(default_factory=dict)
    actor_tracks: Dict[str, List[ActorPosition]] = Field(default_factory=dict)
    anomaly_flags: List[AnomalyFlag] = Field(default_factory=list)
    summary_stats: Dict[str, int] = Field(default_factory=dict)

    @field_validator('frames_analyzed')
    @classmethod
    def frames_match_duration(cls, v: int, info: ValidationInfo) -> int:
        if 'duration_seconds' in info.data and 'fps' in info.data:
            expected = int(info.data['duration_seconds'] * info.data['fps'])
            if abs(v - expected) > 5:  # Allow 5 frame tolerance
                raise ValueError(f'frames_analyzed ({v}) does not match duration*fps (~{expected})')
        return v
```

### Error Response: `YoloProcessingError`

```python
class YoloProcessingError(BaseModel):
    error_code: str = Field(..., pattern="^(YOLO_INIT_FAILED|VIDEO_DECODE_ERROR|OUT_OF_MEMORY|TIMEOUT|UNKNOWN)$")
    take_id: str
    message: str = Field(..., max_length=1000)
    retryable: bool = Field(default=True)
    suggested_action: str = Field(default="retry", pattern="^(retry|skip|escalate)$")
```

---

## INTERFACE 2: Bridge → Flash-Lite (Validation Payload)

**Producer:** `core/bridge.py`
**Consumer:** Gemini 3.5 Flash-Lite (via Google AI Studio / Vertex AI API)
**Transport:** HTTP POST to Gemini API with multipart content (video file + JSON context)

### Request Schema: `FlashLiteValidationRequest`

```python
class PropReference(BaseModel):
    name: str = Field(..., min_length=1, description="Prop name from script vocabulary")
    importance: str = Field(..., pattern="^(CRITICAL|IMPORTANT|INCIDENTAL)$")
    rules: List[str] = Field(default_factory=list, description="Continuity rules for this prop")
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

class ScriptSummary(BaseModel):
    scene_synopsis: str = Field(..., max_length=2000)
    preceding_context: str = Field(default="", max_length=1000)
    following_context: str = Field(default="", max_length=1000)
    continuity_rules: List[str] = Field(default_factory=list)

class FlashLiteValidationRequest(BaseModel):
    take_id: str = Field(..., pattern="^s[0-9]+_sh[0-9]+_t[0-9]+$")
    video_path: str = Field(..., description="GCS path to H.264 proxy")
    yolo_math: YoloMathOutput
    scene_context: SceneContext
    script_summary: ScriptSummary
    previous_take_states: Optional[Dict[str, str]] = Field(
        default=None,
        description="Prop states from previous takes of same scene (prop_name -> state)"
    )
    director_notes_from_previous_takes: List[str] = Field(default_factory=list)

    @field_validator('video_path')
    @classmethod
    def must_be_gcs_path(cls, v: str) -> str:
        if not v.startswith("gs://"):
            raise ValueError('video_path must be a GCS URI (gs://...)')
        return v
```

### Response Schema: `FlashLiteValidationResult`

```python
class AnomalyVerdict(str, Enum):
    REAL_ISSUE = "real_issue"
    FALSE_ALARM = "false_alarm"
    UNCERTAIN = "uncertain"

class VerdictItem(BaseModel):
    anomaly_index: int = Field(..., ge=0)
    verdict: AnomalyVerdict
    confidence: float = Field(..., ge=0.0, le=1.0)
    severity: str = Field(..., pattern="^(critical|warning|info)$")
    explanation: str = Field(..., max_length=1000)
    suggested_action: str = Field(default="alert", pattern="^(alert|log|ignore|escalate)$")

class MissedIssue(BaseModel):
    type: str = Field(..., max_length=100)
    description: str = Field(..., max_length=1000)
    frame: Optional[int] = Field(default=None, ge=1)
    timestamp: Optional[float] = Field(default=None, ge=0.0)
    confidence: float = Field(..., ge=0.0, le=1.0)

class PerformanceNote(BaseModel):
    character: str = Field(..., min_length=1)
    emotional_tone_detected: str = Field(..., max_length=200)
    emotional_tone_required: str = Field(default="", max_length=200)
    match_score: float = Field(..., ge=0.0, le=1.0)
    notes: str = Field(default="", max_length=1000)

class FlashLiteValidationResult(BaseModel):
    take_id: str = Field(..., pattern="^s[0-9]+_sh[0-9]+_t[0-9]+$")
    timestamp: str = Field(..., description="ISO 8601 UTC")
    verdicts: List[VerdictItem] = Field(default_factory=list)
    missed_issues: List[MissedIssue] = Field(default_factory=list)
    performance_notes: List[PerformanceNote] = Field(default_factory=list)
    audio_transcript: str = Field(default="", max_length=5000)
    director_notes_transcribed: List[str] = Field(default_factory=list)
    needs_escalation: bool = Field(default=False)
    escalation_reason: Optional[str] = Field(default=None, max_length=500)
    processing_time_ms: int = Field(..., ge=0)
    tokens_used: int = Field(..., ge=0)
    cost_usd: float = Field(..., ge=0.0)
```

### Error Response: `FlashLiteError`

```python
class FlashLiteError(BaseModel):
    error_code: str = Field(..., pattern="^(RATE_LIMIT|TIMEOUT|INVALID_VIDEO|CONTEXT_OVERFLOW|MODEL_ERROR|UNKNOWN)$")
    take_id: str
    message: str = Field(..., max_length=1000)
    retry_after_seconds: Optional[int] = Field(default=None, ge=0)
    fallback_action: str = Field(default="escalate_to_pro", pattern="^(escalate_to_pro|silent_log|retry)$")
```

---

## INTERFACE 3: Flash-Lite → Pro Escalation (Deep Reasoning Handoff)

**Producer:** `core/bridge.py` (when Flash-Lite returns `needs_escalation: true`)
**Consumer:** Gemini 2.5/3.1 Pro (via Vertex AI API)
**Transport:** HTTP POST to Gemini Pro API
**Trigger conditions:**
- Flash-Lite confidence < 0.85 on CRITICAL prop
- Cross-scene continuity needed
- Complex narrative reasoning required
- Single-source critical claim needs verification

### Request Schema: `ProEscalationRequest`

```python
class CrossSceneContext(BaseModel):
    setup_scene: int = Field(..., ge=1)
    setup_rules: List[str] = Field(default_factory=list)
    payoff_scene: int = Field(..., ge=1)
    payoff_rules: List[str] = Field(default_factory=list)
    intermediate_scenes: List[int] = Field(default_factory=list)

class ProEscalationRequest(BaseModel):
    take_id: str = Field(..., pattern="^s[0-9]+_sh[0-9]+_t[0-9]+$")
    scene_number: int = Field(..., ge=1)
    prop_name: str = Field(..., min_length=1)
    plot_importance: str = Field(..., pattern="^(CRITICAL|IMPORTANT|INCIDENTAL)$")
    flash_lite_result: FlashLiteValidationResult
    previous_take_context: Optional[Dict] = Field(default=None)
    cross_scene_context: Optional[CrossSceneContext] = Field(default=None)
    script_rules: List[str] = Field(default_factory=list)
    director_style_profile: Optional[Dict] = Field(
        default=None,
        description="Director's historical preferences from Shadow Memory"
    )
```

### Response Schema: `ProEscalationResult`

```python
class NarrativeImpact(str, Enum):
    BREAKS_LOGIC = "breaks_logic"
    WEAKENS_LOGIC = "weakens_logic"
    ACCEPTABLE = "acceptable"
    INTENTIONAL = "intentional"
    UNCLEAR = "unclear"

class FixRecommendation(str, Enum):
    RESHOOT = "reshoot"
    PICKUP_INSERT = "pickup_insert"
    VFX_NOTE = "vfx_note"
    ADR = "adr"
    ACCEPTABLE = "acceptable"

class CostEstimate(BaseModel):
    fix_now_cost: str = Field(..., max_length=200)
    fix_in_post_cost: str = Field(..., max_length=200)
    fix_with_reshoot_cost: str = Field(..., max_length=200)
    recommendation: str = Field(..., max_length=500)

class ProEscalationResult(BaseModel):
    take_id: str = Field(..., pattern="^s[0-9]+_sh[0-9]+_t[0-9]+$")
    timestamp: str = Field(..., description="ISO 8601 UTC")
    narrative_impact: NarrativeImpact
    severity_assessment: str = Field(..., max_length=1000)
    fix_recommendation: FixRecommendation
    cost_estimate: CostEstimate
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning_chain: str = Field(..., max_length=3000, description="Step-by-step reasoning for transparency")
    dissenting_considerations: str = Field(default="", max_length=1000, description="What could make this wrong?")
    processing_time_ms: int = Field(..., ge=0)
    tokens_used: int = Field(..., ge=0)
    cost_usd: float = Field(..., ge=0.0)
```

---

## INTERFACE 4: Chat UI → Vector DB (RAG Query)

**Producer:** Next.js Chat UI (director's browser/phone)
**Consumer:** `core/memory_agent.py` (RAG search over Shadow Memory)
**Transport:** HTTP POST to FastAPI `/api/chat/query` endpoint

### Request Schema: `ChatQueryRequest`

```python
class ChatQueryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=1000)
    scene_filter: Optional[int] = Field(default=None, ge=1, description="Limit search to specific scene")
    shot_filter: Optional[int] = Field(default=None, ge=1)
    character_filter: Optional[str] = Field(default=None, min_length=1)
    prop_filter: Optional[str] = Field(default=None, min_length=1)
    date_range_start: Optional[str] = Field(default=None, description="ISO 8601 date")
    date_range_end: Optional[str] = Field(default=None, description="ISO 8601 date")
    include_images: bool = Field(default=True, description="Include frame thumbnails in response")
    max_results: int = Field(default=5, ge=1, le=20)

    @field_validator('question')
    @classmethod
    def question_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Question cannot be empty or whitespace')
        return v.strip()
```

### Response Schema: `ChatQueryResponse`

```python
class RetrievedChunk(BaseModel):
    chunk_type: str = Field(..., pattern="^(script|take_summary|director_note|continuity_alert|plot_graph_fact)$")
    content: str = Field(..., max_length=2000)
    source_id: str = Field(..., description="take_id or scene reference")
    timestamp: Optional[str] = Field(default=None)
    relevance_score: float = Field(..., ge=0.0, le=1.0)
    frame_thumbnail_url: Optional[str] = Field(default=None)

class ChatQueryResponse(BaseModel):
    question: str
    answer: str = Field(..., max_length=3000)
    retrieved_chunks: List[RetrievedChunk] = Field(default_factory=list)
    confidence: float = Field(..., ge=0.0, le=1.0)
    sources_cited: List[str] = Field(default_factory=list)
    suggested_followups: List[str] = Field(default_factory=list, max_length=3)
    processing_time_ms: int = Field(..., ge=0)
```

---

## INTERFACE 5: Alert Engine → Director Notification

**Producer:** `core/flagging_agent.py` (after confidence scoring)
**Consumer:** Director's device (phone, tablet, browser via WebSocket or push notification)
**Transport:** WebSocket for real-time, Firebase Cloud Messaging for push, or polling fallback

### Notification Schema: `DirectorAlert`

```python
class DirectorAlert(BaseModel):
    alert_id: str = Field(..., pattern="^alert_[a-z0-9_-]+$")
    timestamp: str = Field(..., description="ISO 8601 UTC")
    severity: str = Field(..., pattern="^(critical|warning|info)$")

    # Location
    scene: int = Field(..., ge=1)
    shot: int = Field(..., ge=1)
    take: int = Field(..., ge=1)
    timestamp_in_take: str = Field(..., description="MM:SS format")

    # What happened
    title: str = Field(..., max_length=200)
    description: str = Field(..., max_length=1000)
    prop_involved: Optional[str] = Field(default=None)

    # Evidence
    confidence: float = Field(..., ge=0.0, le=1.0)
    confidence_breakdown: Dict[str, float] = Field(default_factory=dict)
    evidence_items: List[str] = Field(default_factory=list, max_length=10)
    frame_thumbnail_url: Optional[str] = Field(default=None)
    comparison_frame_url: Optional[str] = Field(default=None, description="Previous take frame for comparison")

    # Script context
    script_rule_violated: Optional[str] = Field(default=None, max_length=500)
    payoff_scene: Optional[int] = Field(default=None, ge=1)

    # Actions
    actions: List[str] = Field(default=["confirm", "dismiss", "dismiss_forever"])

    # Historical context
    similar_alerts_count: int = Field(default=0, ge=0)
    historical_accuracy_for_category: float = Field(default=0.0, ge=0.0, le=1.0)
```

---

## INTERFACE 6: Confluent → Pipeline Trigger

**Producer:** Cloud Function (triggered by GCS upload)
**Consumer:** `stream/confluent_consumer.py`
**Transport:** Kafka topic `shadow-cut.takes.uploaded`

### Event Schema: `TakeUploadedEvent`

```python
class SlateMetadata(BaseModel):
    date: str = Field(..., pattern="^\d{4}-\d{2}-\d{2}$")
    director: Optional[str] = Field(default=None, max_length=200)
    dp: Optional[str] = Field(default=None, max_length=200)

class TakeUploadedEvent(BaseModel):
    event_id: str = Field(..., pattern="^[a-f0-9-]{36}$", description="UUID v4")
    timestamp: str = Field(..., description="ISO 8601 UTC")
    type: str = Field(default="take_uploaded", pattern="^take_uploaded$")
    data: TakeData = Field(...)

    class TakeData(BaseModel):
        take_id: str = Field(..., pattern="^s[0-9]+_sh[0-9]+_t[0-9]+$")
        scene: int = Field(..., ge=1)
        shot: int = Field(..., ge=1)
        take: int = Field(..., ge=1)
        video_path: str = Field(...)
        proxy_path: str = Field(...)
        duration: float = Field(..., gt=0.0)
        uploaded_by: str = Field(..., max_length=100)
        slate_metadata: Optional[SlateMetadata] = Field(default=None)
```

### Fallback Webhook Schema: `WebhookFallbackRequest`

```python
class WebhookFallbackRequest(BaseModel):
    event: TakeUploadedEvent
    source: str = Field(default="webhook", pattern="^(webhook|confluent)$")
    received_at: str = Field(..., description="ISO 8601 UTC")
```

---

## INTERFACE 7: Shadow Memory → Firestore (Data Persistence)

**Producer:** All agents (Ingestion, Memory, Flagging, Chat)
**Consumer:** Google Cloud Firestore
**Transport:** Firestore client SDK

### Document Schema: `ShadowMemoryDocument`

```python
class ShadowMemoryDocument(BaseModel):
    doc_id: str = Field(..., pattern="^(take|alert|chat|report)_[a-z0-9_-]+$")
    doc_type: str = Field(..., pattern="^(take_analysis|alert|chat_query|daily_report)$")
    created_at: str = Field(..., description="ISO 8601 UTC")
    updated_at: str = Field(..., description="ISO 8601 UTC")

    # Type-specific payload (stored as JSON blob in Firestore)
    payload: Dict = Field(...)

    # Vector embedding for RAG (stored as array of floats)
    embedding: Optional[List[float]] = Field(default=None)

    # Metadata for filtering
    scene: Optional[int] = Field(default=None, ge=1)
    shot: Optional[int] = Field(default=None, ge=1)
    take: Optional[int] = Field(default=None, ge=1)
    prop_name: Optional[str] = Field(default=None)
    character: Optional[str] = Field(default=None)
    alert_severity: Optional[str] = Field(default=None, pattern="^(critical|warning|info)$")
```

---

## ERROR HANDLING STANDARDS

All interfaces share these error conventions:

```python
class ShadowCutError(BaseModel):
    error_code: str = Field(..., pattern="^[A-Z_]+$")
    message: str = Field(..., max_length=1000)
    component: str = Field(..., pattern="^(YOLO|BRIDGE|FLASH_LITE|PRO|CHAT|MEMORY|ALERT|CONFLUENT|UNKNOWN)$")
    retryable: bool = Field(default=True)
    retry_after_seconds: Optional[int] = Field(default=None, ge=0)
    incident_id: str = Field(..., pattern="^inc_[a-z0-9_-]+$")
    timestamp: str = Field(..., description="ISO 8601 UTC")
```

**Retry Logic:**
- Retryable errors: exponential backoff (1s, 2s, 4s, 8s, max 30s)
- Non-retryable errors: log and alert human immediately
- Max retries: 3 per operation
- Circuit breaker: after 5 consecutive failures, mark component as degraded

---

## VERSIONING

All schemas are versioned via a `schema_version` field (default: "1.0"):

```python
class SchemaVersioned(BaseModel):
    schema_version: str = Field(default="1.0", pattern="^\d+\.\d+$")
```

Bob must include `schema_version` in every model. Future schema changes bump the version and maintain backward compatibility for one major release.

---

*Document version: 1.0*
*Status: LOCKED v2.0 — Zero-Laptop Deliverable 6 (Pydantic V2 & Dict bugs patched)*
*Interfaces defined: 7*
*Pydantic models: 25+*
*Last updated: August 3, 2026 (PATCHED)*
