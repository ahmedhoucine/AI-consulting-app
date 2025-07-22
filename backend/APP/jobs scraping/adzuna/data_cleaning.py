import requests
import pandas as pd
from datetime import datetime
import time

APP_ID = "3f027391"
APP_KEY = "2c2ef7f54d3aaf845b4ef8eff14c6771	"

TITLES = [
     "data analyst", "data engineer",
    "data scientist", "machine learning engineer", "devops engineer", 
    "software engineer",
    "cloud engineer", "cybersecurity engineer",  "product manager",
    "qa engineer", "scrum master", "admin systèmes et réseaux",
     "backend developer", "frontend developer", "fullstack developer",
     "chef de projet informatique", "analyste cybersécurité", "ingénieur réseau",
         "développeur python", "développeur java", "développeur node", "développeur .net"

]
CITIES = [
    "Paris", "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", "Strasbourg",
    "Montpellier", "Bordeaux", "Lille", "Rennes", "Reims", "Grenoble",
    "Angers", "Saint-Étienne", "Le Havre", "Clermont-Ferrand", "Tours", "Aix-en-Provence"

]

BASE_URL = "https://api.adzuna.com/v1/api/jobs/fr/search/{page}"

formatted_jobs = []

def get_value_or_default(d, *keys, default="non spécifié"):
    for key in keys:
        if d is None or key not in d:
            return default
        d = d[key]
    return d if d else default

def fetch_with_retry(url, params, retries=3, delay=3):
    for attempt in range(retries):
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response
        print(f"⚠️ Attempt {attempt + 1} failed with {response.status_code}. Retrying in {delay}s...")
        time.sleep(delay)
    print(f"❌ Failed to fetch after {retries} attempts.")
    return None
SKILL_KEYWORDS = [
    # Programming Languages
    "python", "java", "javascript", "typescript", "c", "c++", "c#", "go", "rust", "php", "ruby", "kotlin",
    "swift", "scala", "perl", "matlab", "shell", "bash", "objective-c", "lua", "haskell", "dart",

    # Frontend Frameworks & Technologies
    "react", "angular", "vue", "next.js", "nuxt.js", "svelte", "jquery", "html", "css", "sass", "less",
    "tailwind", "bootstrap", "material-ui", "chakra-ui", "webpack", "vite", "redux", "ajax",

    # Backend Frameworks & Technologies
    "node.js", "express", "spring", "spring boot", "django", "flask", "laravel", "symfony", "asp.net", "dotnet",
    "fastapi", "gin", "rails", "nestjs", "strapi", "adonisjs",

    # Mobile Development
    "flutter", "react native", "swift", "objective-c", "android", "kotlin", "xamarin", "ionic", "cordova",

    # Databases
    "mysql", "postgresql", "mongodb", "sqlite", "oracle", "mariadb", "cassandra", "couchdb", "dynamodb", "redis",
    "neo4j", "elasticsearch", "firebase", "clickhouse", "snowflake", "bigquery", "hive", "influxdb",

    # Cloud Providers & Services
    "aws", "azure", "gcp", "google cloud", "lambda", "ec2", "s3", "cloudformation", "cloud run", "cloudflare",
    "digitalocean", "heroku", "netlify", "vercel",

    # DevOps & Infrastructure
    "docker", "kubernetes", "jenkins", "ansible", "terraform", "vagrant", "helm", "prometheus", "grafana",
    "circleci", "travisci", "github actions", "puppet", "gitlab ci", "logstash", "fluentd", "elastic stack",

    # Version Control
    "git", "github", "gitlab", "bitbucket", "svn",

    # APIs & Integration
    "rest", "graphql", "grpc", "soap", "openapi", "swagger", "postman",

    # Testing & Quality Assurance
    "tdd", "bdd", "jest", "mocha", "chai", "junit", "pytest", "selenium", "cypress", "playwright", "testing library",
    "postman", "karma",

    # Data Science & ML
    "pandas", "numpy", "scikit-learn", "tensorflow", "keras", "pytorch", "opencv", "matplotlib", "seaborn",
    "xgboost", "lightgbm", "spacy", "nltk", "statsmodels", "mlflow", "airflow", "dvc",

    # Data Engineering
    "spark", "hadoop", "kafka", "hive", "beam", "luigi", "dbt", "etl", "elt",

    # Monitoring & Logging
    "prometheus", "grafana", "datadog", "new relic", "splunk", "sentry", "elastic", "logstash", "fluentd", "jaeger", "opentelemetry",

    # Security
    "oauth", "jwt", "https", "ssl", "tls", "sso", "sast", "dast", "owasp", "iam", "burp suite", "zap",

    # Project & Workflow
    "jira", "trello", "asana", "notion", "slack", "monday.com", "confluence",

    # Soft Skills & Methodologies
    "agile", "scrum", "kanban", "devops", "ci/cd", "design thinking", "pair programming", "code review", "clean code",

    # Other Tools & Tech
    "linux", "unix", "windows server", "macos", "visual studio code", "intellij", "eclipse", "android studio", "xcode",
    "figma", "photoshop", "illustrator", "blender", "unity", "unreal engine"
]


