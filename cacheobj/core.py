
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
    _expiration = None # seconds. None for permanent or default
    _strict = False

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
            trans = self._trans_table = {}
            for backend, keys in self._backends.items():
                for akey in keys:
                    if isinstance(akey, tuple):
                        table[akey[0]] = backend
                        trans[akey[0]] = akey[1]
                    else:
                        table[akey] = backend
        #print 'BACKEND', key, self._backend_table[key]
        return self._backend_table[key]

    def _expiration_for_key(self, key):
        return self._expiration

    def get(self, key, default=None, use_cache=False):
        #print 'GET({}) {} ({}) cache:{}'.format(self.__class__.__name__, key, default, use_cache)
        if use_cache:
            try:
                return self._locals[key]
            except KeyError:
                pass
        backend = self._backend_for_key(key)
        result = backend.get(self._cache_key(key), default)
        if key in self._trans_table:
            result = self._trans_table[key](result)
        if use_cache:
            self._locals[key] = result
        return result

    def set(self, key, value, expiration=None, default=None, use_cache=True):
        #print 'SET({}) {}:{} ({}) for {}s cache:{}'.format(self.__class__.__name__, key, value, default, expiration, use_cache)
        backend = self._backend_for_key(key)
        cache_key = self._cache_key(key)
        expiration = self._expiration_for_key(key) if expiration is None else expiration
        if value == default:
            result = backend.delete(cache_key)
        else:
            result = backend.set(self._cache_key(key), value, expiration)
        if use_cache:
            self._locals[key] = value
        return result

    def delete(self, key):
        backend = self._backend_for_key(key)
        cache_key = self._cache_key(key)
        result = backend.delete(cache_key)
        return result

    def delete_all(self):
        for backend, keys in self._backends.items():
            for key in keys:
                cache_key = self._cache_key(key)
                backend.delete(cache_key)


    def __getattr__(self, key):
        if key and key[0] != '_':
            try:
                return self.get(key)
            except KeyError:
                if self._strict:
                    raise
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
                if self._strict:
                    raise
            return
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

    @classmethod
    def _backend(cls):
        if not hasattr(cls, '__backend'):
            cls.__backend = cls._backend_generator()
        return cls.__backend

    def _backend_for_key(self, key):
        if not hasattr(self, '_property_keys'):
            keys = self._property_keys = []
            trans = self._trans_table = {}
            for akey in self._properties:
                if isinstance(akey, tuple):
                    keys.append(akey[0])
                    trans[akey[0]] = akey[1]
                else:
                    keys.append(akey)
        if key in self._property_keys:
            return self._backend()
        raise KeyError

    def delete_all(self):
        backend = self._backend()
        for key in self._properties:
            backend.delete(key)
