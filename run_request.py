import json
import os
import time
import requests

# Secrets se raw JSON read karna
cookies_raw = os.getenv("COOKIES_JSON")

if not cookies_raw:
    print("ERROR: COOKIES_JSON secret is missing!", flush=True)
    exit(1)

# Target Endpoint URL
target_url = "https://app.clusy.io/p/e01db55a-7cee-4039-a300-28aeaf1313ba/s/b4feb907-82be-47fa-8980-b445c7ae4af0"

# Parse Cookies
try:
    cookies_data = json.loads(cookies_raw)
    cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies_data.get("cookies", [])}
except Exception as e:
    print(f"ERROR: Cookie JSON parse fail hua - {e}", flush=True)
    exit(1)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}

print("=== Ping Script Started ===", flush=True)

# Continuous Loop (Har 30 second par Request)
while True:
    try:
        # Strict timeout added taaki request hang na ho
        response = requests.post(target_url, headers=headers, cookies=cookies_dict, timeout=10)
        
        current_time = time.strftime('%H:%M:%S')
        if response.status_code == 200:
            print(f"[{current_time}] SUCCESS: 200 OK - Pinged successfully!", flush=True)
        else:
            print(f"[{current_time}] WARNING: Status Code {response.status_code}", flush=True)
            
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ERROR: Request Failed -> {e}", flush=True)
        
    # Delay for 30 Seconds
    time.sleep(30)
