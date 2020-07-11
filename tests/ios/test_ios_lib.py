import unittest
from unittest.mock import Mock
from logging import Logger


from mirror_lg.lib.ios.ios_lib import IosLib
from mirror_lg.lib.ios.ios_lib import ipv4_commands
from mirror_lg.lib.ios.ios_lib import ipv6_commands


class TestIosApi(unittest.TestCase):
    def setUp(self):
        logger = Mock(Logger)
        self.caller = IosLib(logger=logger)
        self._run_command = Mock(self.caller.run_command)
        self.ipv4_commands = ipv4_commands

        self.target_device = "10.1.1.1"
        self.ssh_key = "ssh_key_name"
        self.username = "username"
        self.password = "password"
        self.ipv4_prefix = '8.8.8.8'
        self.ipv6_prefix = '2001::1'


    def test_class_creation(self):
        self.caller = IosLib(self.target_device, self.ssh_key, self.username,
                             self.password)

        self.assertEqual(self.target_device, self.caller.target_device)
        self.assertEqual(self.ssh_key, self.caller.ssh_key)
        self.assertEqual(self.username, self.caller.username)
        self.assertEqual(self.password, self.caller.password)

    def test_ipv4_commands(self):
        sh_ip_route = f"show ip route {self.ipv4_prefix}"
        sh_ip_bgp = f"show ip bgp {self.ipv4_prefix}"
        sh_bgp_sum = "show ip bgp summary"
        trace = f"traceroute ip {self.ipv4_prefix}"

        caller = ipv4_commands

        output = caller('sh_ip_route', self.ipv4_prefix)
        self.assertEqual(sh_ip_route, output)

        output = caller('sh_ip_bgp', self.ipv4_prefix)
        self.assertEqual(sh_ip_bgp, output)

        output = caller('trace', self.ipv4_prefix)
        self.assertEqual(trace, output)

        output = caller('sh_bgp_sum', self.ipv4_prefix)
        self.assertEqual(sh_bgp_sum, output)

    def test_ipv6_commands(self):
        sh_ip_route = f"show ipv6 route {self.ipv6_prefix}"
        sh_ip_bgp = f"show bgp ipv6 unicast route {self.ipv6_prefix}"
        sh_bgp_sum = "show ip bgp summary"
        trace = f"traceroute ipv6 {self.ipv6_prefix}"

        caller = ipv6_commands

        output = caller('sh_ip_route', self.ipv6_prefix)
        self.assertEqual(sh_ip_route, output)

        output = caller('sh_ip_bgp', self.ipv6_prefix)
        self.assertEqual(sh_ip_bgp, output)

        output = caller('trace', self.ipv6_prefix)
        self.assertEqual(trace, output)

        output = caller('sh_bgp_sum', self.ipv6_prefix)
        self.assertEqual(sh_bgp_sum, output)

