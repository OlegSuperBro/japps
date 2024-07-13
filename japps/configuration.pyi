from __future__ import annotations
from os import PathLike

from typing import List, Dict, Type

from japps.plugin_config_parsers import IParser
from japps.plugins import IPlugin
from japps.runners import IRunner

class Configuration:
    plugins_directory: PathLike
    site_packages_directory: PathLike

    ignore_patterns: List[str]
    package_plugin_info_filename: str

    package_plugin_info_parser: Type[IParser]
    plugin_runner: Type[IRunner]
    plugin_class: Type[IPlugin]

    allow_no_info: bool
    no_info_default: Dict
    allow_dependencies: bool
    allow_onefile_plugins: bool
    allow_package_plugins: bool

    logging_level: int
