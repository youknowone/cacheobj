
class BaseBackend(object):
    def get(self, key, default=None):
        raise NotImplementedError

    def set(self, key, value, expiration=None, sync=True):
        raise NotImplementedError

    def delete(self, key, sync=True):
        raise NotImplementedError

    def sync(self):
        pass