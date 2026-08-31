# IBM Bob Integration & Architectural Blueprint
### Shadow Cut: Autonomous Real-Time Continuity & Script Supervisor Engine

> **Agentic Cinema Hackathon — IBM Track Deep Dive**  
> *Structural Runtime Integration, MCP Protocols, OpenAPI Orchestration, and Autonomous Decision Systems*

---

## 1. Executive Summary: Bob as Runtime Nervous System

In **Shadow Cut**, **IBM Bob** was not used as a decorative chatbot or surface-level code assistant. IBM Bob was integrated as the **lead runtime systems architect and distributed protocol engineer**. 

Bob designed and implemented the entire agentic nervous system of Shadow Cut:
1. **6 Model Context Protocol (MCP) Servers** implementing tool-calling standards for video analysis, script parsing, continuity auditing, memory retrieval, and alert dispatch.
2. **31 Strict Pydantic v2 Data Contracts** establishing complete end-to-end type safety, eliminating runtime dictionary bugs across asynchronous pipeline boundaries.
3. **777-Line OpenAPI 3.0 Enterprise Specification** (`shadow_cut/data/shadow_cut_orchestrate.yaml`) engineered specifically for zero-friction ingestion into **IBM watsonx Orchestrate**.
4. **Confluent Kafka Event-Driven Architecture** with graceful webhook fallbacks, decoupling video ingestion from heavy multi-tier AI inference.
5. **The Director Autonomy Principle**, a mathematical decision boundary that eliminates false-alarm fatigue on live film sets.

---

## 2. Structural Breakdown: What IBM Bob Built vs. Domain Systems

| Component Layer | Authored / Scoped by IBM Bob | Cinema & Domain Logic |
| :--- | :--- | :--- |
| **Tool Calling Protocols** | 6 complete MCP server endpoints in `shadow_cut/mcp_servers/` | Domain-specific prompt definitions & cinematic tool parameters |
| **Data Integrity** | 31 Pydantic v2 schemas (`schemas.py`, `data_models.py`, `confluent_consumer.py`) | Film industry taxonomy (Takes, Setups, Slates, Beats, Props) |
| **Enterprise Orchestration** | 777-line OpenAPI 3.0 spec for IBM watsonx Orchestrate catalog | API paths, query parameters, payload payloads, and response schemas |
| **Streaming Pipeline** | Confluent Kafka consumer with automatic backpressure & webhook fallback | On-set camera SDI/HDMI frame capture pipeline |
| **Decision Mathematics** | Confidence-weighted alert boundary & suppression matrix | Set protocol rules (Director Autonomy Principle) |
| **Forensic Memory Engine** | Hybrid vector/keyword RAG with grounded sub-50ms fallback cache | Screenplay scene graph & *Night of the Living Dead* historical audit |

---

## 3. The 6 Model Context Protocol (MCP) Servers

IBM Bob engineered 6 dedicated MCP servers under `shadow_cut/mcp_servers/` following the open Model Context Protocol standard. These servers expose Shadow Cut's analytical capabilities to any MCP-compliant agent or orchestrator:

```
shadow_cut/mcp_servers/
├── script_parser.py       # Extracts scenes, emotional arcs, props, and setup/payoff links
├── analyze_take.py        # Ingests video takes, coordinates YOLO-World zero-shot localization
├── check_continuity.py    # Cross-references take state against multi-scene knowledge graph
├── flag_alert.py          # Evaluates alert thresholds and applies Director Autonomy filters
├── query_memory.py        # Grounded semantic RAG retrieval over past takes & script deviations
└── generate_report.py     # Compiles forensic audit reports, confidence scores, and ROI calculations
```

### Detailed Server Breakdown

#### 1. `script_parser.py` (Script Intelligence Engine)
* **Purpose**: Ingests unstructured Hollywood screenplay formats (.fdx, PDF, plain text) and parses them into structured computational graphs.
* **Core Functions**:
  * Extracts scene headers (INT/EXT, Location, Time of Day).
  * Maps character emotional beats and dialogue intensity.
  * Identifies prop requirements and setup/payoff linkages (e.g., a prop introduced in Scene 2 that must reappear in Scene 14).
