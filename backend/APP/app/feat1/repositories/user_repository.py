from app.feat1.domain.models.user import User
from app.feat1.repositories.interfaces import UserRepositoryInterface
from app.shared.db import db

class UserRepository(UserRepositoryInterface):
    def get_user_by_id(self, user_id: int):
        return User.query.get(user_id)

    def save_user(self, user):
        db.session.add(user)
        db.session.commit()
        return user