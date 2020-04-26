from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dynrbac import DynRBAC
from flask_dynrbac.domain_model_generator import DomainModelGenerator
from flask_dynrbac.api import generate_rbac_api


try:
    from db_setups import *
except ImportError:
    from .db_setups import *


@pytest.fixture
def flask_app_with_db():
    app = Flask(__name__)
    app.testing = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False
    db = SQLAlchemy(app)

    return app, db


@pytest.fixture
def inited_app(flask_app_with_db):
    app, db = flask_app_with_db
    dmg = DomainModelGenerator(db.Model)
    db.create_all()
    api = generate_rbac_api(app)
    rbac = DynRBAC(app, db.session, lambda: 1, role_class=dmg.Role, permission_class=dmg.Permission,
                   user_class=dmg.User, unit_class=dmg.Unit)

    return app, db, rbac, dmg, api


@pytest.fixture
def app(inited_app):
    app, db, rbac, dmg, api = inited_app
    return app


@pytest.fixture
def db(inited_app):
    app, db, rbac, dmg, api = inited_app
    return db


@pytest.fixture
def rbac(inited_app):
    app, db, rbac, dmg, api = inited_app
    return rbac


@pytest.fixture
def dmg(inited_app):
    app, db, rbac, dmg, api = inited_app
    return dmg


@pytest.fixture
def api(inited_app):
    app, db, rbac, dmg, api = inited_app
    return api


@pytest.fixture
def api_url():
    return '/api/rbac'


@pytest.fixture
def session(db):
    return db.session

