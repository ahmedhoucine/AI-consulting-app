import requests
import json

url = "https://jsearch.p.rapidapi.com/search"

headers = {
    "X-RapidAPI-Key": "c19191ee31msh426d59fac6431f9p14bd42jsn8a92014748d6",
    "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
}

params = {
    "query": "Devops Engineer",
    "page": "100",
    "num_pages": "1",
    "location": "London"
}

response = requests.get(url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    jobs = data.get("data", [])
    count = len(jobs)
    print(count)
    if jobs:
        job = jobs[0]
        mapped_job = {
        "ID": job.get("job_id", "non spécifié"),
        "Job Title": job.get("job_title", "non spécifié"),
        "Publishing Date": job.get("job_posted_at_datetime_utc", "non spécifié"),
        "Start Date": job.get("job_start_date", "non spécifié"),
        "Salary": f"{job.get('job_min_salary', 'non spécifié')} - {job.get('job_max_salary', 'non spécifié')}",
        "Duration": "non spécifié",
        "Location": job.get("job_location", "non spécifié"),
        "Work Mode": "Télétravail" if job.get("job_is_remote") else "Présentiel",
        "Skills": ", ".join(job.get("job_highlights", {}).get("Qualifications", [])) or "non spécifié",
        "Description": job.get("job_description", "non spécifié"),
        "Plateforme": job.get("job_apply_link", "non spécifié"),
        "Scrap Date": "non spécifié",  # Can be set to datetime.today().isoformat() if needed
        "Company Name": job.get("employer_name", "non spécifié"),
        "Number of Candidates": "non spécifié",
        "Number of Employees": job.get("employer_size", "non spécifié"),
        "Sector": "non spécifié",
        "Description E": "non spécifié",
        "Experience": f"{job.get('job_required_experience', {}).get('required_experience_in_months', 'non spécifié')} mois",
        "Contract Type": job.get("job_employment_type", "non spécifié"),
        "Education": job.get("job_required_education", {}).get("education_level", "non spécifié")
    }

    # Display the mapped job
   # print(json.dumps(mapped_job, indent=2))
