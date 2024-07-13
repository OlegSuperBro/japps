from abc import ABCMeta, abstractmethod

from os import PathLike

from japps.configuration import Configuration
from japps.plugins import IPlugin


class IPluginLoader(metaclass=ABCMeta):
    def __init__(self, path: PathLike, config: Configuration) -> None: ...

    @abstractmethod
    def parse_plugin(self) -> IPlugin: ...


class SinglePluginLoader(IPluginLoader):
    def parse_plugin(self) -> IPlugin: ...


class PackagePluginLoader(IPluginLoader):
    def parse_plugin(self) -> IPlugin: ...