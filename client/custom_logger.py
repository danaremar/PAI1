import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
import conf

DEBUG_MODE = conf.DEBUG_MODE
PATH = conf.LOGS

file_logger = logging.getLogger('file_logger')
daily_handler = TimedRotatingFileHandler(f'{PATH}/warnings.log', when="midnight", interval=1)
daily_handler.setLevel(logging.WARNING)
daily_handler.prefix = "%Y%m%d"
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
daily_handler.setFormatter(f_format)


file_logger.addHandler(daily_handler)

def warning(msg):
    file_logger.warning(msg)