from japps.plugins.IPlugin import IPlugin


class SimplePlugin(IPlugin):
    """
    Default plugin class
    """
    AUTHOR: str
    PLUGIN_FUNCS = {
        "run": "run"
    }
