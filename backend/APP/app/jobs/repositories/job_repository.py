from app.jobs.domain.job_entity import JobRecord
from app.shared.db import db

class JobRepository:
    @staticmethod
    def save_all(jobs: list[JobRecord]):
        db.session.bulk_save_objects(jobs)
        db.session.commit()
    @staticmethod
    def get_by_id(job_id: int) -> JobRecord | None:
        return db.session.query(JobRecord).filter(JobRecord.id == job_id).first()
    @staticmethod
    def get_all() -> list[JobRecord]:
        return db.session.query(JobRecord).all()
