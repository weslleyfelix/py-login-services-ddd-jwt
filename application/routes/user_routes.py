from flask import Blueprint, jsonify, request
from functools import wraps
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from config.config import Config
from infrastructure.user_repository import UserRepository

user_bp = Blueprint('user', __name__, url_prefix='/usuarios')

# Injeção de dependências
user_repository = UserRepository('data/usuarios.json')

# Decorador para validar o token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            # Decodifica o token JWT
            token_data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        except ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except InvalidTokenError:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(token_data, *args, **kwargs)
    return decorated

# Decorador para validar permissões baseadas no payload do token
def permission_required(required_permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(token_data, *args, **kwargs):
            roles = token_data.get('roles', [])
            if required_permission not in roles:
                return jsonify({'message': 'You do not have permission to access this resource!'}), 403
            return f(token_data, *args, **kwargs)
        return decorated_function
    return decorator

# Rota para obter todos os usuários
@user_bp.route('/', methods=['GET'])
@token_required
@permission_required('gerencial_admin')
def get_usuarios(token_data):
    return jsonify(user_repository.load_all())

# Rota para criar um novo usuário
@user_bp.route('/', methods=['POST'])
@token_required
@permission_required('gerencial_admin')
def create_usuario(token_data):
    data = request.json
    user_repository.create(data)
    return jsonify({'message': 'User created successfully!'})

# Rota para atualizar um usuário existente
@user_bp.route('/<int:id>', methods=['PUT'])
@token_required
@permission_required('gerencial_admin')
def update_usuario(token_data, id):
    data = request.json
    user_repository.update(id, data)
    return jsonify({'message': 'User updated successfully!'})

# Rota para deletar um usuário existente
@user_bp.route('/<int:id>', methods=['DELETE'])
@token_required
@permission_required('gerencial_admin')
def delete_usuario(token_data, id):
    user_repository.delete(id)
    return jsonify({'message': 'User deleted successfully!'})
