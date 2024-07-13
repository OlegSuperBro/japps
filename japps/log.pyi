import logging

from typing import Union

from japps.configuration import Configuration

log: logging.Logger


def update_logger(config: Union[Configuration, None] = None) -> logging.Logger: ...