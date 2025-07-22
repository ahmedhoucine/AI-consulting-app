import requests
import json

APP_ID = "3f027391"
APP_KEY = "2c2ef7f54d3aaf845b4ef8eff14c6771"

TITLE = "devops engineer"
CITY = "Paris"
PAGE = 1

BASE_URL = f"https://api.adzuna.com/v1/api/jobs/fr/search/{PAGE}"

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "results_per_page": 10,  # Only one job
    "what": TITLE,
    "where": CITY,
    "content-type": "application/json"
}

response = requests.get(BASE_URL, params=params)

if response.status_code == 200:
    data = response.json()
    job = data.get("results", []) # Get the first job
    print(json.dumps(job, indent=2, ensure_ascii=False))
else:
    print(f"❌ Failed to fetch job: {response.status_code}")
