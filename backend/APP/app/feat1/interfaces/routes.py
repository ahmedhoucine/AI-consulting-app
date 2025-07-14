from flask import Blueprint, jsonify, request
from app.feat1.repositories.user_repository import UserRepository
from app.feat1.services.user_service import UserService

user_bp = Blueprint('user', __name__)
user_service = UserService(UserRepository())

@user_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if user:
        return jsonify({'id': user.id, 'name': user.name})
    return jsonify({'error': 'User not found'}), 404


@user_bp.route('/user', methods=['POST'])
def create_post():
    data = request.json
    name = data.get('name')


    if not all([name]):
        return jsonify({'error': 'Missing fields'}), 400

    try:
        user = user_service.create_user(name)
        return jsonify({
            'id': user.id,
            'name': user.name,
        }), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400