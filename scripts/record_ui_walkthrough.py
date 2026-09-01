"""
Record live Next.js UI walkthrough using Playwright and Microsoft Edge.
Outputs high-res 1080p MP4 recording of all key views.
"""
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

output_dir = Path("demo_captures/ui_raw")
output_dir.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(channel="msedge", headless=True)
    context = browser.new_context(
        viewport={"width": 1920, "height": 1080},
        record_video_dir=str(output_dir),
        record_video_size={"width": 1920, "height": 1080},
    )
    page = context.new_page()

    print("Navigating to http://localhost:3000...")
    page.goto("http://localhost:3000", wait_until="networkidle")
    time.sleep(1.0)

    # 1. Dashboard View (11.55s)
    print("Capturing Dashboard View...")
    time.sleep(3.0)
    page.mouse.move(400, 300)
    time.sleep(0.5)
    page.mouse.wheel(0, 250)
    time.sleep(4.0)
    page.mouse.wheel(0, -250)
    time.sleep(4.0)

    # 2. Continuity Alerts & Script Deviations (6.89s)
    print("Navigating to Continuity Alerts...")
    alert_btn = page.get_by_role("button", name="Continuity Alerts")
    if not alert_btn.is_visible():
        alert_btn = page.get_by_text("Continuity Alerts", exact=False).first
    if alert_btn and alert_btn.is_visible():
        alert_btn.click()
        time.sleep(3.5)

    print("Navigating to Script Deviations...")
    script_btn = page.get_by_role("button", name="Script Deviations")
    if not script_btn.is_visible():
        script_btn = page.get_by_text("Script Deviations", exact=False).first
    if script_btn and script_btn.is_visible():
        script_btn.click()
        time.sleep(3.5)

    # 3. Chat View with Instant Grounded Response (7.57s)
    print("Navigating to Chat View...")
    chat_btn = page.get_by_role("button", name="Chat with Shadow")
    if not chat_btn.is_visible():
        chat_btn = page.get_by_text("Chat with Shadow", exact=False).first
    if chat_btn and chat_btn.is_visible():
        chat_btn.click()
        time.sleep(1.0)
        chat_input = page.get_by_placeholder("Ask Shadow about", exact=False)
        if not chat_input.is_visible():
            chat_input = page.locator("input[type='text']")
        if chat_input and chat_input.is_visible():
            chat_input.fill("What continuity issues were flagged in the living room?")
            time.sleep(0.8)
            page.keyboard.press("Enter")
            # Wait for response to populate
            page.wait_for_selector("text=Living Room Continuity Audit", timeout=6000)
            time.sleep(5.8)

    # 4. Trust Report View (12.13s)
    print("Navigating to Trust Report...")
    trust_btn = page.get_by_role("button", name="Trust Report")
    if not trust_btn.is_visible():
        trust_btn = page.get_by_text("Trust Report", exact=False).first
    if trust_btn and trust_btn.is_visible():
        trust_btn.click()
        time.sleep(3.5)
        page.mouse.wheel(0, 250)
        time.sleep(4.5)
        page.mouse.wheel(0, -250)
        time.sleep(4.5)

    print("Finishing capture...")
    context.close()
    browser.close()

# List generated video
for f in output_dir.glob("*.webm"):
    print(f"Recorded video: {f} ({f.stat().st_size} bytes)")
