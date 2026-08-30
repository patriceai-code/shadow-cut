"""
Shadow Cut — Confluent streaming layer with dead-simple webhook fallback.

Architecture
────────────
                     ┌──────────────────────────────┐
                     │  shadow-cut.takes.uploaded    │  Confluent Cloud
                     │  consumer group: shadow-pipeline│
                     └────────────┬─────────────────┘
                                  │ on connect success
                                  ▼
                     ┌──────────────────────────────┐
                     │        process_take()         │  same async handler
                     └────────────▲─────────────────┘
                                  │ on Confluent offline
                     ┌────────────┴─────────────────┐
                     │  POST /webhook/take-uploaded  │  FastAPI fallback
                     │  (identical TakeUploadedEvent)│
                     └──────────────────────────────┘

Both paths validate through TakeUploadedEvent → TakePayload before calling
the pipeline, so the handler receives exactly the same typed dict regardless
of which path delivered the event.
"""
from __future__ import annotations

import asyncio
import json
import logging
import threading
from typing import Awaitable, Callable

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, ValidationError

log = logging.getLogger(__name__)

# ─── Topic / group constants (single source of truth) ───────────────────────

TOPIC         = "shadow-cut.takes.uploaded"
CONSUMER_GROUP = "shadow-pipeline"
AUTO_OFFSET   = "earliest"


# ─── Typed payload models ───────────────────────────────────────────────────

class TakePayload(BaseModel):
    """Inner data object — what the pipeline actually processes."""

    take_id: str = Field(..., pattern=r"^s[0-9]+_sh[0-9]+_t[0-9]+$")
    video_path: str = Field(..., min_length=1)
    scene: int = Field(..., ge=1)
    shot: int = Field(..., ge=1)
    take: int = Field(..., ge=1)
    duration: float = Field(default=0.0, ge=0.0)
    production_id: str = Field(default="shadow-cut-hackathon")


class TakeUploadedEvent(BaseModel):
    """Full Confluent / webhook event envelope."""

    event_id: str = Field(..., pattern=r"^[a-f0-9-]{36}$")
    timestamp: str = Field(..., min_length=1)
    type: str = Field(default="take_uploaded")
    data: TakePayload            # typed inner payload — no Dict[str, Any]


# ─── Type alias for the pipeline callback ───────────────────────────────────

PipelineCallback = Callable[[TakePayload], Awaitable[None]]


# ─── Consumer ───────────────────────────────────────────────────────────────

