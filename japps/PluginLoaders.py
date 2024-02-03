from abc import ABCMeta, abstractmethod

from os import PathLike
from os.path import exists, join

from japps.Configuration import Configuration
from japps.plugins.IPlugin import IPlugin
from japps.plugin_configs.OneFile import OneFileParser
from japps.Utils import import_from_path, install_dependencies


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
        parsed_data: dict = OneFileParser.parse(self.path, self.config)
        for key, value in parsed_data.items():
            setattr(tmp_plugin, key, value)
        if self.config.allow_dependencies and tmp_plugin.DEPENDENCIES:
            install_dependencies(self.config.site_packages_directory, tmp_plugin.DEPENDENCIES)
        tmp_plugin.PLUGIN_OBJECT = import_from_path(self.path)
        return tmp_plugin


class PackagePluginLoader(IPluginLoader):
    def parse_plugin(self) -> IPlugin:
        tmp_plugin = self.config.plugin_class()
        if exists(join(self.path, self.config.package_plugin_info_filename)):
            parsed_data: dict = self.config.package_plugin_info_parser.parse(self.path, self.config)
        else:
            parsed_data: dict = self.config.no_info_default.copy()
            for key in parsed_data.keys():
                parsed_data[key] = parsed_data[key].format(num=hash(self.path))
        for key, value in parsed_data.items():
            setattr(tmp_plugin, key, value)

        if self.config.allow_dependencies and tmp_plugin.DEPENDENCIES:
            install_dependencies(self.config.site_packages_directory, tmp_plugin.DEPENDENCIES)
        tmp_plugin.PLUGIN_OBJECT = import_from_path(self.path)
        return tmp_plugin
