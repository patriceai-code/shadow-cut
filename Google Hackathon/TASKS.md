# Shadow Cut — Project Task Tracker

## CURRENT PRIORITY: ZERO-LAPTOP EXECUTION (Before Laptop Arrives)
These deliverables require zero coding and can be built from a phone/tablet.
They strip-mine every non-coding task so Bob Week is purely compile, test, record.

### Zero-Laptop Deliverable 1: Voiceover Script ✅ DONE — LOCKED (9.5/10 external evaluation, micro-tweak applied)
- [x] Write word-for-word 3-minute voiceover script (400-450 words)
- [x] Time-code to 8 storyboard timestamps
- [x] Energetic, confident, professional tone
- [x] Added to MASTER_DOC.md

### Zero-Laptop Deliverable 2: Plot Knowledge Graph Schema & Prompt ✅ DONE — LOCKED
- [x] Define strict JSON Schema for script extraction
- [x] Separate critical_props (setup/payoff) from incidental_props (background)
- [x] Write the one-shot Gemini 2.5 Pro extraction prompt
- [x] Document edge cases (implied props, off-screen mentions)

### Zero-Laptop Deliverable 3: IBM Bob MCP Server Contracts ✅ DONE — LOCKED (PATCHED)
- [x] Define exact tool schemas (validate_prop_state, query_scene_continuity, escalate_to_pro)
- [x] Write OpenAPI/JSON specifications with strict component references
- [x] Document input/output contracts for each tool
- [x] Map tools to storyboard "Engine" section for demo
- [x] PATCH: Added Confluent fallback + local webhook queue to Bob prompts
- [x] PATCH: Enforced strict Pydantic schema binding (no Dict[str, Any])

### Zero-Laptop Deliverable 4: Confidence & Escalation Logic ✅ DONE — LOCKED v2.0 (PATCHED)
- [x] Fixed Multiplicative Dampening Trap — PlotWeight is now a gate (matrix), not a multiplier
- [x] Fixed Dead-Code Budget Guard — moved to top of function
- [x] Cold-start HistoricalAccuracy raised to 0.95
- [x] Define exact decision matrix (alert vs. silent log)
- [x] Write scoring weights algorithm
- [x] Document override handling (director dismisses → deprioritize)
- [x] Pseudocode ready to drop into backend

### Zero-Laptop Deliverable 5: Devpost Submission Narrative ✅ DONE — LOCKED
- [x] Write elevator pitch (100 words)
- [x] Write project description with problem/solution/impact
- [x] Document tech stack for Devpost form
- [x] Write "What I built" section
- [x] Write "How I built it" section
- [x] Write "Challenges I ran into" section
- [x] Write "Accomplishments I'm proud of" section
- [x] Write "What I learned" section
- [x] Write "What's next for Shadow Cut" section

### Zero-Laptop Deliverable 6: API Contracts Between Components ✅ DONE — LOCKED v2.0 (PATCHED)
- [x] Fixed @validator → @field_validator + @classmethod + ValidationInfo (Pydantic V2 compliance)
- [x] Fixed Dict leaks — TakeData and PropReference properly bound
- [x] Document YOLO → Bridge interface (input/output schemas)
- [x] Document Bridge → Flash-Lite interface
- [x] Document Flash-Lite → Pro escalation interface
- [x] Document Chat → RAG vector DB interface
- [x] Document Alert → Director notification interface
- [x] Document Confluent → Pipeline trigger interface
- [x] Document all error codes and retry logic

### Zero-Laptop Deliverable 7: Google Cloud Deployment Plan ✅ DONE — LOCKED
- [x] Map Cloud Run service architecture
- [x] Design Firestore data model (collections, documents, indexes)
- [x] Map IAM roles and permissions
- [x] Design Cloud Storage bucket structure
- [x] Document environment variables and secrets management
- [x] Plan CI/CD (or manual deployment strategy for hackathon)

### Zero-Laptop Deliverable 8: UI Wireframes & Design Specs ✅ DONE — LOCKED
- [x] Dashboard layout (dark theme, real-time updates, coverage map)
- [x] Alert card design (severity colors, evidence display, action buttons)
- [x] Chat interface layout (message bubbles, timestamp references, image thumbnails)
- [x] Trust Report dashboard (metrics, ROI counter, accuracy graph)
- [x] Mobile-responsive considerations
- [x] Color palette, typography, spacing tokens

### Zero-Laptop Deliverable 9: README & Setup Documentation ✅ DONE — LOCKED
- [x] Project overview and architecture diagram
- [x] Installation instructions
- [x] Environment setup (API keys, cloud accounts)
- [x] Quickstart guide (process a test take)
- [x] Contributing guidelines
- [x] License file


---

