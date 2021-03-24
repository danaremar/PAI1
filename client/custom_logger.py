import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
import conf

DEBUG_MODE = conf.DEBUG_MODE
PATH = conf.LOGS

file_logger = logging.getLogger('file_logger')

#Daily logger
daily_handler = TimedRotatingFileHandler(f'{PATH}/Report.log', when="midnight", interval=1)
daily_handler.setLevel(logging.INFO)
daily_handler.prefix = "%Y%m%d"
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
daily_handler.setFormatter(f_format)

#Monthtly logger
montly_handler = TimedRotatingFileHandler(f'{PATH}/Report.log', when="D", interval=31)
montly_handler.setLevel(logging.INFO)
montly_handler.prefix = "%Y%m"
f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
montly_handler.setFormatter(f_format)

file_logger.addHandler(daily_handler)
file_logger.addHandler(montly_handler)

def warning(msg):
    file_logger.warning(msg)

def info(msg):
    file_logger.info(msg)