import unittest
from unittest.mock import Mock
from logging import Logger

from mirror_lg.lib.ios.ios_lib import IosLib
from mirror_lg.lib.ios.ios_lib import ipv4_commands
from mirror_lg.lib.ios.ios_lib import ipv6_commands


class TestIosApi(unittest.TestCase):
    def setUp(self):
        logger = Logger
        logger.basicConfig = Mock(logger)
        self.caller = IosLib(logger=Mock(logger))

        self.target_device = "10.1.1.1"
        self.ssh_key = "ssh_key_name"
        self.username = "username"
        self.password = "password"

    def test_class_creation(self):
        self.caller = IosLib(self.target_device, self.ssh_key, self.username,
                             self.password)

        self.assertEqual(self.target_device, self.caller.target_device)
        self.assertEqual(self.ssh_key, self.caller.ssh_key)
        self.assertEqual(self.username, self.caller.username)
        self.assertEqual(self.password, self.caller.password)

    def test_ipv4_commands(self):
        prefix = '1.2.3.4'
        show_ip_route = f"show ip route {prefix}"
        traceroute_ipv4 = f"traceroute ip {prefix}"
        show_bgp_ipv4 = f"show ip bgp {prefix}"
        show_ip_bgp_summary = "show ip bgp summary"

        self.caller = ipv4_commands
        output = self.caller(prefix)

        self.assertEqual(show_ip_route, output[0])
        self.assertEqual(traceroute_ipv4, output[1])
        self.assertEqual(show_bgp_ipv4, output[2])
        self.assertEqual(show_ip_bgp_summary, output[3])

    def test_ipv6_commands(self):
        prefix = '2001::1'
        show_ipv6_route = f"show ipv6 route {prefix}"
        traceroute_ipv6 = f"traceroute ipv6 {prefix}"
        show_bgp_ipv6 = f"show bgp ipv6 unicast route {prefix}"
        show_bgp_ipv6_summary = "show bgp ipv6 unicast summary"

        self.caller = ipv6_commands
        output = self.caller(prefix)

        self.assertEqual(show_ipv6_route, output[0])
        self.assertEqual(traceroute_ipv6, output[1])
        self.assertEqual(show_bgp_ipv6, output[2])
        self.assertEqual(show_bgp_ipv6_summary, output[3])

    def OLD_test_ssh_connect(self):
        self.ssh_object = self.caller._ssh_client_connect(self.target_device,
                                                          self.username,
                                                          self.password)

        self.assertEqual(self.ssh_object.target_device,
                         self.caller.target_device)
        self.assertEqual(self.ssh_object.ssh_key, self.caller.ssh_key)
        self.assertEqual(self.ssh_object.username, self.caller.username)
        self.assertEqual(self.ssh_object.password, self.caller.password)
