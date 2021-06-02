import sys
import collections
import click

from .tree import Node, Group, Switch, Options, Value


class ConfigBase:

    root = Group(None, ())

    def __init__(self):
        self.validate_root(self.root)
        # _data is (local) + (intial default)
        self._data = collections.ChainMap({}, self._init_default())

    def _init_default(self):
        data = {}
        if isinstance(self.root, Group):
            data[self.root] = True
        elif isinstance(self.root, Value) and self.root.has_default:
            data[self.root] = self.root.convert(self.root.default)
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
            data[child] = child.convert(value)
        return data

    def validate_root(self, root):
        assert isinstance(root, Node)
        root.validate()

    def update(self, data):
        for key, value in dict(data).items():
            self[key] = value

    def __iter__(self):
        names = (Node.name_from_path(p) for p in self.root.walk())
        return (n for n in names if n)

    def info(self, msg):
        # FIXME On fait quoi pour les messages ? du logging ?
        print("INFO:", msg)

    def __getitem__(self, key):
        if not key:
            raise KeyError(key)
        *path, target = self.root.path_from_name(key)
        if all(map(self._data.get, path)) and target in self._data:
            if isinstance(target, Value):
                return self._data[target]
            elif self._data[target]:
                return True
        raise KeyError(key)

    def __setitem__(self, key, value):
        if not key:
            raise KeyError(key)
        path = self.root.path_from_name(key)
        target = path[-1]
        for parent, child in zip(path[:-1], path[1:]):
            self._data[parent] = True
            if isinstance(parent, Switch):
                actives = {n for n in parent.nodes if self._data.get(n)}
                if actives - {child}:
                    olds = ' and '.join(repr(e.name) for e in actives)
                    self.info(f"{olds} is owerwritten by '{child.name}'")
                    for node in actives:
                        for dct in self._data.maps:
                            dct.pop(node, None)
        self._data[target] = target.convert(value)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self, key):
        raise NotImplementedError("TODO")

    def __or__(self, other):
        assert self.root == other.root
        res = type(self)()
        res._data.maps[0].update(self._data.maps[0])
        res._data.maps[0].update(other._data.maps[0])
        return res


class ConfigCLI(ConfigBase):

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
        self._cli = click.Command(command_name, params=params)

    @staticmethod
    def get_type(node):
        type = getattr(node, "type", None)
        type = getattr(type, '__click_type__', type)
        return type

    def parse_cli(self, args=None, **extra):
        if args is None:
            args = sys.argv[1:]
        ctx = self.cli.make_context(self.cli.name, args, **extra)
        # ctx = self.cli.make_context(None, args, **extra)
        return {k: v for k, v in ctx.params.items() if v is not None}

    def load_cli(self, args=None, **extra):
        self.update(self.parse_cli(args, **extra))


class ConfigSerialize(ConfigBase):

    def to_dict(self):
        res = {}
        for path in self.root.walk():
            key = Node.name_from_path(path)
            try:
                value = self[key]
            except KeyError:
                continue
            res[key] = value
        return res

    def to_nested_dict(self):
        res = {}
        for path in self.root.walk():
            key = Node.name_from_path(path)
            try:
                value = self[key]
            except KeyError:
                continue
            data = res
            for node in path[:-1]:
                if node.name:
                    data = data.setdefault(node.name, {})
            if isinstance(path[-1], Value):
                data[path[-1].name] = value
        return res


class ConfigSimple(ConfigSerialize, ConfigCLI, ConfigBase):

    def __init__(self, root, **kwds):
        self._root = root
        super().__init__(**kwds)

    @property
    def root(self):
        return self._root

