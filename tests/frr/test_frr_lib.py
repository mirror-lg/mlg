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

    def test_class_creation(self):
        target_device = "10.23.0.9"
        username = "root"
        ssh_key = "/home/adam/projects/mirror-lg/ssh_keys/mirror_key"

        self.caller = FrrLib(target_device, ssh_key, username)

        self.assertEqual(target_device, self.caller.target_device)
        self.assertEqual(ssh_key, self.caller.ssh_key)
        self.assertEqual(username, self.caller.username)

    def test_class_error_raised(self):
        # pylint: disable=unused-variable
        # pylint: disable=undefined-variable
        with self.assertRaises(NameError):
            target_device = 'device'
            self.caller = FrrLib(target_device, ssh_key)
            self.caller = FrrLib(target_device, username)

    def test_load_ssh_key(self):
        target_device = "10.23.0.9"
        username = "root"
        ssh_key = "/home/adam/projects/mirror-lg/ssh_keys/mirror_key"

        self.caller = FrrLib()
        self.caller._load_ssh_key()

        self.assertEqual(target_device, self.caller.target_device)
        self.assertEqual(ssh_key, self.caller.ssh_key)
        self.assertEqual(username, self.caller.username)

    def test_ipv4_commands(self):
        prefix = '1.2.3.4'
        show_ip_route = f"vtysh --command \"show ip route {prefix}\""
        traceroute_ipv4 = f"vtysh --command \"traceroute {prefix}\""
        show_bgp_ipv4 = f"vtysh --command \"show bgp ipv4 {prefix}\""
        show_ip_bgp_summary = f"vtysh --command \"show ip bgp summary\""

        caller = ipv4_commands
        output = caller(prefix)

        self.assertEqual(show_ip_route, output[0])
        self.assertEqual(traceroute_ipv4, output[1])
        self.assertEqual(show_bgp_ipv4, output[2])
        self.assertEqual(show_ip_bgp_summary, output[3])

    def test_ipv6_commands(self):
        prefix = '2001::1'
        show_ipv6_route = f"vtysh --command \"show ipv6 route {prefix}\""
        traceroute_ipv6 = f"vtysh --command \"traceroute ipv6 {prefix}\""
        show_bgp_ipv6 = f"vtysh --command \"show bgp ipv6 {prefix}\""
        show_bgp_ipv6_summary = f"vtysh --command \"show bgp ipv6 summary\""

        caller = ipv6_commands
        output = caller(prefix)

        self.assertEqual(show_ipv6_route, output[0])
        self.assertEqual(traceroute_ipv6, output[1])
        self.assertEqual(show_bgp_ipv6, output[2])
        self.assertEqual(show_bgp_ipv6_summary, output[3])

    def test_setup_logger(self):
        self.caller.logger.info('testing logger setup')


if __name__ == '__main__':
    unittest.main()
