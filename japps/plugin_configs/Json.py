import json

from japps.plugin_configs.IParser import IParser
from japps.Configuration import Configuration

from typing import Dict


class JsonParser(IParser):
    @staticmethod
    def parse(path: str, config: Configuration) -> Dict:
        return json.load(open(path + "/" + config.package_plugin_info_filename))
