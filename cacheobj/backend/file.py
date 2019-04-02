
import time
import json

from . import BaseBackend

class JsonFileBackend(BaseBackend):
    def __init__(self, path='cacheobj.json'):
        self.filepath = path
        try:
            with open(self.filepath, 'rb') as jsonfile:
                raw = jsonfile.read()
        except IOError:
            self.storage = {}
            self.expirations = {}
        else:
            data = json.loads(raw)
            self.storage = data['storage']
            self.expirations = data['expire']

    def set(self, key, value, expiration=None, commit=True):
        self.storage[key] = value
        assert value == self.storage[key]
        if expiration:
            self.expirations[key] = time.time() + expiration
        if commit:
            self.commit()
        return True

    def get(self, key, default=None):
        if key in self.expirations:
            if time.time() > self.expirations[key]:
                self.delete(key, commit=False)
        return self.storage.get(key, default)

    def delete(self, key, commit=True):
        if key in self.storage:
            del(self.storage[key])
        if key in self.expirations:
            del(self.expirations[key])
        if commit:
            self.commit()
        return True

    def commit(self):
        data = json.dumps({'storage': self.storage, 'expire': self.expirations}).encode('utf-8')
        with open(self.filepath, 'wb') as jsonfile:
            jsonfile.write(data)
