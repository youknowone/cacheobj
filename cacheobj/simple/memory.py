
from ..core import SimpleCacheObject
from ..backend.memory import MemoryBackend

_common_backend = None

def get_memory_backend():
    global _common_backend
    if not _common_backend:
        _common_backend = MemoryBackend()
    return MemoryBackend()

class MemoryObject(SimpleCacheObject):
    _backend_generator = staticmethod(get_memory_backend)
