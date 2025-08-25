from abc import ABC, abstractmethod
from typing import Optional
from app.consultant.domain.consultant import Consultant

class ConsultantRepositoryInterface(ABC):
    """Repository interface for managing Consultant entities."""

    @abstractmethod
    def get_consultant_by_id(self, consultant_id: int) -> Optional[Consultant]:
        """Retrieve a consultant by their ID, or None if not found."""
        ...

    @abstractmethod
    def save_consultant(self, consultant: Consultant) -> Consultant:
        """Persist a consultant to the storage."""
        ...

    @abstractmethod
    def get_all_consultants(self) -> list[Consultant]:
        """Return all consultants."""
        ...

    @abstractmethod
    def update_consultant(self, consultant: Consultant) -> Consultant:
        """Update the details of an existing consultant."""
        ...

    @abstractmethod
    def delete_consultant(self, consultant_id: int) -> bool:
        """Delete a consultant by ID. Returns True if successful."""
        ...
