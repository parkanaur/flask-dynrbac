import unittest
from flask import Flask
import flask_dynrbac


class ExtensionInitTestCase(unittest.TestCase):
    """Unit tests for extension initialization"""

    def test_simple_initialization(self):
        """Tests initialization via __init__"""
        app = Flask(__name__)
        rbac = flask_dynrbac.DynRBAC(app)

        self.assertIsNotNone(rbac)


if __name__ == '__main__':
    unittest.main()
