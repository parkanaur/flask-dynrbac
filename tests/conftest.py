from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dynrbac import DynRBAC
from flask_dynrbac.mixins import MixinGenerator
from flask_dynrbac.testing_domain_model import *

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from collections import namedtuple

import pytest


@pytest.fixture
def flask_app_with_db():
    app = Flask(__name__)
    app.testing = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    return app, db


@pytest.fixture
def role_class():
    return namedtuple('Role', 'id name parent_id permissions')


@pytest.fixture
def permission_class():
    return namedtuple('Permission', 'id name')


@pytest.fixture
def user_class():
    return namedtuple('User', 'id name roles')


@pytest.fixture
def unit_class():
    return namedtuple('Unit', 'id name')


@pytest.fixture
def inited_app(flask_app_with_db):
    app, db = flask_app_with_db
    rbac = DynRBAC(app, db.session, lambda: 1, role_class=Role, permission_class=Permission, user_class=User,
                   unit_class=Unit)

    return app, db, rbac


@pytest.fixture
def decl_base():
    db = SQLAlchemy()
    return db.Model


@pytest.fixture
def mixins():
    db = SQLAlchemy()
    return MixinGenerator(db.Model)


@pytest.fixture
def session():
    engine = create_engine('sqlite:///:memory:')
    test_base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    return Session()
