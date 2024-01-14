from typing import Dict

from japps.plugin_configs.IParser import IParser
from japps.Utils import import_from_path


class PyParser(IParser):
    @staticmethod
    def parse(path, config) -> Dict:
        plugin = import_from_path(path + "\\" + config.package_plugin_info_filename)
        return {
            key: getattr(plugin, key)
            for key in dir(plugin)
        }
