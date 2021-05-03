from ft.loggers.console_logger import ConsoleLogger
from ft.utils.logging_utils import LoggingUtils


class LoggerFactory:

    @staticmethod
    def get_logger(class_name):
        if LoggingUtils.get_instance().primary_logger_type == "console":
            return ConsoleLogger(class_name)
        else:
            print('Error')
