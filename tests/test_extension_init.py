import flask_dynrbac as fd
from flask_dynrbac.testing_domain_model import *

from flask import Flask
import pytest


def test_simple_initialization(flask_app_with_db, role_class, permission_class, user_class, unit_class):
    """Should call __init__ without errors"""
    app, db = flask_app_with_db

    rbac = fd.DynRBAC(app, session=db.session, user_id_provider=lambda: 1,
                      role_class=role_class, permission_class=permission_class, user_class=user_class,
                      unit_class=unit_class)

    assert rbac is not None
    assert rbac.app == app


def test_init_app_initialization(flask_app_with_db, role_class, permission_class, user_class, unit_class):
    """Should call init_app properly"""
    app, db = flask_app_with_db

    rbac = fd.DynRBAC(session=db.session, user_id_provider=lambda: 1,
                      role_class=role_class, permission_class=permission_class, user_class=user_class,
                      unit_class=unit_class)
    rbac.init_app(app)

    assert rbac is not None


def test_warn_without_sqlalchemy():
    """Should throw a warning if Flask-SQLAlchemy is not initialized before DynRBAC"""

    app = Flask(__name__)

    with pytest.warns(fd.exc.DynRBACInitWarning):
        fd.DynRBAC(app)


def test_warn_without_entity_classes(flask_app_with_db):
    """Should throw a warning if role/permission/user/unit classes are not supplied during initialization"""
    app, db = flask_app_with_db

    with pytest.warns(fd.exc.DynRBACInitWarning):
        fd.DynRBAC(app)


def test_init_with_testing_models(flask_app_with_db):
    """Should init with testing domain model properly"""
    app, db = flask_app_with_db

    rbac = fd.DynRBAC(session=db.session, user_id_provider=lambda: 1,
                      role_class=Role, permission_class=Permission,
                      user_class=User, unit_class=Unit)
    rbac.init_app(app)

    assert rbac is not None
