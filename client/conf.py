import os
import configparser

config = configparser.SafeConfigParser()

config.read("client/conf.cfg")

SERVER_IP = config.get('server', 'IP')
SERVER_PORT = int(config.get('server', 'PORT'))
ALWAYS_CORRECT = config.get('debug', 'DEBUG_MODE')
SECRET = int(config.get('keys', 'SECRET'))
SCAN_DIRECTORY = config.get('path','SCAN_DIRECTORY')