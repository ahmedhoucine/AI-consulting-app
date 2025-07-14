from abc import ABC, abstractmethod

class UserRepositoryInterface(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int):
        pass
    
    @abstractmethod
    def save_user(self, user):
        pass
