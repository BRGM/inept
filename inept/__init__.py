
try:
    from ._version import version as __version__
except ModuleNotFoundError:
    pass

from .tree import Value, Group, Options, Switch
from .tree_builder import TreeBuilder
from .config import ConfigSimple, ConfigBase
from .utils import flatten


class Config(TreeBuilder, ConfigBase):
    pass

