import logging

from logging import StreamHandler

class Loggable:

    def __init__(self):
        self._init_logger()

    def _init_logger(self):
        log_level = logging.INFO
        log_handler = StreamHandler()
        log_handler.setLevel(log_level)
        log_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self._logger = logging.getLogger()
        self._logger.setLevel(log_level)
        self._logger.name = self.__class__.__name__
        self._logger.addHandler(log_handler)

    def log_debug(self, message: str):
        self._logger.debug(message)

    def log_info(self, message: str):
        self._logger.info(message)

    def log_warning(self, message: str):
        self._logger.warn(message)

    def log_error(self, message: str):
        self._logger.error(message)
