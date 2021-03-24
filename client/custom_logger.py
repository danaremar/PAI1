import logging
import logging.config
from logging.handlers import TimedRotatingFileHandler
import conf

DEBUG_MODE = conf.DEBUG_MODE
PATH = conf.LOGS
FAST_LOOP = conf.FAST_LOOP 

file_logger = logging.getLogger('Report')
if FAST_LOOP:
    #Minute logger 
    minute_handler = TimedRotatingFileHandler(f'{PATH}/Report.log', when="m", interval=2)
    minute_handler.setLevel(logging.INFO)
    minute_handler.prefix = "%H%M"
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    minute_handler.setFormatter(f_format)
    file_logger.addHandler(minute_handler)

    #6 minutes logger
    montly_handler = TimedRotatingFileHandler(f'{PATH}/Montly_report.log', when="m", interval=6)
    montly_handler.setLevel(logging.INFO)
    montly_handler.prefix = "%Y%m"
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    montly_handler.setFormatter(f_format)
    file_logger.addHandler(montly_handler)
else:
    #Daily logger
    daily_handler = TimedRotatingFileHandler(f'{PATH}/Report.log', when="midnight", interval=1)
    daily_handler.setLevel(logging.INFO)
    daily_handler.prefix = "%Y%m%d"
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    daily_handler.setFormatter(f_format)
    file_logger.addHandler(daily_handler)

    #Monthtly logger
    montly_handler = TimedRotatingFileHandler(f'{PATH}/Montly_report.log', when="D", interval=31)
    montly_handler.setLevel(logging.INFO)
    montly_handler.prefix = "%Y%m"
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    montly_handler.setFormatter(f_format)
    file_logger.addHandler(montly_handler)




def warning(msg):
    file_logger.warning(msg)

def info(msg):
    file_logger.info(msg)