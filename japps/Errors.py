class DependencyError(ImportError):
    ...


class PluginError(Exception):
    ...


class PluginNameError(PluginError):
    ...


class CallTypeError(PluginError):
    ...
