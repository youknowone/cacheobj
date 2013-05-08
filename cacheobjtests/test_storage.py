

import pytest

from cacheobj.storage import Storage

from cacheobj.backend.memory import MemoryBackend
from cacheobj.backend.file import JsonFileBackend
from cacheobj.backend.memcache import MemcacheBackend
from cacheobj.backend.redis import RedisBackend

memory = MemoryBackend()
jsonfile = JsonFileBackend()
memcache = MemcacheBackend()
redis = RedisBackend()

@pytest.mark.parametrize(('backend',),
    [(memory,),
     (jsonfile,),
     (memcache,),
     (redis,)
])
def test_storage(backend):
    storage = Storage(backend, 'test')
    storage.foo = None # reset
    storage.foo = '1'
    assert '1' == storage.foo
    storage._set_foo('2')
    assert '2' == storage.foo
    assert '2' == storage._get_foo()
    assert '2' == storage._get('foo')
    storage._del('foo')
    assert None == storage.foo
