
from __future__ import absolute_import

import redis
from . import BaseBackend

local_pool = redis.ConnectionPool()

class RedisBackend(BaseBackend):
    def __init__(self, pool=local_pool):
        self.client = redis.Redis(connection_pool=pool)

    def set(self, key, value, expiration=None):
        result = self.client.set(key, value)
        if expiration:
            self.client.expire(key, expiration)
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