class ShadowConsumer:
    """
    Confluent Kafka consumer.

    Runs in a background daemon thread so it doesn't block the FastAPI
    event loop.  Messages are dispatched to the async pipeline callback via
    ``asyncio.run_coroutine_threadsafe``, which safely bridges the sync
    consumer thread and the running asyncio loop.
    """

    def __init__(
        self,
        bootstrap_servers: str,
        api_key: str,
        api_secret: str,
        topic: str = TOPIC,
    ) -> None:
        self._config: dict = {
            "bootstrap.servers": bootstrap_servers,
            "security.protocol": "SASL_SSL",
            "sasl.mechanism": "PLAIN",
            "sasl.username": api_key,
            "sasl.password": api_secret,
            "group.id": CONSUMER_GROUP,
            "auto.offset.reset": AUTO_OFFSET,
            "enable.auto.commit": True,
            # Fail fast on probe so the fallback kicks in quickly
            "socket.timeout.ms": 5_000,
            "session.timeout.ms": 10_000,
        }
        self._topic   = topic
        self._consumer = None
        self._running  = False
        self._thread: threading.Thread | None = None

    # ── Probe ────────────────────────────────────────────────────────────────

    def probe(self) -> bool:
        """
        Return True if the Confluent cluster is reachable.

        Creates a throwaway AdminClient, lists topics with a 5-second
        timeout, and tears down immediately.  Safe to call before ``start``.
        """
        try:
            from confluent_kafka.admin import AdminClient
            admin = AdminClient({
                "bootstrap.servers": self._config["bootstrap.servers"],
                "security.protocol": self._config["security.protocol"],
                "sasl.mechanism":    self._config["sasl.mechanism"],
                "sasl.username":     self._config["sasl.username"],
                "sasl.password":     self._config["sasl.password"],
                "socket.timeout.ms": 5_000,
            })
            meta = admin.list_topics(timeout=5)
            return meta is not None
        except Exception as exc:
            log.warning("Confluent probe failed: %s", exc)
            return False

    # ── Start / stop ─────────────────────────────────────────────────────────

    def start(
        self,
        callback: PipelineCallback,
        loop: asyncio.AbstractEventLoop,
    ) -> None:
        """
        Subscribe and poll in a loop.

        ``loop`` must be the running asyncio event loop so that
        ``run_coroutine_threadsafe`` can schedule the callback safely.
        """
        from confluent_kafka import Consumer, KafkaException, KafkaError

        self._consumer = Consumer(self._config)
        self._consumer.subscribe([self._topic])
        self._running = True
        log.info("ShadowConsumer subscribed to %s (group: %s)", self._topic, CONSUMER_GROUP)

        while self._running:
            msg = self._consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue          # end of partition — normal, keep polling
                log.error("Kafka consumer error: %s", msg.error())
                continue

            raw = msg.value()
            if raw is None:
                continue

            try:
                envelope = json.loads(raw.decode("utf-8"))
                event    = TakeUploadedEvent.model_validate(envelope)
            except (json.JSONDecodeError, ValidationError) as exc:
                log.error("Invalid Kafka message, skipping: %s | raw=%r", exc, raw[:200])
                continue

            # Bridge sync thread → async event loop
            future = asyncio.run_coroutine_threadsafe(callback(event.data), loop)
            try:
                future.result(timeout=120)   # wait so backpressure is respected
            except Exception as exc:
                log.error("Pipeline callback raised for %s: %s", event.data.take_id, exc)

        self._consumer.close()
        log.info("ShadowConsumer stopped.")

    def start_in_thread(
        self,
        callback: PipelineCallback,
        loop: asyncio.AbstractEventLoop,
    ) -> threading.Thread:
        """Spawn a daemon thread running ``start`` and return it."""
        self._thread = threading.Thread(
            target=self.start,
            args=(callback, loop),
            daemon=True,
            name="shadow-consumer",
        )
        self._thread.start()
        return self._thread

    def stop(self) -> None:
        self._running = False


# ─── Webhook fallback ────────────────────────────────────────────────────────

def register_webhook(app: FastAPI, callback: PipelineCallback) -> None:
    """
    Register POST /webhook/take-uploaded on ``app``.

    The endpoint accepts the identical TakeUploadedEvent JSON that Confluent
    would deliver and feeds it through the same pipeline callback.  This makes
    the fallback path byte-for-byte identical to the streaming path — no
    separate code branches in the pipeline itself.

    Usage (direct HTTP call when Confluent is offline):

        curl -X POST http://localhost:8000/webhook/take-uploaded \\
          -H 'Content-Type: application/json' \\
          -d '{
            "event_id": "550e8400-e29b-41d4-a716-446655440000",
            "timestamp": "2026-08-02T10:00:00Z",
            "type": "take_uploaded",
            "data": {
              "take_id": "s5_sh2_t1",
              "video_path": "/tmp/shadow_cut/s5_sh2_t1.mp4",
              "scene": 5, "shot": 2, "take": 1, "duration": 90.0
            }
          }'
    """

    @app.post(
        "/webhook/take-uploaded",
        status_code=status.HTTP_202_ACCEPTED,
        summary="Fallback webhook — identical to Confluent event envelope",
        tags=["streaming"],
    )
    async def fallback_webhook(event: TakeUploadedEvent):
        """
        Receive a TakeUploadedEvent and dispatch it to the pipeline.

        Validates the full envelope (including the typed ``data`` field)
        before handing off, so malformed payloads are rejected with 422
        rather than propagating as runtime errors.
        """
        try:
            await callback(event.data)
        except Exception as exc:
            log.error("Pipeline error for %s via webhook: %s", event.data.take_id, exc)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Pipeline processing failed: {exc}",
            )

        return {
            "status": "accepted",
            "source": "webhook_fallback",
            "take_id": event.data.take_id,
        }
