"""
Library for interacting with a device running frrouting software
"""

from __future__ import annotations

import logging
from typing import Any, List

import paramiko


def ipv4_commands(prefix: str = None):
    """return list of ipv4 commands"""

    show_ip_route = f"vtysh --command \"show ip route {prefix}\""
    traceroute_ipv4 = f"vtysh --command \"traceroute {prefix}\""
    show_bgp_ipv4 = f"vtysh --command \"show bgp ipv4 {prefix}\""
    show_ip_bgp_summary = f"vtysh --command \"show ip bgp summary\""

    ipv4_command_list = [show_ip_route,
                         traceroute_ipv4,
                         show_bgp_ipv4,
                         show_ip_bgp_summary]

    return ipv4_command_list


def ipv6_commands(prefix: str = None):
    """return list of ipv6 commands"""

    show_ipv6_route = f"vtysh --command \"show ipv6 route {prefix}\""
    traceroute_ipv6 = f"vtysh --command \"traceroute ipv6 {prefix}\""
    show_bgp_ipv6 = f"vtysh --command \"show bgp ipv6 {prefix}\""
    show_bgp_ipv6_summary = f"vtysh --command \"show bgp ipv6 summary\""

    ipv6_command_list = [show_ipv6_route,
                         traceroute_ipv6,
                         show_bgp_ipv6,
                         show_bgp_ipv6_summary]

    return ipv6_command_list


class FrrLib:
    """Class provides methods for interaction with a device running
    frrouting suite"""

    def __init__(
            self,
            target_device: str = None,
            ssh_key: str = None,
            username: str = None,
            logger: logging.Logger = logging.getLogger()):
        self.target_device = target_device
        self.ssh_key = ssh_key
        self.username = username
        self.logger = logger.basicConfig(filename='mirror_lg/logs/mlg_frr.log',
                                         filemode='a',
                                         format='%(asctime)s %(message)s',
                                         level=logging.DEBUG)

        self._load_ssh_key()

    def _load_ssh_key(self) -> None:
        """Read device, username and ssh key config from file"""
        # assuming the use of single router for now.
        with open('./config/mlg_ssh_key.conf') as ssh_key_file:
            for line in ssh_key_file.readlines():
                self.target_device, self.username, self.ssh_key = \
                    line.split(':')

    def _ssh_client_connect(self) -> Any:
        """returns ssh_client object to connect to target device"""
        ssh_client = paramiko.SSHClient()
        # workaround for unknown host key in local cache error
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.target_device, username=self.username,
                           key_filename=self.ssh_key)

        return ssh_client

    def _ssh_client_disconnect(self, ssh_client: Any) -> None:
        """properly close/disconnect ssh session"""
        ssh_client.close()
        self.logger.info(f"connection to {self.target_device} has been closed")

    def setup(self):
        """logger setup"""
        self.logger.basicConfig(
            filename='mlg_run.log', filemode='a',
            format='%(asctime)s - %(levelname)s - %(message)s')

    def login(self) -> None:
        """login to the device"""

    def run_command(self, ssh_client: Any, command: str = None,
                    prefix: str = None) -> List[str]:
        # pylint: disable=unused-variable
        # pylint: disable=unused-argument
        """Run command on router"""
        ssh_client = self._ssh_client_connect()
        prefix = '8.8.8.8'
        stdin, stdout, stderr = ssh_client.exec_command(
            f"vtysh --command \"show ip route {prefix}\"")
        result = [s.strip() for s in stdout.readlines()]
        self._ssh_client_disconnect(ssh_client)

        return result
