
from ..core import SimpleCacheObject
from ..backend.file import JsonFileBackend

def get_file_backend(path='cacheobj.json'):
    return JsonFileBackend(path)

class LocalFileObject(SimpleCacheObject):
    _backend_generator = staticmethod(get_file_backend)
