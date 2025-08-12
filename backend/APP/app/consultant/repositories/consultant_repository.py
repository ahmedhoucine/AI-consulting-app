from abc import ABC, abstractmethod
from typing import Optional, List
from sqlalchemy.exc import SQLAlchemyError
from app.shared.db import db
from app.consultant.domain.consultant import Consultant

class ConsultantRepositoryInterface(ABC):
    @abstractmethod
    def get_consultant_by_id(self, consultant_id: int) -> Optional[Consultant]:
        pass

    @abstractmethod
    def save_consultant(self, consultant: Consultant) -> Consultant:
        pass

    @abstractmethod
    def get_all_consultants(self) -> List[Consultant]:
        pass

    @abstractmethod
    def update_consultant(self, consultant: Consultant) -> Consultant:
        pass

    @abstractmethod
    def delete_consultant(self, consultant_id: int) -> bool:
        pass


class ConsultantRepository(ConsultantRepositoryInterface):
    def get_consultant_by_id(self, consultant_id: int) -> Optional[Consultant]:
        return db.session.get(Consultant, consultant_id)

    def save_consultant(self, consultant: Consultant) -> Consultant:
        try:
            db.session.add(consultant)
            db.session.commit()
            return consultant
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def get_all_consultants(self) -> List[Consultant]:
        return db.session.query(Consultant).all()

    def update_consultant(self, consultant: Consultant) -> Consultant:
        try:
            db.session.commit()
            return consultant
        except SQLAlchemyError:
            db.session.rollback()
            raise

    def delete_consultant(self, consultant_id: int) -> bool:
        consultant = self.get_consultant_by_id(consultant_id)
        if not consultant:
            return False
        try:
            db.session.delete(consultant)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            raise
