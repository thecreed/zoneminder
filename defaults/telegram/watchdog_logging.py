#!/usr/bin/python3

# https://realpython.com/python-logging/

import logging
from logging.handlers import RotatingFileHandler

# Create a custom logger
logger = logging.getLogger(__name__)

# Create handlers
c_handler = logging.StreamHandler()
c_handler.setLevel(logging.NOTSET)

f_handler = logging.FileHandler('/tmp/watchdog_zoneminder.log')
f_handler.setLevel(logging.DEBUG)

# Create formatters and add it to handlers
c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S')
c_handler.setFormatter(c_format)

f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', '%m/%d/%Y %I:%M:%S')
f_handler.setFormatter(f_format)

# Rotate the log file.
rotating_handler = RotatingFileHandler('/tmp/watchdog_zoneminder.log', maxBytes=2000, backupCount=5)
logger.addHandler(rotating_handler)

# Add handlers to the logger
logger.addHandler(c_handler)
logger.addHandler(f_handler)








