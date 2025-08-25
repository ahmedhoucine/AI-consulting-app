from app.feat_recommendations.services.recommend_engine_singleton import engine
from app.feat_recommendations.domain.recommendation_entity import RecommendationRecord
from app.shared.db import db

class RecommendationRepository:
    def recommend(self, query: str):
        results = engine.get_recommendations(query)
        return results

    def save(self, query: str, results: list):
        record = RecommendationRecord(
            query=query,
            recommendations="\n\n".join(map(str, results))
        )
        db.session.add(record)
        db.session.commit()
