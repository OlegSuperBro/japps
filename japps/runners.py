from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Any, TYPE_CHECKING

from japps.plugins import IPlugin
from japps.plugins import SimplePlugin
from japps.log import log
from japps.configuration import Configuration
from japps.errors import CallTypeError, UnknownPluginTypeError


if TYPE_CHECKING:
    from japps.plugins import IPlugin
    from japps.configuration import Configuration


class IRunner(ABC):
    @staticmethod
    @abstractmethod
    def run(plugin: IPlugin, config: Configuration, run_type: str, *args, **kwargs) -> Any:
        ...



class SimpleFuncRunner(IRunner):
    @staticmethod
    def run(plugin: IPlugin, config: Configuration, run_type: str, *args, **kwargs) -> Any:
        if not isinstance( plugin, SimplePlugin):
            raise UnknownPluginTypeError()
        if run_type not in plugin.PLUGIN_FUNCS.keys():
            raise CallTypeError()
        func_name = plugin.PLUGIN_FUNCS.get(run_type)
        if func_name is None:
            log.warning("Trying to call non-existent \"%s\" function type from plugin", run_type)
            return
        if not hasattr(plugin.PLUGIN_OBJECT, func_name):
            log.warning("\"%s\" Plugin don't have \"%s\" function", plugin.PLUGIN_OBJECT.__name__, run_type)
            return
        return getattr(plugin.PLUGIN_OBJECT, func_name)(*args, **kwargs)
