from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from japps.plugins.IPlugin import IPlugin
    from japps.Configuration import Configuration


class IRunner(ABC):
    @staticmethod
    @abstractmethod
    def run(plugin: IPlugin, config: Configuration, run_type: str, *args, **kwargs) -> Any:
        ...
