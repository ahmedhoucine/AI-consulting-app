from flask import Blueprint, jsonify
from feedback.services import service

feedback_bp = Blueprint('feedback', __name__)

@feedback_bp.route('/feedbacks', methods=['GET'])
def afficher_feedbacks():
    feedbacks = service.lister_feedbacks()
    feedbacks_serializes = [f.to_dict() for f in feedbacks]
    return jsonify(feedbacks_serializes)
