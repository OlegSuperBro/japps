from __future__ import annotations
from os import PathLike
import logging
from pathlib import Path

from typing import List, Dict, Type, TYPE_CHECKING
import japps.Errors


if TYPE_CHECKING:
    from japps.plugin_configs.IParser import IParser
    from japps.plugins.IPlugin import IPlugin
    from japps.runners.IRunner import IRunner

class Configuration:
    plugins_directory: PathLike = Path("plugins")
    site_packages_directory: PathLike = Path("site-packages")

    ignore_patterns: List[str] = ["__pycache__"]
    package_plugin_info_filename: str = "config.json"

    package_plugin_info_parser: Type[IParser]
    plugin_runner: Type[IRunner]
    plugin_class: Type[IPlugin]

    allow_no_info: bool = False
    no_info_default: Dict = {}
    allow_dependencies: bool = False
    allow_onefile_plugins: bool = True
    allow_package_plugins: bool = True

    logging_level: int = logging.WARNING
