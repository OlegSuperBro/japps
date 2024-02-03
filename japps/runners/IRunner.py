from abc import ABC, abstractmethod

from typing import Any

from japps.plugins.IPlugin import IPlugin


class IRunner(ABC):
    @abstractmethod
    def run(plugin: IPlugin, config, run_type: str, *args, **kwargs) -> Any:
        ...
