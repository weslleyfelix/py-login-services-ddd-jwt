import json
import os

class ProfileRepository:
    def __init__(self, filepath):
        self.filepath = filepath

    def load_profiles(self):
        with open(self.filepath, 'r') as file:
            return json.load(file)['perfis']

    def get_profiles_by_ids(self, profile_ids):
        profiles = self.load_profiles()
        return [profile for profile in profiles if profile['id'] in profile_ids]

    def create_profile(self, profile_data):
        profiles = self.load_profiles()
        profile_data['id'] = max([profile['id'] for profile in profiles]) + 1
        profiles.append(profile_data)
        self.save_profiles(profiles)

    def update_profile(self, profile_id, updated_data):
        profiles = self.load_profiles()
        for profile in profiles:
            if profile['id'] == profile_id:
                profile.update(updated_data)
                break
        self.save_profiles(profiles)

    def delete_profile(self, profile_id):
        profiles = self.load_profiles()
        profiles = [profile for profile in profiles if profile['id'] != profile_id]
        self.save_profiles(profiles)

    def save_profiles(self, profiles):
        with open(self.filepath, 'w') as file:
            json.dump({'perfis': profiles}, file, indent=4)
