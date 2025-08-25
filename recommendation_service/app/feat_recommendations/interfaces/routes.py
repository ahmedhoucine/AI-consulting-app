from flask import Blueprint, request, jsonify
from app.feat_recommendations.services.recommend_service import RecommendationService

recommend_bp = Blueprint('recommend', __name__)
service = RecommendationService()

@recommend_bp.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    query = data.get('query')

    if not query:
        return jsonify({"error": "Missing 'query' in request"}), 400

    try:
        results = service.get_and_save(query)
        return jsonify({"query": query, "recommendations": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
