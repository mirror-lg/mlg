import unittest

from mirror_lg.api.mlg_api import MlgApi


class TestMlgApi(unittest.TestCase):
    def setUp(self):
        self.caller = MlgApi()

    def test_mlg_api_nominal(self):
        output = self.caller.load_config()

        self.assertIsInstance(output, dict)
