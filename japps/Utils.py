import os
from os.path import isdir, basename
import importlib
import importlib.util
import sys
import subprocess

from typing import List


def is_pkg(path: str):
    if isdir(path) and "__init__.py" in os.listdir(path):
        return True
    else:
        return False


def import_from_path(path: str):
    if is_pkg(path):
        spec = importlib.util.spec_from_file_location("__init__", path + "\\__init__.py", submodule_search_locations=[path])
    else:
        spec = importlib.util.spec_from_file_location(basename(path).rstrip(".py"), path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[basename(path).rstrip(".py")] = module
    spec.loader.exec_module(module)
    return module


def install_dependencies(path: str, dependencies: List[str]):
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "-q", "--target", path, " ".join(dependencies)])
