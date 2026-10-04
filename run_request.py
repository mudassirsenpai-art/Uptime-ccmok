import json
import os
import time
from playwright.sync_api import sync_playwright

cookies_raw = os.getenv("COOKIES_JSON")

if not cookies_raw:
    print("ERROR: COOKIES_JSON secret is missing!", flush=True)
    exit(1)

# Target URL
target_url = "https://app.clusy.io/p/e01db55a-7cee-4039-a300-28aeaf1313ba/s/b4feb907-82be-47fa-8980-b445c7ae4af0"

# Load JSON cookies
try:
    cookies_data = json.loads(cookies_raw)
    raw_cookies = cookies_data.get("cookies", [])
    
    # Format cookies for Playwright
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
    print(f"ERROR: Cookie JSON parse failed: {e}", flush=True)
    exit(1)

print("=== Starting Playwright Browser Session ===", flush=True)

with sync_playwright() as p:
    # Launch Chromium in headless mode
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )

    # Inject cookies before navigating
    context.add_cookies(playwright_cookies)
    page = context.new_page()

    print(f"Navigating to {target_url}...", flush=True)
    page.goto(target_url, wait_until="networkidle")

    print(f"Page loaded. Current Title: {page.title()}", flush=True)

    # Loop to keep the session active and trigger periodic reloads/pings
    # Note: GitHub Actions jobs have a timeout limit (default 6 hours)
    start_time = time.time()
    max_duration = 300  # Run for 5 minutes per workflow execution example
    
    while time.time() - start_time < max_duration:
        try:
            # Reload page or wait
            print(f"[{time.strftime('%H:%M:%S')}] Session active. Title: {page.title()}", flush=True)
            time.sleep(30)
            page.reload(wait_until="domcontentloaded")
        except Exception as e:
            print(f"[{time.strftime('%H:%M:%S')}] Page interaction error: {e}", flush=True)

    browser.close()
    print("Browser session closed safely.", flush=True)
