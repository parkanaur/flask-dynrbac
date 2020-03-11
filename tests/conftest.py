from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_dynrbac import DynRBAC

from collections import namedtuple

import pytest


@pytest.fixture
def app():
    app = Flask(__name__)
    app.testing = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)

    return app


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
def inited_app(app, role_class, permission_class, user_class):
    rbac = DynRBAC(app, role_class, permission_class, user_class)

    return app, rbac


@pytest.fixture
def decl_base():
    db = SQLAlchemy()
    return db.Model
