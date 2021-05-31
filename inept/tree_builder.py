from typing import NamedTuple

from . import tree


class AnnotationsDict(dict):

    def __init__(self, namespace):
        self.namespace = namespace

    def __setitem__(self, key, value):
        if self.namespace.level == 0:
            return super().__setitem__(key, value)
        self.namespace.add_type(key, value)


class TreeBuilderNamespace(dict):

    __doc_key__ = '_'

    def __init__(self):
        self.annotations = AnnotationsDict(self)
        self.group = GroupContextManager
        self.switch = SwitchContextManager
        self.extra_new = dict(
            group=self.group(self),
            switch=self.switch(self),
        )
        self.extra = dict(
            __annotations__=self.annotations,
        )
        self._stack = []
        self._entering = False
        self._groups = {}
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
        if key in self.extra_new:
            return self.extra_new[key].new()
        raise KeyError(key)

    def __setitem__(self, key, value):
        if self.level == 0:
            return super().__setitem__(key, value)
        if key == self.__doc_key__:
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
        if node.name == key:
            assert isinstance(node, tree.Value)
            node.type = value
        else:
            self.record(key, tree.NoDefault)
            self._last_record.type = value

    def parent(self, obj):
        if isinstance(obj, GroupContextManagerBase):
            if len(self._stack) >= 2:
                return self._stack[-2]
            else:
                return None
        return self.cm

    def record(self, name, obj):
        if isinstance(obj, GroupContextManagerBase):
            kwds = {}
            if isinstance(obj, GroupContextManager):
                node = tree.Group(name, [], **kwds)
            elif isinstance(obj, SwitchContextManager):
                node = tree.Switch(name, [], **kwds)
            self._groups[obj] = node
            if self.root is None:
                self.root = node
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

    @classmethod
    def __prepare__(mcls, name, bases, **kwds):
        return TreeBuilderNamespace()

    def __new__(mcls, name, bases, namespace):
        root = namespace.root
        namespace = dict(namespace)
        namespace['root'] = root
        return type.__new__(mcls, name, bases, namespace)


class GroupContextManagerBase:

    def __init__(self, namespace, *args, **kwds):
        self.namespace = namespace
        self.args = args
        self.kwds = kwds

    def new(self):
        return type(self)(self.namespace, *self.args, **self.kwds)

    def __enter__(self):
        self.namespace.enter(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.namespace.exit(self)

    def __call__(self, *args, **kwds):
        return type(self)(self.namespace, *args, **kwds)


class GroupContextManager(GroupContextManagerBase):
    pass


class SwitchContextManager(GroupContextManagerBase):
    pass


class TreeBuilder(metaclass=TreeBuilderMeta):
    pass

