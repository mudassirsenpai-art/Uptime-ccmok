import json
import os
import time
import requests

# GitHub Secret se cookies JSON read karna
cookies_raw = os.getenv("COOKIES_JSON")

if not cookies_raw:
    raise ValueError("COOKIES_JSON secret is missing or empty!")

# Target URL
target_url = "https://app.clusy.io/p/e01db55a-7cee-4039-a300-28aeaf1313ba/s/b4feb907-82be-47fa-8980-b445c7ae4af0"

# JSON load & parse
cookies_data = json.loads(cookies_raw)
cookies_dict = {cookie["name"]: cookie["value"] for cookie in cookies_data.get("cookies", [])}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Content-Type": "application/json"
}

print(f"Starting POST Ping loop for: {target_url}\n" + "-" * 50)

# Continuous loop for pings inside the workflow job execution
while True:
    try:
        response = requests.post(target_url, headers=headers, cookies=cookies_dict, timeout=10)
        
        if response.status_code == 200:
            print(f"[{time.strftime('%H:%M:%S')}] SUCCESS: 200 OK - Ping successfully delivered!")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] WARNING: Received status code {response.status_code}")
            
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] ERROR: Request failed - {e}")
        
    # GitHub Actions job timeout limits ke mutabiq safe delay interval
    time.sleep(30)
