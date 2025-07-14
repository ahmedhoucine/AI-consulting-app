from app.feat2.domain.models.post import Post
from app.feat2.repositories.interfaces import PostRepositoryInterface

class PostRepository(PostRepositoryInterface):
    def get_post_by_id(self, user_id: int):
        return Post.query.get(user_id)
