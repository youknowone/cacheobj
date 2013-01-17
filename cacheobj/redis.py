
from .core import SimpleCacheObject
from .backends.redis import RedisBackend, local_pool

_common_backends = {}

def get_redis_object(pool):
    def backend_generator():
        global _common_backends

        backend = _common_backends.get(pool, None)
        if not backend:
            backend = _common_backends[pool] = RedisBackend(pool)
        return backend

    class RedisObject(SimpleCacheObject):
        _backend_generator = staticmethod(backend_generator)

    return RedisObject

LocalRedisObject = get_redis_object(local_pool)
