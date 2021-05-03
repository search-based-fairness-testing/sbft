from ft.loggers.logger import Logger
from datetime import datetime


class ConsoleLogger(Logger):

    def __init__(self, class_name):
        super().__init__(class_name)

    def debug(self, message):
        current_datetime = datetime.now()
        print('[' + self.class_name + '][' + str(current_datetime) + '] ' + message)
