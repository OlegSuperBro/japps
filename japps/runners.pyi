from __future__ import annotations
from abc import ABC, abstractmethod

from typing import Any

from japps.plugins import IPlugin
from japps.configuration import Configuration


class IRunner(ABC):
    @staticmethod
    @abstractmethod
    def run(plugin: IPlugin, config: Configuration, run_type: str, *args, **kwargs) -> Any: ...



class SimpleFuncRunner(IRunner):
    @staticmethod
    def run(plugin: IPlugin, config: Configuration, run_type: str, *args, **kwargs) -> Any: ...