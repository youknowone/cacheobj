
from .field import Field, SimpleField

class CacheObject(object):
    """
    General purpose cache object. _backends should be constant for default implementaiton.
    For dynamic overloading, try to override _backend_table or _backend_for_key.

    _backends should be formatted as like:

    from cacheobj.backend.memcache import MemcacheBackend
    from cacheobj.backend.redis import RedisBackend
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

    @property
    def _int_id(self):
        return int(self._id)

    def _get_key_func(self, field):
        def get_key(self, default=None, use_cache=False):
            result = field.get(self, default, read_cache=use_cache)
            return result
        return get_key

    def _set_key_func(self, field):
        def set_key(self, value, expiration=None, default=None, use_cache=False):
            result = field.set(self, value, expiration, read_cache=use_cache)
            return result
        return set_key

    def _del_key_func(self, backend, key):
        def del_key(self):
            cache_key = self._cache_key(key)
            result = backend.delete(cache_key)
            return result
        return del_key

    def _set_property(self, prop, backend):
        cls = self.__class__
        if not isinstance(prop, Field):
            assert type(prop) == str
            field = SimpleField(backend, prop)
        else:
            field = prop
            field.backend = backend
        field.owner = self

        get_key = self._get_key_func(field)
        set_key = self._set_key_func(field)
        setattr(cls, '_get_' + field.name, get_key)
        setattr(cls, '_set_' + field.name, set_key)
        setattr(cls, '_del_' + field.name, self._del_key_func(backend, field.key))
        setattr(cls, field.name, property(get_key, set_key))

    def _get(self, key, **params):
        getter = getattr(self, '_get_' + key)
        return getter(**params)

    def _set(self, key, value, **params):
        setter = getattr(self, '_set_' + key)
        return setter(value, **params)


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
                backend.delete(cache_key, commit=False)
            backend.commit()


class SimpleCacheObject(CacheObject):
    """
    SimpleCacheObject provides easy-to-inherit interface for one backend based cache object.

    Example:
    from cacheobj.backend.memory import MemoryBackend
    def backend_generator():
        return MemoryBackend()
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

    def _init(self):
        cls = self.__class__
        if hasattr(cls, '_SET'):
            return

        for prop in self._properties:
            self._set_property(prop, cls._backend())

        cls._SET = True

    def delete_all(self):
        backend = self._backend()
        for prop in self._properties:
            if not isinstance(prop, Field):
                field = SimpleField(backend, prop)
            else:
                field = prop
                field.backend = backend
            cache_key = self._cache_key(field.key)
            #print 'del:', cache_key
            backend.delete(cache_key, commit=False)
        backend.commit()
