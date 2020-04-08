import flask_dynrbac as fd
from flask_dynrbac.domain_model_generator import DomainModelGenerator

from flask import Flask
import pytest


def test_simple_initialization(flask_app_with_db):
    """Should call __init__ without errors"""
    app, db = flask_app_with_db
    dmg = DomainModelGenerator(db.Model)

    rbac = fd.DynRBAC(app, session=db.session, user_id_provider=lambda: 1,
                      role_class=dmg.Role, permission_class=dmg.Permission,
                      user_class=dmg.User, unit_class=dmg.Unit)

    assert rbac is not None
    assert rbac.app == app


def test_init_app_initialization(flask_app_with_db):
    """Should call init_app properly"""
    app, db = flask_app_with_db
    dmg = DomainModelGenerator(db.Model)

    rbac = fd.DynRBAC(session=db.session, user_id_provider=lambda: 1,
                      role_class=dmg.Role, permission_class=dmg.Permission,
                      user_class=dmg.User, unit_class=dmg.Unit)
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
