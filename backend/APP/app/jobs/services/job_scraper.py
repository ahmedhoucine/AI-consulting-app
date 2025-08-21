import requests
import pandas as pd
from datetime import datetime
import time
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

BASE_URL = "https://api.adzuna.com/v1/api/jobs/fr/search/{page}"

TITLES = [# "data analyst", "data engineer", # "data scientist", "machine learning engineer", "devops engineer", #"devops engineer","AI engineer" #"software engineer", #"cloud engineer", "cybersecurity engineer", "product manager", #"qa engineer", "scrum master", "admin systèmes et réseaux", # "backend developer", "frontend developer", "fullstack developer", # "chef de projet informatique", "analyste cybersécurité", "ingénieur réseau", # "développeur python", "développeur java", "développeur node", "développeur .net" ,
     "informatique","administratif","Commercial" 
     ]
CITIES = [ "Paris",
          "Lyon", 
          # "Marseille","Toulouse","Nice","Nantes","Strasbourg","Montpellier","Bordeaux",
     #"Lille","Rennes","Reims","Grenoble","Angers","Saint-Étienne","Le Havre","Clermont-Ferrand","Tours","Aix-en-Provence" 
     ]

SKILL_KEYWORDS = [
    # Programming Languages
    "python", "java", "c#", "c++", "javascript", "typescript", "php", "ruby",
    
    # Web Development
    "html", "css", "react", "angular", "vue.js", "node.js", "next.js", "react native", "flutter", "swift", "kotlin",
    
    # Databases
    "sql", "mysql", "postgresql", "mongodb", "oracle", "redis",
    
    # Cloud Platforms
    "aws", "azure", "google cloud", "heroku",
    
    # DevOps / CI/CD
    "docker", "kubernetes", "jenkins", "gitlab ci", "terraform", "ansible",
    
    # Operating Systems
    "linux", "windows server", "macos",
    
    # Networking
    "tcp/ip", "vpn", "dns", "firewall", "routing", "switching",
    
    # Cybersecurity
    "ethical hacking", "penetration testing", "siem", "owasp",
    
    # AI / Machine Learning
    "tensorflow", "pytorch", "scikit-learn", "nlp", "computer vision",
    
    # Big Data
    "hadoop", "spark", "kafka",
    
    # Version Control
    "git", "github", "gitlab", "bitbucket",
    
    # Testing
    "unit testing", "integration testing", "selenium", "junit", "cypress",
    
    # APIs
    "restful api", "graphql", "soap",
    
    # Soft Skills - IT
    "problem-solving", "analytical thinking", "attention to detail", "teamwork", "project management", "scrum", "kanban",
    
    # Administrative / Office
    "microsoft word", "microsoft excel", "microsoft powerpoint", "microsoft outlook",
    "google docs", "google sheets", "google slides", "gmail", "calendar",
    "data entry", "database management", "filing", "document organization",
    "scheduling", "calendar management", "bookkeeping", "quickbooks", "sage",
    "office equipment", "crm", "report writing", "email management", "hr administration", "payroll", "onboarding",
    
    # Soft Skills - Administrative
    "organization", "time management", "communication", "multitasking", "team coordination",
    
    # Commercial / Sales
    "b2b sales", "b2c sales", "inside sales", "outside sales",
    "lead generation", "prospecting", "salesforce", "hubspot", "zoho crm",
    "market research", "negotiation", "closing deals", "product presentation",
    "account management", "e-commerce", "shopify", "woocommerce", "magento",
    "seo", "sem", "social media marketing", "kpi tracking", "customer support",
    
    # Soft Skills - Commercial
    "persuasion", "networking", "relationship management", "adaptability", "resilience", "goal orientation", "result-driven", "team collaboration"
]

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

def extract_skills(description, skill_list):
    if not description:
        return "non spécifié"
    description = description.lower()
    found_skills = {skill.lower() for skill in skill_list if skill.lower() in description}
    return ", ".join(sorted(found_skills)) if found_skills else "non spécifié"


def fetch_jobs(titles=TITLES, cities=CITIES, max_pages=8, results_per_page=50, sleep_time=1):
    """
    Fetch jobs from Adzuna API and return them as a DataFrame.
    """
    formatted_jobs = []

    for title in titles:
        for city in cities:
            print(f"\n=== Querying '{title}' jobs in {city} ===")
            for page in range(1, max_pages + 1):
                print(f"🔍 Fetching page {page}...")
                url = BASE_URL.format(page=page)
                params = {
                    "app_id": APP_ID,
                    "app_key": APP_KEY,
                    "results_per_page": results_per_page,
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
                        "Sector": "non spécifié" if get_value_or_default(job, "category", "label") == "Unknown"
                                   else get_value_or_default(job, "category", "label"),
                        "Description E": "non spécifié",
                        "Experience": "non spécifié",
                        "Contract Type": job.get("contract_type") or "non spécifié",
                        "Education": "non spécifié",
                        "estm_publishdate": "non spécifié",
                        "scrap_date_parsed": "non spécifié"
                    })

                time.sleep(sleep_time)

    return pd.DataFrame(formatted_jobs)
