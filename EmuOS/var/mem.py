class Memory:
    _shared_variables = {}

    @classmethod
    def get(cls, name, default=None):
        return cls._shared_variables.get(name, default)

    @classmethod
    def set(cls, name, value):
        cls._shared_variables[name] = value

    @classmethod
    def delete(cls, name):
        if name in cls._shared_variables:
            del cls._shared_variables[name]
