from app.feat1.domain.models.user import User

class UserService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def get_user(self, user_id):
        return self.user_repo.get_user_by_id(user_id)
    
    def create_user(self,name):
        user = User(name=name)
        return self.user_repo.save_user(user)
