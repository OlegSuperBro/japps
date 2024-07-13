import os
from os.path import isdir
from re import match
from pathlib import Path

from typing import List, Any, Dict, TypeVar, Union

try:
    from typing import Self, Literal
except ImportError:
    from typing_extensions import Self, Literal  # type: ignore

from japps.Configuration import Configuration
from japps.plugins.IPlugin import IPlugin as _IPlugin
from japps.PluginLoaders import SinglePluginLoader, PackagePluginLoader, IPluginLoader
from japps.Utils import is_pkg
from japps.Log import log, update_logger
from japps.Errors import PluginNameError, PluginConfigError, PluginImportError, PluginNoInfoError

IPlugin = TypeVar("IPlugin", bound=_IPlugin)

class PluginManager:
    _instance = None

    def __new__(cls, *args, **kwargs) -> Self:
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, config: Configuration) -> None:
        log.info("Starting initialazing Plugin Manager")
        self._config: Configuration = config
        self._plugins: List[_IPlugin] = []
        update_logger(self._config)
        log.info("Done initialazing Plugin Manager")

    def load_plugins(self) -> None:
        log.info("Starting loading plugins")
        for file in os.listdir(self._config.plugins_directory):
            log.debug("Loading plugin %s", file)

            # it's jank, but it works?
            if [None] != [match(pattern, file) for pattern in self._config.ignore_patterns]:
                log.debug("Path %s in ignore list, skipping...", file)
                continue

            full_path: Path = Path(self._config.plugins_directory) / file

            if not self._check_is_allowed(full_path):
                continue

            loader: IPluginLoader
            if (is_pkg(full_path)):
                if (self._config.package_plugin_info_filename not in os.listdir(full_path)
                    and not self._config.allow_no_info):
                    raise PluginNoInfoError(f"Can't find {self._config.package_plugin_info_filename} in package {file} and it's not allowed")

                loader = PackagePluginLoader(full_path, self._config)

            elif not isdir(full_path):
                loader = SinglePluginLoader(full_path, self._config)

            else:
                log.warning(f"{file} is not a plugin. Skipping...")
                continue

            if loader is not None:
                plugin = loader.parse_plugin()
                self._plugins.append(plugin)
        log.info("Done loading plugins. Total loaded %s", len(self._plugins))
        self._check_plugins()

    def _check_is_allowed(self, path) -> Literal[True]:
        if (not self._config.allow_package_plugins and is_pkg(path)):
            log.error(f"{path} is package, but they are not allowed")
            raise PluginImportError(f"{path} is package, but they are not allowed")

        if (not self._config.allow_onefile_plugins and not is_pkg(path)):
            log.error(f"{path} is a onefile plugin, but they are not allowed")
            raise PluginImportError(f"{path} is a onefile plugin, but they are not allowed")

        return True

    def _check_plugins(self):
        log.info("Starting checking plugins")

        plugin_names: Dict[str, List[_IPlugin]] = {}
        for plugin in self._plugins:
            log.debug("Checking plugin %s", plugin.NAME)
            if not plugin_names.get(plugin.NAME):
                plugin_names[plugin.NAME] = []
            plugin_names[plugin.NAME].append(plugin)

        # i think that's too much junk...
        if any(map(lambda x: len(x) > 1, plugin_names.values())):
            doubled = [y.NAME for y in self._plugins]
            raise PluginNameError(f"Plugins with same {doubled}")

    def reload_plugins(self) -> None:
        del self._plugins
        self.load_plugins()

    def get_first_plugin(self, field: str, value: str) -> Union[IPlugin, None]:
        try:
            return self.get_plugins(field, value)[0]
        except IndexError:
            return None

    def get_plugins(self, field: str, value: str) -> List[_IPlugin]:
        return list(filter(lambda plugin: (getattr(plugin, field) == value), self._plugins))

    def get_all_plugin(self) -> List[_IPlugin]:
        return self._plugins.copy()

    def _run_plugin(self, plugin: _IPlugin, run_type: str, *args, **kwargs) -> Any:
        log.info("\tRunning %s in %s", plugin.NAME, self._config.plugin_runner.__name__)
        return self._config.plugin_runner.run(plugin, self._config, run_type, *args, **kwargs)

    def run_by_field(self, field: str, value: str, run_type: str,  *args, **kwargs) -> Dict[str, Any]:
        log.info("Running through plugins with %s == %s", field, value)
        return {plugin.NAME: 
                    self._run_plugin(plugin, run_type, *args, **kwargs)
                for plugin in self.get_plugins(field, value)}

    def run_by_name(self, name: str, run_type: str,  *args, **kwargs) -> Union[List[Any], None]:
        plugins_names = [plugin.NAME for plugin in self._plugins]
        if not any([plugin_name == name for plugin_name in plugins_names]):
            log.warning("Trying run plugin \"%s\" but it don't exist", name)
            return None
        log.info("Running plugin with name %s", name)
        plugin = list(filter(lambda x: x.NAME == name, self._plugins))[0]  # more junk :D
        return self._run_plugin(plugin, run_type, *args, **kwargs)

    def run_by_type(self, _type: str, run_type: str,  *args, **kwargs) -> List[Any]:
        log.info("Running through %s plugins", _type)
        return [self._run_plugin(plugin, run_type, *args, **kwargs) for plugin in filter(lambda plugin: plugin.TYPE == _type, self._plugins)]
