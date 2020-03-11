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

.. automodule:: flask_dynrbac.util
   :members:

Mixins
======

You can use mixins in order to expand or create new entity classes that
fit into your domain model. Alternatively, you can simply copy and paste
the mixins' source code into your classes.

All mixins derive from :class:`flask_dynrbac.util.mixins.EntityBase` class,
which contains ``ID`` and ``tablename`` attributes.

In order to use a mixin, derive your entity class both from a mixin and
SQLAlchemy's model class (e.g. `declarative_base` or flask-sqlalchemy's `Model`)::

   from flask_sqlalchemy import SQLAlchemy
   from flask_dynrbac.util.mixins import *

   db = SQLAlchemy(app)

   class Role(db.Model, RoleMixin):
      pass

.. automodule:: flask_dynrbac.util.mixins
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
