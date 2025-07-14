from typing import Optional
from app.consultant.domain.consultant import Consultant
from app.consultant.repositories.consultant_repository import ConsultantRepositoryInterface

class ConsultantService:
    def __init__(self, consultant_repo: ConsultantRepositoryInterface):
        self.consultant_repo = consultant_repo
    
    def get_consultant(self, consultant_id: int) -> Optional[Consultant]:
        return self.consultant_repo.get_consultant_by_id(consultant_id)
    
    def create_consultant(self, nom: str, email: str, cv: str, status: str = 'pending') -> Consultant:
        consultant = Consultant(nom=nom, email=email, cv=cv, status=status)
        return self.consultant_repo.save_consultant(consultant)
    
    def get_all_consultants(self) -> list[Consultant]:
        return self.consultant_repo.get_all_consultants()
    
    def update_consultant(self, consultant_id: int, **kwargs) -> Optional[Consultant]:
        consultant = self.get_consultant(consultant_id)
        if consultant:
            for key, value in kwargs.items():
                setattr(consultant, key, value)
            return self.consultant_repo.update_consultant(consultant)
        return None
    
    def delete_consultant(self, consultant_id: int) -> bool:
        return self.consultant_repo.delete_consultant(consultant_id)