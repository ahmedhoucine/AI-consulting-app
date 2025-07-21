import requests
import csv
from datetime import datetime

APP_ID = "6a26d068"
APP_KEY = "08d20e5bc9de55c2f6e090e0b2d0e4e5"

url = "https://api.adzuna.com/v1/api/jobs/gb/search/1"

params = {
    "app_id": APP_ID,
    "app_key": APP_KEY,
    "what": "IT",
    "where": "france",
    "results_per_page": 1000,
    "sort_by": "date"
}

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    jobs = data.get("results", [])

    # CSV Output
    with open("adzuna_jobs_full.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "ID", "Job Title", "Publishing Date", "Start Date", "Salary",
            "Duration", "Location", "Work Mode", "Skills", "Description",
            "Plateforme", "Scrap Date", "Company Name", "Number of Candidates",
            "Number of Employees", "Sector", "Description E", "Experience",
            "Contract Type", "Education"
        ])

        for i, job in enumerate(jobs):
            title = job.get("title", "N/A")
            pub_date = job.get("created", "N/A")
            start_date = "N/A"
            salary_min = job.get("salary_min")
            salary_max = job.get("salary_max")
            salary = f"{salary_min} - {salary_max}" if salary_min and salary_max else "N/A"
            duration = "N/A"
            location = job.get("location", {}).get("display_name", "N/A")
            remote = job.get("telecommute", 0)
            work_mode = "Remote" if remote == 1 else "On-site"
            skills = "N/A"
            description = job.get("description", "N/A")
            plateforme = "Adzuna"
            scrap_date = datetime.now().strftime("%Y-%m-%d")
            company = job.get("company", {}).get("display_name", "N/A")
            candidates = "N/A"
            employees = "N/A"
            sector = job.get("category", {}).get("label", "N/A")
            description_e = description
            experience = "N/A"
            contract_type = job.get("contract_type", "N/A")
            education = "N/A"

            writer.writerow([
                i + 1, title, pub_date, start_date, salary, duration,
                location, work_mode, skills, description, plateforme, scrap_date,
                company, candidates, employees, sector, description_e,
                experience, contract_type, education
            ])

    print("✅ Jobs saved to adzuna_jobs_full.csv")

else:
    print(f"❌ API Error {response.status_code}")
    print(response.text)
