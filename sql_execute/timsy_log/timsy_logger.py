import logging
# import timsy_log._constants as c
from ._constants import set_logger_initialized

from .logging_misc import (
    console_handler_factory,
    file_handler_factory
)

logger = logging.getLogger()


def setup_logger():
    class InfoFilter(logging.Filter):
        def filter(self, record):
            return record.levelno == logging.INFO

    logger.setLevel(logging.DEBUG)
    log_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh = logging.FileHandler('logs/timsy_app.log')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(log_formatter)
    logger.addHandler(fh)

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(log_formatter)
    ch.addFilter(InfoFilter())
    logger.addHandler(ch)


def init_root_logger():
    """ Opinionated Default Root Logger """
    # global TIMSY_LOGGER_INITIALIZED
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = file_handler_factory()
    ch = console_handler_factory(use_info_filter=True)

    entry_fh = logging.FileHandler('logs/timsy_app.log')
    entry_fh.setLevel(logging.DEBUG)
    logger.addHandler(entry_fh)
    logger.debug("-------------------------")
    logger.debug("Root Logger Initialized.")
    logger.debug("-------------------------")
    logger.removeHandler(entry_fh)
    logger.addHandler(fh)
    logger.addHandler(ch)
    set_logger_initialized(True)


def getLogger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name)
