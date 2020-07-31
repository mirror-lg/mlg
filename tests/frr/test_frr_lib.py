import unittest
from unittest.mock import Mock
from logging import Logger

from mirror_lg.lib.frr.frr_lib import FrrLib
from mirror_lg.lib.frr.frr_lib import ipv4_commands
from mirror_lg.lib.frr.frr_lib import ipv6_commands


class TestFrrApi(unittest.TestCase):
    def setUp(self):
        logger = Logger
        logger.basicConfig = Mock(logger)
        self.caller = FrrLib(logger=Mock(logger))

        self.target_device = "10.23.0.9"
        self.username = "root"
        self.ssh_key = "/home/adam/projects/mirror-lg/ssh_keys/mirror_key"

        self.ipv4_prefix = '8.8.8.8'
        self.ipv6_prefix = '2001::1'

    def test_class_creation(self):
        self.caller = FrrLib(self.target_device, self.ssh_key, self.username)

        self.assertEqual(self.target_device, self.caller.target_device)
        self.assertEqual(self.ssh_key, self.caller.ssh_key)
        self.assertEqual(self.username, self.caller.username)

    def test_load_ssh_key(self):
        self.caller = FrrLib()
        self.caller._load_ssh_key()

        self.assertEqual(self.target_device, self.caller.target_device)
        self.assertEqual(self.ssh_key, self.caller.ssh_key)
        self.assertEqual(self.username, self.caller.username)

    def test_ipv4_commands(self):
        show_ip_route = f"vtysh --command \"show ip route {self.ipv4_prefix}\""
        traceroute_ipv4 = f"vtysh --command \"traceroute {self.ipv4_prefix}\""
        show_bgp_ipv4 = f"vtysh --command \"show bgp ipv4 {self.ipv4_prefix}\""
        show_ip_bgp_summary = f"vtysh --command \"show ip bgp summary\""

        caller = ipv4_commands
        output = caller(self.ipv4_prefix)

        self.assertEqual(show_ip_route, output[0])
        self.assertEqual(traceroute_ipv4, output[1])
        self.assertEqual(show_bgp_ipv4, output[2])
        self.assertEqual(show_ip_bgp_summary, output[3])

    def test_ipv6_commands(self):
        show_ipv6_route = "vtysh --command "\
                          f"\"show ipv6 route {self.ipv6_prefix}\""
        traceroute_ipv6 = "vtysh --command "\
                          f"\"traceroute ipv6 {self.ipv6_prefix}\""
        show_bgp_ipv6 = "vtysh --command "\
                        f"\"show bgp ipv6 {self.ipv6_prefix}\""
        show_bgp_ipv6_summary = f"vtysh --command \"show bgp ipv6 summary\""

        caller = ipv6_commands
        output = caller(self.ipv6_prefix)

        self.assertEqual(show_ipv6_route, output[0])
        self.assertEqual(traceroute_ipv6, output[1])
        self.assertEqual(show_bgp_ipv6, output[2])
        self.assertEqual(show_bgp_ipv6_summary, output[3])
