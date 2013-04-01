
import time
import pytest
from cacheobj.inmemory import InMemoryObject
from cacheobj.redis import LocalRedisObject
from cacheobj.memcache import LocalMemcacheObject

from cacheobj.field import SimpleField

class AMemoryObject(InMemoryObject):
    _properties = ['test1']
    _strict = True

mem1 = AMemoryObject()
mem2 = AMemoryObject()
memx = AMemoryObject(8)

class AMemcacheObject(LocalMemcacheObject):
    _properties = ['test1']
    _strict = True

mc1 = AMemcacheObject()
mc2 = AMemcacheObject()
mcx = AMemcacheObject(8)

def intif(v):
    try:
        return int(v)
    except:
        return v

class ARedisObject(LocalRedisObject):
    _properties = [SimpleField(None, 'test1', getfilter=intif)]
    _strict = True

rd1 = ARedisObject()
rd2 = ARedisObject()
rdx = ARedisObject(8)


@pytest.mark.parametrize(('obj',), [
    (mem1, ),
    (mc1, ),
    (rd1, ),
])
def test_basic(obj):
    obj.delete_all()
    assert obj.test1 is None
    obj.test1 = 10
    assert obj.test1 is not None
    obj.test1 = None
    assert obj.test1 is None
    obj._set_test1(20)
    assert obj._get_test1() == 20
    assert obj.test1 == obj._get_test1()
    obj._del_test1()
    assert obj.test1 is None


@pytest.mark.parametrize(('o1', 'o2'), [
    (mem1, mem2),
    (mc1, mc2),
    (rd1, rd2),
])
def test_reload(o1, o2):
    o1.test1 = 10
    assert o1.test1 == o2.test1

@pytest.mark.parametrize(('o1', 'o2'), [
    (mem1, memx),
    (mc1, mcx),
    (rd1, rdx),
])
def test_reloadx(o1, o2):
    """This tests object has separated scope or not"""
    o2.test1 = 5
    o1.test1 = 10
    assert o2.test1 != 10


def test_local_cache():
    t1, t2 = mc1, mc2

    t1.test1 = 1
    t2.test1 = 2

    assert t1._get_test1(use_cache=True) != t2._get_test1(use_cache=True)
    assert t1._get_test1() == t2._get_test1()

    t1.test1 = 1
    t2.test1 = 2
    assert t1._get('test1', use_cache=True) != t2._get('test1', use_cache=True)
    assert t1._get('test1') == t2._get('test1')

@pytest.mark.parametrize(('t1', 't2'), [
    (mem1, mem2),
    (mc1, mc2),
    (rd1, rd2),
])
def test_expiration(t1, t2):
    t1._set_test1(10, 1)
    assert t1.test1 == 10
    time.sleep(1)
    assert t1.test1 != 10
    
    t1._set_test1(10, 2)
    assert t1.test1 == 10
    time.sleep(1)
    assert t1.test1 == 10

