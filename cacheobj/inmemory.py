
from .core import SimpleCacheObject
from .backends.inmemory import InMemoryBackend

_common_backend = None

def get_memory_backend():
    global _common_backend
    if not _common_backend:
        _common_backend = InMemoryBackend()
    return InMemoryBackend()

class InMemoryObject(SimpleCacheObject):
    _backend_generator = staticmethod(get_memory_backend)
