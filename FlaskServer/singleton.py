

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]



#def metaclass_resolver(*classes):
#    metaclass = tuple(set(type(cls) for cls in classes))
#    metaclass = metaclass[0] if len(metaclass)==1 \
#                else type("_".join(mcls.__name__ for mcls in metaclass), metaclass, {})
#    return metaclass("_".join(cls.__name__ for cls in classes), classes, {})    