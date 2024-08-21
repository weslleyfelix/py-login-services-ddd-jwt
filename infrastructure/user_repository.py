import json
import os

class UserRepository:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_users(self):
        with open(self.filepath, 'r') as file:
            return json.load(file)['usuarios']

    def find_user_by_username(self, username):
        users = self.load_users()
        return next((user for user in users if user['usuario'] == username), None)

    def create_user(self, user_data):
        users = self.load_users()
        user_data['id'] = max([user['id'] for user in users]) + 1
        users.append(user_data)
        self.save_users(users)

    def update_user(self, user_id, updated_data):
        users = self.load_users()
        for user in users:
            if user['id'] == user_id:
                user.update(updated_data)
                break
        self.save_users(users)

    def delete_user(self, user_id):
        users = self.load_users()
        users = [user for user in users if user['id'] != user_id]
        self.save_users(users)

    def save_users(self, users):
        with open(self.filepath, 'w') as file:
            json.dump({'usuarios': users}, file, indent=4)
