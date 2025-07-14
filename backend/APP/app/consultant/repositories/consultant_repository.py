from abc import ABC, abstractmethod
from typing import Optional, List
from app.shared.db import db
from app.consultant.domain.consultant import Consultant

# Interface
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

# Concrete implementation
class ConsultantRepository(ConsultantRepositoryInterface):
    def get_consultant_by_id(self, consultant_id: int) -> Optional[Consultant]:
        return Consultant.query.get(consultant_id)
    
    def save_consultant(self, consultant: Consultant) -> Consultant:
        db.session.add(consultant)
        db.session.commit()
        return consultant
    
    def get_all_consultants(self) -> List[Consultant]:
        return Consultant.query.all()
    
    def update_consultant(self, consultant: Consultant) -> Consultant:
        db.session.commit()
        return consultant
    
    def delete_consultant(self, consultant_id: int) -> bool:
        consultant = self.get_consultant_by_id(consultant_id)
        if consultant:
            db.session.delete(consultant)
            db.session.commit()
            return True
        return False