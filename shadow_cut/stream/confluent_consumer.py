"""
Confluent consumer with fallback webhook.
One topic. One consumer. Fallback webhook for local offline demo.
"""
import asyncio
import json
import os
from fastapi import FastAPI, Request

class ShadowConsumer:
    def __init__(self, bootstrap_servers: str, api_key: str, api_secret: str, topic: str):
        self.config = {
            "bootstrap.servers": bootstrap_servers,
            "security.protocol": "SASL_SSL",
            "sasl.mechanism": "PLAIN",
            "sasl.username": api_key,
            "sasl.password": api_secret,
            "group.id": "shadow-pipeline",
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True
        }
        self.topic = topic
        self.consumer = None
        self.running = False

    def start(self, process_callback):
        try:
            from confluent_kafka import Consumer, KafkaException
            self.consumer = Consumer(self.config)
            self.consumer.subscribe([self.topic])
            self.running = True
            print(f"Subscribed to {self.topic}")

            while self.running:
                msg = self.consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    print(f"Consumer error: {msg.error()}")
                    continue

                try:
                    event = json.loads(msg.value().decode("utf-8"))
                    asyncio.create_task(process_callback(event.get("data", event)))
                except Exception as e:
                    print(f"Error processing message: {e}")

        except Exception as e:
            print(f"Kafka connection skipped/failed: {e}")
            print("Running in webhook fallback mode...")

    def stop(self):
        self.running = False
        if self.consumer:
            self.consumer.close()

def register_webhook(app: FastAPI, process_callback):
    @app.post("/webhook/take-uploaded")
    async def fallback_webhook(request: Request):
        event = await request.json()
        payload = event.get("data", event)
        await process_callback(payload)
        return {"status": "queued", "source": "webhook_fallback", "take_id": payload.get("take_id")}
    return fallback_webhook
