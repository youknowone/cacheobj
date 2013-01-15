
from cacheobj import CacheObject
from cacheobj.backends.inmemory import InMemoryBackend
from cacheobj.backends.memcacheb import MemcacheBackend
from cacheobj.backends.redisb import RedisBackend
from cacheobj.inmemory import InMemoryObject
from cacheobj.rediso import LocalRedisObject
from cacheobj.memcacheo import LocalMemcacheObject

memory = InMemoryBackend()
memcache = MemcacheBackend()
redis = RedisBackend()

class TestObject(CacheObject):
    _backends = {
        memory: ['mem1', 'mem2'],
        memcache: ['mc1', 'mc2'],
        redis: ['redis1', 'redis2'],
    }

t = TestObject()
assert t._cache_key('key') == 'TestObject.0.key'

t.mem1 = 'a'
assert t.mem1 == 'a'
t.mem2 = 1

try:
    t.mc1 = 'b'
    assert t.mc1 == 'b'
    t.mc2 = 2
except:
    print 'local memcache server looks not available.'
    raise

try:
    t.redis1 = 'c'
    assert t.redis1 == 'c'
    t.redis2 = 3
except:
    print 'local redis server looks not available.'
    raise

t = TestObject()
assert t.mem1 == 'a'
assert t.mem2 == 1
assert t.mc1 == 'b'
assert t.mc2 == 2
assert t.redis1 == 'c'
assert t.redis2 == '3' # redis is string based always

t = TestObject(1)
assert t.mem1 is None

class AMemoryObject(InMemoryObject):
    _properties = ['test1']

t = AMemoryObject()
t.test1 = 10

t = AMemoryObject()
assert t.test1 == 10


class AMemcacheObject(LocalMemcacheObject):
    _properties = ['test1']

t = AMemcacheObject()
t.test1 = 10

t = AMemcacheObject()
assert t.test1 == 10


class ARedisObject(LocalRedisObject):
    _properties = ['test1']

t = ARedisObject()
t.test1 = 10

t = ARedisObject()
assert t.test1 == '10'


t1 = AMemcacheObject()
t2 = AMemcacheObject()

t1.test1 = 1
t2.test1 = 2

assert t1.get('test1', use_cache=True) != t2.get('test1', use_cache=True)
assert t1.get('test1') == t2.get('test1')
