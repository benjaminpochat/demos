import logging
import logging.config

from src.main.python.commons.configuration import Configuration


class Loggable:

    def __init__(self):
        self._init_logger()

    def _init_logger(self):
        configuration = Configuration()
        configuration.configure_logging()
        self._logger = logging.getLogger('delib-archiver')

    def log_debug(self, message: str):
        self._logger.debug(message)

    def log_info(self, message: str):
        self._logger.info(message)

    def log_warning(self, message: str):
        self._logger.warn(message)

    def log_error(self, message: str):
        self._logger.error(message)

