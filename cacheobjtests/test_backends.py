

import pytest
from cacheobj.backends.inmemory import InMemoryBackend
from cacheobj.backends.memcache import MemcacheBackend
from cacheobj.backends.redis import RedisBackend

memory = InMemoryBackend()
memcache = MemcacheBackend()
redis = RedisBackend()

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