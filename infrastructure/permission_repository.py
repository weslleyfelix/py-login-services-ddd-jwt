import json
import os

class PermissionRepository:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_permissions(self):
        with open(self.filepath, 'r') as file:
            return json.load(file)['permissoes']

    def get_permissions_by_profile_ids(self, profile_ids):
        permissions = self.load_permissions()
        return [permission for permission in permissions if permission['perfilId'] in profile_ids]

    def create_permission(self, permission_data):
        permissions = self.load_permissions()
        permission_data['id'] = max([permission['id'] for permission in permissions]) + 1
        permissions.append(permission_data)
        self.save_permissions(permissions)

    def update_permission(self, permission_id, updated_data):
        permissions = self.load_permissions()
        for permission in permissions:
            if permission['id'] == permission_id:
                permission.update(updated_data)
                break
        self.save_permissions(permissions)

    def delete_permission(self, permission_id):
        permissions = self.load_permissions()
        permissions = [permission for permission in permissions if permission['id'] != permission_id]
        self.save_permissions(permissions)

    def save_permissions(self, permissions):
        with open(self.filepath, 'w') as file:
            json.dump({'permissoes': permissions}, file, indent=4)
