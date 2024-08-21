# domain/authentication.py

class AuthenticationService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    def validate_user(self, username, password):
        user = self.user_repository.find_user_by_username(username)
        if user and user['senha'] == password:
            return True
        return False

    #def validate_user(self, username, password):
    #    print(f"Validando usuário: {username} com senha: {password}")
    #    user = self.user_repository.find_user_by_username(username)
    #    
    #    if user:
    #        print(f"Usuário encontrado: {user['usuario']}, Senha armazenada: {user['senha']}")
    #    if user and user['senha'] == password:
    #        return True
    #    return False
