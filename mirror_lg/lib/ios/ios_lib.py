"""
Library for interacting with a device running classic Cisco IOS software
"""

from __future__ import annotations

import logging
from typing import Any, Dict

from napalm import get_network_driver


def ipv4_commands(cmd: str, prefix: str) -> Any:
    """pass ios ipv4 commands to:

    - query the ipv4 routing table
    - query the ipv4 bgp table
    - display ipv4 bgp neighbours
    - traceroute to ipv4 destination
    """

    ipv4 = {
        'sh_ip_route': f'show ip route {prefix}',
        'sh_ip_bgp': f'show ip bgp {prefix}',
        'sh_bgp_sum': 'show ip bgp summary',
        'trace': f'traceroute ip {prefix}'
    }

    return ipv4[cmd]


def ipv6_commands(cmd: str, prefix: str) -> Any:
    """pass ios ipv6 commands to:

    - query the ipv6 routing table
    - query the ipv6 bgp table
    - display ipv6 bgp neighbours
    - traceroute to ipv6 destination
    """

    ipv6 = {
        'sh_ip_route': f'show ipv6 route {prefix}',
        'sh_ip_bgp': f'show bgp ipv6 unicast route {prefix}',
        'sh_bgp_sum': 'show ip bgp summary',
        'trace': f'traceroute ipv6 {prefix}'
    }

    return ipv6[cmd]


class IosLib:
    """Class provides methods for interaction with a device running
    Cisco legacy IOS"""

    # pylint: disable=too-many-arguments
    # could fix this by passing in a single object with the required attributes
    def __init__(self,
                 target_device: str = None,
                 ssh_key: str = None,
                 username: str = None,
                 password: str = None,
                 logger: logging.Logger = logging.getLogger()):
        self.target_device = target_device
        self.ssh_key = ssh_key
        self.username = username
        self.password = password
        self.logger = logger
        self.ios_driver = get_network_driver('ios')

    def _ssh_client_connect(self) -> Any:
        """returns ssh_client object to connect to target device"""
        # TODO: load ssh key and use it to connect
        ssh_client = self.ios_driver(self.target_device,
                                     self.username, self.password)
        ssh_client.open()
        self.logger.info(f"connection to {self.target_device} opened")

        return ssh_client

    def _ssh_client_disconnect(self, ssh_client: Any) -> None:
        """properly close/disconnect ssh session"""
        ssh_client.close()
        self.logger.info(f"connection to {self.target_device} has been closed")

    def run_command(self, command: str) -> Dict:
        """execute command on the device"""
        # TODO: check for password or ssh auth
        # TODO: add try/except block
        router_conn = self.ios_driver(self.target_device,
                                      self.username,
                                      self.password)

        router_conn.open()
        self.logger.info(f"connection to {self.target_device} opened")
        output = router_conn.device.send_command(command)

        return output

    def backup_config_ios(self) -> Dict:
        """take backup of ios device configuration"""

        ssh_client = self.ios_driver(self.target_device,
                                     self.username, self.password)
        ssh_client.open()

        result = ssh_client.get_config()
        for x, y in result.items():
            print(x, y)

        return result
