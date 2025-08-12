from typing import Optional, List
from app.jobs.domain.job_entity import JobRecord
from app.shared.db import db
from sqlalchemy.exc import SQLAlchemyError

class JobRepositoryInterface:
    def save_all(self, jobs: List[JobRecord]) -> None:
        raise NotImplementedError

    def get_by_id(self, job_id: int) -> Optional[JobRecord]:
        raise NotImplementedError

    def get_all(self) -> List[JobRecord]:
        raise NotImplementedError


class JobRepository(JobRepositoryInterface):
    def save_all(self, jobs: List[JobRecord]) -> None:
        try:
            db.session.bulk_save_objects(jobs)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def get_by_id(self, job_id: int) -> Optional[JobRecord]:
        return db.session.query(JobRecord).filter(JobRecord.id == job_id).first()

    def get_all(self) -> List[JobRecord]:
        return db.session.query(JobRecord).all()
