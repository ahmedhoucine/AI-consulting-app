from flask import Blueprint, jsonify
from app.job_clustering.services.cluster_service import ClusterService

cluster_bp = Blueprint("clusters", __name__)
service = ClusterService()

@cluster_bp.route("/clusters", methods=["GET"])
def get_clusters():
    clusters = service.get_clusters()
    return jsonify([
        {
            "cluster_id": c.cluster_id,
            "cardinality": c.cardinality,
            "most_frequent_title": c.most_frequent_title,
            "created_at": c.created_at.isoformat()
        }
        for c in clusters
    ])
@cluster_bp.route("/clusters/run", methods=["POST"])
def run_clustering():
    try:
        service.run_and_save_clusters()
        return jsonify({"message": "Clustering completed and saved."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
