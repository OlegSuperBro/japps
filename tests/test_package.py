import os
from os.path import abspath
from pathlib import Path
from copy import deepcopy
from japps.Configuration import Configuration
from japps.PluginManager import PluginManager
from japps.plugin_configs.Json import JsonParser
from japps.plugin_configs.Py import PyParser
from japps.plugins.SimplePlugin import SimplePlugin
from japps.runners.SimpleFuncRunner import SimpleFuncRunner
from japps.Errors import PluginNoInfoError

from tests.resources.test_types import TestPlugin


config = Configuration()

config.plugins_directory = Path(abspath("tests/resources/package_plugins"))
config.site_packages_directory = Path(abspath("tests/resources/site-packages"))
config.allow_dependencies = True
config.no_info_default = {
    "NAME": "Unknown{num}",
    "AUTHOR": "Unknown{num}",
    "TYPE": "TestPlugin"
}
config.package_plugin_info_parser = JsonParser
config.plugin_class = SimplePlugin
config.plugin_runner = SimpleFuncRunner
config.logging_level = 10
config.allow_no_info = True

def test_default():
    local_config = deepcopy(config)
    local_config.allow_no_info = True
    manager = PluginManager(local_config)
    manager.load_plugins()

    assert len(manager.get_plugins("NAME", "Json Plugin")) == 1


def test_parsing_json():
    manager = PluginManager(config)
    manager.load_plugins()

    plugin: TestPlugin | None = manager.get_first_plugin("NAME", "Json Plugin")

    assert plugin is not None
    assert plugin.AUTHOR == "Oleg"


def test_parsing_py():
    config.package_plugin_info_parser = PyParser
    config.package_plugin_info_filename = "config.py"
    manager = PluginManager(config)
    manager.load_plugins()

    plugin: TestPlugin | None = manager.get_first_plugin("NAME", "Py Plugin")

    assert plugin is not None
    assert plugin.AUTHOR == "Oleg"


def test_noconf_ignore():
    config.allow_no_info = False

    manager = PluginManager(config)
    try:
        manager.load_plugins()
        assert False, "Should raise PluginNoInfoError exception"
    except PluginNoInfoError:
        pass

def test_noconf_read():
    config.allow_no_info = True
    config.no_info_default = {
        "NAME": "Unknown{num}",
        "AUTHOR": "Unknown{num}",
        "TYPE": "TestPlugin"
    }

    manager = PluginManager(config)
    manager.load_plugins()

    plugin: TestPlugin | None = manager.get_first_plugin("NAME", "Unknown{}".format(hash(Path(config.plugins_directory) / "noconf")))

    assert plugin is not None


def test_dependency():
    try:
        os.remove(config.site_packages_directory)
    except Exception:
        pass
    manager = PluginManager(config)
    manager.load_plugins()
    manager.run_by_type("TestPlugin3", "run")
