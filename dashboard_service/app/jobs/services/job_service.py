import pandas as pd
from typing import Optional
from dotenv import load_dotenv
import os
import requests
from app.jobs.domain.job_entity import JobRecord
from app.jobs.repositories.job_repository import JobRepositoryInterface
from app.jobs.services.job_scraper import fetch_jobs
from app.job_clustering.services.cluster_service import ClusterService

class JobService:
    def __init__(self, job_repository: JobRepositoryInterface):
        self.job_repository = job_repository
    
    def reinitialize_recommendation(self):
        try:
            host = os.getenv("DB_HOST", "localhost")
            url = f"http://{host}:5000/api/recommendation/reinitialize_recommendation"

            response = requests.post(url)
            if response.status_code == 200:
                print("✅ Cluster recommendation reinitialized successfully:")
            else:
                print(f"⚠️ Failed to reinitialize (status {response.status_code}):", response.text)
        
        except requests.exceptions.RequestException as e:
            print("❌ Error while calling API:", e)

    def load_data_from_api(self) -> None:
        df = fetch_jobs()
        self.job_repository.save_all(df)
        self.reinitialize_cluster_recommendation()

    def reinitialize_cluster_recommendation(self):
        cluster_service = ClusterService()
        cluster_service.run_and_save_clusters()
        self.reinitialize_recommendation()

    def get_job_by_id(self, job_id: int) -> Optional[JobRecord]:
        return self.job_repository.get_by_id(job_id)

    def get_all_jobs(self) -> list[JobRecord]:
        return self.job_repository.get_all()

    @staticmethod
    def _map_row_to_job(row) -> JobRecord:
        return JobRecord(
            job_title=row['Job Title'],
            publishing_date=row['Publishing Date'],
            start_date=row['Start Date'],
            salary=row['Salary'],
            duration=row['Duration'],
            location=row['Location'],
            work_mode=row['Work Mode'],
            skills=row['Skills'],
            description=row['Description'],
            plateforme=row['Plateforme'],
            scrap_date=row['Scrap Date'],
            company_name=row['Company Name'],
            number_of_candidates=row['Number of Candidates'],
            number_of_employees=row['Number of Employees'],
            sector=row['Sector'],
            description_e=row['Description E'],
            experience=row['Experience'],
            contract_type=row['Contract Type'],
            education=row['Education'],
            scrap_date_parsed=row['scrap_date_parsed'],
            estm_publishdate=row['estm_publishdate']
        )
