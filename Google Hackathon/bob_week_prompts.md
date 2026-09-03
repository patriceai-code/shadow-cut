# Shadow Cut — Bob Week: Copy-Paste Prompts
## Day 1 of Laptop Week: Feed These to IBM Bob Verbatim

---

## PROMPT 1: Project Scaffold (Day 1, Morning)

```
Bob, scaffold a production-ready Python project called "shadow_cut" for the Agentic Cinema Hackathon.

REQUIREMENTS:
- Python 3.11, Google ADK for agent orchestration
- FastAPI for REST API with Pydantic v2 models (STRICT typing — no Dict[str, Any] anywhere)
- Confluent Kafka client for event streaming
- Firestore client (native mode) for data persistence
- Google Cloud Storage client for video proxy uploads
- Google GenAI client for Gemini API (Flash-Lite, Pro, Flash)
- pytest + pytest-asyncio for testing
- python-dotenv for environment config
- uvicorn for ASGI server

DIRECTORY STRUCTURE:
shadow_cut/
├── config/          # Pydantic settings, env validation
├── models/          # ALL Pydantic v2 data models
├── core/            # Business logic (plot_graph, confidence, vision_pipeline, bridge)
├── agents/          # Google ADK agent definitions
├── stream/          # Confluent consumer + fallback webhook
├── api/             # FastAPI routes (takes, alerts, chat, reports)
├── mcp_servers/     # IBM Bob-built MCP tools
├── data/            # Mock data generators
└── tests/           # Test suite

Create requirements.txt, .env.example, and a working FastAPI hello-world endpoint.
Deploy a health-check route at GET /health that returns {"status": "ok", "version": "0.1.0"}.
```

---

## PROMPT 2: MCP Servers (Day 1, Afternoon)

```
Bob, build 6 MCP servers using Pydantic v2 strict models. Each tool must have @tool decorator, typed inputs, typed outputs, and ZERO Dict[str, Any].

TOOL 1: parse_script
- Input: script_text: str, format: Literal["pdf", "fountain", "txt"]
- Output: PlotKnowledgeGraph (Pydantic model with scenes, props, emotional_arcs, setups)
- Logic: Call Gemini 2.5 Pro with the extraction prompt, validate output against schema

TOOL 2: analyze_take
- Input: video_path: str, yolo_math: YoloMath, scene_context: SceneContext
- Output: FlashLiteResult (verdicts, performance_notes, audio_transcript, needs_escalation)
- Logic: Build prompt with video + YOLO math + scene context, call Gemini Flash-Lite

TOOL 3: check_continuity
- Input: current_take: Take, previous_takes: list[Take], plot_graph: PlotKnowledgeGraph
- Output: ContinuityReport (matches, mismatches, cross_scene_issues)
- Logic: Compare prop states, positions, emotional tones across takes

TOOL 4: flag_alert
- Input: anomaly: Anomaly, confidence: float, plot_weight: Literal["CRITICAL", "IMPORTANT", "INCIDENTAL"]
- Output: AlertDecision (action: Literal["ALERT", "SILENT_LOG", "SUPPRESS", "ESCALATE"], reasoning: str)
- Logic: Implement the Decision Matrix from confidence_escalation_logic.md exactly

TOOL 5: query_memory
- Input: question: str, scene_filter: int | None = None, top_k: int = 5
- Output: MemoryQueryResult (chunks: list[MemoryChunk], sources: list[str])
- Logic: Embed question, search vector DB, retrieve top_k chunks, format for chat

TOOL 6: generate_report
- Input: date_range: tuple[str, str], production_id: str
- Output: DailyReport (takes_analyzed, alerts_generated, accuracy, cost, savings_estimate)
- Logic: Aggregate Shadow Memory, calculate metrics, format Trust Report

Generate the server YAML spec for watsonx Orchestrate deployment.
ALL schemas must be Pydantic v2 with Field validators. No loose typing.
```

---

## PROMPT 3: Confluent Consumer + Fallback (Day 2, Morning)

