import flask_dynrbac as fd

from flask import Flask
import pytest


def test_simple_initialization(app, role_class, permission_class, user_class):
    """Should call __init__ without errors"""
    rbac = fd.DynRBAC(app, role_class=role_class, permission_class=permission_class, user_class=user_class)

    assert rbac is not None
    assert rbac.app == app


def test_init_app_initialization(app, role_class, permission_class, user_class):
    """Should call init_app properly"""

    rbac = fd.DynRBAC(app, role_class=role_class, permission_class=permission_class, user_class=user_class)
    rbac.init_app(app)

    assert rbac is not None


def test_warn_without_sqlalchemy():
    """Should throw a warning if Flask-SQLAlchemy is not initialized before DynRBAC"""

    app = Flask(__name__)

    with pytest.warns(fd.util.DynRBACInitWarning):
        fd.DynRBAC(app)


def test_warn_without_entity_classes(app):
    """Should throw a warning if role/permission/user classes are not supplied during initialization"""

    with pytest.warns(fd.util.DynRBACInitWarning):
        fd.DynRBAC(app)
