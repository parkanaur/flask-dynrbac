.. Flask-DynRBAC documentation master file, created by
   sphinx-quickstart on Fri Feb 28 17:30:24 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Flask-DynRBAC's documentation!
=========================================

Flask-DynRBAC is a Flask extension which allows for dynamic
role based access control and management, which is based on
database lookups and stores::

   # No hard-coded roles!
   @rbac()
   def func():
      # logic goes here

Role and permission management can be done manually or via
the pluggable API with optional HTML views.

Documentation
=============

All the work is done by the :meth:`flask_dynrbac.DynRBAC.rbac` decorator.

.. automodule:: flask_dynrbac
   :members:

.. automodule:: flask_dynrbac.util
   :members:

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Pluggable API
=============

HTML Views
=============

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`