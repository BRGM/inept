import sys
import click

from .tree import Node, Group, Exclusive, Option


class ConfigBase:

    root = Group(None, ())

    def __init__(self):
        self._data = {}
        self.validate_root(self.root)

    def validate_root(self, root):
        assert isinstance(root, Node)
        root.validate()

    def update(self, data):
        for key, value in dict(data).items():
            self[key] = value

    @property
    def valid_keys(self):
        return [Node.name_from_path(p) for p in self.root.walk()]

    def info(self, msg):
        # FIXME On fait quoi pour les messages ? du logging ?
        print("INFO:", msg)

    def path_from_name(self, name):
        mapping = {Node.name_from_path(p): p for p in self.root.walk()}
        return mapping[name]

    def _walk_path(self, key):
        path = self.path_from_name(key)
        yield from zip(path[:-1], path[1:])

    def __setitem__(self, key, value):
        data = self._data
        for parent, child in self._walk_path(key):
            data = data.setdefault(parent, {})
            if isinstance(parent, Exclusive) and not {child}.issuperset(data.keys()):
                olds = ' and '.join(repr(e.name) for e in data.keys())
                self.info(f"{olds} is owerwritten by '{child.name}'")
                data.clear()
        if isinstance(child, Option):
            type = child.type
            try:
                value = type(value)
            except Exception as err:
                raise ValueError(
                    f"Wrong value ({value!r}) for {key!r}, "
                    f"should be of type {type.__qualname__}."
                )
            else:
                data[child] = value
        elif isinstance(child, Group):
            if value:
                data.setdefault(child, {})
            else:
                data.pop(child)
        else:
            raise RuntimeError(f"Not able to handle key {key!r}")

    def __getitem__(self, key):
        data = self._data
        for parent, child in self._walk_path(key):
            is_missing = parent not in data
            data = data.get(parent, {})

            if isinstance(parent, Exclusive):
                if not {child}.issuperset(data.keys()):
                    raise KeyError(key)
                if data:
                    continue
                if isinstance(child, Group) and not (child.has_default and child.default):
                    raise KeyError(key)
            elif isinstance(parent, Group) and parent.is_flag:
                is_valid = parent.has_default and parent.default
                if is_missing and not is_valid:
                    raise KeyError(key)

        if child in data:
            if isinstance(child, Option):
                return data[child]
            else:
                return True
        elif child.has_default:
            return child.default
        raise KeyError(key)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __delitem__(self, key):
        raise NotImplementedError("TODO")


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
            node = p[-1]
            opt = click.Option(
                [f"--{name}"],
                expose_value=False,
                type=self.get_type(node),
                help=node.doc,
                # is_flag=node.is_flag,
            )
            opt.name = name
            opt.expose_value = True
            params.append(opt)
        self._cli = click.Command(command_name, params=params)

    @staticmethod
    def get_type(node):
        if isinstance(node, Group) and node.is_flag:
            return bool
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
            if isinstance(path[-1], Option):
                data[path[-1].name] = value
        return res


class ConfigSimple(ConfigSerialize, ConfigCLI, ConfigBase):

    def __init__(self, root, **kwds):
        self._root = root
        super().__init__(**kwds)

    @property
    def root(self):
        return self._root

