

import pytest
from cacheobj.backends.inmemory import InMemoryBackend
from cacheobj.backends.memcache import MemcacheBackend
from cacheobj.backends.redis import RedisBackend

memory = InMemoryBackend()
memcache = MemcacheBackend()
redis = RedisBackend()

memory2 = InMemoryBackend()
memcache2 = MemcacheBackend()
redis2 = RedisBackend()

@pytest.mark.parametrize(('backend',),
    [(memory,),
     (memcache,),
     (redis,)
])
def test_backend(backend):
    v = backend.get('foo') # just do not raise error
    backend.set('foo', 'bar')
    v = backend.get('foo')
    assert v == 'bar'


@pytest.mark.parametrize(('b1', 'b2'),
    [(memory, memory2),
     (memcache, memcache2),
     (redis, redis2)
])
def test_backends(b1, b2):
    b1.set('foo', 'bar')
    v = b2.get('foo')
    assert v == 'bar'
