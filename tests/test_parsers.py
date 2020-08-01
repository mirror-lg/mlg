"""
tests for parser functions
"""

import unittest

from mirror_lg.lib.parsers import parse_exploded_address

class TestParsers(unittest.TestCase):
    def setUp(self):
        self.ipv4_prefix = '8.8.8.8/32'
        self.ipv6_prefix = '2001::1/64'

    def test_parse_exploded_address(self):

        output = parse_exploded_address(self.ipv4_prefix)
        expected_output = '8.8.8.8'

        self.assertEqual(expected_output, output)

        output = parse_exploded_address(self.ipv6_prefix)
        expected_output = '2001::1'

        self.assertEqual(expected_output, output)
