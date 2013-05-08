

import pytest
from cacheobj.backend.memory import MemoryBackend
from cacheobj.backend.file import JsonFileBackend
from cacheobj.backend.memcache import MemcacheBackend
from cacheobj.backend.redis import RedisBackend

memory = MemoryBackend()
file = JsonFileBackend()
memcache = MemcacheBackend()
redis = RedisBackend()

memory2 = MemoryBackend()
file2 = JsonFileBackend()
memcache2 = MemcacheBackend()
redis2 = RedisBackend()

@pytest.mark.parametrize(('backend',),
    [(memory,),
     (file,),
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
     (file, file2),
     (memcache, memcache2),
     (redis, redis2)
])
def test_backends(b1, b2):
    b1.set('foo', 'bar')
    v = b2.get('foo')
    assert v == 'bar'
