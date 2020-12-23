import unittest
from unittest.mock import Mock
from logging import Logger

import coloredlogs

from mirror_lg.lib.logging.verbose import verbose_logging


class TestVerboseLogging(unittest.TestCase):
    def setUp(self):
        logger = Mock(Logger)
        logger.basicConfig = Mock(logger)
        self.verbose_logger = verbose_logging()
        self.colour_styles = coloredlogs.DEFAULT_LEVEL_STYLES

    def test_verbose_logger(self):
        with self.assertLogs(logger=self.verbose_logger, level="CRITICAL"):
            self.verbose_logger.critical('log a critical')

        with self.assertLogs(logger=self.verbose_logger, level="DEBUG"):
            self.verbose_logger.debug('log a debug')

        with self.assertLogs(logger=self.verbose_logger, level="ERROR"):
            self.verbose_logger.error('log an error')

        with self.assertLogs(logger=self.verbose_logger, level="INFO"):
            self.verbose_logger.info('log an info')

        with self.assertLogs(logger=self.verbose_logger, level="WARNING"):
            self.verbose_logger.warning('log a warning')

    def test_stdout_log_colours(self):
        self.assertEqual(self.colour_styles['critical']['color'], 196)
        self.assertEqual(self.colour_styles['debug']['color'], 39)
        self.assertEqual(self.colour_styles['error']['color'], 124)
        self.assertEqual(self.colour_styles['info']['color'], 231)
        self.assertEqual(self.colour_styles['warning']['color'], 226)

    def test_stdout_handler(self):
        self.assertTrue(self.verbose_logger.hasHandlers())
