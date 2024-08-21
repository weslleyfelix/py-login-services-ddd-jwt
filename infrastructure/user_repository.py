import json
from infrastructure.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, filepath):
        self.filepath = filepath

    def load_all(self):
        with open(self.filepath, 'r') as file:
            return json.load(file)['usuarios']

    def find_by_id(self, user_id):
        users = self.load_all()
        return next((user for user in users if user['id'] == user_id), None)

    def find_user_by_username(self, username):
        users = self.load_all()
        return next((user for user in users if user['usuario'] == username), None)

    def create(self, user_data):
        users = self.load_all()
        user_data['id'] = max([user['id'] for user in users]) + 1
        users.append(user_data)
        self.save_users(users)

    def update(self, user_id, updated_data):
        users = self.load_all()
        for user in users:
            if user['id'] == user_id:
                user.update(updated_data)
                break
        self.save_users(users)

    def delete(self, user_id):
        users = self.load_all()
        users = [user for user in users if user['id'] != user_id]
        self.save_users(users)

    def save_users(self, users):
        with open(self.filepath, 'w') as file:
            json.dump({'usuarios': users}, file, indent=4)
