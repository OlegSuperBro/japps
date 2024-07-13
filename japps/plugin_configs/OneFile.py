import ast

from typing import Dict, List, Union

from japps.plugin_configs.IParser import IParser


def _filter_key(x: ast.AST) -> bool:
    return isinstance(x, ast.Assign)

class OneFileParser(IParser):
    @staticmethod
    def parse(path, config) -> Dict:
        plugin_file = open(path)
        plugin_content = plugin_file.read()
        dump = ast.parse(plugin_content)
        lines: List[ast.Assign] = list(filter(_filter_key, ast.iter_child_nodes(dump)))  # type: ignore[arg-type]

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
