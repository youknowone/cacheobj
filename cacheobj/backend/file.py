
import time
import json

from . import BaseBackend

class InMemoryBackend(BaseBackend):
    def __init__(self, path='cacheobj.json'):
        self.filepath = path
        raw = file(self.filepath, 'r').read()
        data = json.loads(raw)
        self.storage = data['storage']
        self.expirations = data['expire']

    def set(self, key, value, expiration=None):
        self.storage[key] = value
        assert value == self.storage[key]
        if expiration:
            self.expirations[key] = time.time() + expiration
        self.sync()
        return True

    def get(self, key, default=None):
        if key in self.expirations:
            if time.time() > self.expirations[key]:
                self.delete(key)
        return self.storage.get(key, default)

    def delete(self, key):
        if key in self.storage:
            del(self.storage[key])
        self.sync()
        return True

    def sync(self):
        data = json.dumps({'storage': self.storage, 'expire': self.expirations})