def extract_skills(description, skill_list):
    if not description:
        return "non spécifié"
    description = description.lower()
    found_skills = set()
    for skill in skill_list:
        if skill.lower() in description:
            found_skills.add(skill.lower())
    return ", ".join(sorted(found_skills)) if found_skills else "non spécifié"

for title in TITLES:
    for city in CITIES:
        print(f"\n=== Querying '{title}' jobs in {city} ===")
        for page in range(1, 21):  # Max 20 pages per query
            print(f"🔍 Fetching page {page}...")
            url = BASE_URL.format(page=page)
            params = {
                "app_id": APP_ID,
                "app_key": APP_KEY,
                "results_per_page": 50,
                "what": title,
                "where": city,
                "content-type": "application/json"
            }

            response = fetch_with_retry(url, params)
            if not response:
                print(f"❌ Skipping page {page} due to repeated errors.")
                break

            data = response.json()
            jobs = data.get("results", [])
            if not jobs:
                print(f"⚠️ No more jobs found on page {page}, moving to next query.")
                break

            for job in jobs:
                salary_min = job.get("salary_min")
                salary_max = job.get("salary_max")
                salary = f"{salary_min} - {salary_max}" if salary_min and salary_max else "non spécifié"

                formatted_jobs.append({
                    "ID": len(formatted_jobs) + 1,
                    "Job Title": job.get("title") or "non spécifié",
                    "Publishing Date": job.get("created") or "non spécifié",
                    "Start Date": "non spécifié",
                    "Salary": salary,
                    "Duration": "non spécifié",
                    "Location": get_value_or_default(job, "location", "display_name"),
                    "Work Mode": job.get("contract_time") or "non spécifié",
                    "Skills": extract_skills(job.get("description", ""), SKILL_KEYWORDS),
                    "Description": job.get("description") or "non spécifié",
                    "Plateforme": "adzuna",
                    "Scrap Date": datetime.today().strftime('%Y-%m-%d'),
                    "Company Name": get_value_or_default(job, "company", "display_name"),
                    "Number of Candidates": "non spécifié",
                    "Number of Employees": "non spécifié",
                    "Sector": "non spécifié" if get_value_or_default(job, "category", "label") == "Unknown" else get_value_or_default(job, "category", "label"),
                    "Description E": "non spécifié",
                    "Experience": "non spécifié",
                    "Contract Type": job.get("contract_type") or "non spécifié",
                    "Education": "non spécifié"
                })

            time.sleep(1)  # avoid hitting rate limits

# Save to CSV
# Save or append to CSV
import os

df = pd.DataFrame(formatted_jobs)
file_path = "adzuna_jobs.csv"

if os.path.exists(file_path):
    # Append without headers
    df.to_csv(file_path, mode='a', index=False, header=False, encoding='utf-8-sig')
    print(f"\n✅ Appended {len(df)} new jobs to {file_path}")
else:
    # Create new file with headers
    df.to_csv(file_path, index=False, encoding='utf-8-sig')
    print(f"\n✅ Created {file_path} with {len(df)} jobs")

print(f"\n✅ Total jobs saved: {len(formatted_jobs)}")
