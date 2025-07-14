from abc import ABC, abstractmethod

class PostRepositoryInterface(ABC):
    @abstractmethod
    def get_post_by_id(self, post_id: int):
        pass
