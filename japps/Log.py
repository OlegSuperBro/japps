import logging

from japps.Configuration import Configuration

log = logging.getLogger(__name__)


def update_logger(config: Configuration = None):
    global log
    log = logging.getLogger(__name__)
    if config is None:
        return log

    log.setLevel(config.logging_level)
