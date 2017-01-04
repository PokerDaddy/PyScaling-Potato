from abc import ABCMeta, abstractproperty, abstractmethod

class PathedObject(object):
    __metaclass__ = ABCMeta

    def __init__(self, path):
        self.path = path

    @abstractmethod
    def __call__(self, **kwargs):
        return

    @abstractmethod
    def set(self, path, value):
        return

    def __setitem__(self, name, value):
        if name == "path":
            self.__dict__[name] = value

        self.set(self.joiner(self.path, name), value)

    def __inherit__(self, newpath):
        return cls( newpath )

    def __getitem__(self, name):
        cls = type(self)

        return self.__inherit__( self.joiner(self.path, name) )

    #def __setattr__(self, name, value):
    #    self[name] = value

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        
        return self[name]

    def __repr__(self):
        return str(self())
