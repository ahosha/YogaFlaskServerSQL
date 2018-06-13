import unittest
import FlaskServer.Routes.System as systemService

class SystemTester(unittest.TestCase):
    """description of class"""

    #def setUp(self):
    #    self.systemService = systemService

    def test_system(self):
        self.assertEqual('test_system', 'test_system')

