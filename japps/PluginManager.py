from typing import List, Self
import os
from os.path import isdir
from re import match

from japps.Configuration import Configuration
from japps.Plugin import IPlugin
from japps.PluginLoaders import SinglePluginLoader, PackagePluginLoader
from japps.Utils import is_pkg
from japps.Log import log, update_logger


class PluginManager:
    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config: Configuration) -> None:
        log.info("Starting initialazing Plugin Manager")
        self._config: Configuration = config
        self._plugins: List[IPlugin] = []
        update_logger(self._config)
        log.info("Done initialazing Plugin Manager")

    def load_plugins(self) -> None:
        log.info("Starting loading plugins")
        for file in os.listdir(self._config.plugins_directory):

            # it's jank, but it works?
            if [[None]] != list([match(pattern, file)] for pattern in self._config.ignore_patterns):
                log.debug("Path %s in ignore list, skipping...", file)
                continue

            loader = None
            full_path = self._config.plugins_directory + "\\" + file

            if (self._config.allow_package_plugins
               and is_pkg(full_path)):

                if (self._config.package_plugin_info_filename not in os.listdir(full_path)
                   and not self._config.allow_no_info):
                    log.debug("%s is package and don't have plugin info file, skipping...", file)
                    continue

                loader = PackagePluginLoader(full_path, self._config)

            elif not isdir(full_path) and self._config.allow_onefile_plugins:
                loader = SinglePluginLoader(full_path, self._config)

            if loader is not None:
                self._plugins.append(loader.parse_plugin())

    def reload_plugins(self) -> None:
        del self._plugins
        self.load_plugins()
        # for plugin in self.plugins:
        #     log.info("Reloading %s", plugin)
        #     plugin.PLUGIN_OBJECT = importlib.reload(plugin.PLUGIN_OBJECT)

    def get_first_plugin(self, field: str, value: str) -> IPlugin | None:
        try:
            return self.get_plugins(field, value)[0]
        except IndexError:
            return None

    def get_plugins(self, field: str, value: str) -> List[IPlugin]:
        return list(filter(lambda plugin: (getattr(plugin, field) == value), self._plugins))

    def get_all_plugin(self) -> List[IPlugin]:
        return self._plugins.copy()

    def _run_plugin(self, plugin, run_type: str, *args, **kwargs) -> None:
        log.info("\tRunning %s in %s", plugin.PLUGIN_OBJECT.__name__, self._config.plugin_runner.__name__)
        self._config.plugin_runner.run(plugin, self._config, run_type, *args, **kwargs)

    def run_by_field(self, field: str, value: str, run_type: str,  *args, **kwargs):
        log.info("Running through plugins with %s == %s", field, value)
        for plugin in self.get_plugins(field, value):
            self._run_plugin(plugin, run_type, *args, **kwargs)

    def run_by_type(self, _type: str, run_type: str,  *args, **kwargs):
        log.info("Running through %s plugins", _type)
        for plugin in filter(lambda plugin: plugin.TYPE == _type, self._plugins):
            self._run_plugin(plugin, run_type, *args, **kwargs)
