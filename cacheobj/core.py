
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

        self._init()

    def _get_key_func(self, backend, key, trans):
        cache_key = self._cache_key(key)
        def get_key(self, default=None, use_cache=False):
            if use_cache:
                try:
                    return self._locals[key]
                except KeyError:
                    pass
            #print 'get:', cache_key
            result = backend.get(cache_key, default)
            if trans:
                result = trans(result)
            if use_cache:
                self._locals[key] = result
            return result
        return get_key
            
    def _set_key_func(self, backend, key):
        cache_key = self._cache_key(key)
        def set_key(self, value, expiration=None, default=None, use_cache=True):
            expiration = self._expiration_for_key(key) if expiration is None else expiration
            if value == default:
                result = backend.delete(cache_key)
            else:
                result = backend.set(self._cache_key(key), value, expiration)
            if use_cache:
                self._locals[key] = value
            return result
        return set_key
    
    def _del_key_func(self, backend, key):
        cache_key = self._cache_key(key)
        def del_key(self):
            result = backend.delete(cache_key)
            return result
        return del_key

    def _set_property(self, prop, backend):
        cls = self.__class__
        if isinstance(prop, tuple):
            key, trans = prop
        else: # str
            key = prop
            trans = None

        get_key = self._get_key_func(backend, key, trans)
        set_key = self._set_key_func(backend, key)
        setattr(cls, '_get_' + key, get_key)
        setattr(cls, '_set_' + key, set_key)
        setattr(cls, '_del_' + key, self._del_key_func(backend, key))
        setattr(cls, key, property(get_key, set_key))


    def _init(self):
        cls = self.__class__
        if hasattr(cls, '_SET'):
            return

        for backend, props in self._backends.items():
            for prop in props:
                self._set_property(prop, backend)

        cls._SET = True 

    @property
    def _cache_prefix(self):
        return self.__class__.__name__ + self._prefix

    def _cache_key(self, key):
        return '.'.join((self._cache_prefix, self._str_id, key))

    def _expiration_for_key(self, key):
        return self._expiration

    def delete_all(self):
        for backend, keys in self._backends.items():
            for key in keys:
                cache_key = self._cache_key(key)
                backend.delete(cache_key)


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
    
    def _init(self):
        cls = self.__class__
        if hasattr(cls, '_SET'):
            return

        backend = cls._backend = cls._backend_generator()
        for prop in self._properties:
            self._set_property(prop, backend)

        cls._SET = True 

    def delete_all(self):
        backend = self._backend
        for prop in self._properties:
            if isinstance(prop, tuple):
                key = prop[0]
            else:
                key = prop
            cache_key = self._cache_key(key)
            #print 'del:', cache_key
            backend.delete(cache_key)
