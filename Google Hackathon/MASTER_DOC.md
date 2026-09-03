# SHADOW CUT — Master Project Document
## Agentic Cinema Hackathon | IBM Track | Devpost
### Full Architecture, Design Decisions, Prompts, and Execution Plan

---

## TABLE OF CONTENTS

1. [Executive Summary](#1-executive-summary)
2. [The Problem](#2-the-problem)
3. [The Solution](#3-the-solution)
4. [Full Architecture](#4-full-architecture)
5. [Tech Stack Deep Dive](#5-tech-stack-deep-dive)
6. [Data Models & Schemas](#6-data-models--schemas)
7. [Prompts](#7-prompts)
8. [Cost Model](#8-cost-model)
9. [Demo Video Storyboard](#9-demo-video-storyboard)
10. [IBM Bob Integration Plan](#10-ibm-bob-integration-plan)
11. [Timeline & Milestones](#11-timeline--milestones)
12. [Risk Assessment & Mitigations](#12-risk-assessment--mitigations)
13. [Devpost Submission Plan](#13-devpost-submission-plan)
14. [External Validation Summary](#14-external-validation-summary)
15. [Open Questions](#15-open-questions)

---

## 1. EXECUTIVE SUMMARY

**Shadow Cut** is an AI script supervisor that watches every take during film production, detects continuity errors in real-time, and alerts the director while they're still on set — before the location is wrapped and reshoots cost $50,000+ per day.

**The Pitch:** For the price of a pizza ($7), Shadow Cut prevents a $50,000 reshoot. That's a 7,000x ROI.

**The Architecture:** A three-tier agentic cascade — YOLO-World detects objects locally on every frame, Gemini Flash-Lite validates anomalies with script context, and Gemini Pro handles critical escalations. All orchestrated via Google ADK, with IBM Bob-built MCP servers and Confluent real-time streaming.

**The Gap:** There is NO AI tool for on-set continuity assistance. Every AI filmmaking tool is either pre-production (scheduling, breakdowns) or post-production (editing, VFX). The production phase itself is a complete blind spot in a $25.48 billion market.

**The Precedent:** SurgAgent (1st place, Google Cloud AI Hackathon Dec 2025) used a similar Gemini + video + object detection architecture for surgical compliance. Shadow Cut applies this proven approach to an untouched domain with a harder problem: reconciling visual reality against narrative intent across non-linear time.

**The Odds:** External AI evaluation: 70-85% chance of placing top 3 in the IBM track, provided the 3-minute demo video is compelling.

---

## 2. THE PROBLEM

### 2.1 The Script Supervisor Crisis

Modern film production has created a crisis for script supervisors ("scriptys"):

- **Multi-camera overwhelm:** Productions now use 3-4 cameras simultaneously. Script supervisors report it's "almost humanly impossible to follow all of those cameras all the time." (Dawn Gilliam, *The Hunger Games*)
- **Digital shooting ratios:** Directors roll cameras constantly. Shooting ratios of 30:1 to 150:1 are common. A 2-hour film generates 25-375 hours of raw footage.
- **Data entry burden:** Going digital has shifted script supervisors' focus to data entry, reducing their interaction with actors and directors. (Jayne-Anne Tenggren, *Star Wars* / *James Bond*)
- **Chronic understaffing:** The industry is developing apprenticeship programs because they can't hire enough script supervisors.

### 2.2 The Cost of Continuity Errors

Continuity errors are not just coffee cups in the wrong hand. The expensive ones are:

- **Performance mismatches:** An actor is calm in the wide shot and agitated in the close-up. The two shots refuse to sit next to each other. The editor loses half the scene.
- **Prop state errors:** A letter is folded in Scene 5 but open in Scene 23's payoff. The narrative logic collapses.
- **Cross-scene contradictions:** Scene 42 (the breakup) is shot on Day 1. Scene 41 (the argument leading to it) is shot on Day 18. The emotional arcs don't match.

**Cost to fix on set:** $0 (reset the prop, reshoot the take).
**Cost to fix in post:** $5,000-20,000 (VFX paint-out, ADR, editing workarounds).
**Cost to fix with reshoots:** $20,000-100,000+ per day (location re-rental, actor recall, crew rehire).

### 2.3 The Market Gap

Comprehensive 2026 surveys of AI filmmaking tools show:

| Phase | Tools | AI On-Set Assistant? |
|-------|-------|---------------------|
| Pre-production | Storyflow, Celtx, Arc Studio, Final Draft, AI storyboards | ❌ No |
| Production logistics | StudioBinder (scheduling, call sheets) | ❌ No |
| Video generation | Runway, Sora, LTX Studio | ❌ No |
| Voice/ADR | ElevenLabs | ❌ No |
| Editing | Descript, Premiere + Firefly | ❌ No (post only) |
| Research | NotebookLM | ❌ No |

**There is zero competition in on-set AI continuity assistance.** The global AI in media market is $25.48 billion (24.5% CAGR). None of it is going here.

### 2.4 Competitive Landscape (Honest Assessment)

**Existing tools DO exist in the AI continuity space:**

| Tool | What It Does | What Shadow Cut Does Differently |
|------|-------------|----------------------------------|
| **Studiovity** | AI-assisted continuity/prop flagging synced across production team | Monitors the **actual footage** with computer vision, not just script notes |
| **ScriptE / Scripto** | Digital script supervisor notebooks, take-by-take logging | **Automated** detection — no manual data entry per take |
| **Scriptation** | Script annotation and sharing for production teams | **Real-time alerts** during shooting, not post-shoot review |
| **StudioBinder** | Scheduling, call sheets, breakdowns (pre-production) | Operates **during production**, not before |
| **Storyflow** | AI script analysis and continuity planning | Analyzes **uploaded video frames**, not just the script text |

**The honest reframe:**

Shadow Cut is NOT "the only AI tool for film continuity." That claim is false and judges will ding us for it.

Shadow Cut IS the only tool that:
1. **Processes the actual uploaded footage** with computer vision (YOLO) in real-time
2. **Builds a Plot Knowledge Graph from the script** to know what's important vs. incidental
3. **Alerts during the shoot** while the director is still on set
4. **Reasons across non-linear schedules** (Scene 42 shot on Day 1, Scene 41 on Day 18)

Existing tools track continuity in scripts and notes. Shadow Cut tracks continuity in **pixels**.

### 2.5 Why This Problem Fits the Hackathon

The hackathon theme is "Agentic Cinema." Most participants will build:
- AI screenwriters (pre-production)
- AI video generators (post-production)
- AI chatbots that "talk about movies"

Shadow Cut operates **DURING production**, where creative decisions actually happen. It doesn't replace the director — it helps them make better decisions while the cameras are still rolling.

---

## 3. THE SOLUTION

### 3.1 What Shadow Cut Is

An invisible AI assistant that:
1. **Reads the script** before Day 1 and builds a Plot Knowledge Graph (what's important, what isn't)
2. **Watches every take** as it's uploaded by the DIT
3. **Compares** the take against previous takes of the same scene AND the script's requirements
4. **Alerts the director** only when something genuinely matters — with confidence scores, evidence, and script context
5. **Answers questions** via chat — "What did I say about Scene 5?" "Did the watch move?" "Are we missing coverage?"

### 3.2 What Shadow Cut Is NOT

- ❌ It does NOT choose which shots to use (that's the director's joy)
- ❌ It does NOT edit the film (that's the editor's job)
- ❌ It does NOT generate content (it's a verification tool, not a creative tool)
- ❌ It does NOT replace the script supervisor (it augments them)

### 3.3 The Director's Experience

**95% of the time:** The director sees nothing. Shadow works silently.

**4% of the time:** A gentle notification appears:
> "Watch switched from left to right wrist between Take 2 and Take 4. This is a CRITICAL prop — the script requires left wrist for continuity with Scene 23. Confidence: 96%."

**1% of the time:** The director opens the chat and asks:
> "Did Character A seem more confident in Take 3?"
> 
> Shadow: "In Take 3, Gemini detected 'controlled confidence' (0.82). In Take 1, 'visible anxiety' (0.71). Take 3 is 16% more confident. You circled Take 3 and said 'Love the energy, keep it.'"

### 3.4 Key Design Principles

1. **Trust through transparency:** Every alert shows its evidence trail, confidence score, and source data. The director can verify every claim.
2. **Accountability:** Shadow tracks its own accuracy. "I've analyzed 12 takes today. 3 alerts, 2 confirmed, 1 dismissed. Accuracy: 87%."
3. **Learning from dismissals:** If the director dismisses a category of alert 3 times, Shadow deprioritizes that category.
4. **Script as training data:** The agent doesn't "learn" during shooting. It already knows what's important because it read the script.
5. **Human-in-the-loop:** The director always decides. Shadow only informs.

---

## 4. FULL ARCHITECTURE

### 4.1 High-Level Data Flow

```
PRE-PRODUCTION (Before Day 1)
=============================
  Director uploads script (PDF/Fountain/TXT)
    ↓
  Gemini 2.5 Pro parses entire script (1M token context)
    ↓
  PLOT KNOWLEDGE GRAPH generated:
    - Props with importance levels (CRITICAL/IMPORTANT/INCIDENTAL)
    - Continuity rules per prop
    - Emotional arcs per character
    - Setup/payoff links across scenes
    - Scene contexts (lighting, tone, characters)
    ↓
  Graph stored in Firestore

DURING PRODUCTION (Every Take)
==============================
  Camera → Card → DIT uploads H.264 proxy to Cloud Storage
    ↓
  Cloud Function triggered by upload
    ↓
  ┌─────────────────────────────────────────────┐
  │  TIER 1: YOLO-WORLD (Local, Every Frame)    │
  │                                             │
  │  • Runs on DIT laptop or cheap cloud GPU    │
  │  • Detects ONLY props from script vocab     │
  │  • Tracks positions, states, presence       │
  │  • Compares frame N to frame N-1            │
  │  • Flags anomalies locally (free, instant)  │
  │                                             │
  │  Output: Structured JSON "math"             │
  │  (bounding boxes, state changes, positions) │
  └─────────────────────────────────────────────┘
    ↓
  ┌─────────────────────────────────────────────┐
  │  TIER 2: GEMINI FLASH-LITE (One API Call)   │
  │                                             │
  │  Receives:                                  │
  │    • Original video (H.264 proxy)           │
  │    • Full YOLO math (all frames)            │
  │    • Plot Graph slice (this scene only)     │
  │    • Script summary (500 tokens)            │
  │                                             │
  │  Does:                                      │
  │    • Validates YOLO anomaly flags           │
  │    • Checks for things YOLO missed          │
  │    • Analyzes emotional tone/performance    │
  │    • Transcribes audio (director notes)     │
  │    • Cross-references script importance     │
  │                                             │
  │  Cost: ~$0.002 per take                     │
  │  Speed: ~15-25 seconds                      │
  └─────────────────────────────────────────────┘
    ↓
  ┌─────────────────────────────────────────────┐
  │  TIER 3: GEMINI PRO (Rare Escalation)       │
  │                                             │
  │  Called ONLY when:                          │
  │    • Flash-Lite confidence < 70%            │
  │    • Plot weight = CRITICAL                 │
  │    • Cross-scene continuity needed          │
  │    • Complex narrative reasoning required   │
  │                                             │
  │  Cost: ~$0.05-0.20 per escalation           │
  │  Frequency: ~10% of takes                   │
  └─────────────────────────────────────────────┘
    ↓
  ┌─────────────────────────────────────────────┐
  │  CONFIDENCE ENGINE                            │
  │                                             │
  │  • Scores each finding (0.0-1.0)            │
  │  • Considers evidence quality, plot weight  │
  │  • Tracks historical accuracy per category  │
  │  • Adjusts for director override rates      │
  │                                             │
  │  Rules:                                     │
  │    • < 70% confidence → NEVER alert         │
  │    • CRITICAL + >85% confidence → ALERT     │
  │    • Director dismisses category 3x →       │
  │      Deprioritize that category             │
  └─────────────────────────────────────────────┘
    ↓
  ┌─────────────────────────────────────────────┐
  │  ALERT DECISION                             │
  │                                             │
  │  IF important AND high confidence:          │
  │    → Push notification to director          │
  │  ELSE:                                      │
  │    → Silent log for chat interface          │
  └─────────────────────────────────────────────┘
    ↓
  SHADOW MEMORY (Firestore)
    - Structured JSON per take (~2KB)
    - Vector embeddings for RAG search
    - Historical accuracy tracking
    ↓
  RAG VECTOR DB (Firestore or Vertex AI)
    - Semantic search across all takes
    - Director queries retrieve relevant context
    ↓
  CHAT INTERFACE (Next.js / Streamlit)
    - Director asks natural language questions
    - System retrieves context, generates answer
    - Can reference images, timestamps, evidence
```

### 4.2 The Three-Tier Detection System

#### Tier 1: YOLO-World (Local, Every Frame, Free)

**What it does:**
- Detects objects from the script vocabulary only
- Tracks bounding boxes frame-by-frame
- Detects state changes (position, orientation, presence)
- Runs entirely locally on DIT laptop CPU/GPU

**What it outputs:**
```json
{
  "frame_121": {
    "watch": {"bbox": [210, 280, 240, 300], "state": "left_wrist", "confidence": 0.94},
    "letter": {"bbox": [120, 340, 180, 400], "state": "folded", "confidence": 0.91}
  }
}
```

**Limitation:** YOLO is weak at subtle state changes ("half-full vs. empty", "slightly askew"). It detects spatial presence, not semantic state.

**Mitigation:** YOLO's job is "where is the prop?" Flash-Lite's job is "what state is the prop in?"

#### Tier 2: Gemini Flash-Lite (API, Anomalies Only, Cheap)

**What it does:**
- Receives video + YOLO math + script context
- Validates whether YOLO's flags are real or false alarms
- Checks for things YOLO missed (semantic states, emotional tone)
- Transcribes audio (director notes, dialogue)

**Why it's faster than processing raw video:**
- YOLO already found the objects. Flash-Lite doesn't start from zero.
- The Plot Graph filters out noise. Flash-Lite knows what's important.
- Flash-Lite validates pre-computed data rather than discovering it.

**Cost:** ~$0.002 per take (video sampled at 1fps, ~100 tokens/second)

#### Tier 3: Gemini Pro (API, Rare, Expensive but Rare)

**What it does:**
- Deep reasoning on complex, ambiguous cases
- Cross-scene continuity ("Does Scene 5's performance match Scene 2's setup?")
- Narrative logic validation ("If the letter is open here, does Scene 23's payoff still work?")

**When it's called:**
- Flash-Lite confidence < 70%
- CRITICAL prop with conflicting evidence
- Non-sequential scene comparison needed

**Cost:** ~$0.05-0.20 per call, ~10% of takes

### 4.3 The Confidence Engine (v2.0 — Patched)

The confidence engine makes scores actually trustworthy by grounding them in verifiable data. **Two critical bugs were fixed in external review:**

**Bug #1 (Fixed):** The original formula `Confidence = Evidence × PlotWeight × History × Trust` crushed legitimate alerts below 0.70 due to multiplicative dampening. Even CRITICAL props with good evidence scored ~0.58.

**Bug #2 (Fixed):** The budget guard in `should_escalate_to_pro()` was dead code — `return True` triggered before the guard was ever reached.

---

#### The Confidence Formula (Fixed)

```
TechnicalConfidence = EvidenceQuality × HistoricalAccuracy × DirectorTrust
```

**PlotWeight is NOT a multiplier.** It is a **gate** that determines action severity via the Decision Matrix below.

**Cold-start HistoricalAccuracy raised to 0.95** so new categories aren't penalized until they actually fail.

---

#### Evidence Quality (Base Reliability)

| Source | Reliability | Example |
|--------|-------------|---------|
| Script supervisor note | 0.95 | Human-verified on set |
| Slate metadata | 0.92 | Objective recording data |
| YOLO detection (multi-frame) | 0.85 | Computer vision, verifiable |
| YOLO detection (single frame) | 0.65 | Possible false positive |
| Audio transcript (Gemini-native) | 0.75 | AI-transcribed, may miss jargon |
| Plot graph inference | 0.65 | AI-inferred from script |
| Performance analysis | 0.60 | Subjective interpretation |
| Gemini Flash-Lite validation | 0.70 | Model judgment |
| Gemini Pro escalation | 0.88 | Deeper reasoning |

**Composite Evidence:**
- Two independent sources agree → boost by +0.08 (max 0.98)
- Sources conflict → drop to lowest source × 0.85
- No direct evidence (pure inference) → cap at 0.65

---

#### Historical Accuracy (Self-Scoring)

```
HistoricalAccuracy = confirmed_alerts / (confirmed_alerts + false_positives)
```

| Tier | Modifier | Example |
|------|----------|---------|
| Proven (>90%) | 1.00 | "Watch position" — 12 sent, 11 confirmed |
| Reliable (75-90%) | 0.95 | "Letter state" — 8 sent, 7 confirmed |
| Unproven (50-75%) | 0.90 | "Performance energy" — new category |
| Unreliable (<50%) | 0.60 | "Lighting consistency" — 4 sent, 1 confirmed |

**Cold start:** New categories begin at **0.95**.

---

#### Director Trust (Learning from Overrides)

```
DismissalCount = times director dismissed this category in last 7 days

if DismissalCount >= 3:   DirectorTrust = 0.50, SeverityCap = "warning"
elif DismissalCount == 2:  DirectorTrust = 0.75
elif DismissalCount == 1:  DirectorTrust = 0.90
else:                      DirectorTrust = 1.00
```

**Decay:** Counts decay by 1 every 48 hours.

---

#### Decision Matrix (PlotWeight as Gate)

| TechnicalConfidence | CRITICAL Prop | IMPORTANT Prop | INCIDENTAL Prop |
|---------------------|---------------|----------------|-----------------|
| **High (>0.75)** | ALERT (Instant) | ALERT (Standard) | SILENT LOG |
| **Medium (0.50–0.75)** | ESCALATE TO PRO | SILENT LOG | SILENT LOG |
| **Low (<0.50)** | SILENT LOG | SILENT LOG | SUPPRESS |

**Hard Rules:**
1. Below 0.50 TechnicalConfidence → NEVER alert (chat-queryable or suppressed)
2. CRITICAL + High confidence → ALWAYS alert (safety override)
3. INCIDENTAL → NEVER alert regardless of confidence
4. Performance/emotion → NEVER alert above MEDIUM unless director opts in

---

#### Escalation Matrix (Budget Guard Fixed)

```python
def should_escalate_to_pro(anomaly, technical_confidence, plot_weight):
    # 1. HARD CEILING: Budget guard FIRST (was dead code before)
    if pro_escalation_count_today >= pro_budget:
        if plot_weight != PlotWeight.CRITICAL:
            return False
        # CRITICAL props bypass budget (safety override)

    # 2. Hard skip rules
    if technical_confidence >= 0.90: return False
    if plot_weight == PlotWeight.INCIDENTAL: return False

    # 3. Auto-escalate triggers
    if plot_weight == PlotWeight.CRITICAL and technical_confidence < 0.85: return True
    if anomaly.is_cross_scene: return True
    if anomaly.is_novel and plot_weight in [CRITICAL, IMPORTANT]: return True

    return False
```

**Escalation budget:** Max 15% of takes escalate to Pro. If exceeded, only CRITICAL props escalate.

---

#### Cost Guardrails

| Guardrail | Value |
|-----------|-------|
| Max Pro escalations/day | 50 |
| Max Pro escalations/take | 2 |
| Min confidence for Pro | 0.40 |
| Flash-Lite timeout | 30 sec |
| Pro timeout | 60 sec |

> **Full pseudocode and edge cases:** See `confidence_escalation_logic.md` (Deliverable 4).

### 4.4 The Plot Knowledge Graph

Built once from the script before Day 1. Stored in Firestore. Queried by every agent.

**Structure:**
```json
{
  "scenes": {
    "5": {
      "title": "The Confrontation",
      "characters": ["Alex", "Morgan"],
      "emotional_tone": "desperate, building tension",
      "lighting": "harsh overhead, shadows",
      "critical_props": {
        "letter": {
          "importance": "CRITICAL",
          "rules": ["Must still be FOLDED", "Held in LEFT hand"],
          "payoff_scene": 23
        },
        "watch": {
          "importance": "CRITICAL",
          "rules": ["Still on LEFT wrist"]
        }
      },
      "setups": ["Character_A suspects B"],
      "payoffs": []
    }
  },
  "props": {
    "letter": {
      "first_scene": 1,
      "last_scene": 23,
      "plot_weight": "CRITICAL",
      "continuity_rules": ["Must remain folded until Scene 23"]
    }
  },
  "emotional_arcs": {
    "Alex": [
      {"scene": 1, "emotion": "suspicious", "intensity": 0.7},
      {"scene": 5, "emotion": "desperate", "intensity": 0.9},
      {"scene": 23, "emotion": "resigned", "intensity": 0.5}
    ]
  },
  "setups": {
    "fear_of_water": {"scene": 3, "payoff_scene": 28, "weight": "CRITICAL"}
  }
}
```

**Key insight:** The graph is tiny. A feature film's entire graph is ~50-100KB. It fits in memory. Queries are instant.

### 4.5 The Chat Interface

**How it works:**
1. Director types a question
2. Question is converted to an embedding vector
3. Vector DB searches for similar chunks (takes, notes, alerts)
4. Relevant chunks retrieved (top 5)
5. Gemini 3.6 Flash generates answer using retrieved context

**Example queries it handles:**
- "What did I say about Scene 5?" → Retrieves director notes from all takes of Scene 5
- "Did the watch move?" → Retrieves watch state changes across all takes
- "How did Character A's emotion change?" → Retrieves emotional tone analyses
- "Show me the moment the letter opened" → Retrieves timestamp + frame reference
- "Are we missing coverage for Scene 12?" → Compares shot list against completed takes

**The vector DB stores:**
- Script chunks (per scene)
- Take summaries (per take)
- Director notes (transcribed audio)
- Continuity alerts (flagged issues)
- Plot graph facts (structured data)

Each chunk is ~500 bytes. For 500 takes = ~250KB total. The RAG is microscopic.

---

## 5. TECH STACK DEEP DIVE

### 5.1 Why Each Tool Was Chosen

| Tool | Role | Why This One |
|------|------|-------------|
| **YOLO-World** | Object detection | Open-vocabulary (detects any prop name), open-source, runs locally on CPU, zero cost |
| **Gemini 2.5 Pro** | Script parsing | 1M token context = entire feature script in one shot. Best reasoning for complex narrative analysis. |
| **Gemini 3.5 Flash-Lite** | Per-take analysis | Built for agentic workflows, high-volume, low-latency. Cheapest Gemini with video input. |
| **Gemini 2.5/3.1 Pro** | Escalated reasoning | Best for cross-scene continuity, complex narrative logic, ambiguous cases. |
| **Gemini 3.6 Flash** | Chat interface | Latest model, best conversational quality, multimodal (can reference images). |
| **Gemini Embeddings** | RAG vector search | Native Google Cloud integration, cheap, fast. |
| **Google ADK** | Agent orchestration | Required by hackathon. Purpose-built for multi-agent systems. |
| **IBM Bob** | MCP server builder | Required for IBM track. Bob builds the tools our agents call. Deep integration, not shallow usage. |
| **Confluent** | Event streaming | "Strongly encouraged" for IBM track. One topic, one consumer, minimal complexity. |
| **Firestore** | Data storage | Native Google Cloud, free tier generous, vector search built-in, simple. |
| **Cloud Run** | Hosting | Free tier (2M requests/month), serverless, auto-scales, easy deployment. |
| **Google Cloud Storage** | Video storage | Production already uses this. Shadow just stores pointers, not video. |

### 5.2 What We DON'T Use (And Why)

| Tool | Why Not |
|------|---------|
| **Whisper (OpenAI)** | BANNED by hackathon rules. Only Google Cloud AI allowed. We use Gemini's native audio transcription. |
| **GPT-4 / Claude / Bedrock** | BANNED. Only Gemini models. |
| **Gemma 4 (local)** | Technically allowed, but API is cheaper and simpler for hackathon scale. Mentioned as "future scaling" talking point. |
| **Vertex AI Vector Search** | Overkill. Firestore vector search is simpler and sufficient for our data volume. |
| **Kubernetes / GKE** | Overkill. Cloud Run handles our scale with zero config. |
| **Complex CI/CD** | Overkill. Manual deployment is fine for a hackathon. |

### 5.3 The Hackathon Rules Compliance Checklist

| Rule | How We Comply |
|------|--------------|
| **Only Google Cloud AI** | All AI models are Gemini variants. Zero external AI. |
| **Use chosen partner product** | IBM Bob builds our MCP servers. Bob is used in development AND runtime. |
| **Functional agent** | Multi-agent cascade with real reasoning, not a single prompt wrapper. |
| **Hosted project URL** | Deployed on Cloud Run with public URL. |
| **3-minute demo video** | Screen recording of working system, not cinematic trailer. |
| **Public open-source repo** | GitHub repo with complete license. |
| **Actual runtime use of Google Cloud** | Cloud Run, Firestore, Cloud Storage, Gemini API all used in code (not just README). |

---

## 6. DATA MODELS & SCHEMAS

### 6.1 Core Data Types

See `models/__init__.py` for full implementation. Key types:

- **Take:** Single video capture (scene, shot, take, duration, props, performance notes)
- **Scene:** Script scene (number, title, characters, props, emotional tone, setups, payoffs)
- **Prop:** Physical object (name, description, plot weight, continuity rules, state history)
- **ShadowAlert:** Generated alert (severity, confidence, evidence, source trail, suggested action)
- **DirectorQuery:** Chat question (question, context, response, sources, confidence)

### 6.2 Confluent Event Schema (Minimal — Checkbox, Not Cathedral)

**Philosophy:** IBM track "strongly encourages" Confluent. We use it. But we do not build a cathedral. One topic. One consumer. One JSON schema. If Confluent fails, a local webhook queue catches the event.

**One topic:** `shadow-cut.takes.uploaded`
**Partitions:** 1
**Retention:** 7 days

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TakeUploadedEvent",
  "type": "object",
  "required": ["event_id", "timestamp", "type", "data"],
  "properties": {
    "event_id": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "type": { "type": "string", "enum": ["take_uploaded"] },
    "data": {
      "type": "object",
      "required": ["take_id", "scene", "shot", "take", "video_path", "duration"],
      "properties": {
        "take_id": { "type": "string", "pattern": "^s[0-9]+_sh[0-9]+_t[0-9]+$" },
        "scene": { "type": "integer", "minimum": 1 },
        "shot": { "type": "integer", "minimum": 1 },
        "take": { "type": "integer", "minimum": 1 },
        "video_path": { "type": "string" },
        "proxy_path": { "type": "string" },
        "duration": { "type": "number", "minimum": 0 },
        "uploaded_by": { "type": "string" },
        "slate_metadata": {
          "type": "object",
          "properties": {
            "date": { "type": "string", "format": "date" },
            "director": { "type": "string" },
            "dp": { "type": "string" }
          }
        }
      }
    }
  }
}
```

**One consumer:** Shadow pipeline trigger. Group ID: `shadow-pipeline`. Auto-offset: earliest.

**Fallback Webhook Queue:**
```python
@app.post("/webhook/take-uploaded")
async def fallback_webhook(event: TakeUploadedEvent):
    # Receives events directly when Confluent is unavailable
    await shadow_pipeline.process_take(event.data)
    return {"status": "queued"}
```

If Confluent is down, the Cloud Function directly calls the webhook. The pipeline processes identically. Zero complexity. Zero debugging nightmares.

### 6.3 YOLO Math Output Schema

```json
{
  "take_id": "s5_sh3_t2",
  "scene": 5,
  "shot": 3,
  "take": 2,
  "duration_seconds": 242.5,
  "frames_analyzed": 7275,
  "fps": 30,
  "object_tracks": {
    "watch": {
      "class": "watch",
      "first_seen_frame": 1,
      "last_seen_frame": 7275,
      "confidence_avg": 0.93,
      "positions": [
        {"frame": 1, "timestamp": 0.03, "bbox": [210, 280, 240, 300], "state": "left_wrist"}
      ],
      "state_changes": [
        {"from": "left_wrist", "to": "right_wrist", "frame": 3637, "timestamp": 121.23, "confidence": 0.91}
      ]
    }
  },
  "anomaly_flags": [
    {
      "type": "prop_position_change",
      "prop": "watch",
      "from": "left_wrist",
      "to": "right_wrist",
      "frame": 3637,
      "timestamp": 121.23,
      "severity": "high",
      "confidence": 0.91
    }
  ]
}
```

### 6.4 Flash-Lite Result Schema

```json
{
  "take_id": "s5_sh3_t2",
  "timestamp": "2026-08-01T14:23:45Z",
  "verdicts": [
    {
      "anomaly_index": 1,
      "verdict": "real_issue",
      "confidence": 0.94,
      "severity": "critical",
      "explanation": "Watch switched from left to right wrist. Script requires left wrist for continuity with Scene 23 payoff."
    }
  ],
  "missed_issues": [],
  "performance_notes": "Performance appears consistent with required emotional tone.",
  "audio_transcript": "Director: 'Cut! Let's go again, more intensity.'",
  "needs_escalation": true,
  "escalation_reason": "Critical prop continuity issue detected."
}
```

---

## 7. PROMPTS

### 7.1 Script Parser Prompt (Gemini 2.5 Pro)

```
You are a film script analysis engine. Parse the following script and extract a structured Plot Knowledge Graph.

For EACH scene, extract:
1. Scene number and title
2. Characters present
3. ALL props mentioned or implied
4. Emotional tone (suspicious, desperate, shocked, etc.)
5. Lighting notes (if mentioned)
6. Setups (things established that need payoffs later)
7. Payoffs (things resolved that were set up earlier)

For EACH prop, determine:
- Plot importance: CRITICAL (setup/payoff prop), IMPORTANT (supporting detail), or INCIDENTAL (background)
- Continuity rules (must remain folded, must stay on left wrist, etc.)
- First scene it appears
- Last scene it appears (if known)
- Payoff scene (if it's a setup prop)

For EACH character, extract:
- Emotional arc points (scene number, emotion, intensity 0.0-1.0)
- Knowledge state (what do they know at this point?)

Return as valid JSON matching this schema:
{
  "scenes": { "1": { ... }, "5": { ... } },
  "props": { "letter": { ... }, "watch": { ... } },
  "emotional_arcs": { "Alex": [ ... ] },
  "setups": { "fear_of_water": { "scene": 3, "payoff_scene": 28 } }
}
```

### 7.2 Flash-Lite Validation Prompt

```
You are SHADOW, a film script supervisor AI. Analyze this take with the following context:

=== SCENE CONTEXT ===
Scene: {scene_number} - {scene_title}
Characters in scene: {characters}
Required emotional tone: {emotional_tone}
Lighting notes: {lighting_notes}

=== CRITICAL PROPS (from script) ===
{critical_props_formatted}

=== SCRIPT SUMMARY ===
{script_summary}

=== YOLO DETECTION DATA ===
Take: {take_id}
Duration: {duration}s
Frames analyzed: {frames_analyzed}
Objects tracked: {object_names}

=== YOLO ANOMALY FLAGS ===
{anomalies_formatted}

=== YOUR TASK ===
Review the YOLO anomaly flags and determine if each is a REAL continuity issue or a FALSE ALARM.

For EACH anomaly, output:
- "verdict": "real_issue", "false_alarm", or "uncertain"
- "confidence": 0.0 to 1.0
- "severity": "critical", "warning", or "info"
- "explanation": Brief reason for your verdict

Also check:
1. Are any CRITICAL props missing or in wrong states?
2. Did YOLO miss any important changes?
3. Does the performance match the required emotional tone?
4. Any audio notes (director comments, dialogue issues)?

If ANY critical prop has an issue with confidence > 0.85, set "needs_escalation": true.

Return ONLY valid JSON.
```

### 7.3 Pro Escalation Prompt

```
You are SHADOW EXPERT, a senior film continuity analyst. This case requires deep reasoning.

=== CONTEXT ===
Scene: {scene_number}
Prop: {prop_name}
Plot importance: CRITICAL
Script rules: {rules}

=== FLASH-LITE FINDINGS ===
{flash_lite_result}

=== PREVIOUS TAKE CONTEXT ===
{previous_take_states}

=== CROSS-SCENE CONTEXT ===
This prop was established in Scene {setup_scene} with rules: {setup_rules}
It pays off in Scene {payoff_scene}.

=== YOUR TASK ===
1. Verify if this continuity error breaks the narrative logic.
2. Assess the severity of the impact on the edit.
3. Recommend specific action (reshoot, pickup insert, VFX note, or acceptable).
4. Estimate the cost of fixing now vs. fixing in post.

Return structured analysis with high confidence.
```

### 7.4 Chat Interface Prompt

```
You are SHADOW, a film production assistant with perfect memory.

=== RETRIEVED CONTEXT ===
{retrieved_chunks}

=== DIRECTOR'S QUESTION ===
{question}

=== YOUR TASK ===
Answer the director's question concisely and accurately using ONLY the retrieved context.
If the answer requires a video reference, include the timestamp and take ID.
If uncertain, say so and explain what information is missing.
Never hallucinate. Only use facts from the retrieved context.
```

---

## 8. COST MODEL

### 8.1 Per-Take Breakdown

| Component | Cost | Notes |
|-----------|------|-------|
| YOLO processing | $0.00 | Local CPU/GPU, open-source |
| Flash-Lite analysis | $0.002 | One API call per take, 1fps sampling |
| Pro escalation (10% of takes) | $0.10 | Only for critical/ambiguous cases |
| Storage (structured data) | ~$0.0001 | 2KB JSON per take |
| **Average per take** | **~$0.012** | |

### 8.2 Full Movie Costs

| Production Type | Takes | Total API Cost | + Cloud | Grand Total |
|----------------|-------|---------------|---------|-------------|
| Indie (5:1 ratio) | 150 | $1.80 | $0 | ~$2 |
| Average feature (10:1) | 500 | $7.00 | $0 | ~$7 |
| Big-budget (30:1) | 1,500 | $19.50 | $0-10 | ~$20-30 |
| Blockbuster (100:1) | 5,000 | $65.00 | $0-20 | ~$65-85 |

### 8.3 ROI

| Metric | Value |
|--------|-------|
| Shadow Cut cost (average feature) | ~$7 |
| One prevented reshoot day | $20,000-$100,000+ |
| ROI | 2,800x - 14,000x |
| Script supervisor salary (30 days) | $8,000-$15,000 |
| Shadow Cut as augmentation | ~$7 vs. $8K-15K |

### 8.4 Hackathon Demo Cost

| Item | Cost |
|------|------|
| 50 test takes processed | ~$0.10 |
| 5 Pro escalations | ~$0.50 |
| Cloud Run (free tier) | $0 |
| Firestore (free tier) | $0 |
| Confluent (free trial) | $0 |
| **Total demo cost** | **~$0.60** |

---

## 9. DEMO VIDEO STORYBOARD

### CRITICAL FEEDBACK FROM EXTERNAL AI EVALUATION

**Overall Verdict: 8.5/10** — Narrative arc is killer, but 3 critical blind spots will cost the IBM track prize if not fixed.

**What works:**
- Hook (GoT cup / Braveheart watch) = instant 10/10
- Watch vs. coffee cup alert = most important moment in video
- Trust Report / ROI screen = executive catnip

**What must change:**
1. **Voiceover is MANDATORY** — "text captions work fine" is a death sentence. Judges look away from screen. Use energetic human voice or professional AI TTS (ElevenLabs).
2. **Upload/progress bar is 22 seconds of dead air** — Cut from 30s to 6-8s. Reclaim time for architecture beat.
3. **IBM Bob is invisible until the closing slide** — For the IBM track prize, Bob must appear IN the video as a structural component, not a logo at the end.
4. **Chat query is too subjective** — "Did Character A seem more confident?" drifts from core UVP. Use hard continuity query instead.

---

### REVISED STORYBOARD (3 Minutes)

#### 0:00–0:15 — The Hook
**Visual:** Black screen. Text fades in.

**Voiceover (energetic, confident, reverent):**
> "Film captures lightning in a bottle — a performance that happens once, and never again."

*[PAUSE — HARD CUT TO ERROR]*

**Voiceover:**
> "But one continuity error can ruin that magic forever. Caught too late, they cost fifty thousand dollars a day to fix. Caught on set? They cost zero."

**Cut to:** Montage — beautiful emotional close-up (Creative Commons), then **HARD CUT** to the same shot ruined by a famous continuity error (Game of Thrones Starbucks cup, Braveheart wristwatch, etc.). The contrast should hurt.

**Text overlay:**
> *$50,000 / day vs. $0*

---

#### 0:15–0:30 — The Problem
**Visual:** Screen recording of a script supervisor's chaotic notebook — handwritten notes, arrows, crossed-out corrections, coffee stains.

**Voiceover:**
> "Script supervisors are overwhelmed. Three to four cameras. Thirty-to-one shooting ratios. Thousands of takes. And there is NO AI tool that helps them on set."

**Text overlay (key stats pop in):**
> *3-4 cameras simultaneously*
> *30:1 shooting ratio*
> *Zero on-set AI tools exist*

---

#### 0:30–0:50 — The Solution & Upload
**Visual:** Shadow Cut dashboard appears. Clean, dark UI.

**Voiceover:**
> "Meet Shadow Cut. An AI script supervisor that watches every take and catches errors before you wrap."

**Visual:** DIT drags a video file into cloud storage. Brief flash of pipeline stages:
```
UPLOAD → YOLO detects → Flash-Lite validates → ALERT (if needed)
```

**Speed:** This entire sequence is **6-8 seconds maximum**. No progress bar. Just a rapid-fire visual of the pipeline stages.

**Voiceover:**
> "Upload a take. Shadow processes it in under thirty seconds."

---

#### 0:50–1:15 — The Engine (IBM Track Killer)
**Visual:** Sleek architecture diagram animates in.

**Show:**
```
YOLO-WORLD (Local, Every Frame)
    ↓
IBM BOB MCP SERVER (Orchestrates)
    ↓
GEMINI FLASH-LITE (Validates + Script Context)
    ↓
GEMINI PRO (Escalates Critical Issues)
    ↓
DIRECTOR NOTIFICATION
```

**Voiceover:**
> "Here's how it works. YOLO-World detects every prop on every frame — locally, instantly, for free. But here's the magic: IBM Bob built the MCP servers that orchestrate the entire cascade. Bob's tools feed structured detection data into Gemini Flash-Lite, which cross-references the script's Plot Knowledge Graph. If something is critical and uncertain, Gemini Pro handles the deep reasoning. This isn't just AI — it's agentic AI, built with IBM Bob."

**Text overlay:**
> *Built with IBM Bob MCP Servers*
> *Multi-Agent Cascade*
> *Google Cloud Gemini + Confluent Streaming*

**Why this section exists:** IBM track judges will actively downgrade projects that slap the IBM logo on at the end. This section **proves** Bob is structurally essential to the architecture.

---

#### 1:15–1:45 — The Alert (The Money Shot)
**Visual:** Dashboard shows alert popping up with a subtle notification sound.

**The alert card:**
```
┌─────────────────────────────────────────┐
│  ⚠️  SCENE 5, SHOT 3, TAKE 4            │
│                                         │
│  WATCH CONTINUITY ISSUE                 │
│                                         │
│  Watch switched from LEFT to RIGHT      │
│  wrist at 01:34.                        │
│                                         │
│  This is a CRITICAL prop — script       │
│  requires left wrist for continuity     │
│  with Scene 23 payoff.                  │
│                                         │
│  Confidence: 96%                        │
│  Source: YOLO detection + Script rule   │
└─────────────────────────────────────────┘
```

**Split screen:**
- **Left:** Frame from Take 4 — watch on RIGHT wrist
- **Right:** Frame from Take 2 — watch on LEFT wrist
- **Below:** Script excerpt: *"The watch must remain on Alex's left wrist (established Scene 1, payoff Scene 23)"*

**Voiceover:**
> "Shadow doesn't just detect objects. It understands narrative. The watch is flagged because the script says it's critical — it pays off in Scene 23. A coffee cup in the background? Silent. But a critical prop that breaks continuity? Instant alert, with evidence, confidence, and the script rule that was violated."

**Text overlay:**
> *Coffee cup → SILENT*
> *Critical prop → ALERT*

---

#### 1:45–2:15 — The Scripty Chat
**Visual:** Director opens chat interface. Clean, conversational UI.

**Director types:**
> "In which takes did the letter stay folded? I need one for the Scene 23 payoff."

**Shadow responds:**
```
Scene 5, Shot 2:
  • Take 1: Letter FOLDED (confidence: 0.91) ✅
  • Take 2: Letter OPEN at 01:02 (confidence: 0.87) ❌
  • Take 3: Letter FOLDED (confidence: 0.89) ✅

Recommendation: Use Take 1 or Take 3 for Scene 23 continuity.
Take 2 shows the letter open — this contradicts the payoff.
```

**Visual:** Thumbnail frames from each take appear next to the answer.

**Voiceover:**
> "Ask anything. Shadow remembers every take, every prop state, every director note. It doesn't just search — it reasons across non-linear shooting schedules and narrative arcs."

**Text overlay:**
> *Ask anything. Shadow remembers everything.*

---

#### 2:15–2:45 — The ROI Dashboard
**Visual:** Trust Report dashboard animates in. Numbers count up.

```
SHADOW TRUST REPORT — DAY 5
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Takes analyzed:        47
Alerts generated:       3
Confirmed by director:  3
Accuracy:             100%

Cost so far:         $0.56
Estimated savings: $50,000+
ROI:               89,000x
```

**Voiceover:**
> "Shadow Cut costs seven dollars for an entire feature film. One prevented reshoot day saves fifty thousand dollars. That's not just a tool — that's a seven-thousand-X return on investment."

**Text overlay (punch in one by one):**
> *$7 / movie*
> *$50,000+ saved*
> *7,000x ROI*

---

#### 2:45–3:00 — The Closing
**Visual:** Shadow Cut logo animates. Clean, cinematic.

**Tagline (large text):**
> **SHADOW CUT**
> *The director still directs. The Shadow just remembers.*

**Below logo, tech stack badges animate in:**
> 🔷 Google Cloud Gemini | 🔷 IBM Bob | 🔷 Confluent

**Voiceover:**
> "Shadow Cut. Built for Agentic Cinema."

**Fade to:**
- GitHub repo URL
- Live demo URL
- Devpost project URL

**Final text:**
> *github.com/yourname/shadow-cut*
> *shadow-cut-demo.web.app*

---

### Recording Specifications

| Element | Specification |
|---------|--------------|
| **Voiceover** | MANDATORY. Energetic, confident. Human preferred. AI TTS (ElevenLabs) acceptable if crisp and professional. |
| **Captions** | YES — as backup for accessibility, but voiceover drives the narrative. |
| **Music** | Royalty-free cinematic underscore, low volume (20-30% under voiceover). |
| **Pacing** | No section longer than 25 seconds. The Engine section (0:50-1:15) is the longest at 25s. |
| **Transitions** | Simple cuts. No fancy effects. Let the content carry the video. |
| **Font** | Inter or Roboto. White text on dark background. High contrast. |
| **Color scheme** | Dark dashboard (#1a1a2e), accent color for alerts (#e94560), green for success (#0f3460). |
| **Screen recording** | OBS at 1080p, 30fps. Clean desktop, no distracting icons. |

### Pre-Production Checklist for Demo Video

- [ ] Source 3-4 famous continuity error clips (Creative Commons or fair use)
- [ ] Record voiceover script (practice 3-5 times for energy)
- [ ] Build dashboard UI in Next.js or Streamlit (dark theme, clean)
- [ ] Create architecture diagram (Figma, Excalidraw, or similar)
- [ ] Prepare 3-4 test video clips with intentional errors
- [ ] Record screen captures of upload, alert, chat, and dashboard
- [ ] Edit in DaVinci Resolve, Premiere, or CapCut
- [ ] Add music, captions, and transitions
- [ ] Export at 1080p, H.264, upload to YouTube/Vimeo
- [ ] Watch back at 1.5x speed — if it's boring at 1.5x, it's boring at 1x

---

## 9B. DEMO VIDEO VOICEOVER SCRIPT (Word-for-Word)

**Total word count: ~420 words**
**Reading speed: ~140 words/minute = 3 minutes exactly**
**Tone: Energetic, confident, authoritative. Like a founder pitching investors.**
**Delivery notes: [PAUSE] = 1-second pause. [EMPHASIS] = slight vocal emphasis.**

---

### 0:00–0:15 — THE HOOK

*[Music: Subtle cinematic underscore fades in. Black screen.]*

**VO:**
"Film captures lightning in a bottle — a performance that happens once, and never again."

*[PAUSE — HARD CUT TO ERROR]*

**VO:**
"But one continuity error can ruin that magic forever. Caught too late, they cost fifty thousand dollars a day to fix. Caught on set? They cost zero."

*[Text overlay: $50,000 / day vs. $0]*

---

### 0:15–0:30 — THE PROBLEM

*[Music drops to background. Screen recording: chaotic notebook.]*

**VO:**
"Script supervisors are overwhelmed. Three to four cameras. Thirty-to-one shooting ratios. Thousands of takes. And there is NO AI tool that helps them on set."

*[PAUSE]*

**VO:**
"Until now."

---

### 0:30–0:50 — THE SOLUTION & UPLOAD

*[Music lifts. Dashboard UI appears. Clean, dark, professional.]*

**VO:**
"Meet Shadow Cut. An AI script supervisor that watches every take and catches errors before you wrap."

*[Quick visual: file drag-and-drop, pipeline stages flash rapidly]*

**VO:**
"Upload a take. Shadow processes it in under thirty seconds."

---

### 0:50–1:15 — THE ENGINE (IBM TRACK KILLER)

*[Music becomes more technical, rhythmic. Architecture diagram animates in.]*

**VO:**
"Here's how it works. YOLO-World detects every prop on every frame — locally, instantly, for free."

*[PAUSE]*

**VO:**
"But here's the magic: IBM Bob built the MCP servers that orchestrate the entire cascade. Bob's tools feed structured detection data into Gemini Flash-Lite, which cross-references the script's Plot Knowledge Graph."

*[PAUSE]*

**VO:**
"If something is critical and uncertain, Gemini Pro handles the deep reasoning. This isn't just AI — it's agentic AI, built with IBM Bob."

---

### 1:15–1:45 — THE ALERT (THE MONEY SHOT)

*[Music shifts to alert tone — subtle, urgent but not alarming. Notification sound.]*

**VO:**
"Shadow doesn't just detect objects. It understands narrative."

*[PAUSE]*

**VO:**
"The watch is flagged because the script says it's critical — it pays off in Scene 23. A coffee cup in the background? Silent. But a critical prop that breaks continuity?"

*[PAUSE]*

**VO:**
"Instant alert. With evidence, confidence, and the exact script rule that was violated."

---

### 1:45–2:15 — THE SCRIPTY CHAT

*[Music becomes conversational, warm. Chat interface opens.]*

**VO:**
"Ask anything. 'Which take did the letter stay folded in Scene 14?' Shadow remembers every take, every prop state, every director note."

*[PAUSE]*

**VO:**
"It doesn't just search — it reasons across non-linear shooting schedules and narrative arcs. So you never lose a setup, never miss a payoff, and never shoot yourself into a fifty-thousand-dollar reshoot."

---

### 2:15–2:45 — THE ROI DASHBOARD

*[Music builds to crescendo. Dashboard numbers count up.]*

**VO:**
"Shadow Cut costs seven dollars for an entire feature film. One prevented reshoot day saves fifty thousand dollars."

*[PAUSE]*

**VO:**
"That's not just a tool. That's a seven-thousand-X return on investment."

---

### 2:45–3:00 — THE CLOSING

*[Music resolves. Logo appears. Clean, cinematic.]*

**VO:**
"Shadow Cut. The director still directs. The Shadow just remembers."

*[PAUSE]*

**VO:**
"Because every story deserves to be told without interruption."

*[Music fades. URLs appear on screen.]*

**Tagline (large text):**
> **SHADOW CUT**
> *The director still directs. The Shadow just remembers.*

**Below logo, tech stack badges animate in:**
> 🔷 Google Cloud Gemini | 🔷 IBM Bob | 🔷 Confluent

**Final text:**
> *github.com/yourname/shadow-cut*
> *shadow-cut-demo.web.app*

---

### RECORDING NOTES FOR VOICEOVER

| Timestamp | Words | Delivery Tip |
|-----------|-------|-------------|
| 0:00–0:15 | 40 | Slow, reverent. Let "lightning in a bottle" land. The HARD CUT does the work — don't rush it. |
| 0:15–0:30 | 36 | Build intensity. "NO AI tool" should punch. |
| 0:30–0:50 | 28 | Upbeat, optimistic. "Meet Shadow Cut" is the reveal. |
| 0:50–1:15 | 62 | Technical but excited. This is the IBM section — sound like you BELIEVE in the architecture. |
| 1:15–1:45 | 54 | Urgent but controlled. The alert is the hero moment. |
| 1:45–2:15 | 56 | Conversational, reassuring. Like you're explaining to a director on set. |
| 2:15–2:45 | 42 | Crescendo. "Seven thousand X" should be the peak energy of the entire video. |
| 2:45–3:00 | 18 | Calm, confident, memorable. Let the tagline breathe. |

**Total: ~406 words | ~135 WPM | 3:00 runtime**

### ALTERNATIVE: IF YOU HATE YOUR OWN VOICE

Use ElevenLabs "Adam" or "Bella" voice with these settings:
- Stability: 0.75
- Clarity + Similarity Enhancement: 0.85
- Style: 0.30 (slightly dramatic but not theatrical)
- Speed: 1.0x (normal pace)

Paste the script section by section. ElevenLabs has a 5,000 character limit per generation — this entire script fits in one go.

---
## 10. IBM BOB INTEGRATION PLAN

### 10.1 What Bob Does For Us

**Level 1: Development Process (Required)**
- Bob scaffolds the Python project
- Bob builds MCP servers with `@tool` decorators
- Bob deploys agents to watsonx Orchestrate
- We document this in README and demo

**Level 2: Runtime Architecture (Competitive Edge)**
- Bob-built MCP servers become the Shadow's tools
- Each tool is an `@tool` decorated method
- Gemini agent calls these tools via MCP protocol

### 10.2 The MCP Tools We Build With Bob

| Tool | Input | Output | Built By |
|------|-------|--------|----------|
| `parse_script` | Script text (PDF/TXT) | Plot Knowledge Graph JSON | Bob |
| `analyze_take` | Video path + YOLO math | Flash-Lite result JSON | Bob |
| `check_continuity` | Current take + previous takes | Continuity comparison | Bob |
| `flag_alert` | Anomaly + confidence + plot weight | Alert decision (notify/log) | Bob |
| `query_memory` | Director question | Retrieved chunks + answer | Bob |
| `generate_report` | Date range | Daily Shadow summary | Bob |

### 10.3 Bob Prompts (What We Tell Bob)

**PATCH: Strict Pydantic Schema Binding**

> ⚠️ **Critical requirement:** Bob must generate Pydantic models for ALL tool inputs/outputs. Do NOT use `Dict[str, Any]` or loose typing. Every field must be typed, validated, and documented. This prevents runtime type errors and makes the MCP contract explicit.

**Prompt 1: Project Scaffold**
```
Bob, scaffold a Python project for a film production AI assistant called Shadow Cut.

Requirements:
- Google ADK for agent orchestration
- Confluent Kafka client for event streaming
- Firestore client for data storage
- Google Cloud Storage client for video proxies
- Gemini API client for multimodal analysis
- FastAPI for REST API endpoints
- Pydantic v2 for strict schema validation on ALL data models
- pytest for testing

Create the directory structure, requirements.txt, and basic config files.
```

**Prompt 2: MCP Server**
```
Bob, build an MCP server with these tools using Pydantic v2 models:

1. parse_script(script_text: str) -> PlotKnowledgeGraph
   - Parses film script into Plot Knowledge Graph
   - Returns structured JSON with scenes, props, emotional arcs
   - Use strict Pydantic models, no Dict[str, Any]

2. analyze_take(video_path: str, yolo_math: YoloMath, scene_context: SceneContext) -> FlashLiteResult
   - Validates YOLO anomalies with script context
   - Returns verdicts, performance notes, audio transcript

3. query_memory(question: str, scene_filter: int = None) -> MemoryQueryResult
   - Searches Shadow Memory for director queries
   - Returns relevant takes, notes, and alerts

4. validate_prop_state(prop_name: str, current_state: str, expected_state: str) -> ValidationResult
   - Checks if a prop's current state matches the script's requirements

5. check_continuity(current_take: Take, previous_takes: list[Take]) -> ContinuityReport
   - Compares current take against previous takes + script rules

6. escalate_to_pro(anomaly: Anomaly, scene_context: SceneContext) -> ProEscalationResult
   - Hands off ambiguous critical issues to Gemini Pro for deep reasoning

7. flag_alert(anomaly: Anomaly, confidence: float, plot_weight: str) -> AlertDecision
   - Uses the Decision Matrix to determine ALERT / SILENT_LOG / SUPPRESS

Use the @tool decorator from ibm-agents library.
Generate the server YAML spec for watsonx Orchestrate.
ALL schemas must be Pydantic v2 with strict validation. No loose Dict types.
```

**Prompt 3: Deployment**
```
Bob, deploy the Shadow Cut agent to watsonx Orchestrate.

Requirements:
- Import the agent YAML
- Configure the MCP server endpoints
- Test with sample data
- Generate deployment report
```

**PATCH: Confluent Fallback in Bob Prompts**

> Bob must implement a fallback webhook queue in the Confluent consumer. If Confluent fails, events are caught by a local `/webhook/take-uploaded` endpoint. The pipeline processes identically regardless of which path the event took.

```python
# Bob-generated consumer pseudocode:
@app.post("/webhook/take-uploaded")
async def fallback_webhook(event: TakeUploadedEvent):
    # Receives events directly when Confluent is unavailable
    await shadow_pipeline.process_take(event.data)
    return {"status": "queued"}
```

---

## 11. TIMELINE & MILESTONES

### Week 1: Architecture Lock (Aug 1-7)
**Goal:** Prove the pipeline works on mock data. Lock all design decisions.

| Day | Task | Deliverable |
|-----|------|-------------|
| Aug 1 | ✅ Pipeline test with mock data | Working end-to-end on synthetic data |
| Aug 2 | Demo video storyboard | 3-minute script with timestamps |
| Aug 3 | Write all Gemini prompts | Prompts for Flash-Lite, Pro, Chat, Script Parser |
| Aug 4 | Design Confluent schema | One topic, one consumer, minimal complexity |
| Aug 5 | Design Cloud deployment | Cloud Run, Firestore, IAM roles mapped |
| Aug 6 | Source test video clips | 3-4 clips with intentional continuity errors |
| Aug 7 | Week 1 review | All designs locked, ready for Week 2 |

### Week 2: Integration Design (Aug 8-14)
**Goal:** Set up all accounts and environments. Test real APIs.

| Day | Task | Deliverable |
|-----|------|-------------|
| Aug 8 | Set up Google Cloud project | Project created, APIs enabled |
| Aug 9 | Set up Confluent Cloud | Topic created, free trial active |
| Aug 10 | Set up IBM watsonx | Account ready for Bob deployment |
| Aug 11 | Create GitHub repo | Public repo with license, README template |
| Aug 12 | Test real Gemini API | Video analysis works on test clip |
| Aug 13 | Draft Devpost narrative | Project description, problem, solution, tech stack |
| Aug 14 | Week 2 review | All environments ready, real API tested |

### Week 3: Environment Prep (Aug 15-21)
**Goal:** Deploy skeleton. Test end-to-end with real video.

| Day | Task | Deliverable |
|-----|------|-------------|
| Aug 15 | Deploy Cloud Run skeleton | Hello World endpoint live |
| Aug 16 | Configure Firestore | Data models deployed, test writes work |
| Aug 17 | Set up Confluent consumer | Consumer reads events, triggers pipeline |
| Aug 18 | Test full pipeline with real video | Upload → process → alert → chat |
| Aug 19 | Fix integration issues | All components talk to each other |
| Aug 20 | Record demo B-roll | Dashboard footage, chat footage, alert footage |
| Aug 21 | Week 3 review | Full pipeline works, demo footage captured |

### Week 4: Bob Week (Aug 22-28)
**Goal:** Build production code with Bob. Deploy. Record final demo. Submit.

| Day | Task | Deliverable |
|-----|------|-------------|
| Aug 22 | Feed Bob architecture docs | Bob scaffolds production code |
| Aug 23 | Bob builds MCP servers | All 6 tools implemented and tested |
| Aug 24 | Test with real data | End-to-end works with production code |
| Aug 25 | Debug and polish | Fix Bob-generated issues, UI polish |
| Aug 26 | Deploy final version | Live URL, judges can test |
| Aug 27 | Record final demo video | 3-minute video edited and exported |
| Aug 28 | Submit to Devpost | All requirements met, submitted before deadline |

---

## 12. RISK ASSESSMENT & MITIGATIONS

### ⚠️ THE BRUTAL TIMELINE REALITY (From Third-Party Evaluator)

> "One week of actual laptop time in a five-week window, landing 16 days before deadline, to wire together Confluent + Firestore/ClickHouse + Cloud Run + real video testing + a demo video that's reportedly 40% of the decision — that's not 'tight,' that's 'everything works first try or it doesn't ship.'"

**This is the single biggest risk.** Not the idea. Not the competition. The timeline.

**What this means:**
- We cannot afford integration bugs that take 2 days to debug
- We cannot afford to discover Gemini Vision doesn't work on real video in Week 4
- We cannot afford to rewrite the demo video script in Week 4
- We cannot afford scope creep. Every feature must be ruthlessly justified.

**The rule:** If a feature doesn't appear in the 3-minute demo video, it doesn't get built.

### 12.1 High Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Bob week is too short** | High | Critical | Prep ruthlessly in Weeks 1-3. Have exact specs ready. Cut non-essential features. |
| **Demo video is weak** | Medium | Critical | Start storyboarding NOW. Spend 30% of Bob week on video. Rehearse narration. |
| **Gemini Vision quality poor** | Medium | High | Test with real video in Week 2. If quality is bad, pivot to metadata-only demo. |
| **Integration bugs eat time** | High | High | Use simplest possible integrations. One Confluent topic. One Firestore collection. No fancy configs. |

### 12.2 Medium Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Latency too slow** | Medium | Medium | Set expectations in demo. "20-40 seconds per take" is acceptable for proof-of-concept. |
| **YOLO misses subtle errors** | Medium | Medium | Document limitation honestly. "Catches 95% of visible changes; semantic state validated by Gemini." |
| **Solo vs. teams disadvantage** | High | Medium | Compensate with deeper architecture and better story. Teams often have weaker cohesion. |

### 12.3 Low Risks

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| **Cost overruns** | Low | Low | Free tiers cover everything. API costs are pennies. |
| **Google Cloud downtime** | Low | Low | Have fallback screenshots/video if live demo fails. |
| **Devpost submission issues** | Low | Low | Submit 24 hours before deadline. Test submission form early. |

---

## 13. DEVPOST SUBMISSION PLAN

### 13.1 Project Name
**Shadow Cut**

### 13.2 Tagline
"The director still directs. The Shadow just remembers."

### 13.3 Elevator Pitch (100 words)
Film productions lose $50,000+ per day to continuity errors caught too late. Script supervisors are overwhelmed by multi-camera shoots and 30:1 shooting ratios. Shadow Cut is an AI script supervisor that watches every take in real-time, detects continuity errors while you're still on set, and alerts the director before the location is wrapped. For $7 per movie, it prevents $50,000+ reshoots — a 7,000x ROI. Built with Google Cloud Gemini, IBM Bob MCP servers, and Confluent streaming.

### 13.4 Tech Stack (For Devpost Form)
- Google Cloud: Gemini 2.5 Pro, Gemini 3.5 Flash-Lite, Gemini 3.6 Flash, Cloud Run, Firestore, Cloud Storage
- IBM: Bob (MCP server builder), watsonx Orchestrate
- Confluent: Kafka event streaming
- Open Source: YOLO-World, Python, FastAPI, Next.js

### 13.5 Screenshots Needed
1. Dashboard showing live production status
2. Alert notification with evidence card
3. Chat interface with director query and response
4. Trust report showing accuracy metrics
5. Plot Knowledge Graph visualization

### 13.6 Links Needed
- GitHub repo (public)
- Live demo URL (Cloud Run)
- Demo video (YouTube/Vimeo)

---

## 14. EXTERNAL VALIDATION SUMMARY

### 14.1 Third-Party AI Evaluation #1 (Claude 3.5 Sonnet)

An external AI evaluated Shadow Cut with no prior context:

| Criteria | Score | Quote |
|----------|-------|-------|
| Problem | 10/10 | "Massive, commercially visceral blind spot" |
| Architecture | Elite | "Cost-Aware Cascade is elite architecture design" |
| Differentiation | Yes | "Fundamentally different from SurgAgent" |
| Winning odds | 70-85% | "Provided your demo video isn't boring" |
| Biggest weakness | Execution | "Over-engineered plumbing colliding with 1-week bottleneck" |

**Key advice from external AI:**
1. Drop Confluent complexity — use minimal implementation
2. Use no-laptop time to build assets (storyboard, test clips, schemas)
3. Protect the 3-minute video at all costs
4. YOLO should be a spatial cropper, not a state analyzer
5. Explicitly state proxy workflow (H.264, not RAW)

### 14.2 Third-Party AI Evaluation #2 (Strict Evaluator — Direct Hackathon Page Research)

This evaluator checked the hackathon page directly and cross-referenced factual claims:

**Verified Correct:**
- ✅ Multi-cam continuity tracking is a documented, established pain point
- ✅ Tiered cascade (YOLO → Flash-Lite → Pro) is the right shape for cost/latency-constrained video pipeline
- ✅ IBM track requirements are accurate: Bob must be used in development, Confluent optional but strongly encouraged, projects without Bob usage disqualified from IBM track
- ✅ SurgAgent was a winning entry from a different, earlier hackathon (Dec 2025 Google Cloud/ODSC) — it's precedent, not competition
- ✅ 2,577 registered participants across 5 tracks. Registration overstates actual submissions — most never ship

**Critical Corrections:**
- ⚠️ **"Zero competition" claim is overstated.** Studiovity, ScriptE, Scriptation, and Storyflow already exist in AI continuity. The honest reframe: "nobody's doing automated computer-vision monitoring of actual footage during the shoot."
- ⚠️ **Timeline is the real threat, not the idea.** One week of laptop time to wire Confluent + Firestore + Cloud Run + real video testing + demo video (40% of decision) — everything must work first try.

**Bottom Line:**
> "The idea earns you a real look from judges. Whether you place comes down entirely to whether Aug 22–Sept 7 survives contact with reality."

### 14.3 SurgAgent Precedent

December 2025 Google Cloud AI Hackathon 1st place winner:
- Used Gemini + video + object detection + reasoning
- Achieved 98% accuracy on real surgical video
- Didn't even fully integrate YOLO (used as hypothetical options for Gemini)
- Proves this architectural pattern wins Google Cloud hackathons

Shadow Cut applies the same pattern to film production — a harder problem (non-linear, cross-scene, narrative intent) in an untouched niche.

---

## 15. OPEN QUESTIONS

### 15.1 Technical Questions

1. **Can Gemini Flash-Lite actually process video reliably?** → Test in Week 2 with real clip.
2. **What is the actual latency on a 4-minute take?** → Measure in Week 3.
3. **Does YOLO-World run fast enough on CPU for real-time?** → Benchmark in Week 2.
4. **How accurate is Gemini's audio transcription for director notes?** → Test in Week 2.
5. **Can we get away with Firestore instead of Vertex AI Vector Search?** → Test query performance in Week 3.

### 15.2 Demo Questions

1. **Where do we get test video clips with intentional errors?** → Film simple scenes with phone, or source Creative Commons clips.
2. **Should we use voiceover or text captions?** → Text captions are safer (no audio quality issues).
3. **What music should we use?** → Royalty-free cinematic underscore, low volume.
4. **How do we show the "before Shadow" vs. "after Shadow" contrast?** → Split screen: left = chaotic notebook, right = clean dashboard.

### 15.3 Business Questions

1. **Is this actually a viable product beyond the hackathon?** → Yes, if we can get to 95%+ accuracy and sub-10-second latency.
2. **Who pays for this?** → Production companies, studios, streaming platforms.
3. **What's the go-to-market?** → Start with indie films ($7 is nothing), prove value, scale to studios.
4. **What's the moat?** → The Plot Knowledge Graph + historical accuracy data. Gets better with every production.

---

## APPENDIX A: File Structure

```
shadow_cut/
├── README.md
├── TASKS.md
├── MASTER_DOC.md (this file)
├── requirements.txt
├── .gitignore
├── config/
│   ├── __init__.py
│   └── settings.py
├── models/
│   ├── __init__.py
│   └── data_models.py
├── core/
│   ├── __init__.py
│   ├── plot_graph.py
│   ├── confidence.py
│   ├── vision_pipeline.py
│   └── bridge.py
├── agents/
│   ├── __init__.py
│   ├── ingestion_agent.py
│   ├── memory_agent.py
│   ├── plot_agent.py
│   ├── continuity_agent.py
│   ├── flagging_agent.py
│   └── chat_agent.py
├── stream/
│   ├── __init__.py
│   └── confluent_consumer.py
├── ui/
│   ├── __init__.py
│   └── dashboard.py (Streamlit or Next.js)
├── data/
│   ├── __init__.py
│   ├── mock_generator.py
│   └── mock_output/
│       ├── script.json
│       ├── day1_takes.json
│       └── day5_takes.json
├── tests/
│   ├── __init__.py
│   └── test_pipeline.py
└── mcp_servers/
    ├── __init__.py
    ├── script_parser.py
    ├── analyze_take.py
    ├── check_continuity.py
    ├── flag_alert.py
    ├── query_memory.py
    └── generate_report.py
```

## APPENDIX B: Quick Reference

| Question | Answer |
|----------|--------|
| Hackathon deadline | Sept 7, 2026 @ 2:00pm PDT |
| Track | IBM |
| Prize for 1st | $7,500 |
| Total participants | ~2,450 |
| Our estimated odds | 70-85% (if demo is strong) |
| Laptop arrives | ~Aug 22-25 |
| Actual coding time | ~7 days (Bob week) |
| Total API cost (full movie) | ~$7 |
| Demo cost | ~$0.60 |
| ROI | 7,000x |
| Biggest risk | Over-engineering infrastructure |
| Second biggest risk | Weak demo video |
| Winning precedent | SurgAgent (Dec 2025 Google Cloud AI Hackathon) |
| Market gap | Zero on-set AI continuity tools exist |

---

*Document created: August 1, 2026*
*Last updated: August 2, 2026*
*Status: Architecture locked, awaiting real API testing*


---

## APPENDIX C: Deliverable Files

All zero-laptop deliverables are maintained as separate files for easy reference:

| File | Purpose | Status |
|------|---------|--------|
| `TASKS.md` | Living task tracker with checkboxes | Updated Aug 2 |
| `plot_graph_schema.json` | Strict JSON Schema for script extraction | Locked |
| `script_extraction_prompt.txt` | One-shot Gemini 2.5 Pro extraction prompt | Locked |
| `edge_cases.md` | 12 edge cases + CRITICAL/IMPORTANT/INCIDENTAL matrix | Locked |
| `mcp_tools_schema.json` | 7 IBM Bob MCP tool contracts (OpenAPI format) | Locked |
| `bob_quickstart.md` | Exact prompts to feed Bob on Day 1 of Bob Week | Locked |
| `confidence_escalation_logic.md` | Full algorithmic ruleset (PATCHED v2.0) | Locked |
| `confluent_schema.md` | Minimal streaming design (one topic, one consumer) | Locked |

*All files available for download from the project output directory.*
