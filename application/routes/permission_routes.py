from flask import Blueprint, jsonify, request
from infrastructure.permission_repository import PermissionRepository

permission_bp = Blueprint('permission', __name__, url_prefix='/permissoes')
permission_repository = PermissionRepository('data/permissoes.json')

@permission_bp.route('/', methods=['GET'])
def get_permissions():
    return jsonify(permission_repository.load_permissions())

@permission_bp.route('/', methods=['POST'])
def create_permission():
    data = request.json
    permission_repository.create_permission(data)
    return jsonify({'message': 'Permission created successfully!'})

@permission_bp.route('/<int:id>', methods=['PUT'])
def update_permission(id):
    data = request.json
    permission_repository.update_permission(id, data)
    return jsonify({'message': 'Permission updated successfully!'})

@permission_bp.route('/<int:id>', methods=['DELETE'])
def delete_permission(id):
    permission_repository.delete_permission(id)
    return jsonify({'message': 'Permission deleted successfully!'})
