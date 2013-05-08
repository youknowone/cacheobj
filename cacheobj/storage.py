
class Storage(object):
    def __init__(self, backend, keygen):
        self._backend = backend
        if callable(keygen):
            self._keygen = keygen
        else:
            def _keygen(key):
                key = '.'.join((keygen, key))
                return key
            self._keygen = _keygen

    def _get(self, key, default=None):
        return self._backend.get(self._keygen(key), default=default)

    def _set(self, key, value, expiration=None, default=None, commit=True):
        return self._backend.set(self._keygen(key), value, expiration, commit=commit)

    def _del(self, key, commit=True):
        return self._backend.delete(self._keygen(key), commit=commit)

    def _commit(self):
        return self._backend.commit()

    def __getattr__(self, key):
        if key[0] == '_':
            if key.startswith('_get_'):
                def _get_(default=None):
                    return self._get(key[5:], default)
                return _get_
            elif key.startswith('_set_'):
                def _set_(value, expiration=None, default=None, commit=True):
                    return self._set(key[5:], value, expiration, default, commit)
                return _set_
            elif key.startswith('_del_'):
                def _del_():
                    return self._del(key[5:])
                return _del_
            else:
                try:
                    return super(Storage, self).__getattr__(key)
                except AttributeError:
                    return self.__getattribute__(key)
        else:
            return self._get(key)

    def __setattr__(self, key, value):
        if key[0] == '_':
            return super(Storage, self).__setattr__(key, value)
        else:
            return self._set(key, value)
