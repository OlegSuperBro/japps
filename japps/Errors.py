class DependencyError(ImportError):
    ...


class PluginError(Exception):
    ...


class PluginNameError(PluginError):
    ...


class CallTypeError(PluginError):
    ...


class PluginImportError(PluginError):
    ...


class PluginConfigError(PluginError):
    ...


class PluginNoInfoError(PluginConfigError):
    ...


class RunnerError(Exception):
    ...


class UnknownPluginTypeError(RunnerError):
    ...
