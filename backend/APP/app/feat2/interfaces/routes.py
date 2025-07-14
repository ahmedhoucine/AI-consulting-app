from flask import Blueprint, jsonify
from app.feat2.repositories.post_repository import PostRepository
from app.feat2.services.post_service import PostService

post_bp = Blueprint('post', __name__)
post_service =PostService(PostRepository())

@post_bp.route('/post/<int:post_id>', methods=['GET'])
def get_post(post_id):
    post = post_service.get_post(post_id)
    if post:
        return jsonify({'id': post.id, 'name': post.title})
    return jsonify({'error': 'post not found'}), 404
