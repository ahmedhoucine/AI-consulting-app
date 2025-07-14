import pandas as pd
from app.jobs.repositories.job_repository import JobRepository
from app.jobs.domain.job_entity import JobRecord

class JobService:
    @staticmethod
    def load_csv_from_path(path: str):
        df = pd.read_csv(path)
        df = df.where(pd.notnull(df), None)
        jobs = []
        for _, row in df.iterrows():
            jobs.append(JobRecord(
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
            ))

        JobRepository.save_all(jobs)
    @staticmethod
    def get_job_by_id(job_id: int) -> JobRecord | None:
        return JobRepository.get_by_id(job_id)

    @staticmethod
    def get_all_jobs() -> list[JobRecord]:
        return JobRepository.get_all()

