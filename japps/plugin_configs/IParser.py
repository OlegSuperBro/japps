from abc import ABC, abstractstaticmethod

from typing import Dict


class IParser(ABC):
    @abstractstaticmethod
    def parse(path, config) -> Dict:
        ...
