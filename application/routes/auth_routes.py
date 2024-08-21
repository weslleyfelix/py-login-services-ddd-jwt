from flask import Blueprint, request, jsonify
import jwt
import datetime
from domain.authentication import AuthenticationService
from config.config import Config
from infrastructure.user_repository import UserRepository
from infrastructure.profile_repository import ProfileRepository
from infrastructure.permission_repository import PermissionRepository

auth_bp = Blueprint('auth', __name__)

# Injeção de dependências
user_repository = UserRepository('data/usuarios.json')
profile_repository = ProfileRepository('data/perfis.json')
permission_repository = PermissionRepository('data/permissoes.json')
auth_service = AuthenticationService(user_repository)

@auth_bp.route('/login', methods=['POST'])
def login():
    auth = request.json

    if not auth or not auth.get('usuario') or not auth.get('senha'):
        return jsonify({'message': 'Could not verify', 'WWW-Authenticate': 'Basic auth="Login required"'}), 401

    if not auth_service.validate_user(auth['usuario'], auth['senha']):
        return jsonify({'message': 'Invalid credentials'}), 401

    current_user = user_repository.find_user_by_username(auth['usuario'])

    # Obter perfis e permissões do usuário
    perfil_ids = [current_user.get('perfilId')]
    perfis = profile_repository.get_profiles_by_ids(perfil_ids)
    permissoes = permission_repository.get_permissions_by_profile_ids(perfil_ids)

    # Criação do payload adicional
    payload = {
        'name': current_user['nome'].split()[0],
        'email': current_user['email'],
        'profile': [perfil['perfil'] for perfil in perfis],
        'roles': [permissao['permissao'] for permissao in permissoes]
    }

    # Gera o token JWT com o payload adicional
    token = jwt.encode({
        'user': current_user['usuario'],
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
        **payload  # Inclui o payload no token
    }, Config.SECRET_KEY, algorithm="HS256")

    # Retorna o token JWT junto com as informações adicionais
    return jsonify({
        'id': current_user['id'],
        'username': current_user['nome'],
        'password': current_user['senha'],  # Reitero que enviar senhas não é seguro
        'firstName': current_user['nome'].split()[0],
        'lastName': ' '.join(current_user['nome'].split()[1:]),
        'token': token,
        'email': current_user['email']
    })
