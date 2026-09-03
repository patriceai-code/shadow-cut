# Shadow Cut — IBM Bob Quick-Start Guide
## What to Feed Bob on Day 1 of Bob Week

---

## Prompt 1: Project Scaffold

```
Bob, scaffold a Python project for Shadow Cut, an AI script supervisor for film production.

Requirements:
- Google ADK for agent orchestration
- FastAPI for REST API endpoints
- Confluent Kafka client for event streaming
- Firestore client for data storage  
- Google Cloud Storage client for video proxy pointers
- Gemini API client (google-genai) for multimodal analysis
- pytest for testing
- Docker for Cloud Run deployment

IMPORTANT: Include a local async webhook/FastAPI BackgroundTasks fallback for take uploads so the pipeline can run offline or without Kafka during local testing and demo recording. If Confluent connects cleanly, use it. If not, flip one flag to the fallback queue.

Directory structure should match:
  shadow_cut/
  ├── config/
  ├── models/
  ├── core/
  │   ├── plot_graph.py
  │   ├── confidence.py
  │   ├── vision_pipeline.py
  │   └── bridge.py
  ├── agents/
  ├── stream/
  ├── ui/
  ├── data/
  ├── tests/
  └── mcp_servers/

Create requirements.txt, Dockerfile, and basic config files.
```

---

## Prompt 2: MCP Server Implementation

```
Bob, implement the MCP server for Shadow Cut using the attached OpenAPI schema (mcp_tools_schema.json).

Build 7 @tool decorated methods:
1. parse_script(script_text, production_title, format="plain")
2. validate_prop_state(prop_name, detected_state, scene_number, take_id, yolo_evidence, previous_take_id=None)
3. check_continuity(current_take, scene_number, shot_number, previous_takes, graph_snapshot)
4. escalate_to_pro(case_id, flash_lite_result, yolo_math, scene_context, escalation_reason)
5. flag_alert(issue, confidence_score, plot_weight, category, director_history)
6. query_memory(question, scene_filter=None, character_filter=None, prop_filter=None, top_k=5)
7. generate_report(date, production_id)

Each tool must:
- Validate inputs against the schema
- Return the exact response structure defined in the schema
- Include proper error handling
- Be async where appropriate
- Include docstrings explaining when the tool is called
- CRITICAL: When creating Pydantic request/response models, import and bind data structures directly from plot_graph_schema.json so validation is strictly typed. Do NOT use generic Dict[str, Any] — use the exact schema definitions.

Generate the watsonx Orchestrate YAML spec for deployment.
```

---

## Prompt 3: Core Pipeline Integration

```
Bob, wire the core Shadow Cut pipeline:

1. When a new take uploads (triggered by Confluent event), call:
   - YOLO-World detection (local, every frame)
   - Flash-Lite validation (one API call with video + YOLO math + graph slice)
   - If needed, escalate_to_pro()
   - flag_alert() for final decision
   - Store result in Shadow Memory (Firestore)

2. The chat interface calls:
   - query_memory() for RAG retrieval
   - Gemini 3.6 Flash for answer generation

3. Daily report calls:
   - generate_report() with Trust Report metrics

Use the existing core/ modules (plot_graph.py, confidence.py, bridge.py) as reference.
```

---

## Prompt 4: Deployment

```
Bob, deploy Shadow Cut to Google Cloud:

1. Build Docker image for Cloud Run
2. Configure Firestore collections (takes, alerts, memory, reports)
3. Set up Confluent topic (shadow-cut.takes.uploaded)
4. Configure IAM roles (Cloud Run service account, Firestore access)
5. Set environment variables for Gemini API keys
6. Generate deployment report with URLs and test commands
```

---

## Files Bob Needs Access To

1. `mcp_tools_schema.json` — OpenAPI tool definitions
2. `plot_graph_schema.json` — Plot Knowledge Graph schema
3. `script_extraction_prompt.txt` — Gemini 2.5 Pro prompt
4. `edge_cases.md` — Edge case handling rules
5. `MASTER_DOC.md` — Full architecture reference
6. `core/*.py` — Existing Python modules

---

*Generated: August 2, 2026*
*For: IBM Bob Week (Aug 22-28)*
