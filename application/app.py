from flask import Flask, request, jsonify
import jwt
import datetime
from functools import wraps
from domain.authentication import AuthenticationService
from infrastructure.user_repository import UserRepository
from infrastructure.profile_repository import ProfileRepository
from infrastructure.permission_repository import PermissionRepository
from config.config import Config

# Configuração do Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY

# Injeção de dependências
user_repository = UserRepository('data/usuarios.json')
profile_repository = ProfileRepository('data/perfis.json')
permission_repository = PermissionRepository('data/permissoes.json')
auth_service = AuthenticationService(user_repository)

# Função de verificação do token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({'message': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = user_repository.find_user_by_username(data['user'])
            if not current_user:
                return jsonify({'message': 'User not found!'}), 403
        except:
            return jsonify({'message': 'Token is invalid!'}), 403
        return f(current_user, *args, **kwargs)
    return decorated

def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            perfil_ids = current_user.get('perfilId')
            permissoes = permission_repository.get_permissions_by_profile_ids([perfil_ids])
            permissoes_usuario = [p['permissao'] for p in permissoes]

            if permission not in permissoes_usuario:
                return jsonify({'message': 'You do not have permission to access this resource!'}), 403

            return f(current_user, *args, **kwargs)
        return decorated_function
    return decorator

# Rota de login
@app.route('/auth/login', methods=['POST'])
def login():
    auth = request.json

    if not auth or not auth.get('usuario') or not auth.get('senha'):
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    if not auth_service.validate_user(auth['usuario'], auth['senha']):
        return jsonify({'message': 'Invalid credentials'}), 401

    # Gera o token JWT
    token = jwt.encode({
        'user': auth['usuario'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }, app.config['SECRET_KEY'], algorithm="HS256")

    return jsonify({'token': token})

# Rota protegida que retorna as informações do usuário logado
@app.route('/auth/protected', methods=['GET'])
@token_required
def protected_route(current_user):
    if current_user:
        # Busca o perfil do usuário com base no perfilId
        perfil_ids = [current_user.get('perfilId')]
        perfis = profile_repository.get_profiles_by_ids(perfil_ids)

        # Busca as permissões do usuário com base no perfil
        permissoes = permission_repository.get_permissions_by_profile_ids(perfil_ids)

        # Monta a resposta com os perfis e permissões do usuário
        return jsonify({
            'nome': current_user['nome'],
            'email': current_user['email'],
            'perfis': [perfil['perfil'] for perfil in perfis],
            'regras': [permissao['permissao'] for permissao in permissoes]
        })
    return jsonify({'message': 'User not found'}), 404

# Rotas CRUD para usuários com proteção de permissões
@app.route('/usuarios', methods=['GET'])
@token_required
@permission_required('gerencial_admin')
def get_usuarios(current_user):
    return jsonify(user_repository.load_users())

@app.route('/usuarios', methods=['POST'])
@token_required
@permission_required('gerencial_admin')
def create_usuario(current_user):
    data = request.json
    user_repository.create_user(data)
    return jsonify({'message': 'User created successfully!'})

@app.route('/usuarios/<int:id>', methods=['PUT'])
@token_required
@permission_required('gerencial_admin')
def update_usuario(current_user, id):
    data = request.json
    user_repository.update_user(id, data)
    return jsonify({'message': 'User updated successfully!'})

@app.route('/usuarios/<int:id>', methods=['DELETE'])
@token_required
@permission_required('gerencial_admin')
def delete_usuario(current_user, id):
    user_repository.delete_user(id)
    return jsonify({'message': 'User deleted successfully!'})
