
from ..core import SimpleCacheObject
from ..backend.file import JsonFileBackend

def get_jsonfile_backend(path='cacheobj.json'):
    return JsonFileBackend(path)

class LocalJsonFileObject(SimpleCacheObject):
    _backend_generator = staticmethod(get_jsonfile_backend)
