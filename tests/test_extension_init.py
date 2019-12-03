import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_dynrbac as fd


class ExtensionInitTestCase(unittest.TestCase):
    """Unit tests for extension initialization"""

    def test_simple_initialization(self):
        """Should call __init__ without errors"""
        app = Flask(__name__)
        db = SQLAlchemy(app)

        rbac = fd.DynRBAC(app)

        self.assertIsNotNone(rbac)

    def test_crash_without_sqlalchemy(self):
        """Should throw an exception if Flask-SQLAlchemy is not initialized before DynRBAC"""

        app = Flask(__name__)

        self.assertRaises(fd.util.SQLAlchemyNotSuppliedException, lambda: fd.DynRBAC(app))


if __name__ == '__main__':
    unittest.main()
