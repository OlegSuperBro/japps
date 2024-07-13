from typing import Any

from japps.runners.IRunner import IRunner
from japps.plugins.IPlugin import IPlugin
from japps.plugins.SimplePlugin import SimplePlugin
from japps.Log import log
from japps.Configuration import Configuration
from japps.Errors import CallTypeError, UnknownPluginTypeError


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
