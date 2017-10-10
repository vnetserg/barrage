
class Attributed:
    attrs = []

    def __init__(self, *args):
        for attr, arg in zip(self.attrs, args):
            setattr(self, attr, arg)
        for attr in self.attrs:
            if not hasattr(self, attr):
                setattr(self, attr, None)
    
    def __str__(self):
        return "{}({})".format(self.__class__.__name__,
                                ", ".join("{}={}".format(attr, getattr(self, attr)) for attr in self.attrs))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        for attr in self.attrs:
            if getattr(self, attr) != getattr(other, attr):
                return False
        return True
