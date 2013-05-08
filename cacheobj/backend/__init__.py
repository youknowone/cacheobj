
class BaseBackend(object):
    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value, expiration=None):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError