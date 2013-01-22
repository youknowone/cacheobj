
from . import BaseBackend

global_storage = {}

class InMemoryBackend(BaseBackend):
    def __init__(self, storage=None):
        if storage is None:
            storage = global_storage # not good enough for big
        self.storage = storage

    def set(self, key, value):
        self.storage[key] = value

    def get(self, key, default=None):
        return self.storage.get(key, default)

    def delete(self, key):
        del self.storage[key]
