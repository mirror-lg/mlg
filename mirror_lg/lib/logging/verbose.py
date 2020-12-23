"""
Verbose logging to console decorator
"""

import sys
import logging

import coloredlogs


def verbose_logging():
    stdout_logger = logging.getLogger()
    stdout_logger.setLevel(logging.DEBUG)
    coloredlogs.DEFAULT_LEVEL_STYLES = \
        {
            'critical': {'bold': True, 'color': 196},
            'debug': {'color': 39},
            'error': {'color': 124},
            'info': {'color': 231},
            'warning': {'color': 226}
        }

    coloredlogs.install(level='DEBUG')

    stdout_log = logging.StreamHandler(sys.stdout)
    stdout_logger.addHandler(stdout_log)

    return stdout_logger
