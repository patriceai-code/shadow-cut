import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def capture():
    out_dir = Path("docs/images")
    out_dir.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="msedge", headless=True)
        page = await browser.new_page(viewport={"width": 1920, "height": 1080})

        print("Navigating to http://localhost:3000...")
        await page.goto("http://localhost:3000", wait_until="networkidle")
        await page.wait_for_timeout(2000)

        # 1. Dashboard Overview
        print("Capturing 1. dashboard_overview.png...")
        await page.screenshot(path=str(out_dir / "dashboard_overview.png"))

        # 2. Continuity Alerts & Triage View
        print("Clicking Continuity Alerts tab...")
        await page.click("text=Continuity Alerts")
        await page.wait_for_timeout(1000)
        print("Capturing 2. alert_triage.png...")
        await page.screenshot(path=str(out_dir / "alert_triage.png"))

        # 3. Chat with Shadow
        print("Clicking Chat with Shadow tab...")
        await page.click("text=Chat with Shadow")
        await page.wait_for_timeout(1000)
        
        input_box = page.locator("textarea, input[type='text']").last
        if await input_box.count() > 0:
            print("Submitting query to chat...")
            await input_box.fill("What was placed on the table in Scene 18?")
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(2000)
            
        print("Capturing 3. director_chat.png...")
        await page.screenshot(path=str(out_dir / "director_chat.png"))

        # 4. Trust Report
        print("Clicking Trust Report tab...")
        await page.click("text=Trust Report")
        await page.wait_for_timeout(1000)
        print("Capturing 4. trust_report.png...")
        await page.screenshot(path=str(out_dir / "trust_report.png"))

        await browser.close()
        print("All high-res screenshots captured in docs/images/!")

if __name__ == "__main__":
    asyncio.run(capture())
