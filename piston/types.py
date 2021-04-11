


class PistonType:
    def __str__(self) -> str:
        return f"<{self.__class__.__name__}: {self.__dict__}>"

    def __repr__(self) -> str:
        return self.__str__()


class Language(PistonType):
    def __init__(
        self,
        r=dict,
        **kwargs
    ):
        self.name = r['name']
        self.aliases = r['aliases']
        try:
            self.version = r['version']
        except KeyError:
            self.version = None