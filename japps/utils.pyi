from os import PathLike

from types import ModuleType
from typing import List


def is_pkg(path: PathLike) -> bool: ...

def import_from_path(path: PathLike) -> ModuleType: ...

def install_dependencies(path: PathLike, dependencies: List[str]) -> None: ...
