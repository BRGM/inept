from importlib_metadata import version, PackageNotFoundError
try:
    __version__ = version("inept")
except (PackageNotFoundError, ModuleNotFoundError):
    # package is not installed
    pass


from .tree import Value, Group, Options, Switch
from .tree_builder import TreeBuilder
from .config import ConfigSimple, ConfigBase


class Config(TreeBuilder, ConfigBase):
    pass

