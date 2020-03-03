import unittest
from collections import namedtuple

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import flask_dynrbac as fd


class ExtensionInitTestCase(unittest.TestCase):
    """Unit tests for extension initialization"""

    role_class = namedtuple('Role', 'id name parent_id permissions')
    permission_class = namedtuple('Permission', 'id name')
    user_class = namedtuple('User', 'id name roles')

    @staticmethod
    def _generate_app():
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db = SQLAlchemy(app)

        return app

    def test_simple_initialization(self):
        """Should call __init__ without errors"""

        app = self._generate_app()

        rbac = fd.DynRBAC(app, role_class=self.role_class, permission_class=self.permission_class,
                          user_class=self.user_class)

        self.assertIsNotNone(rbac)
        self.assertEqual(rbac.app, app)

    def test_init_app_initialization(self):
        """Should call init_app properly"""

        app = self._generate_app()

        rbac = fd.DynRBAC(role_class=self.role_class, permission_class=self.permission_class,
                          user_class=self.user_class)
        rbac.init_app(app)

        self.assertIsNotNone(rbac)

    def test_warn_without_sqlalchemy(self):
        """Should throw a warning if Flask-SQLAlchemy is not initialized before DynRBAC"""

        app = Flask(__name__)

        self.assertRaises(fd.util.DynRBACInitWarning, lambda: fd.DynRBAC(app))

    def test_warn_without_entity_classes(self):
        """Should throw a warning if role/permission/user classes are not supplied during initialization"""

        app = self._generate_app()

        self.assertRaises(fd.util.DynRBACInitWarning, lambda: fd.DynRBAC(app))


if __name__ == '__main__':
    unittest.main()
