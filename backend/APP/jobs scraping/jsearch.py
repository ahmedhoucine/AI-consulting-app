import requests
import json

url = "https://jsearch.p.rapidapi.com/search"

headers = {
    "X-RapidAPI-Key": "c19191ee31msh426d59fac6431f9p14bd42jsn8a92014748d6",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

all_jobs = []
for page in range(1, 6):  # pages 1 à 5
    params = {
        "query": "Devops Engineer",
        "page": str(page),
        "num_pages": "1",
        "location": "London"
    }

    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        jobs = data.get("data", [])
        print(f"Page {page} : {len(jobs)} jobs")
        all_jobs.extend(jobs)
    else:
        print(f"Erreur pour la page {page} : {response.status_code}")

print(f"Total jobs collectés : {len(all_jobs)}")

with open("jobs.json", "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=2)

print("✅ Jobs saved to jobs.json")
