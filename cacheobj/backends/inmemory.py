
from . import BaseBackend

global_storage = {}

class InMemoryBackend(BaseBackend):
    def __init__(self, storage=None):
        if storage is None:
            storage = global_storage # not good enough for big
        self.storage = storage

    def set(self, key, value, expiration=None):
        self.storage[key] = value
        assert value == self.storage.get(key, None)
        return True

    def get(self, key, default=None):
        return self.storage.get(key, default)

    def delete(self, key):
        del self.storage[key]
        return True
