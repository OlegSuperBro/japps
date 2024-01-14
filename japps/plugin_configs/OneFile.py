import ast

from typing import Dict, List

from japps.plugin_configs.IParser import IParser


class OneFileParser(IParser):
    @staticmethod
    def parse(path, config) -> Dict:
        plugin_file = open(path)
        plugin_content = plugin_file.read()
        dump = ast.parse(plugin_content)
        lines: List[ast.Assign] = list(filter(lambda x: isinstance(x, ast.Assign), ast.iter_child_nodes(dump)))

        result = {}
        for line in lines:
            if isinstance(line.value, ast.List):
                values = [const.value for const in line.value.elts]
            elif isinstance(line.value, ast.Name):
                values = line.value.id
            else:
                values = line.value.value
            result[line.targets[0].id] = values
        return result
