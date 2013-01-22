
class BaseBackend(object):
    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError