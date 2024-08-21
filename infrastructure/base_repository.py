from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def load_all(self):
        pass

    @abstractmethod
    def find_by_id(self, entity_id):
        pass

    @abstractmethod
    def create(self, entity_data):
        pass

    @abstractmethod
    def update(self, entity_id, updated_data):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass
