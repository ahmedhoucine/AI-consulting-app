from flask import Blueprint, jsonify, request
from app.consultant.repositories.consultant_repository import ConsultantRepository
from app.consultant.services.consultant_service import ConsultantService

consultant_bp = Blueprint('consultant', __name__)
consultant_service = ConsultantService(ConsultantRepository())

def consultant_to_dict(consultant):
    """Serialize consultant object to dict."""
    return {
        'id': consultant.id,
        'nom': consultant.nom,
        'email': consultant.email,
        'cv': consultant.cv,
        'status': consultant.status,
        'date_creation': consultant.date_creation.isoformat()
    }

@consultant_bp.route('/consultants', methods=['POST'])
def create_consultant():
    data = request.get_json()
    required_fields = ['nom', 'email', 'cv']

    if not data or not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        consultant = consultant_service.create_consultant(
            nom=data['nom'],
            email=data['email'],
            cv=data['cv'],
            status=data.get('status', 'pending')
        )
        return jsonify(consultant_to_dict(consultant)), 201
    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        # Log error here for debugging
        return jsonify({'error': 'Internal server error'}), 500

@consultant_bp.route('/consultants/<int:consultant_id>', methods=['GET'])
def get_consultant(consultant_id):
    consultant = consultant_service.get_consultant(consultant_id)
    if consultant:
        return jsonify(consultant_to_dict(consultant))
    return jsonify({'error': 'Consultant not found'}), 404

@consultant_bp.route('/consultants', methods=['GET'])
def get_all_consultants():
    consultants = consultant_service.get_all_consultants()
    return jsonify([consultant_to_dict(c) for c in consultants])

@consultant_bp.route('/consultants/<int:consultant_id>', methods=['PUT'])
def update_consultant(consultant_id):
    data = request.get_json() or {}
    consultant = consultant_service.update_consultant(consultant_id, **data)
    if consultant:
        return jsonify(consultant_to_dict(consultant))
    return jsonify({'error': 'Consultant not found'}), 404

@consultant_bp.route('/consultants/<int:consultant_id>', methods=['DELETE'])
def delete_consultant(consultant_id):
    if consultant_service.delete_consultant(consultant_id):
        return jsonify({'message': 'Consultant deleted successfully'})
    return jsonify({'error': 'Consultant not found'}), 404
