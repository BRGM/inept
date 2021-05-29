import collections
from .types import Identity


NoDefault = object()


class Node:

    def __init__(self, name, default=NoDefault, doc=None, nodes=()):
        self.name = None if name is None else str(name)
        self.doc = None if doc is None else str(doc)
        self.default = default
        self.nodes = list(nodes)

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.name!r}>"

    @property
    def has_default(self):
        return self.default is not NoDefault

    def walk(self):
        yield (self,)

    @staticmethod
    def name_from_path(path):
        assert all(isinstance(e, Node) for e in path)
        return '.'.join(e.name for e in path if e.name)

    def validate(self):
        pass


class Value(Node):

    def __init__(self, name, type=Identity, default=NoDefault, doc=None):
        assert name
        super().__init__(name, default, doc)
        self.type = type


class Group(Node):

    def __init__(self, name, nodes, default=NoDefault, doc=None):
        super().__init__(name, default, doc, nodes)
        assert all(isinstance(e, Node) for e in nodes)

    def walk(self):
        yield (self,)
        for node in self.nodes:
            for path in node.walk():
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

    def walk(self):
        yield (self,)
        for node in self.nodes:
            for path in node.walk():
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
