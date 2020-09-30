"""
Library for interacting with a device running frrouting software
"""

from __future__ import annotations

import logging
from typing import Any, List

import paramiko


def ipv4_commands(cmd: str, prefix: str = None):
    """list of ipv4 commands"""

    ipv4 = {
        'sh_ip_route': f"vtysh --command \"show ip route {prefix}\"",
        'sh_ip_bgp': f"vtysh --command \"show bgp ipv4 {prefix}\"",
        'sh_bgp_sum': f"vtysh --command \"show ip bgp summary\"",
        'trace': f"vtysh --command \"traceroute {prefix}\""
    }

    return ipv4[cmd]


def ipv6_commands(cmd: str, prefix: str = None):
    """return list of ipv6 commands"""

    ipv6 = {
        'sh_ip_route': f"vtysh --command \"show ipv6 route {prefix}\"",
        'sh_ip_bgp': f"vtysh --command \"show bgp ipv6 {prefix}\"",
        'sh_bgp_sum': f"vtysh --command \"show bgp ipv6 summary\"",
        'trace': f"vtysh --command \"traceroute ipv6 {prefix}\""
    }

    return ipv6[cmd]


class FrrLib:
    # pylint: disable=too-many-arguments
    """Class provides methods for interaction with a device running
    frrouting suite"""

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
        self.logger = logger

    def _ssh_client_connect(self) -> Any:
        """returns ssh_client object to connect to target device"""
        ssh_client = paramiko.SSHClient()
        # workaround for unknown host key in local cache error
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_client.connect(self.target_device, username=self.username,
                           password=self.password)

        return ssh_client

    def _ssh_client_disconnect(self, ssh_client: Any) -> None:
        """properly close/disconnect ssh session"""
        ssh_client.close()
        self.logger.info(f"connection to {self.target_device} has been closed")

    def run_command(self, cmd: str) -> List[str]:
        # pylint: disable=unused-variable
        # pylint: disable=unused-argument
        """Run command on router"""
        ssh_client = self._ssh_client_connect()
        stdin, stdout, stderr = ssh_client.exec_command(cmd)
        result = [s.strip() for s in stdout.readlines()]
        self._ssh_client_disconnect(ssh_client)

        return result
