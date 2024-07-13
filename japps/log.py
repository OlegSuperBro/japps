import logging

from typing import Union

from japps.configuration import Configuration

log = logging.getLogger(__name__)


def update_logger(config: Union[Configuration, None] = None):
    global log
    log = logging.getLogger(__name__)
    if config is None:
        return log

    log.setLevel(config.logging_level)

    return log