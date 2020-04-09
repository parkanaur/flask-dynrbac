.. Flask-DynRBAC documentation master file, created by
   sphinx-quickstart on Fri Feb 28 17:30:24 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flask-DynRBAC's documentation!
=========================================

**ATTENTION**: this extension is still WIP. Use at your own risk.


Flask-DynRBAC is a Flask extension which allows for dynamic
role based access control and management, which is based on
database lookups and stores::

   # No hard-coded roles!
   @rbac()
   def func():
      # logic goes here

Role and permission management can be done manually or via
the pluggable API with optional HTML views.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

How it works
============

All the work is done by the :meth:`flask_dynrbac.DynRBAC.rbac` decorator.

.. automodule:: flask_dynrbac
   :members:

.. automodule:: flask_dynrbac.exc
   :members:

Domain Model generation
=======================

You can use :class:`flask_dynrbac.domain_model_generator.DomainModelGenerator` in order to expand
or create new entity classes that fit into your domain model.
Alternatively, you can simply copy and paste
the domain models' source code into your classes.

In order to use a default domain model, create an instance of `DomainModelGenerator`
with declarative base as a constructor argument (SQLAlchemy's `declarative_base` or
Flask-SQLAlchemy's `SQLAlchemy.model`)::

   from flask import Flask
   from flask_sqlalchemy import SQLAlchemy
   from flask_dynrbac.domain_model_generator import DomainModelGenerator

   app = Flask(__name__)
   db = SQLAlchemy(app)

   dmg = DomainModelGenerator(db.Model)

   # Use dmg.User, dmg.Permission, dmg.Role classes...

.. automodule:: flask_dynrbac.domain_model_generator
   :members:

Pluggable API
=============

HTML Views
=============

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
