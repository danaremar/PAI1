import os
import configparser

config = configparser.SafeConfigParser()

config.read("./conf.cfg")

SCAN_DIRECTORY = [ ]