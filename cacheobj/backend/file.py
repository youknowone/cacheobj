
import time
import json

from . import BaseBackend

class JsonFileBackend(BaseBackend):
    def __init__(self, path='cacheobj.json'):
        self.filepath = path
        try:
            with file(self.filepath, 'rb') as jsonfile:
                raw = jsonfile.read()
            data = json.loads(raw)
            self.storage = data['storage']
            self.expirations = data['expire']
        except IOError:
            self.storage = {}
            self.expirations = {}

    def set(self, key, value, expiration=None, sync=True):
        self.storage[key] = value
        assert value == self.storage[key]
        if expiration:
            self.expirations[key] = time.time() + expiration
        if sync:
            self.sync()
        return True

    def get(self, key, default=None):
        if key in self.expirations:
            if time.time() > self.expirations[key]:
                self.delete(key, sync=False)
        return self.storage.get(key, default)

    def delete(self, key, sync=True):
        if key in self.storage:
            del(self.storage[key])
        if key in self.expirations:
            del(self.expirations[key])
        if sync:
            self.sync()
        return True

    def sync(self):
        data = json.dumps({'storage': self.storage, 'expire': self.expirations})
        with file(self.filepath, 'wb') as jsonfile:
            jsonfile.write(data)
