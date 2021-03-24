import os
import configparser

config = configparser.SafeConfigParser()

config.read("conf.cfg")

SERVER_IP = config.get('server', 'IP')
SERVER_PORT = int(config.get('server', 'PORT'))
ALWAYS_CORRECT = "True" == config.get('debug', 'ALWAYS_CORRECT')
DEBUG_MODE = "True" == config.get('debug', 'DEBUG_MODE')
SECRET = int(config.get('keys', 'SECRET'))
SCAN_DIRECTORY = config.get('path','SCAN_DIRECTORY')