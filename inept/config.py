import sys
import copy
import collections

import click

from .tree import Node, Group, Switch, Options, Value


class ValuePathError(Exception):
    pass


class RootDescriptor:

    def __get__(self, instance, owner=None):
        if instance is None:
            return owner.__root__
        return instance.__root__

    def __set__(self, instance, value):
        raise AttributeError("can't set attribute")


class ConfigTree:

    __root__ = Group(None, ())

    root = RootDescriptor()

    def __init__(self):
        self.validate_root(self.root)
        self.__base_path__ = ()
        self._node_ids = {}
        # _data is (local) + (intial default)
        self._data = collections.ChainMap({}, self._init_default())

    def _register(self, node, id=None):
        if node in self._node_ids:
            if id is None:
                return
            raise ValueError(f"node {node} is already registered")
        assert isinstance(node, Node)
        if id is None:
            id = hash(node)
        self._node_ids[node] = id

    def _id(self, node):
        return self._node_ids.get(node, None)

    def _init_default(self):
        _id = self._id
        data = {}
        self._register(self.root)
        if isinstance(self.root, Group):
            data[_id(self.root)] = True
        elif isinstance(self.root, Value) and self.root.has_default:
            data[_id(self.root)] = self.root.convert(self.root.default)
        for parent, child in self.root.iter_edges():
            if child.has_default:
                value = child.default
            elif isinstance(child, Value):
                continue
            elif isinstance(parent, Options):
                value = False
            elif isinstance(parent, Group):
                value = True
            else:
                continue
            self._register(child)
            data[_id(child)] = child.convert(value)
        return data

    def validate_root(self, root):
        assert isinstance(root, Node)
        root.validate()

    def all_keys(self):
        names = (Node.name_from_path(p) for p in self.root.walk(filter=False))
        names = (n for n in names if n)
        seen = set()
        seen_add = seen.add
        return [x for x in names if not (x in seen or seen_add(x))]

    def _get_base_path(self, node):
        for *base, leaf in self.root.walk(filter=False):
            if leaf == node:
                return tuple(base)
        raise ValueError(f"node {node} is not in self.root")

    def extract_node(self, node):
        base_path = self._get_base_path(node)
        root = node.rename(None)
        self._register(root, self._id(node))
        res = copy.copy(self)
        res.__root__ = root
        res.__base_path__ = base_path
        return res

    def iter_values(self):
        for path in self.root.walk():
            path = self.__base_path__ + path
            target = path[-1]
            try:
                yield path, self.get_value(path)
            except ValuePathError:
                pass

    def get_value(self, path):
        *path, target = path
        if not isinstance(target, Value):
            raise ValuePathError("not a Value")
        id_path = map(self._id, path)
        id_target = self._id(target)
        if all(map(self._data.get, id_path)) and id_target in self._data:
            return self._data[id_target]
        raise ValuePathError("inactive path")

    def __bool__(self):
        return any(True for _ in self.iter_values())


class ConfigMapping(ConfigTree):

    # TODO: complete the mapping API

    def info(self, msg):
        # FIXME On fait quoi pour les messages ? du logging ?
        # FIXME On garde vraiment ?
        print("INFO:", msg)

    def _get_path(self, key):
        return self.__base_path__ + self.root.path_from_name(key)

    def __getitem__(self, key):
        if not key:
            raise KeyError(key)
        path = self._get_path(key)
        target = path[-1]
        if isinstance(target, Value):
            try:
                return self.get_value(path)
            except ValuePathError:
                raise KeyError(key)
        else:
            return self.extract_node(target)

    def __setitem__(self, key, value):
        if not key:
            raise KeyError(key)
        _id = self._id
        path = self._get_path(key)
        target = path[-1]
        for parent, child in zip(path[:-1], path[1:]):
            self._register(parent)
            self._data[_id(parent)] = True
            if isinstance(parent, Switch):
                actives = {n for n in parent.nodes if self._data.get(_id(n))}
                if actives - {child}:
                    olds = ' and '.join(repr(e.name) for e in actives)
                    self.info(f"{olds} is owerwritten by '{child.name}'")
                    for node in actives:
                        for dct in self._data.maps:
                            dct.pop(_id(node), None)
        self._register(target)
        self._data[_id(target)] = target.convert(value)

    def __delitem__(self, key):
        raise NotImplementedError("TODO")

    def __or__(self, other):
        assert self.root == other.root
        res = type(self)()
        res._node_ids = self._node_ids | other._node_ids
        res._data.maps[0].update(self._data.maps[0])
        res._data.maps[0].update(other._data.maps[0])
        return res

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def update(self, data):
        for key, value in dict(data).items():
            self[key] = value


class ConfigCLI(ConfigMapping):

    def __init__(self, command_name=None, **kwds):
        super().__init__(**kwds)
        self.make_cli(command_name)

    @property
    def cli(self):
        return self._cli

    def make_cli(self, command_name):
        params = []
        for p in self.root.walk():
            name = Node.name_from_path(p)
            if not name:
                continue
            node = p[-1]
            opt = click.Option(
                [f"--{name}"],
                expose_value=False,
                type=self.get_type(node),
                help=node.doc,
            )
            opt.name = name
            opt.expose_value = True
            params.append(opt)
        help = self.root.doc
        self._cli = click.Command(command_name, params=params, help=help)

    @staticmethod
    def get_type(node):
        type = getattr(node, "type", None)
        type = getattr(type, '__click_type__', type)
        return type

    def parse_cli(self, args=None, **extra):
        if args is None:
            args = sys.argv[1:]
        ctx = self.cli.make_context(self.cli.name, args, **extra)
        return {k: v for k, v in ctx.params.items() if v is not None}

    def load_cli(self, args=None, **extra):
        try:
            self.update(self.parse_cli(args, **extra))
        except click.exceptions.Exit as err:
            sys.exit(err.exit_code)


class ConfigSerialize(ConfigTree):

    def to_dict(self):
        res = {}
        base_path = self.__base_path__
        n = len(base_path)
        for path, value in self.iter_values():
            assert path[:n] == base_path
            key = Node.name_from_path(path[n:])
            res[key] = value
        return res

    def to_nested_dict(self):
        res = {}
        base_path = list(self.__base_path__)
        n = len(base_path)
        for (*path, target), value in self.iter_values():
            assert path[:n] == base_path
            data = res
            for node in path[n:]:
                if node.name:
                    data = data.setdefault(node.name, {})
            if isinstance(target, Value):
                data[target.name] = value
        return res


class ConfigBase(ConfigSerialize, ConfigCLI, ConfigMapping):
    pass


class ConfigSimple(ConfigBase):

    def __init__(self, root, **kwds):
        self.__root__ = root
        super().__init__(**kwds)

