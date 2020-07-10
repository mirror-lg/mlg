"""
Library for interacting with a device running classic Cisco IOS software
"""

from __future__ import annotations

import logging
from typing import Any

from napalm import get_network_driver


def test_connect():
    ios_driver = get_network_driver('ios')
    password = 'Reload7'
    device = ios_driver('10.23.0.100', 'root', password)
    device.open()
    print(device.get_config()['running'])
    device.close()


def ipv4_commands(prefix: str = None):
    """return list of ipv4 commands"""

    show_ip_route = f"show ip route {prefix}"
    traceroute_ipv4 = f"traceroute ip {prefix}"
    show_bgp_ipv4 = f"show ip bgp {prefix}"
    show_ip_bgp_summary = "show ip bgp summary"

    ipv4_command_list = [show_ip_route,
                         traceroute_ipv4,
                         show_bgp_ipv4,
                         show_ip_bgp_summary]

    return ipv4_command_list


def ipv6_commands(prefix: str = None):
    """return list of ipv6 commands"""

    show_ipv6_route = f"show ipv6 route {prefix}"
    traceroute_ipv6 = f"traceroute ipv6 {prefix}"
    show_bgp_ipv6 = f"show bgp ipv6 unicast route {prefix}"
    show_bgp_ipv6_summary = "show bgp ipv6 unicast summary"

    ipv6_command_list = [show_ipv6_route,
                         traceroute_ipv6,
                         show_bgp_ipv6,
                         show_bgp_ipv6_summary]

    return ipv6_command_list


class IosLib:
    """Class provides methods for interaction with a device running
    Cisco legacy IOS"""

    def __init__(
            self,
            target_device: str = None,
            ssh_key: str = None,
            username: str = None,
            password: str = None,
            logger: logging.Logger = logging.getLogger()):
        self.target_device = target_device
        self.ssh_key = ssh_key
        self.username = username
        self.password = password
        self.logger = logger.basicConfig(filename='mirror_lg/logs/mlg_frr.log',
                                         filemode='a',
                                         format='%(asctime)s %(message)s',
                                         level=logging.DEBUG)
        self.ios_driver = get_network_driver('ios')

    def _ssh_client_connect(self) -> Any:
        """returns ssh_client object to connect to target device"""
        ssh_client = self.ios_driver(self.target_device,
                                     self.username, self.password)
        ssh_client.open()
        self.logger.info(f"connection to {self.target_device} opened")

        return ssh_client

    def _ssh_client_disconnect(self, ssh_client: Any) -> None:
        """properly close/disconnect ssh session"""
        ssh_client.close()
        self.logger.info(f"connection to {self.target_device} has been closed")
