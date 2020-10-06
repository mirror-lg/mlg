"""
Shared library functions
"""
import ipaddress
import logging
from typing import Dict

import yaml


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

    def load_config_file(self, filename='./config/mlg_conf.yaml') -> Dict:
        """
        load device info from yaml config file

        default location/filename is:
        './config/mlg_conf.yaml'
        """

        try:
            with open(filename) as config_file:
                device_config = yaml.safe_load(config_file)
        except FileNotFoundError as file_not_found:
            self.logger.error(f"Config file not found, {file_not_found}")
            raise file_not_found

        return device_config
