from typing import Type
import logging

from typing import List, Dict

from japps.plugins.IPlugin import IPlugin
from japps.plugin_configs.IParser import IParser
from japps.runners.IRunner import IRunner


class Configuration:
    plugins_directory: str = "plugins"
    site_packages_directory: str = "site-packages"

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
