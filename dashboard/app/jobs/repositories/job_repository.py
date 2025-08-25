from typing import Optional, List
import pandas as pd
from app.jobs.domain.job_entity import JobRecord
from app.shared.db import db

class JobRepositoryInterface:
    def save_all(self, jobs: List[JobRecord]) -> None:
        raise NotImplementedError

    def get_by_id(self, job_id: int) -> Optional[JobRecord]:
        raise NotImplementedError

    def get_all(self) -> List[JobRecord]:
        raise NotImplementedError


class JobRepository(JobRepositoryInterface):
    def save_all(self, df: pd.DataFrame):
        from app.shared.db import db
        from app.jobs.domain.job_entity import JobRecord

        db.session.query(JobRecord).delete()
        db.session.commit()

        jobs = []
        for _, row in df.iterrows():
            job = JobRecord(
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
            jobs.append(job)

        db.session.bulk_save_objects(jobs)
        db.session.commit()

    def get_by_id(self, job_id: int) -> Optional[JobRecord]:
        return db.session.query(JobRecord).filter(JobRecord.id == job_id).first()

    def get_all(self) -> List[JobRecord]:
        return db.session.query(JobRecord).all()
