import serpapi
import json
import os

api_key = "ca19d55804da2eb1c1f8ed1215b4ae7eba35611d1c0b04e86ecc9fc78b29b076"
client = serpapi.Client(api_key=api_key)

job_titles = ["devops engineer", "cloud engineer", "site reliability engineer"]
locations = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]

output_file = 'serpapi_all_jobs.json'

# Load existing jobs if file exists
if os.path.exists(output_file):
    with open(output_file, 'r', encoding='utf-8') as f:
        all_jobs = json.load(f)
else:
    all_jobs = []

for title in job_titles:
    for loc in locations:
        print(f"Fetching jobs for '{title}' in '{loc}'...")
        params = {
            'engine': 'google_jobs',
            'q': title,
            'location': loc,
            'gl': 'fr',
            'hl': 'fr'
        }
        while True:
            results = client.search(params)
            jobs = results.get('jobs_results', [])
            all_jobs.extend(jobs)

            # Save after each page of results
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(all_jobs, f, ensure_ascii=False, indent=2)

            serpapi_pagination = results.get('serpapi_pagination', {})
            next_page_token = serpapi_pagination.get('next_page_token')

            if not next_page_token:
                break

            params['next_page_token'] = next_page_token
            params.pop('start', None)

print(f"Total jobs fetched: {len(all_jobs)}")
