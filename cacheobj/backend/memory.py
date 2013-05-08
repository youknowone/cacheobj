
import time
from . import BaseBackend

global_storage = {}
global_expirations = {}

class MemoryBackend(BaseBackend):
    def __init__(self, storageset=None):
        if storageset:
            self.storage, self.expirations = storageset
        else:
            self.storage, self.expirations = global_storage, global_expirations # not good enough for big

    def set(self, key, value, expiration=None, sync=True):
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

    def delete(self, key, sync=True):
        if key in self.storage:
            del(self.storage[key])
        if key in self.expirations:
            del(self.expirations[key])
        return True
