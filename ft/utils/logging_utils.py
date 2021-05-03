import numpy as np
from ft.configs.configs_manager import ConfigsManager


class LoggingUtils:
    loggers = list()
    instance = None

    def __init__(self):
        self.primary_logger_type = ConfigsManager.get_instance().primary_logger_type

    def add_logger(self, logger):
        self.loggers.append(logger)

    @staticmethod
    def get_instance():
        if LoggingUtils.instance is None:
            LoggingUtils.instance = LoggingUtils()

        return LoggingUtils.instance

    def debug(self, message):
        for logger in self.loggers:
            logger.debug(message)
