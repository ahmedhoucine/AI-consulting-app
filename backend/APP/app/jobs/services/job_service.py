import pandas as pd
from typing import Optional
from app.jobs.domain.job_entity import JobRecord
from app.jobs.repositories.job_repository import JobRepositoryInterface

class JobService:
    def __init__(self, job_repository: JobRepositoryInterface):
        self.job_repository = job_repository

    def load_csv_from_path(self, path: str) -> None:
        """Load job records from a CSV file and save them."""
        try:
            df = pd.read_csv(path)
            df = df.where(pd.notnull(df), None)
        except Exception as e:
            raise RuntimeError(f"Failed to load CSV file '{path}': {e}")
        df = pd.read_csv(path).where(pd.notnull(df), None)
        jobs = [self._map_row_to_job(row) for _, row in df.iterrows()]
        self.job_repository.save_all(jobs)

    def get_job_by_id(self, job_id: int) -> Optional[JobRecord]:
        return self.job_repository.get_by_id(job_id)

    def get_all_jobs(self) -> list[JobRecord]:
        return self.job_repository.get_all()

    @staticmethod
    def _map_row_to_job(row) -> JobRecord:
        """Convert a CSV row into a JobRecord entity."""
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
