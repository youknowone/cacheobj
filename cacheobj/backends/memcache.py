
from __future__ import absolute_import

import memcache
from . import BaseBackend

local_pool = ["127.0.0.1:11211"]

class MemcacheBackend(BaseBackend):
    def __init__(self, pool=local_pool):
        self.client = memcache.Client(pool)

    def set(self, key, value):
        result = self.client.set(key, value)
        if not result:
            raise AttributeError("can't set attribute")

    def get(self, key, default=None):
        value = self.client.get(key)
        if value is None:
            return default
        return value

    def delete(self, key):
        self.client.delete(key)