## Week 1: Architecture Lock (Aug 1-7)
- [x] Finalize data flow architecture
- [x] Build data models (Take, Alert, Scene, etc.)
- [x] Build Plot Knowledge Graph parser
- [x] Build Confidence Scoring Engine
- [x] Build Vision Pipeline scaffold
- [x] Build YOLO-to-Flash-Lite Bridge
- [x] Build Mock Data Generator
- [x] **PIPELINE TEST** — End-to-end mock test (Aug 1)
- [x] **DEMO VIDEO STORYBOARD** — Structure locked, 8 sections, IBM track optimized
- [x] **DEMO VIDEO VOICEOVER SCRIPT** — Word-for-word, time-coded, 400-450 words
- [x] **PLOT KNOWLEDGE GRAPH SCHEMA** — JSON Schema + extraction prompt + edge cases locked
- [x] Design simplified Confluent schema (one topic, one consumer) ✅ DONE — LOCKED
- [x] Design Google Cloud deployment plan → MOVED TO Zero-Laptop Deliverable 7
- [ ] Test with REAL Gemini API on a sample video
- [ ] Validate prompt quality with real model responses

## Week 2: Integration Design (Aug 8-14)
- [ ] Set up Google Cloud project (free tier)
- [ ] Set up Confluent Cloud (free trial)
- [ ] Set up IBM watsonx account
- [ ] Create GitHub repo (public, with license)
- [x] Write exact API contracts between components → MOVED TO Zero-Laptop Deliverable 6
- [x] Draft Devpost submission narrative → MOVED TO Zero-Laptop Deliverable 5
- [ ] Prepare sample video clips for demo (with intentional continuity errors)
- [ ] Test real video upload → Cloud Function → processing flow

## Week 3: Environment Prep (Aug 15-21)
- [ ] Deploy Cloud Run service skeleton
- [ ] Configure Firestore for Shadow Memory
- [ ] Set up Confluent topic + consumer (minimal)
- [ ] Test end-to-end with real video + real APIs
- [ ] Fix integration issues
- [ ] Validate cost model with real usage
- [ ] Record demo video B-roll (dashboard, chat, alerts)
- [x] Write README and setup docs → MOVED TO Zero-Laptop Deliverable 9

## Week 4: Bob Week (Aug 22-28) — LAPTOP ARRIVES
- [ ] Feed Bob the architecture docs
- [ ] Bob scaffolds production code
- [ ] Bob builds MCP servers
- [ ] Test, debug, fix integration issues
- [ ] Deploy final version to Google Cloud
- [ ] Record final demo video
- [ ] Submit to Devpost
- [ ] Cross fingers 🤞

## Current Status
**Week 1, Day 4 (Aug 3)** — Core architecture scaffolded, mock-tested, storyboard locked (10/10), voiceover script written (9.5/10), Plot Knowledge Graph schema + prompt + edge cases locked (9.5/10), IBM Bob MCP Server Contracts locked (9/10), Confidence & Escalation Logic locked v2.0 (bugs patched), Confluent schema locked (one topic, one consumer), Devpost narrative locked (10/10), API Contracts locked v2.0 (Pydantic V2 compliance), Google Cloud Deployment Plan locked (stupidly simple, $0 cost), UI Wireframes & Design Specs locked (9.5/10, 16:9 recording rule patched), **README & Setup Documentation locked (full quickstart, deployment guide, cost breakdown)**. **ALL ZERO-LAPTOP DELIVERABLES COMPLETE. WEEK 1 IS OFFICIALLY DONE.**
External AI evaluation: 8.5/10 storyboard → revised to 1st-place contender with IBM track optimization + Empress emotional hook injected.

## Honest Risk Assessment
- **HIGH CONFIDENCE:** Architecture, data flow, cost model, alert logic, problem validation, storyboard
- **MEDIUM CONFIDENCE:** Prompt quality (need real API test), voiceover delivery
- **LOW CONFIDENCE:** Real-world latency, edge cases, demo polish in 1 week
- **BIGGEST RISK:** Over-engineering infrastructure instead of investing in demo video
- **SECOND BIGGEST RISK:** Bob week is tight. Complex integrations need human debugging.
- **THIRD BIGGEST RISK:** Voiceover energy level — a flat voiceover kills an 8.5/10 video

## Bonus Prep Files (Chat-Only, No Laptop Needed) — ALL DONE

| # | File | Status |
|---|------|--------|
| B1 | Test Clip Scripts | ✅ DONE |
| B2 | Bob Week Prompts | ✅ DONE |
| B3 | Judge Q&A Prep | ✅ DONE |
| B4 | **Subtle Hollywood Bloopers Research** | ✅ DONE — Famous but NOT obvious errors that took years to spot |

