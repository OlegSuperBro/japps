import os
from os.path import abspath
import sys

from japps.Configuration import Configuration
from japps.PluginManager import PluginManager
from japps.plugin_configs.OneFile import OneFileParser
from japps.plugins.SimplePlugin import SimplePlugin
from japps.runners.SimpleFuncRunner import SimpleFuncRunner

from resources.test_types import TestPlugin


config = Configuration()

config.plugins_directory = abspath("tests/resources/single_file_plugins")
config.site_packages_directory = abspath("tests/resources/site-packages")
config.allow_package_plugins = True
config.allow_dependencies = True
config.package_plugin_info_parser = OneFileParser
config.plugin_class = SimplePlugin
config.plugin_runner = SimpleFuncRunner

sys.path.append(config.site_packages_directory)


def test_default():
    manager = PluginManager(config)
    manager.load_plugins()

    assert len(manager.get_plugins("NAME", "Test Plugin")) == 1


def test_parsing():
    manager = PluginManager(config)
    manager.load_plugins()

    plugin: TestPlugin = manager.get_first_plugin("NAME", "Test Plugin")

    assert plugin.AUTHOR == "OlegSuperBro"


def test_dependency():
    try:
        os.remove(config.site_packages_directory)
    except Exception:
        pass
    manager = PluginManager(config)
    manager.load_plugins()
    manager.run_by_type("TestType", "run")
