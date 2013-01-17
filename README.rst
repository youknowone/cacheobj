Cache object
~~~~~~~~~~~~

Cache object is general purpose object-property interface.

Example
-------
There is some pre-defined common types.

in-memory, memcache and redis backends are included. And its common general interfaces too.

    >>> from cacheobj.redis import LocalRedisObject
    >>> class UserCache(LocalRedisObject):
    ...   _properties = ['username', 'name']
    ... 
    >>> user = UserCache(id=10)
    >>> print user.username
    None
    >>> user.username = 'username'
    >>> user.name = 'Real Name'
    >>> print user.username
    username
    >>> user10 = UserCache(id=10)
    >>> print user10.username
    username

Cache is stored with class name and given id.

    >>> print user.get('username', use_cache=True)
    username

If you don't want to hit backend again, there is use_cache option for local memory cache.

For non-local cache backend, try a easy generator.

    >>> from cacheobj.redis import get_redis_object
    >>> import redis
    >>> MyRedisObject = get_redis_object(redis.ConnectionPool()) # any connection pool
    >>> class MyUserCache(MyRedisObject):
    ...   pass
    ... 

Custom Backend
--------------

Upper examples are shortcut for basic configuration.

    >>> from cacheobj import SimpleCacheObject
    >>> from cacheobj.backends.memcache import MemcacheBackend
    >>> def get_backend():
    ...   return MemcacheBackend(['127.0.0.1:11211'])
    ...
    >>> class UserCache(SimpleCacheObject):
    ...   _backend_generator = staticmethod(get_backend)
    ...   _properties = ['username', 'name']
    ...

This object works as upper UserCache object.
You can put custom backend with this.

See source code to write a backend. It is just a few lines.

Composite Example
-----------------

You can composite multiple backends for an object.

    >>> from cacheobj import CacheObject
    >>> from cacheobj.backends.inmemory import InMemoryBackend
    >>> from cacheobj.backends.memcache import MemcacheBackend
    >>> from cacheobj.backends.redis import RedisBackend
    >>> 
    >>> memory = InMemoryBackend()
    >>> memcache = MemcacheBackend()
    >>> redis = RedisBackend()
    >>>
    >>> class CompositeCache(CacheObject):
    ... _backends = {
    ...   memory: ['mem1', 'mem2'],
    ...   memcache: ['mc1', 'mc2'],
    ...   redis: ['redis1', 'redis2'],
    ... }
    ...
    >>> c = CompositeCache()
    >>> c.mem1 # with backend memory
    >>> c.mc1 # with backend memcache
    >>> c.redis1 # with backend redis