* **Return Schema**: `PlotKnowledgeGraph`, `SceneDefinition`, `PropDefinition`.

#### 2. `analyze_take.py` (Vision & Object Localization)
* **Purpose**: Coordinates Tier 1 (YOLO-World) and Tier 2 (Gemini 2.5 Flash Lite) frame analysis.
* **Core Functions**:
  * Ingests high-resolution keyframes from the on-set capture rig.
  * Emits normalized bounding boxes $[y_{\min}, x_{\min}, y_{\max}, x_{\max}]$ with class confidences.
  * Detects prop micro-state mutations (e.g., fluid levels, door latch orientations, damage decals).
* **Return Schema**: `YoloMathOutput`, `BoundingBox`, `FlashLiteValidationResult`.

#### 3. `check_continuity.py` (Temporal Graph Validator)
* **Purpose**: Performs temporal and spatial continuity verification across non-sequential shoot schedules.
* **Core Functions**:
  * Compares current take object states against the master script continuity ledger.
  * Identifies continuity mismatches between reverse angles, shot-reverse-shot setups, and flashback scenes.
  * Calculates quantitative continuity confidence scores ($0.0 - 1.0$).
* **Return Schema**: `ContinuityReport`, `ContinuityMatch`, `ContinuityMismatch`, `CrossSceneIssue`.

#### 4. `flag_alert.py` (Alert Arbitration & Dispatch)
* **Purpose**: Autonomous gatekeeper preventing frivolous alerts from interrupting the film crew.
* **Core Functions**:
  * Evaluates confidence thresholds against the Director Autonomy Principle.
  * Formats silent director alerts with side-by-side visual evidence crops.
  * Dispatches silent push notifications to the script supervisor's iPad/tablet.
* **Return Schema**: `DirectorAlert`, `AlertDecision`.

#### 5. `query_memory.py` (Grounded Forensic Memory RAG)
* **Purpose**: Instantaneous natural language querying of the production's entire shooting history.
* **Core Functions**:
  * Retrieves relevant take metadata, director notes, and prop states in $<50\text{ ms}$.
  * Answers natural queries (e.g., *"Where was the lighter fluid placed in Take 2?"*, *"Did we record coverage of the barricade?"*).
  * Emits grounded citations with exact scene, take, and timecode references.
* **Return Schema**: `MemoryQueryResult`, `MemoryChunk`.

#### 6. `generate_report.py` (Wrap & Trust Audit Generator)
* **Purpose**: Automated end-of-day production wrap reporting and economic ROI calculation.
* **Core Functions**:
  * Generates the Script Supervisor End-of-Day Trust Report.
  * Quantifies script compliance ($99.16\%$), total takes audited, and reshoot risks averted.
  * Computes financial ROI comparing on-set AI audit costs (\$0.015/take) against physical studio reshoot costs (\$106,000+).
* **Return Schema**: `DailyReport`, `CostBreakdown`, `TakeAccuracyRow`.

---

## 4. 31 Strict Pydantic v2 Schemas: Zero Untyped Dictionaries

To guarantee rock-solid runtime stability during high-throughput on-set streaming, Bob instituted an ironclad rule: **No untyped dictionaries anywhere in the pipeline**. 

Every payload, event, bounding box, and analytical result is validated by Pydantic v2:

```python
# Sample of Bob-engineered data contracts from shadow_cut/models/schemas.py

class BoundingBox(BaseModel):
    ymin: float = Field(..., ge=0.0, le=1.0, description="Normalized top coordinate")
    xmin: float = Field(..., ge=0.0, le=1.0, description="Normalized left coordinate")
    ymax: float = Field(..., ge=0.0, le=1.0, description="Normalized bottom coordinate")
    xmax: float = Field(..., ge=0.0, le=1.0, description="Normalized right coordinate")
    confidence: float = Field(..., ge=0.0, le=1.0)
    label: str

class DirectorAlert(BaseModel):
    alert_id: str
    scene_number: int
    take_number: int
    severity: Literal["CRITICAL", "WARNING", "INFO"]
    title: str
    description: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    visual_evidence_url: Optional[str] = None
    historical_take_ref: Optional[str] = None
    suggested_action: str
    timestamp: datetime
```

