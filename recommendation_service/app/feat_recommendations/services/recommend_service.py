from app.feat_recommendations.repositories.recommend_repository import RecommendationRepository

class RecommendationService:
    def __init__(self):
        self.repo = RecommendationRepository()

    def get_and_save(self, query: str):
        results = self.repo.recommend(query)
        self.repo.save(query, results)
        return results
