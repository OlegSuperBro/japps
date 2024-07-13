import os
from os.path import isdir, basename
from os import PathLike
import importlib
import importlib.util
import sys
import subprocess
from pathlib import Path

from types import ModuleType
from typing import List

from japps.errors import PluginImportError


def is_pkg(path: PathLike):
    if isdir(path) and "__init__.py" in os.listdir(path):
        return True
    else:
        return False


def import_from_path(path: PathLike):
    path = Path(path)
    if is_pkg(path):
        spec = importlib.util.spec_from_file_location("__init__", path / "__init__.py", submodule_search_locations=[str(path)])
    else:
        spec = importlib.util.spec_from_file_location(basename(path).rstrip(".py"), path)

    if spec is None or spec.loader is None:
        raise PluginImportError(f"Can't load plugin from {path}")

    module: ModuleType = importlib.util.module_from_spec(spec)
    sys.modules[basename(path).rstrip(".py")] = module
    spec.loader.exec_module(module)
    return module


def install_dependencies(path: PathLike, dependencies: List[str]):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-q", "--target", path, " ".join(dependencies)])
