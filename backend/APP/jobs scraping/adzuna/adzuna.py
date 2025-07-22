import requests
import pandas as pd
import time

APP_ID = "6a26d068"
APP_KEY = "08d20e5bc9de55c2f6e090e0b2d0e4e5"

TITLES = ["développeur", "ingénieur logiciel", "data analyst"]
CITIES = ["Paris", "Lyon", "Marseille", "Toulouse", "Lille"]

BASE_URL = "https://api.adzuna.com/v1/api/jobs/fr/search/{page}"

results = []

for title in TITLES:
    for city in CITIES:
        for page in range(1, 21):  # Max 20 pages
            print(f"🔍 Fetching: {title} in {city}, page {page}")
            url = BASE_URL.format(page=page)
            params = {
                "app_id": APP_ID,
                "app_key": APP_KEY,
                "results_per_page": 50,
                "what": title,
                "where": city,
                "content-type": "application/json"
            }

            response = requests.get(url, params=params)
            if response.status_code != 200:
                print(f"❌ Failed to fetch page {page}: {response.status_code}")
                break

            data = response.json()
            jobs = data.get("results", [])
            if not jobs:
                break  # No more results
            results.extend(jobs)

            time.sleep(1)  # avoid hitting rate limits

# Save all job dictionaries as-is
df = pd.DataFrame(results)
df.to_csv("adzuna_jobs_raw.csv", index=False, encoding='utf-8-sig')

print(f"✅ Total jobs saved: {len(results)}")
