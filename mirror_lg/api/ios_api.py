"""
cisco ios public api
"""

from __future__ import annotations
import logging
from typing import Dict

from mirror_lg.lib.ios.ios_lib import IosLib
from mirror_lg.lib.ios.ios_lib import ipv4_commands
from mirror_lg.lib.ios.ios_lib import ipv6_commands
from mirror_lg.lib.parsers import parse_exploded_address


class IosApi:
    """
    Cisco ios functions
    """

    def __init__(self,
                 caller,
                 logger: logging.Logger = logging.getLogger()):
        self.logger = logger
        self.caller = caller

        self.ipv4_commands = ipv4_commands
        self.ipv6_commands = ipv6_commands

    def show_ipv4_route(self, cmd: str, prefix: str) -> Dict:
        """
        execute show ipv4 route command
        """
        prefix = parse_exploded_address(prefix)

        output = self.caller.run_command(self.ipv4_commands(cmd, prefix))

        return output

    def show_ipv6_route(self, cmd: str, prefix: str) -> Dict:
        """
        execute show ipv6 route command
        """
        prefix = parse_exploded_address(prefix)

        output = self.caller.run_command(self.ipv6_commands(cmd, prefix))

        return output
