class PostService:
    def __init__(self, post_repo):
        self.post_repo = post_repo

    def get_post(self, post_id):
        return self.post_repo.get_post_by_id(post_id)
