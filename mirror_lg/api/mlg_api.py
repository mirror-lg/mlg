"""
mlg public api
"""

from __future__ import annotations
import logging
from typing import Dict

from mirror_lg.lib.helpers import Helper

class MlgApi:
    """
    mlg functions
    """
    def __init__(self,
                 logger: logging.Logger = logging.getLogger()):
        self.logger = logger
        self.helper = Helper()

    def load_config(self) -> Dict:
        """
        Load YAML configuration file
        """
        result = self.helper.load_config_file()

        return result