```
Bob, implement the Confluent streaming layer with a dead-simple fallback.

REQUIREMENTS:
- One topic: "shadow-cut.takes.uploaded"
- One consumer group: "shadow-pipeline"
- Auto-offset: earliest
- Schema: TakeUploadedEvent (Pydantic model, see confluent_schema.md)

FALLBACK WEBHOOK (critical for hackathon reliability):
- FastAPI endpoint: POST /webhook/take-uploaded
- Receives identical TakeUploadedEvent JSON
- If Confluent is down, the Cloud Function calls this webhook directly
- Both paths feed into the same shadow_pipeline.process_take() function
- Zero behavioral difference between Confluent path and fallback path

IMPLEMENTATION:
- Consumer runs as async background task in FastAPI
- On message: validate schema, trigger pipeline, commit offset
- On failure: log error, retry 3x with exponential backoff, then dead-letter
- Webhook endpoint: identical validation, identical pipeline trigger

Document the fallback mechanism in code comments so judges can see it.
```

---

## PROMPT 4: UI Components (Day 2, Afternoon)

```
Bob, build the Next.js dashboard UI using these exact design tokens from ui_wireframes.md:

COLORS:
- bg-primary: #0a0a0f
- bg-secondary: #12121a
- accent-cyan: #00d4ff
- severity-critical: #ff3366
- severity-warning: #ffaa33
- severity-success: #33ff99
- text-primary: #f0f0f5
- text-secondary: #a0a0b0

COMPONENTS TO BUILD:
1. Dashboard page: Status cards (4-up), Coverage Map, Live Feed, Recent Alerts list
2. Alert Detail page: Severity header, confidence bar, frame comparison, script rule card, action buttons
3. Chat page: Message bubbles (director right/cyan, Shadow left/elevated), input bar, suggested prompts
4. Trust Report page: Accuracy donut, cost tracker, ROI hero card, bar charts, line graph

RULES:
- Tailwind CSS for styling
- shadcn/ui components as base (customize with our tokens)
- All demo data hardcoded from demo_mock_data.json
- Animations: alert slide-in (400ms), number count-up, progress bar fill
- Mobile responsive but optimize for 1024x768 tablet (demo recording)
- Dark theme ONLY — no light mode toggle

Connect to FastAPI backend at /api/* routes. Use React Query for data fetching.
```

---

## PROMPT 5: Integration & Polish (Day 3-4)

```
Bob, wire everything together and fix integration bugs.

TASKS:
1. Connect the Confluent consumer to the pipeline
2. Connect the pipeline to Firestore writes
3. Connect the API routes to the agents
4. Connect the UI to the API
5. Add error handling and logging
6. Add health checks for all external services
7. Generate a deployment report

DEBUGGING PRIORITIES:
- If Gemini API returns malformed JSON: retry with stricter prompt
- If YOLO math is empty: skip to Flash-Lite with video-only analysis
- If Firestore write fails: queue in memory, retry every 5 seconds
- If Confluent is down: webhook fallback activates automatically

DEPLOYMENT:
- Generate Dockerfile
- Generate Cloud Run service YAML
- Test locally with: docker build + docker run
- Deploy to Cloud Run
- Verify public URL works
```

---

## PROMPT 6: Demo Video Assets (Day 5-6)

```
Bob, help me generate the demo video assets.

ASSETS NEEDED:
1. Architecture diagram (SVG or PNG) showing the 3-tier cascade
2. IBM Bob MCP server diagram showing tools → agents → watsonx
3. Clean screenshots of each UI screen at 1440x900
4. Mock data consistency check: ensure all demo data references match across screens

SCREEN RECORDING SETUP:
- Browser viewport: 1440x900 (desktop) or 1024x768 (tablet)
- OBS canvas: 1920x1080
- Record each storyboard section separately for editing
- Use the voiceover script timestamps to time clicks

FINAL CHECKS:
- [ ] All UI text uses real production data (no "Lorem Ipsum")
- [ ] Alert screenshots show the watch + letter errors
- [ ] Chat screenshots show the "Which take did the letter stay folded?" query
- [ ] Trust Report shows $0.56 cost and 7,142x ROI
- [ ] IBM Bob logo appears in the Engine section (0:50-1:15)
```

---

## EMERGENCY FALLBACK: If Bob Breaks

If Bob generates broken code or gets stuck in loops:

1. **Regenerate from scratch:** Delete the file, paste the prompt again with "Start fresh"
2. **Narrow scope:** Instead of "build the whole UI," say "build just the AlertCard component"
3. **Use the mock pipeline:** The test_pipeline.py we wrote works. Use it as a reference implementation.
4. **Skip the feature:** If a component is eating time, cut it. The demo video is 40% of the decision.
5. **Manual override:** You know the architecture. You can write the code yourself if Bob fails.

---

*These prompts are designed to be copy-pasted verbatim into IBM Bob on Day 1 of laptop week.*
*Each prompt references the locked deliverables so Bob has full context.*
