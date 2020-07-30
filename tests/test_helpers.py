"""
tests for helper functions
"""

import unittest
import ipaddress
from unittest.mock import Mock
from logging import Logger

from mirror_lg.lib.helpers import Helper


class TestHelpers(unittest.TestCase):
    def setUp(self):
        self.logger = Mock(Logger)
        self.helper = Helper(self.logger)

        self.ipv4_prefix = '8.8.8.8'
        self.ipv6_prefix = '2001::1'

        self.ipv4_error = '256.256.256.256'
        self.ipv6_error = '2001::GG'


    def test_validate_ipv4_prefix(self):
        output = self.helper.validate_prefix(self.ipv4_prefix)
        expected_output = self.helper.validate_prefix(self.ipv4_prefix)

        self.assertEqual(expected_output, output)

    def test_validate_ipv6_prefix(self):
        output = self.helper.validate_prefix(self.ipv6_prefix)
        expected_output = self.helper.validate_prefix(self.ipv6_prefix)

        self.assertEqual(expected_output, output)

    def test_validate_prefix_raise_error(self):
        """test value error is raised"""
        with self.assertRaises(ValueError):
            self.helper.validate_prefix(self.ipv4_error)

        with self.assertRaises(ValueError):
            self.helper.validate_prefix(self.ipv6_error)
