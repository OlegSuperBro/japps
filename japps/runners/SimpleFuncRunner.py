from japps.runners.IRunner import IRunner
from japps.Plugin import IPlugin
from japps.Log import log
from japps.Configuration import Configuration


class SimpleFuncRunner(IRunner):
    def run(plugin: IPlugin, config: Configuration, run_type: str, *args, **kwargs):
        func_name = config.plugin_actions.get(run_type)
        if func_name is None:
            log.warning("Trying to call non-existent \"%s\" function type from plugin", run_type)
            return
        if not hasattr(plugin.PLUGIN_OBJECT, func_name):
            log.warning("\"%s\" Plugin don't have \"%s\" function", plugin.PLUGIN_OBJECT.__name__, run_type)
            return
        getattr(plugin.PLUGIN_OBJECT, func_name)(*args, **kwargs)
