from __future__ import annotations
from abc import ABC, abstractmethod
from os import PathLike

from typing import Dict, TYPE_CHECKING

if TYPE_CHECKING:
    from japps.Configuration import Configuration

class IParser(ABC):
    @staticmethod
    @abstractmethod
    def parse(path: PathLike, config: Configuration) -> Dict:
        ...
