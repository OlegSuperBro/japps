from types import ModuleType

from typing import List, Dict


class IPlugin:
    """
    Class used to create Plugin subclasses
    """
    TYPE: str
    PLUGIN_OBJECT: ModuleType
    DEPENDENCIES: List[str]
    NAME: str


class SimplePlugin(IPlugin):
    """
    Default plugin class
    """
    AUTHOR: str
    PLUGIN_FUNCS: Dict[str, str]