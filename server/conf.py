import os
import configparser

config = configparser.SafeConfigParser()

config.read("server/conf.cfg")

print(config.sections())
SERVER_IP = config.get('server', 'IP')
SERVER_PORT = int(config.get('server', 'PORT'))
ALWAYS_CORRECT = config.get('debug', 'DEBUG_MODE')
SECRET = config.get('keys', 'SECRET')