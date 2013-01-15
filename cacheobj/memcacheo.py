
from .core import SimpleCacheObject
from .backends.memcacheb import MemcacheBackend, local_pool

_common_backends = {}

def get_memcache_object(pool):
    def backend_generator():
        global _common_backends

        pool_tuple = tuple(pool)
        backend = _common_backends.get(pool_tuple, None)
        if not backend:
            backend = _common_backends[pool_tuple] = MemcacheBackend(pool_tuple)
        return backend

    class MemcacheObject(SimpleCacheObject):
        _backend_generator = staticmethod(backend_generator)

    return MemcacheObject

LocalMemcacheObject = get_memcache_object(local_pool)
