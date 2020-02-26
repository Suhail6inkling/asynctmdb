class Object:
    def __eq__(self, other):
        if isinstance(other, Object):
            try:
                return type(self) is type(other) and self.id == other.id 
            except:
                return super().__eq__(other)
        return super().__eq__(other)

class AttributedDict(Object):
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)