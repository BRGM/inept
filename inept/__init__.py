
try:
    from importlib_metadata import version, PackageNotFoundError
    __version__ = version("inept")
except (PackageNotFoundError, ModuleNotFoundError):
    # package is not installed
    pass


from .tree import Group, Exclusive, Option
from .config import Config
