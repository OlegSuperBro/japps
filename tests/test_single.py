import os
from os.path import abspath
import sys
from pathlib import Path 
from copy import deepcopy

from japps.Configuration import Configuration
from japps.PluginManager import PluginManager
from japps.plugin_configs.OneFile import OneFileParser
from japps.plugins.SimplePlugin import SimplePlugin
from japps.runners.SimpleFuncRunner import SimpleFuncRunner
from japps.Errors import PluginNoInfoError

from tests.resources.test_types import TestPlugin


config = Configuration()

config.plugins_directory = Path(abspath("tests/resources/single_file_plugins"))
config.site_packages_directory = Path(abspath("tests/resources/site-packages"))
config.allow_package_plugins = True
config.allow_dependencies = True
config.package_plugin_info_parser = OneFileParser
config.plugin_class = SimplePlugin
config.plugin_runner = SimpleFuncRunner
config.logging_level = 10

sys.path.append(str(config.site_packages_directory))


def test_default_error():
    local_config = deepcopy(config)
    local_config.allow_no_info = False
    manager = PluginManager(local_config)
    manager.load_plugins()


def test_default_no_error():
    manager = PluginManager(config)
    try:
        manager.load_plugins()
    except PluginNoInfoError:
        assert False, "Should not raise PluginNoInfoError"
    assert len(manager.get_plugins("NAME", "Test Plugin")) == 1


def test_parsing():
    manager = PluginManager(config)
    manager.load_plugins()

    plugin: TestPlugin | None = manager.get_first_plugin("NAME", "Test Plugin")

    assert plugin is not None
    assert plugin.AUTHOR == "OlegSuperBro"


def test_dependency():
    try:
        os.remove(config.site_packages_directory)
    except Exception:
        pass
    manager = PluginManager(config)
    manager.load_plugins()
    manager.run_by_type("TestType", "run")
