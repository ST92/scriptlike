g = globals()
import pathlib, functools

class Scriptlike:
    def __init__(self, path):
        self.__path = path
        self.__clean = dict(
            **g,
        )
        self.__clean.pop('Scriptlike')
        self.__clean.pop('g')
        self.__box = dict()
        self.__update()
        
    def __update(self):
        for k in self.__box.keys():
            if k in self.__dict__:
                val = self.__dict__[k]
                if callable(val):
                    if val.__doc__.endswith('\nscriptlike'):
                        self.__dict__.pop(k)

        self.__box = dict(
            **self.__clean
        )
        script = self.__path.read_text()
        exec(script, self.__box)
        
    
        for k,v in self.__box.items():
            if callable(v):
                self.__dict__[k] = self.__wrap(k)
    
    def __wrap(self, name):
        def _call(*args, **kwargs):
            self.__update()
            return self.__box.get(name)(*args, **kwargs) # type: ignore
        functools.update_wrapper(_call, self.__box.get(name))
        if not _call.__doc__: _call.__doc__=''
        _call.__doc__+='\nscriptlike'
        return _call
     
    def __getattribute__(self, __name: str):
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            if __name.startswith('__'):
                raise
            try:
                v = self.__box.get(__name)
                if callable(v):
                    return self.__wrap(__name) # redundant!
                return v
            except IndexError:
                raise AttributeError(__name)
        

for scriptfile in pathlib.Path(__file__).parent.glob('*.py'):
    if scriptfile.samefile(__file__):
        continue
    
    globals()[scriptfile.name[:-3]] = Scriptlike(scriptfile)
    del scriptfile


