import sys
import collections
import click

from .tree import Node, Group, Switch, Options, Value


class ConfigMapping:

    root = Group(None, ())

    def __init__(self):
        self.validate_root(self.root)
        self._base_path = ()
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

    def update(self, data):
        for key, value in dict(data).items():
            self[key] = value

    def __iter__(self):
        names = (Node.name_from_path(p) for p in self.root.walk())
        return (n for n in names if n)

    def info(self, msg):
        # FIXME On fait quoi pour les messages ? du logging ?
        print("INFO:", msg)

    def _get_path(self, key):
        return self._base_path + self.root.path_from_name(key)

    def __getitem__(self, key):
        if not key:
            raise KeyError(key)
        *path, target = self._get_path(key)
        path = map(self._id, path)
        id_target = self._id(target)
        if all(map(self._data.get, path)) and id_target in self._data:
            if isinstance(target, Value):
                return self._data[id_target]
            elif self._data[id_target]:
                return True
        raise KeyError(key)

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
        res._node_ids = self._node_ids | other._node_ids
        res._data.maps[0].update(self._data.maps[0])
        res._data.maps[0].update(other._data.maps[0])
        return res


class ConfigExtract(ConfigMapping):

    def _get_base_path(self, node):
        for *base, leaf in self.root.walk(filter=False):
            if leaf == node:
                return tuple(base)
        raise ValueError(f"node {node} is not in self.root")

    def extract_node(self, node):
        base_path = self._get_base_path(node)
        root = node.rename(None)
        self._register(root, self._id(node))
        res = type(self)()
        res.root = root
        res._base_path = base_path
        res._node_ids = self._node_ids
        res._data = self._data
        return res


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


class ConfigSerialize(ConfigMapping):

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


class ConfigBase(ConfigSerialize, ConfigCLI, ConfigExtract, ConfigMapping):
    pass


class ConfigSimple(ConfigBase):

    def __init__(self, root, **kwds):
        self._root = root
        super().__init__(**kwds)

    @property
    def root(self):
        return self._root

