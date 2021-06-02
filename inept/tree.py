import collections
from .types import Identity


NoDefault = object()


class Node:

    def __init__(self, name, type=bool, default=NoDefault, doc=None, nodes=()):
        self.name = None if name is None else str(name)
        self.doc = None if doc is None else str(doc)
        self.default = default
        self.nodes = list(nodes)
        self.type = type

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.name!r}>"

    @property
    def has_default(self):
        return self.default is not NoDefault

    def convert(self, value):
        type = self.type
        try:
            value = type(value)
        except Exception as err:
            raise ValueError(
                f"Wrong value ({value!r}) for {self!r}, "
                f"should be of type {type.__qualname__}."
            )
        return value

    def iter_edges(self):
        for child in self.nodes:
            yield (self, child)
            yield from child.iter_edges()

    def walk(self, filter=True):
        yield (self,)

    @staticmethod
    def name_from_path(path):
        assert all(isinstance(e, Node) for e in path)
        return '.'.join(e.name for e in path if e.name)

    def path_from_name(self, name):
        mapping = {Node.name_from_path(p): p for p in self.walk()}
        return mapping[name]

    def validate(self):
        pass

    def rename(self, name):
        res = object.__new__(type(self))
        res.__dict__.update(self.__dict__)
        res.name = None if name is None else str(name)
        return res


class Value(Node):

    def __init__(self, name, type=Identity, default=NoDefault, doc=None):
        assert name
        super().__init__(name, type=type, default=default, doc=doc)


class Group(Node):

    def __init__(self, name, nodes, default=NoDefault, doc=None):
        super().__init__(name, default=default, doc=doc, nodes=nodes)
        assert all(isinstance(e, Node) for e in nodes)

    def walk(self, filter=True):
        yield (self,)
        for node in self.nodes:
            for path in node.walk(filter):
                if filter:
                    head, *tail = path
                    if not tail and not isinstance(head, Value):
                        continue
                yield (self,) + path

    def validate(self):
        for child in self.nodes:
            if not isinstance(child, Node):
                raise ValueError(
                    f"nodes must {Node.__qualname__} objects, "
                    "get {child!r} instead."
                )
        names = [n.name for n in self.nodes]
        if len(names) != len(set(names)):
            dupes = [
                n for n, count in collections.Counter(names).items()
                if count > 1
            ]
            raise ValueError(f"duplicated names : {dupes}")
        for child in self.nodes:
            child.validate()


class Options(Group):

    def walk(self, filter=True):
        yield (self,)
        for node in self.nodes:
            for path in node.walk(filter):
                yield (self,) + path


class Switch(Options):

    def validate(self):
        super().validate()
        defaults = [
            n for n in self.nodes
            if n.has_default and not (isinstance(n, Group) and not n.default)
        ]
        if len(defaults) > 1:
            raise ValueError(
                "Can't have multiple nodes with default: "
                f"{list(defaults)}"
            )
