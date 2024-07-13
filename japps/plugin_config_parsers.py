from __future__ import annotations
from abc import ABC, abstractmethod
from os import PathLike
from pathlib import Path
import json
import ast

from typing import Dict, TYPE_CHECKING, Any, List, Union

from japps.utils import import_from_path

if TYPE_CHECKING:
    from japps.configuration import Configuration


class IParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(path: PathLike, config: Configuration) -> Dict:
        ...


class JsonParser(IParser):
    @staticmethod
    def parse(path: PathLike, config: Configuration) -> Dict:
        path = Path(path)
        return json.load(open(path / config.package_plugin_info_filename))


class OneFileParser(IParser):
    @staticmethod
    def _filter_key(x: ast.AST) -> bool:
        return isinstance(x, ast.Assign)

    @staticmethod
    def parse(path, config) -> Dict:
        plugin_file = open(path)
        plugin_content = plugin_file.read()
        dump = ast.parse(plugin_content)
        lines: List[ast.Assign] = list(filter(OneFileParser._filter_key, ast.iter_child_nodes(dump)))  # type: ignore[arg-type]

        result = {}
        values: Union[List, str]
        for line in lines:
            if isinstance(line.value, ast.List):
                values = [const.value for const in line.value.elts]  # type: ignore[attr-defined]  # no it does
            elif isinstance(line.value, ast.Name):
                values = line.value.id
            else:
                values = line.value.value  # type: ignore[attr-defined]  # no it does
            result[line.targets[0].id] = values  # type: ignore[attr-defined]  # no it does
        return result


class PyParser(IParser):
    @staticmethod
    def parse(path, config) -> Dict[str, Any]:
        path = Path(path)
        plugin = import_from_path(path / config.package_plugin_info_filename)
        return {
            key: getattr(plugin, key)
            for key in dir(plugin)
        }
