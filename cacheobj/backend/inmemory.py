
import time
from . import BaseBackend

global_storage = {}
global_expirations = {}

class InMemoryBackend(BaseBackend):
    def __init__(self, storageset=None):
        if storageset:
            self.storage, self.expirations = storageset
        else:
            self.storage, self.expirations = global_storage, global_expirations # not good enough for big

    def set(self, key, value, expiration=None):
        self.storage[key] = value
        assert value == self.storage[key]
        if expiration:
            self.expirations[key] = time.time() + expiration
        return True

    def get(self, key, default=None):
        if key in self.expirations:
            if time.time() > self.expirations[key]:
                self.delete(key)
        return self.storage.get(key, default)

    def delete(self, key):
        if key in self.storage:
            del(self.storage[key])
        return True
