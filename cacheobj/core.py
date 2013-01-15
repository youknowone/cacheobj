
class CacheObject(object):
    """
    General purpose cache object. _backends should be constant for default implementaiton.
    For dynamic overloading, try to override _backend_table or _backend_for_key.

    _backends should be formatted as like:

    from cacheobj.backends.memcache import MemcacheBackend
    from cacheobj.backends.redis import RedisBackend
    memcache = MemcacheBackend()
    redis = RedisBackend()

    _backends = {
        memcache: ['field1', 'field2',]
        redis: ['prop1', 'prop2'],
    }

    This allows your object caches field1 and field2 on memcache and prop1 and prop2 on redis.
    """

    _backends = {} # constant table

    def __init__(self, id=0, prefix=''):
        self._id = id
        self._str_id = str(id)
        self._prefix = prefix
        self._locals = {}
    
    @property
    def _cache_prefix(self):
        return self.__class__.__name__ + self._prefix

    def _cache_key(self, key):
        return '.'.join((self._cache_prefix, self._str_id, key))

    def _backend_for_key(self, key):
        if not hasattr(self, '_backend_table'):
            table = self._backend_table = {}
            for backend, keys in self._backends.items():
                for key in keys:
                    table[key] = backend
        return self._backend_table[key]
    
    def get(self, key, default=None, use_cache=False):
        if use_cache:
            try:
                return self._locals[key]
            except KeyError:
                pass
        backend = self._backend_for_key(key)
        result = backend.get(self._cache_key(key), default)
        if use_cache:
            self._locals[key] = result
        return result

    def set(self, key, value, use_cache=True):
        backend = self._backend_for_key(key)
        result = backend.set(self._cache_key(key), value)
        if use_cache:
            self._locals[key] = value
        return result

    def __getattr__(self, key):
        if key and key[0] != '_':
            try:
                return self.get(key)
            except KeyError:
               pass
        sup = super(CacheObject, self)
        try:
            return sup.__getattr__(key)
        except:
            return sup.__getattribute__(key)

    def __setattr__(self, key, value):
        if key and key[0] != '_':
            try:
                self.set(key, value)
            except KeyError:
                pass
        sup = super(CacheObject, self)
        return sup.__setattr__(key, value)


class SimpleCacheObject(CacheObject):
    """
    SimpleCacheObject provides easy-to-inherit interface for one backend based cache object.

    Example:
    from cacheobj.backends.inmemory import InMemoryBackend
    def backend_generator():
        return InMemoryBackend()
    class ASimpleCacheObejct(SimpleCacheObject):
        _backend_generator = staticmethod(backend_generator)
        _properties = ['field1', 'field2']
    """
    _backend_generator = None
    _properties = []

    @property
    def _backend(self):
        if not hasattr(self, '__backend'):
            self.__backend = self._backend_generator()
        return self.__backend

    def _backend_for_key(self, key):
        if key in self._properties:
            return self._backend
        raise KeyError
