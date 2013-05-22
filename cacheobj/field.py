
def pass_filter(value):
    return value

class Field(object):
    def __init__(self, name, key=None):
        self.name = name
        self.key = key if key else name
        self.has_cache = False

    def cache_key(self, cobj):
        return cobj._cache_key(self.key)

class SimpleField(Field):
    def __init__(self, backend, name, key=None, expiration=None, default=None,
                 getfilter=pass_filter, setfilter=pass_filter):
        self.name = name
        self.key = key if key else name
        self.cache = default
        self.owner = None

        self.expiration = expiration
        self.default = default
        self.backend = backend
        self.getfilter = getfilter
        self.setfilter = setfilter

    def get(self, cobj, default=None, read_cache=False, write_cache=True):
        if read_cache and self.key in cobj._locals:
            return cobj._locals[self.key]
        result = self.getfilter(self.backend.get(self.cache_key(cobj), default))
        if write_cache:
            cobj._locals[self.key] = result
        return result

    def set(self, cobj, value, expiration=None, default=None, read_cache=False, write_cache=True):
        if read_cache and self.key in cobj._locals and cobj._locals[self.key] == value:
            return
        if value != default:
            if expiration is None:
                expiration = self.expiration
            value = self.setfilter(value)
            result = self.backend.set(self.cache_key(cobj), value, expiration)
        else:
            result = self.backend.delete(self.cache_key(cobj))
        if write_cache:
            cobj._locals[self.key] = value
        return result

