import json
import os
import time
import pathlib
from playwright.sync_api import sync_playwright

# GitHub Secret kadun cookies gheta ahe
cookies_raw = os.getenv("COOKIES_JSON")

if not cookies_raw:
    print("ERROR: COOKIES_JSON secret nahi milala!", flush=True)
    exit(1)

target_url = "https://app.clusy.io/p/e01db55a-7cee-4039-a300-28aeaf1313ba/s/b4feb907-82be-47fa-8980-b445c7ae4af0"

try:
    cookies_data = json.loads(cookies_raw)
    raw_cookies = cookies_data.get("cookies", [])
    
    playwright_cookies = []
    for c in raw_cookies:
        cookie_obj = {
            "name": c["name"],
            "value": c["value"],
            "domain": c["domain"],
            "path": c.get("path", "/")
        }
        playwright_cookies.append(cookie_obj)

except Exception as e:
    print(f"ERROR: Cookie JSON parse fail zala -> {e}", flush=True)
    exit(1)

SHOT_DIR = pathlib.Path("screenshots")
SHOT_DIR.mkdir(exist_ok=True)

print("=== Starting Playwright Browser Session ===", flush=True)

with sync_playwright() as p:
    # Chromium browser launch
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    # Cookies add karne
    context.add_cookies(playwright_cookies)
    page = context.new_page()

    print(f"Opening page: {target_url}", flush=True)
    page.goto(target_url, wait_until="networkidle")

    print(f"Page Loaded! Title: {page.title()}", flush=True)
    page.screenshot(path=str(SHOT_DIR / "00_loaded.png"), full_page=True)

    # Continuous active ping loop (5 mins max limit per job run)
    start_time = time.time()
    max_duration = 300  # 5 Min Run

    while time.time() - start_time < max_duration:
        try:
            current_time = time.strftime('%H:%M:%S')
            print(f"[{current_time}] Ping Sent. Title: {page.title()} | URL: {page.url}", flush=True)
            shot = SHOT_DIR / f"ping_{time.strftime('%H%M%S')}.png"
            page.screenshot(path=str(shot), full_page=True)
            print(f"Screenshot saved: {shot}", flush=True)
            time.sleep(30)
            page.reload(wait_until="domcontentloaded")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Error: {e}", flush=True)

    browser.close()
    print("Browser closed successfully.", flush=True)
