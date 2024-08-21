from flask import Blueprint, jsonify, request
from infrastructure.profile_repository import ProfileRepository

profile_bp = Blueprint('profile', __name__, url_prefix='/perfis')
profile_repository = ProfileRepository('data/perfis.json')

@profile_bp.route('/', methods=['GET'])
def get_profiles():
    return jsonify(profile_repository.load_profiles())

@profile_bp.route('/', methods=['POST'])
def create_profile():
    data = request.json
    profile_repository.create_profile(data)
    return jsonify({'message': 'Profile created successfully!'})

@profile_bp.route('/<int:id>', methods=['PUT'])
def update_profile(id):
    data = request.json
    profile_repository.update_profile(id, data)
    return jsonify({'message': 'Profile updated successfully!'})

@profile_bp.route('/<int:id>', methods=['DELETE'])
def delete_profile(id):
    profile_repository.delete_profile(id)
    return jsonify({'message': 'Profile deleted successfully!'})
