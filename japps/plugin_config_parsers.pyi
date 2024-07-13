from __future__ import annotations
from abc import ABC, abstractmethod
from os import PathLike

from typing import Dict, Any

from japps.configuration import Configuration


class IParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(path: PathLike, config: Configuration) -> Dict: ...


class JsonParser(IParser):
    @staticmethod
    def parse(path: PathLike, config: Configuration) -> Dict: ...

class OneFileParser(IParser):

    @staticmethod
    def parse(path, config) -> Dict: ...

class PyParser(IParser):
    @staticmethod
    def parse(path, config) -> Dict[str, Any]: ...