# Shadow Cut 🎬

> **The director still directs. The Shadow just remembers.**

[![Hackathon](https://img.shields.io/badge/Agentic%20Cinema-IBM%20Track-blue)](https://agentic-cinema.devpost.com/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Gemini%20%7C%20Cloud%20Run%20%7C%20Firestore-4285F4?logo=google-cloud)](https://cloud.google.com/)
[![IBM](https://img.shields.io/badge/IBM-Bob%20%7C%20watsonx-054ADA?logo=ibm)](https://www.ibm.com/watsonx)
[![Confluent](https://img.shields.io/badge/Confluent-Kafka%20Streaming-000000?logo=apache-kafka)](https://www.confluent.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**Shadow Cut** is an AI script supervisor for film production. It watches every take as it's uploaded, detects continuity errors in real-time, and alerts the director while they're still on set — before the location is wrapped and reshoots cost $50,000+ per day.

For **$7 per movie**, it prevents **$50,000+ reshoots**. That's a **7,000x ROI**.

---

## 🎥 Demo Video

[![Shadow Cut Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://youtube.com/watch?v=YOUR_VIDEO_ID)

**[▶ Watch the 3-minute demo](https://youtube.com/watch?v=YOUR_VIDEO_ID)**

---

## 🎯 The Problem

Modern film production has created a crisis for script supervisors:

- **3-4 cameras** shooting simultaneously — "almost humanly impossible to follow" (*Dawn Gilliam, The Hunger Games*)
- **30:1 to 150:1 shooting ratios** — thousands of takes per production
- **Continuity errors caught in post** cost $20,000-$100,000+ per reshoot day
- **Zero AI tools** exist for on-set continuity assistance during production

Every AI filmmaking tool is either **pre-production** (scheduling, breakdowns) or **post-production** (editing, VFX). The production phase itself is a complete blind spot in a $25.48 billion market.

---

## 💡 The Solution

Shadow Cut is an invisible AI assistant that:

1. **Reads the script** before Day 1 and builds a **Plot Knowledge Graph** — which props are critical, which are incidental, emotional arcs, setup/payoff links
2. **Watches every take** as it's uploaded by the DIT
3. **Compares** the take against previous takes AND the script's requirements
4. **Alerts the director** only when something genuinely matters — with confidence scores, evidence, and script context
5. **Answers questions** via chat — "What did I say about Scene 5?" "Did the watch move?"

**The director is still the artist. The Shadow just remembers.**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PRE-PRODUCTION                                  │
│  ┌─────────────┐    ┌─────────────────────────────┐    ┌─────────────────┐  │
│  │   Script    │───▶│  Gemini 2.5 Pro (1M tokens)  │───▶│ Plot Knowledge  │  │
│  │  (PDF/TXT)  │    │  Script Parser               │    │    Graph        │  │
│  └─────────────┘    └─────────────────────────────┘    └─────────────────┘  │
│                                                                  │           │
│                                                                  ▼           │
│                                                         ┌─────────────────┐  │
│                                                         │    Firestore    │  │
│                                                         └─────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              DURING PRODUCTION                               │
│                                                                              │
│  Camera ──▶ Card ──▶ DIT Uploads H.264 Proxy ──▶ Google Cloud Storage        │
│                                                          │                   │
│                                                          ▼                   │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TIER 1: YOLO-WORLD (Local, Every Frame, $0)                        │   │
│  │  • Detects props from script vocabulary                             │   │
│  │  • Tracks positions, states, presence                              │   │
│  │  • Flags anomalies instantly                                       │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TIER 2: GEMINI FLASH-LITE (~$0.002/take)                            │   │
│  │  • Validates YOLO flags with script context                         │   │
│  │  • Checks for things YOLO missed                                    │   │
│  │  • Analyzes performance + transcribes audio                         │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼ (if uncertain + CRITICAL)               │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  TIER 3: GEMINI PRO (~$0.10/escalation)                            │   │
│  │  • Deep reasoning on cross-scene continuity                         │   │
│  │  • Complex narrative logic validation                               │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                                    ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  CONFIDENCE ENGINE                                                   │   │
│  │  • TechnicalConfidence = Evidence × History × Trust                │   │
│  │  • PlotWeight is a gate (CRITICAL/IMPORTANT/INCIDENTAL)            │   │
│  │  • < 70% confidence → NEVER alert                                  │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                         │
│                    ┌───────────────┴───────────────┐                         │
│                    ▼                               ▼                         │
│           ┌─────────────┐                 ┌─────────────┐                    │
│           │ PUSH ALERT  │                 │ SILENT LOG  │                    │
│           │  (>85% +    │                 │  (chat-     │                    │
│           │  CRITICAL)  │                 │  queryable) │                    │
│           └─────────────┘                 └─────────────┘                    │
│                    │                               │                         │
│                    ▼                               ▼                         │
│           ┌─────────────┐                 ┌─────────────┐                    │
│           │  Director   │                 │   RAG       │                    │
│           │  Phone/Tab  │                 │  Vector DB  │                    │
│           └─────────────┘                 └─────────────┘                    │
│                                                          │                   │
│                                                          ▼                   │
│                                                 ┌─────────────┐              │
│                                                 │  Chat Bot   │              │
│                                                 │  (Gemini    │              │
│                                                 │   3.6 Flash)│              │
│                                                 └─────────────┘              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Multi-Agent Cascade

| Tier | Model | Job | Cost | Speed |
|------|-------|-----|------|-------|
| **YOLO** | Local (open-source) | Detect props on every frame | **$0** | Real-time |
| **Flash-Lite** | Gemini 3.5 Flash-Lite | Validate anomalies + audio | **~$0.002/take** | ~20 sec |
| **Pro** | Gemini 2.5/3.1 Pro | Deep reasoning (rare) | **~$0.10/escalation** | ~15 sec |
| **Chat** | Gemini 3.6 Flash | Director Q&A | **~$0.01/query** | ~2 sec |

### IBM Bob Integration

IBM Bob is not just our IDE — it's our **runtime infrastructure**:

- Bob built the **MCP servers** that power every tool our agents call
- Bob's `@tool` decorated methods handle: script parsing, continuity checking, memory queries, alert flagging
- Bob deployed the agent to **watsonx Orchestrate**

**Shallow Bob usage:** "We used Bob to help write code."  
**Deep Bob usage (us):** "Bob's MCP framework IS our agent's nervous system."

---

## 🚀 Quickstart

### Prerequisites

- Python 3.11+
- Node.js 18+ (for UI)
- Google Cloud account (free tier sufficient)
- IBM watsonx account (for Bob deployment)
- Confluent Cloud account (free trial)

### 1. Clone & Install

```bash
git clone https://github.com/yourname/shadow-cut.git
cd shadow-cut

# Backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd ui
npm install
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json
GEMINI_API_KEY=your-gemini-api-key

# IBM watsonx / Bob
IBM_WATSONX_API_KEY=your-ibm-key
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com

# Confluent
CONFLUENT_BOOTSTRAP_SERVERS=your-cluster.kafka.cloud:9092
CONFLUENT_API_KEY=your-confluent-key
CONFLUENT_API_SECRET=your-confluent-secret
CONFLUENT_TOPIC=shadow-cut.takes.uploaded

# Firestore
FIRESTORE_PROJECT_ID=your-project-id

# Cloud Storage
GCS_BUCKET=your-bucket-name

# App
SHADOW_CUT_ENV=development
LOG_LEVEL=INFO
```

### 3. Set Up Google Cloud

```bash
# Enable APIs
gcloud services enable run.googleapis.com
gcloud services enable firestore.googleapis.com
gcloud services enable storage.googleapis.com
gcloud services enable aiplatform.googleapis.com

# Create Firestore database (Native mode)
gcloud firestore databases create --location=nam5 --type=firestore-native

# Create Cloud Storage bucket
gsutil mb -l us-central1 gs://your-bucket-name

# Create service account
gcloud iam service-accounts create shadow-cut-sa   --display-name="Shadow Cut Service Account"

gcloud projects add-iam-policy-binding your-project-id   --member="serviceAccount:shadow-cut-sa@your-project-id.iam.gserviceaccount.com"   --role="roles/datastore.user"

gcloud projects add-iam-policy-binding your-project-id   --member="serviceAccount:shadow-cut-sa@your-project-id.iam.gserviceaccount.com"   --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding your-project-id   --member="serviceAccount:shadow-cut-sa@your-project-id.iam.gserviceaccount.com"   --role="roles/aiplatform.user"

# Download key
gcloud iam service-accounts keys create service-account.json   --iam-account=shadow-cut-sa@your-project-id.iam.gserviceaccount.com
```

### 4. Set Up Confluent (Minimal — One Topic, One Consumer)

```bash
# Create topic (via Confluent Cloud UI or CLI)
confluent kafka topic create shadow-cut.takes.uploaded   --partitions 1   --replication-factor 3

# Create API key for the consumer
confluent api-key create --resource your-cluster-id
```

### 5. Build the Plot Knowledge Graph

```bash
python -m shadow_cut.script_parser --script data/your_script.pdf
# Output: plot_graph.json (stored in Firestore)
```

### 6. Run Locally

```bash
# Terminal 1: Backend
python -m shadow_cut.api
# → http://localhost:8000

# Terminal 2: Stream consumer
python -m shadow_cut.stream.consumer

# Terminal 3: UI
npm run dev
# → http://localhost:3000
```

### 7. Process a Test Take

```bash
# Upload a test video
curl -X POST http://localhost:8000/api/takes/upload   -F "video=@test_take.mp4"   -F "scene=5"   -F "shot=3"   -F "take=4"

# Check the alert (or watch the dashboard)
curl http://localhost:8000/api/alerts/latest
```

---

## 📁 Project Structure

```
shadow_cut/
├── README.md                 # This file
├── TASKS.md                  # Living task tracker
├── MASTER_DOC.md             # Full architecture & design specs
├── LICENSE                   # MIT License
├── requirements.txt          # Python dependencies
├── .env.example              # Environment template
├── .gitignore
│
├── config/                   # Configuration
│   ├── __init__.py
│   └── settings.py           # Pydantic settings, env validation
│
├── models/                   # Data models (Pydantic v2)
│   ├── __init__.py
│   └── data_models.py        # Take, Alert, Scene, Prop, etc.
│
├── core/                     # Core business logic
│   ├── __init__.py
│   ├── plot_graph.py         # Script → Plot Knowledge Graph
│   ├── confidence.py         # Trustworthy confidence scoring
│   ├── vision_pipeline.py    # Frame sampling, YOLO, Gemini Vision
│   └── bridge.py             # YOLO math → Flash-Lite validation
│
├── agents/                   # Google ADK agents
│   ├── __init__.py
│   ├── ingestion_agent.py    # Normalize incoming data
│   ├── memory_agent.py       # Store/retrieve Shadow Memory
│   ├── plot_agent.py         # Query Plot Knowledge Graph
│   ├── continuity_agent.py   # Detect mismatches
│   ├── flagging_agent.py     # Alert vs. silent log decision
│   └── chat_agent.py         # Director Q&A
│
├── stream/                   # Confluent integration
│   ├── __init__.py
│   └── confluent_consumer.py # One topic, one consumer, fallback webhook
│
├── api/                      # FastAPI backend
│   ├── __init__.py
│   ├── main.py               # FastAPI app
│   ├── routes/
│   │   ├── takes.py          # Upload, status, list
│   │   ├── alerts.py         # Get, dismiss, resolve
│   │   ├── chat.py           # Query, history
│   │   └── reports.py        # Trust report, metrics
│   └── dependencies.py       # Auth, DB clients
│
├── ui/                       # Next.js frontend
│   ├── app/                  # App router
│   ├── components/           # Reusable components
│   │   ├── AlertCard.tsx
│   │   ├── ChatBubble.tsx
│   │   ├── CoverageMap.tsx
│   │   ├── ConfidenceBar.tsx
│   │   ├── FrameComparison.tsx
│   │   ├── LiveFeed.tsx
│   │   ├── TrustReport.tsx
│   │   └── SkeletonLoader.tsx
│   ├── lib/                  # Utils, API clients
│   ├── styles/               # Tailwind config, globals
│   └── public/               # Static assets
│
├── mcp_servers/              # IBM Bob-built MCP tools
│   ├── __init__.py
│   ├── script_parser.py      # parse_script tool
│   ├── analyze_take.py       # analyze_take tool
│   ├── check_continuity.py   # check_continuity tool
│   ├── flag_alert.py         # flag_alert tool
│   ├── query_memory.py       # query_memory tool
│   └── generate_report.py    # generate_report tool
│
├── data/                     # Test data & mocks
│   ├── __init__.py
│   ├── mock_generator.py
│   └── mock_output/
│       ├── script.json
│       ├── day1_takes.json
│       └── day5_takes.json
│
└── tests/                    # Test suite
    ├── __init__.py
    ├── test_pipeline.py      # End-to-end mock pipeline
    ├── test_confidence.py    # Confidence engine unit tests
    └── test_api.py           # API integration tests
```

---

## 🧪 Testing

### Run the Mock Pipeline (No API calls, no real video)

```bash
python -m tests.test_pipeline
# Validates: script parsing → YOLO math → confidence scoring → alerts
```

### Run Unit Tests

```bash
pytest tests/ -v
```

### Test with Real Video

```bash
# Upload a test clip with an intentional continuity error
python -m shadow_cut.test_real_video --video test_clips/watch_error.mp4
```

---

## 🌐 Deployment

### Deploy to Google Cloud Run

```bash
# Build (Artifact Registry — gcr.io deprecated 2025)
# One-time: create the repository
gcloud artifacts repositories create shadow-cut-repo \
  --repository-format=docker \
  --location=us-central1 \
  --description="Shadow Cut container images" \
  2>/dev/null || echo "Repo already exists"

gcloud builds submit --tag us-central1-docker.pkg.dev/your-project-id/shadow-cut-repo/shadow-cut

# Deploy
gcloud run deploy shadow-cut   --image us-central1-docker.pkg.dev/your-project-id/shadow-cut-repo/shadow-cut   --platform managed   --region us-central1   --allow-unauthenticated   --set-env-vars "GOOGLE_CLOUD_PROJECT=your-project-id"   --set-env-vars "GEMINI_API_KEY=your-key"
```

**Cost:** Free tier covers everything for the hackathon demo. Real production: ~$7 per movie.

---

## 📊 Cost Breakdown

| Component | Per-Take | Full Movie (500 takes) |
|-----------|----------|------------------------|
| YOLO processing | $0.00 | $0.00 |
| Flash-Lite analysis | $0.002 | $1.00 |
| Pro escalation (10%) | $0.10 | $5.00 |
| Storage | ~$0.0001 | $0.05 |
| Cloud Run (free tier) | $0.00 | $0.00 |
| Firestore (free tier) | $0.00 | $0.00 |
| **Total** | **~$0.012** | **~$7.00** |

**ROI:** One prevented reshoot day saves $50,000+. **7,000x return on investment.**

---

## 🤝 Contributing

This project was built for the **Agentic Cinema Hackathon** (IBM Track). While it's primarily a solo effort for the competition, contributions are welcome post-hackathon.

### How to Contribute

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/amazing-thing`
3. Commit your changes: `git commit -m 'Add amazing thing'`
4. Push to the branch: `git push origin feature/amazing-thing`
5. Open a Pull Request

### Development Guidelines

- **Pydantic v2** for ALL data models — no `Dict[str, Any]`
- **Type hints** everywhere
- **Tests** for every core function
- **No external AI APIs** — Google Cloud Gemini only (hackathon rule)
- **Dark theme first** — all UI components must work in low-light environments

---

## 📜 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

- **Google Cloud** — Gemini models, Cloud Run, Firestore
- **IBM** — Bob MCP server builder, watsonx Orchestrate
- **Confluent** — Kafka event streaming
- **YOLO-World** — Open-vocabulary object detection
- **SurgAgent** — Proved the Gemini + video + object detection architecture wins hackathons

---

## 📬 Contact

- **Devpost:** [Shadow Cut](https://devpost.com/software/shadow-cut)
- **Demo:** [shadow-cut-demo.web.app](https://shadow-cut-demo.web.app)
- **Email:** your-email@example.com

---

<p align="center">
  <strong>Built for Agentic Cinema 2026 🎬</strong><br>
  <em>The director still directs. The Shadow just remembers.</em>
</p>
