

NoDefault = object()


class Node:

    def __init__(self, name, default=NoDefault, doc=None, nodes=()):
        self.name = None if name is None else str(name)
        self.doc = None if doc is None else str(doc)
        self.default = default
        self.nodes = list(nodes)

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

    def validate(self):
        pass


class Option(Node):
    def __init__(self, name, type=None, default=NoDefault, doc=None):
        assert name
        super().__init__(name, default, doc)
        self.type = type or (lambda x: x)


class Group(Node):
    def __init__(self, name, nodes, is_flag=False, default=NoDefault, doc=None):
        super().__init__(name, default, doc, nodes)
        assert all(isinstance(e, Node) for e in nodes)
        self.is_flag = bool(is_flag)

    def is_option(self):
        return super().is_option() and self.is_flag

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


class Exclusive(Group):

    def validate(self):
        super().validate()
        defaults = {n: n.default for n in self.nodes if n.has_default}
        if len(defaults) > 1:
            raise ValueError(
                "Can't have multiple nodes with default: "
                f"{list(defaults)}"
            )
