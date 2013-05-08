
class BaseBackend(object):
    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value, expiration=None, commit=True):
        raise NotImplementedError

    def delete(self, key, commit=True):
        raise NotImplementedError

    def commit(self):
        pass