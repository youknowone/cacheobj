
import time
from cacheobj import CacheObject
from cacheobj.backends.inmemory import InMemoryBackend
from cacheobj.backends.memcache import MemcacheBackend
from cacheobj.backends.redis import RedisBackend
from cacheobj.inmemory import InMemoryObject
from cacheobj.redis import LocalRedisObject
from cacheobj.memcache import LocalMemcacheObject

memory = InMemoryBackend()
memcache = MemcacheBackend()
redis = RedisBackend()

class TestObject(CacheObject):
    _backends = {
        memory: ['mem1', 'mem2'],
        memcache: ['mc1', 'mc2'],
        redis: ['redis1', 'redis2'],
    }
    _strict = True

def test_object():
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

def test_reload():
    t = TestObject()
    assert t.mem1 == 'a'
    assert t.mem2 == 1
    assert t.mc1 == 'b'
    assert t.mc2 == 2
    assert t.redis1 == 'c'
    assert t.redis2 == '3' # redis is string based always

    t1 = TestObject(1)
    t.delete_all()

    assert t.mem1 is None
    assert t.mem2 is None
    assert t.mc1 is None
    assert t.mc2 is None
    assert t.redis1 is None
    assert t.redis2 is None

