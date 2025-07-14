from abc import ABC, abstractmethod
from typing import Optional
from app.consultant.domain.consultant import Consultant

class ConsultantRepositoryInterface(ABC):
    @abstractmethod
    def get_consultant_by_id(self, consultant_id: int) -> Optional[Consultant]:
        pass
    
    @abstractmethod
    def save_consultant(self, consultant: Consultant) -> Consultant:
        pass
    
    @abstractmethod
    def get_all_consultants(self) -> list[Consultant]:
        pass
    
    @abstractmethod
    def update_consultant(self, consultant: Consultant) -> Consultant:
        pass
    
    @abstractmethod
    def delete_consultant(self, consultant_id: int) -> bool:
        pass