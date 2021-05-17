

NoDefault = object()


class Node:
    name = None
    nodes = ()
    default = NoDefault

    def __init__(self, name, is_flag=False):
        self.name = None if name is None else str(name)
        self.is_flag = bool(is_flag)

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.name!r}>"

    def is_option(self):
        return self.name is not None

    @property
    def has_default(self):
        return self.default is not NoDefault

    def walk(self):
        if self.is_option():
            yield (self,)
        for node in self.nodes:
            for path in node.walk():
                yield (self,) + path

    @staticmethod
    def name_from_path(path):
        assert all(isinstance(e, Node) for e in path)
        return '.'.join(e.name for e in path if e.name)


class Option(Node):
    def __init__(self, name, type=None, default=NoDefault, *args, **kwds):
        assert name
        super().__init__(name, *args, **kwds)
        self.type = type or (lambda x: x)
        self.default = default


class Group(Node):
    def __init__(self, name, nodes, *args, **kwds):
        super().__init__(name, *args, **kwds)
        assert all(isinstance(e, Node) for e in nodes)
        self.nodes = list(nodes)

    def is_option(self):
        return super().is_option() and self.is_flag


class Exclusive(Group):
    pass

