"""
Logging config decorator
"""

import sys
import functools
import logging


def logger_object(verbose='n'):
    """
    Create logging object
    """
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # setup stdout and file logging
    file_log = logging.FileHandler("./mirror_lg/logs/mirror_lg.log")
    file_log.setFormatter(log_format)
    if verbose == 'y':
        stdout_log = logging.StreamHandler(sys.stdout)
        stdout_log.setFormatter(log_format)
        logger.addHandler(stdout_log)

    # attach to logger object
    logger.addHandler(file_log)

    return logger


def error_logging(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = logger_object()
        try:
            return function(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            # re-raise the exception
            raise e
    return wrapper
