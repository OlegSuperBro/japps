from __future__ import annotations
import json
from os import PathLike
from pathlib import Path

from japps.plugin_configs.IParser import IParser

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from japps.Configuration import Configuration


class JsonParser(IParser):
    @staticmethod
    def parse(path: PathLike, config: Configuration) -> Dict:
        path = Path(path)
        return json.load(open(path / config.package_plugin_info_filename))