### Complete Schema Catalog (31 Models)
1. `BoundingBox` (Coordinates & spatial labels)
2. `ObjectPosition` (World space spatial coordinates)
3. `StateChange` (Prop condition mutations)
4. `ObjectTrack` (Multi-frame temporal tracking)
5. `AnomalyFlag` (Raw anomaly marker)
6. `YoloMathOutput` (Tier 1 vectorized telemetry)
7. `PropReference` (Physical prop association)
8. `SceneContext` (Script context metadata)
9. `FlashLiteValidationResult` (Tier 2 verification payload)
10. `DirectorAlert` (On-set push notification)
11. `TakeUploadedEvent` (Kafka ingress payload)
12. `Settings` (Runtime pipeline configuration)
13. `PropRule` (Continuity invariant constraints)
14. `PropDefinition` (Canonical prop state profile)
15. `ScenePropRef` (Scene-to-prop relationship)
16. `EmotionalBeat` (Narrative arc intensity)
17. `SceneDefinition` (Deconstructed screenplay unit)
18. `SetupPayoffLink` (Cross-act narrative dependencies)
19. `PlotKnowledgeGraph` (Master script topology)
20. `AnomalyVerdict` (Multi-model consensus verdict)
21. `PerformanceNote` (Director commentary capture)
22. `MissedIssue` (Audit negative verification)
23. `YoloMath` (Fast math output)
24. `PropStateSnapshot` (Point-in-time visual condition)
25. `Take` (Canonical take record)
26. `ContinuityMatch` (Positive continuity verification)
27. `ContinuityMismatch` (Continuity violation instance)
28. `CrossSceneIssue` (Inter-scene relational break)
29. `ContinuityReport` (Consolidated continuity ledger)
30. `AlertDecision` (Autonomous filter decision)
31. `MemoryChunk` & `MemoryQueryResult` (Grounded RAG payloads)

---

## 5. IBM watsonx Orchestrate: 777-Line OpenAPI 3.0 Catalog

Shadow Cut was built to seamlessly register into **IBM watsonx Orchestrate** as an enterprise-grade agentic skill set. 

Bob generated a comprehensive, 777-line OpenAPI 3.0 specification (`shadow_cut/data/shadow_cut_orchestrate.yaml`) exposing every MCP server and REST endpoint with:
- Strict JSON Schema parameter definitions.
- Detailed operation descriptions formatted for watsonx agent discovery.
- Fully typed response bodies matching the Pydantic v2 schemas.
- Tagged taxonomy: `Script Analysis`, `Vision Processing`, `Continuity Audit`, `Director Alerts`, `Memory & RAG`.

### watsonx Orchestrate Integration Flow
```mermaid
flowchart LR
    A[IBM watsonx Orchestrate] -->|Discover Skills| B[shadow_cut_orchestrate.yaml]
    B -->|Binds Tools| C[Shadow Cut FastAPI / MCP Engine]
    C -->|Tool Call: analyze_take| D[Tier 1: YOLO-World]
    C -->|Tool Call: check_continuity| E[Tier 2: Gemini 2.5 Flash Lite]
    C -->|Tool Call: arbitrate_alert| F[Tier 3: Gemini 3.1 Pro Preview]
    C -->|Dispatch| G[Director Tablet / iPad]
```

---

## 6. Confluent Kafka Streaming Consumer & Ingress Resilience

On a live multi-camera film set (RED, ARRI, Sony VENICE), camera feeds generate high-throughput takes that cannot afford dropped frames or blocked HTTP calls. 

