#!/usr/bin/env python
# -*- coding: utf-8 -*-

import update
import sys
from logger import setup_logger

logger = setup_logger()
# import logging

# log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
# logger = logging.getLogger(__name__)

# # To override the default severity of logging
# logger.setLevel('DEBUG')

# # Use FileHandler() to log to a file
# file_handler = logging.FileHandler("mylogs.log")
# formatter = logging.Formatter(log_format)
# file_handler.setFormatter(formatter)

# # Don't forget to add the file handler
# logger.addHandler(file_handler)


def check_update():
    logger.info('Checking for updates...')
    return update.updater()

def start():
    pass

def main():
    if not check_update():
        sys.exit(1)
    else:
        start()
    
if __name__ == '__main__':
    main()