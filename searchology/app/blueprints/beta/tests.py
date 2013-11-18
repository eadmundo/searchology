import unittest
from searchology.app import create_app

class TestBetaBlueprint(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()
