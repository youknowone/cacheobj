
from __future__ import absolute_import

import memcache
from . import BaseBackend

local_pool = ["127.0.0.1:11211"]

class MemcacheBackend(BaseBackend):
    def __init__(self, pool=local_pool):
        self.client = memcache.Client(pool)

    def set(self, key, value, expiration=0):
        if expiration is None:
            expiration = 0
        result = self.client.set(key, value, expiration)
        if not result:
            raise AttributeError("can't set attribute")
        return result

    def get(self, key, default=None):
        value = self.client.get(key)
        if value is None:
            return default
        return value

    def delete(self, key):
        return self.client.delete(key)
