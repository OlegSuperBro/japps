from types import ModuleType

from typing import List


class IPlugin:
    """
    Class used to create Plugin subclasses
    """
    TYPE: str
    PLUGIN_OBJECT: ModuleType
    DEPENDENCIES: List[str] = []


class Plugin(IPlugin):
    """
    Default plugin class
    """
    NAME: str
    AUTHOR: str
