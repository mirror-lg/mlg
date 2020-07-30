"""
Shared library functions
"""
import ipaddress
import logging


class Helper:
    """implements shared methods"""

    def __init__(self,
                 logger: logging.Logger = logging.getLogger()):

        self.logger = logger

    def validate_prefix(self, prefix: str):
        """
        check if prefix is a valid ipv4 or ipv6 address, return an ipaddress
        object or raise exception
        """

        try:
            prefix = ipaddress.ip_network(prefix, strict=False)
        except ValueError as invalid_prefix:
            self.logger.error(f"Invalid input prefix, {invalid_prefix}")
            raise invalid_prefix

        return prefix
