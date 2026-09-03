# Shadow Cut — Confluent Event Streaming Schema
## Zero-Laptop Deliverable: Minimal Streaming Design
### Status: LOCKED — One topic, one consumer, 20 lines of code

---

## Philosophy: Checkbox, Not Cathedral

IBM track "strongly encourages" Confluent. We use it. But we do not build a cathedral.

**One topic.** One consumer. One JSON schema. If Confluent fails, a local webhook queue catches the event. Zero complexity. Zero debugging nightmares.

---

## 1. TOPIC DESIGN

```
Topic Name: shadow-cut.takes.uploaded
Partitions: 1      (we don't need parallelism for hackathon scale)
Retention: 7 days  (enough for a production shoot, cheap)
```

**Why one topic?**
- The only event that matters is "a new take was uploaded"
- The Shadow pipeline is triggered by this single event
- Everything else (processing, alerting, logging) happens downstream in the pipeline
- Multiple topics = multiple failure points. One topic = one thing to debug.

---

## 2. EVENT SCHEMA

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "TakeUploadedEvent",
  "type": "object",
  "required": ["event_id", "timestamp", "type", "data"],
  "properties": {
    "event_id": {
      "type": "string",
      "format": "uuid",
      "description": "Unique event identifier for idempotency"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time",
      "description": "ISO 8601 UTC when the take finished uploading"
    },
    "type": {
      "type": "string",
      "enum": ["take_uploaded"],
      "description": "Event type — only one type exists"
    },
    "data": {
      "type": "object",
      "required": ["take_id", "scene", "shot", "take", "video_path", "duration"],
      "properties": {
        "take_id": {
          "type": "string",
          "pattern": "^s[0-9]+_sh[0-9]+_t[0-9]+$",
          "description": "Scene_Shot_Take identifier, e.g. s5_sh3_t2"
        },
        "scene": {
          "type": "integer",
          "minimum": 1,
          "description": "Scene number from script"
        },
        "shot": {
          "type": "integer",
          "minimum": 1,
          "description": "Shot number within scene"
        },
        "take": {
          "type": "integer",
          "minimum": 1,
          "description": "Take number for this shot"
        },
        "video_path": {
          "type": "string",
          "description": "GCS path to proxy video, e.g. gs://shadow-cut/proxies/s5_sh3_t2.mp4"
        },
        "proxy_path": {
          "type": "string",
          "description": "H.264 proxy path (same as video_path if already proxy)"
        },
        "duration": {
          "type": "number",
          "minimum": 0,
          "description": "Duration in seconds"
        },
        "uploaded_by": {
          "type": "string",
          "description": "DIT station identifier, e.g. dit_station_1"
        },
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

**Example event:**
```json
{
  "event_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2026-08-01T14:23:00Z",
  "type": "take_uploaded",
  "data": {
    "take_id": "s5_sh3_t2",
    "scene": 5,
    "shot": 3,
    "take": 2,
    "video_path": "gs://shadow-cut/proxies/s5_sh3_t2.mp4",
    "proxy_path": "gs://shadow-cut/proxies/s5_sh3_t2.mp4",
    "duration": 242.5,
    "uploaded_by": "dit_station_1",
    "slate_metadata": {
      "date": "2026-08-01",
      "director": "Jane Smith",
      "dp": "Alex Chen"
    }
  }
}
```

---

## 3. CONSUMER DESIGN

```
Consumer Group: shadow-pipeline
Consumers: 1     (one instance of the Shadow pipeline)
Auto-offset: earliest (process from beginning if consumer restarts)
```

**What the consumer does:**
1. Receives `take_uploaded` event
2. Acknowledges immediately (don't block the stream)
3. Triggers the Shadow pipeline asynchronously:
   - YOLO processing
   - Flash-Lite validation
   - Confidence scoring
   - Alert decision
4. Logs outcome to Firestore

**Pseudocode:**
```python
from confluent_kafka import Consumer

consumer = Consumer({
    'bootstrap.servers': os.getenv('CONFLUENT_BOOTSTRAP'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanism': 'PLAIN',
    'sasl.username': os.getenv('CONFLUENT_API_KEY'),
    'sasl.password': os.getenv('CONFLUENT_API_SECRET'),
    'group.id': 'shadow-pipeline',
    'auto.offset.reset': 'earliest'
})

consumer.subscribe(['shadow-cut.takes.uploaded'])

while True:
    msg = consumer.poll(timeout=1.0)
    if msg is None:
        continue

    event = json.loads(msg.value())

    # Acknowledge immediately — don't block stream
    consumer.commit(msg)

    # Trigger pipeline asynchronously
    asyncio.create_task(shadow_pipeline.process_take(event['data']))
```

---

## 4. FALLBACK: LOCAL WEBHOOK QUEUE

If Confluent is down, misconfigured, or the free trial expires:

```python
# Fallback: Cloud Function HTTP endpoint
@app.post("/webhook/take-uploaded")
async def fallback_webhook(event: TakeUploadedEvent):
    # Receives events directly when Confluent is unavailable
    await shadow_pipeline.process_take(event.data)
    return {"status": "queued"}
```

**How it works:**
- DIT upload triggers Cloud Function via HTTP
- Cloud Function tries Confluent first
- If Confluent fails → directly calls `/webhook/take-uploaded`
- Event is processed identically, just without the streaming layer
- Shadow pipeline doesn't know or care which path the event took

**This is our safety net.** The hackathon judges see Confluent in the code. If it breaks during judging, the fallback keeps everything working.

---

## 5. WHY THIS IS ENOUGH

| Complexity We Skip | Why |
|-------------------|-----|
| Multiple topics | One event type = one topic |
| Stream processing (Flink) | We don't transform streams, just trigger pipelines |
| Schema Registry | One schema, version 1, hardcoded |
| Consumer groups with multiple instances | One consumer is plenty for hackathon scale |
| Exactly-once semantics | At-least-once is fine; pipeline is idempotent by take_id |
| Dead letter queues | Fallback webhook handles failures |

**Lines of Confluent-specific code in production: ~20**
**Lines of fallback code: ~10**
**Total streaming complexity: ~30 lines**

---

## 6. COST

| Item | Cost |
|------|------|
| Confluent Cloud (free trial) | $0 for 30 days |
| After trial (minimal usage) | ~$0-5/month |
| Fallback webhook (Cloud Run) | $0 (within free tier) |

---

*Document version: 1.0*
*Status: LOCKED — Zero-Laptop Deliverable*
*Philosophy: Checkbox, not cathedral*
*Last updated: August 2, 2026*
