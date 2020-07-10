"""
Shared library functions
"""
import ipaddress
from typing import Generic


def validate_prefix(prefix: str) -> Generic:
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
