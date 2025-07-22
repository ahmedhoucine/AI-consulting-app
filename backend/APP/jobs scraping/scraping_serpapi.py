import serpapi
import json

api_key = "443dfd5db14820e0de61247907c512cadf047e412a7308237e1f2a919b161a1b"
client = serpapi.Client(api_key=api_key)

job_titles = ["devops engineer", "cloud engineer", "site reliability engineer"]
locations = ["Paris", "Lyon", "Marseille", "Toulouse", "Nice"]

all_jobs = []

for title in job_titles:
    for loc in locations:
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

            serpapi_pagination = results.get('serpapi_pagination', {})
            next_page_token = serpapi_pagination.get('next_page_token')

            if not next_page_token:
                break

            params['next_page_token'] = next_page_token
            params.pop('start', None)


print(f"Total jobs fetched: {len(all_jobs)}")

# Save all jobs to a JSON file
with open('all_jobs.json', 'w', encoding='utf-8') as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=2)
