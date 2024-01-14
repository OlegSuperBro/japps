from abc import ABC, abstractmethod

from japps.Plugin import IPlugin


class IRunner(ABC):
    @abstractmethod
    def run(plugin: IPlugin, config, run_type: str, *args, **kwargs):
        ...
