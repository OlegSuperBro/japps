from abc import ABCMeta, abstractmethod

from os import PathLike
from os.path import relpath

from typing import Dict

from japps.configuration import Configuration
from japps.plugins import IPlugin
from japps.plugin_config_parsers import OneFileParser
from japps.utils import import_from_path, install_dependencies
from japps.log import log
from japps.errors import PluginConfigError


class IPluginLoader(metaclass=ABCMeta):
    def __init__(self, path: PathLike, config: Configuration) -> None:
        self.path = path
        self.config = config

    @abstractmethod
    def parse_plugin(self) -> IPlugin:
        ...


class SinglePluginLoader(IPluginLoader):
    def parse_plugin(self) -> IPlugin:
        tmp_plugin = self.config.plugin_class()
        default_data: dict = self.config.no_info_default.copy()
        parsed_data: dict = OneFileParser.parse(self.path, self.config)
        for key in default_data.keys():
            if key in parsed_data.keys():
                continue
            parsed_data[key] = default_data[key].format(num=hash(self.path))

        for key, value in parsed_data.items():
            setattr(tmp_plugin, key, value)
        if self.config.allow_dependencies and tmp_plugin.DEPENDENCIES:
            install_dependencies(self.config.site_packages_directory, tmp_plugin.DEPENDENCIES)
        tmp_plugin.PLUGIN_OBJECT = import_from_path(self.path)
        return tmp_plugin


class PackagePluginLoader(IPluginLoader):
    def parse_plugin(self) -> IPlugin:
        log.debug(f"Loading plugin from package {self.path}")
        tmp_plugin = self.config.plugin_class()

        default_data: Dict[str, str] = self.config.no_info_default.copy()
        parsed_data: dict = {}
        try:
            parsed_data = self.config.package_plugin_info_parser.parse(self.path, self.config)
        except FileNotFoundError:
            log.debug(f"Can't get config from package \"{relpath(self.path)}\", using config default")

        for key in default_data.keys():
            if key in parsed_data.keys():
                continue
            parsed_data[key] = default_data[key].format(num=hash(self.path))

        if not (parsed_data.get("NAME")
                or parsed_data.get("TYPE")):
            raise PluginConfigError(f"Can't find name or type in config from package {relpath(self.path)}")

        for key, value in parsed_data.items():
            setattr(tmp_plugin, key, value)

        if self.config.allow_dependencies and tmp_plugin.DEPENDENCIES:
            install_dependencies(self.config.site_packages_directory, tmp_plugin.DEPENDENCIES)
        tmp_plugin.PLUGIN_OBJECT = import_from_path(self.path)
        return tmp_plugin
