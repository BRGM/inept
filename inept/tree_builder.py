from . import tree


class GroupContextManagerBase:

    def __init__(self, namespace, **kwds):
        self.namespace = namespace
        self.kwds = kwds

    def __enter__(self):
        self.namespace.enter(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.namespace.exit(self)

    @property
    def on(self):
        return type(self)(self.namespace, default=True)

    @property
    def off(self):
        return type(self)(self.namespace, default=False)

class GroupContextManager(GroupContextManagerBase):
    node_type = tree.Group


class OptionsContextManager(GroupContextManagerBase):
    node_type = tree.Options


class SwitchContextManager(GroupContextManagerBase):
    node_type = tree.Switch


class ContextManagerNamespace:
    def __init__(self, namespace):
        self.__namespace__ = namespace

    @property
    def group(self):
        return GroupContextManager(self.__namespace__)

    @property
    def options(self):
        return OptionsContextManager(self.__namespace__)

    @property
    def switch(self):
        return SwitchContextManager(self.__namespace__)


class AnnotationsDict(dict):

    def __init__(self, namespace):
        self.namespace = namespace

    def __setitem__(self, key, value):
        if self.namespace.level == 0:
            return super().__setitem__(key, value)
        self.namespace.add_type(key, value)


class TreeBuilderNamespace(dict):

    def __init__(self, magic_name):
        self._magic_name = str(magic_name)
        self.extra = {
            '__annotations__': AnnotationsDict(self),
            self._magic_name: ContextManagerNamespace(self),
        }
        self._stack = []
        self._entering = False
        self._groups = {}
        self._injected_nodes = set()
        self.root = None

    @property
    def level(self):
        return len(self._stack)

    @property
    def cm(self):
        return self._stack[-1] if self._stack else None

    def __getitem__(self, key):
        try:
            return super().__getitem__(key)
        except KeyError:
            pass
        if key in self.extra:
            return self.extra[key]
        raise KeyError(key)

    def __setitem__(self, key, value):
        if self.level == 0:
            return super().__setitem__(key, value)
        if key == self._magic_name:
            return self.add_doc(value)
        entering, self._entering = self._entering, False
        if entering and value is self.cm:
            self._last_record.name = key
        else:
            self.record(key, value)

    def add_doc(self, value):
        assert isinstance(value, str)
        assert self._last_record.doc is None
        self._last_record.doc = value

    def add_type(self, key, value):
        node = self._last_record
        if node in self._injected_nodes:
            raise SyntaxError(
                "do not use annotation when assigning an existing tree"
                f" ('{key}: {value} = ...')"
            )
        if node.name == key:
            assert isinstance(node, tree.Value)
            node.type = value
        else:
            self.record(key, tree.NoDefault)
            self._last_record.type = value

    def parent(self, obj):
        if isinstance(obj, GroupContextManagerBase):
            if self.level >= 2:
                return self._stack[-2]
            else:
                return None
        return self.cm

    def record(self, name, obj):
        if isinstance(obj, GroupContextManagerBase):
            node = obj.node_type(name, [], **obj.kwds)
            self._groups[obj] = node
            if self.root is None:
                self.root = node
        elif isinstance(obj, tree.Node):
            node = obj.rename(name)
            self._injected_nodes.add(node)
        else:
            node = tree.Value(name, None, obj)
        parent = self.parent(obj)
        if parent:
            self._groups[parent].nodes.append(node)
        self._last_record = node

    def enter(self, cm):
        assert isinstance(cm, GroupContextManagerBase)
        self._stack.append(cm)
        self.record(None, cm)
        self._entering = True

    def exit(self, cm):
        assert cm is self._stack.pop()


class TreeBuilderMeta(type):

    __namespace_key__ = '_'

    @classmethod
    def __prepare__(mcls, name, bases, **kwds):
        return TreeBuilderNamespace(mcls.__namespace_key__)

    def __new__(mcls, name, bases, namespace):
        root = namespace.root
        if root is not None:
            root.validate()
        namespace = dict(namespace)
        namespace['root'] = root
        return type.__new__(mcls, name, bases, namespace)


class TreeBuilder(metaclass=TreeBuilderMeta):
    pass

