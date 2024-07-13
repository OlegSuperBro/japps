from typing import List, Any, Dict, TypeVar, Union

try:
    from typing import Self, Literal
except ImportError:
    from typing_extensions import Self, Literal  # type: ignore

from japps.configuration import Configuration
from japps.plugins import IPlugin as _IPlugin

IPlugin = TypeVar("IPlugin", bound=_IPlugin)

class PluginManager:
    def __new__(cls, *args, **kwargs) -> Self: ...

    def __init__(self, config: Configuration) -> None: ...

    def load_plugins(self) -> None: ...

    def _check_is_allowed(self, path) -> Literal[True]: ...

    def _check_plugins(self) -> None: ...

    def reload_plugins(self) -> None: ...

    def get_first_plugin(self, field: str, value: str) -> Union[IPlugin, None]: ...

    def get_plugins(self, field: str, value: str) -> List[_IPlugin]: ...

    def get_all_plugin(self) -> List[_IPlugin]: ...

    def _run_plugin(self, plugin: _IPlugin, run_type: str, *args, **kwargs) -> Any: ...

    def run_by_field(self, field: str, value: str, run_type: str,  *args, **kwargs) -> Dict[str, Any]: ...

    def run_by_name(self, name: str, run_type: str,  *args, **kwargs) -> Union[List[Any], None]: ...

    def run_by_type(self, _type: str, run_type: str,  *args, **kwargs) -> List[Any]: ...