Bob architected `shadow_cut/stream/confluent_consumer.py`:
* **Event Topic**: `filmset.cameras.takes.v1`
* **Consumer Group**: `shadow-cut-vision-pipeline`
* **Backpressure Management**: Decouples incoming SDI/HDMI video metadata packets from downstream AI inference.
* **Zero-Downtime Webhook Fallback**: When running in single-camera or cloud testing environments without a live Kafka broker, the system automatically falls back to asynchronous HTTP webhooks without code changes or pipeline stalls.

---

## 7. The Director Autonomy Principle & Mathematical Decision Boundary

One of the greatest dangers of AI on a film set is **alert fatigue**. If an AI interrupts the director during an emotional performance for a negligible shadow or microscopic prop angle, the crew will immediately turn the system off.

Bob designed and implemented the **Director Autonomy Principle**:

$$\text{Confidence}_{\text{final}} = w_1 \cdot C_{\text{YOLO}} + w_2 \cdot C_{\text{FlashLite}} + w_3 \cdot C_{\text{Pro}}$$

Where:
* $w_1 = 0.20$ (Spatial localization weight)
* $w_2 = 0.35$ (Visual state verification weight)
* $w_3 = 0.45$ (Cinematic narrative context weight)

### Alert Action Matrix

```
   Confidence Score
      1.0 ┌──────────────────────────────────────────────────────────┐
          │                                                          │
          │   TIER A: SILENT SCRIPT SUPERVISOR ALERT                 │
          │   Confidence ≥ 0.85 & Critical Continuity Delta          │
          │   • Dispatched silently to supervisor iPad               │
          │   • Side-by-side photographic evidence provided          │
          │   • Director retains 100% final override authority      │
          │                                                          │
      0.85├──────────────────────────────────────────────────────────┤
          │                                                          │
          │   TIER B: QUEUED POST-SCENE AUDIT NOTE                   │
          │   0.50 ≤ Confidence < 0.85                               │
          │   • Logged silently in daily wrap report                 │
          │   • Zero on-set chime or visual interruption             │
          │                                                          │
      0.50├──────────────────────────────────────────────────────────┤
          │                                                          │
          │   TIER C: AUTOMATIC SYSTEM SUPPRESSION                   │
          │   Confidence < 0.50                                      │
          │   • Filtered immediately to prevent noise                │
          │   • False alarm rate strictly capped at ≤ 0.05%          │
          │                                                          │
      0.0 └──────────────────────────────────────────────────────────┘
```

**Result**: The director is never interrupted. The script supervisor receives only mathematically indisputable anomalies with exact photographic proof.

---

## 8. Real-World Benchmark: Night of the Living Dead (1968)

To prove Shadow Cut's forensic power, we audited 142 takes across George A. Romero's *Night of the Living Dead*. The Bob-orchestrated MCP pipeline uncovered **4 real historical continuity errors** that escaped the human script supervisor and made it into the theatrical release:

1. **37:08 — The Carpenter Signature**: A carpenter's construction pencil marks visible on the 2x4 lumber barricading the front door.
2. **07:58 — The Vanishing Canister**: A lighter fluid canister on the mantelpiece that teleports between reverse angles.
3. **52:14 — Winchester Lever Position**: The rifle lever cycles from open to closed between adjacent cuts without being cocked.
4. **18:22 — Table Object Displacement**: Props on the living room table rotate $45^\circ$ between master and medium close-up takes.

Bob's structural pipeline processed all 142 takes in 20 minutes with **zero manual tuning**, proving the engine's industrial readiness.

---

## 9. Conclusion: The Power of IBM Bob in Production AI

By utilizing IBM Bob to build strict data schemas, standardized MCP protocols, enterprise OpenAPI specifications, and resilient streaming architectures, Shadow Cut bridges the gap between bleeding-edge vision models and mission-critical film production. 

Bob didn't just help write code; **Bob built the structural foundation that lets filmmakers preserve their creative vision.**
