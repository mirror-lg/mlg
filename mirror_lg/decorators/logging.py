"""
Logging config decorator
"""

import functools
import logging


def log_to_file():
    """
    Create logging object
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        "%Y-%m-%d %H:%M:%S")

    # setup file logging
    file_log = logging.FileHandler("./mirror_lg/logs/mirror_lg.log")
    file_log.setFormatter(log_format)

    # attach to logger object
    logger.addHandler(file_log)

    return logger


def error_logging(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = log_to_file()
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            # re-raise the exception
            raise e
    return wrapper
