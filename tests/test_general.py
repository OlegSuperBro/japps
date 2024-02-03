import os
from os.path import abspath
from japps.Configuration import Configuration
from japps.PluginManager import PluginManager
from japps.plugin_configs.Json import JsonParser
from japps.plugins.SimplePlugin import SimplePlugin
from japps.runners.SimpleFuncRunner import SimpleFuncRunner


config = Configuration()

config.plugins_directory = abspath("tests/resources/package_plugins")
config.site_packages_directory = abspath("tests/resources/site-packages")
config.allow_dependencies = True

config.allow_no_info = True
config.no_info_default = {
    "NAME": "Unknown{num}",
    "AUTHOR": "Unknown{num}",
    "TYPE": "TestPlugin"
}

config.package_plugin_info_parser = JsonParser
config.plugin_class = SimplePlugin
config.plugin_runner = SimpleFuncRunner


def test_default():
    manager = PluginManager(config)
    manager.load_plugins()

    assert len(manager.get_all_plugin()) != 0


def test_run():
    manager = PluginManager(config)
    manager.load_plugins()
    manager.run_by_type("TestType", "run")


def test_dependency():
    try:
        os.remove(config.site_packages_directory)
    except Exception:
        pass
    manager = PluginManager(config)
    manager.load_plugins()
    manager.run_by_type("TestPlugin3", "run")
