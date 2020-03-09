from . import util

from functools import wraps
import warnings


class DynRBAC(object):
    """Allows for dynamic role-based access control (RBAC)
    by means of providing a decorator for using on some endpoint/method to
    register it, as well as HTTP API and an optional web interface for
    role handling.

    In order to function properly, the extension has to be supplied with the
    Role, Permission, and User classes, which in turn have to be based
    on SQLAlchemy's `declarative_base` (Flask-SQLAlchemy provides an alias - `flask_sqlalchemy.Model`, which
    most common entities inherit from).
    Mixins are available for quicker development.

    :param app: Flask app
    :param role_class: Role entity class
    :param permission_class: Permission entity class
    :param user_class: User entity class
    :param global_error_code: HTTP error code to return in case of permission mismatch. Defaults to 403 Forbidden
    """

    def __init__(self, app=None, role_class=None, permission_class=None, user_class=None, global_error_code=403):
        """Initializes, configures and binds the extension instance to an app"""
        self.app = app
        self.global_error_code = global_error_code
        self.role_class = role_class
        self.permission_class = permission_class
        self.user_class = user_class

        #: Current endpoint collection
        self.registered_endpoints = {}

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Configures the extension to be used later.

        :param app: Flask app
        """
        self._validate_requirements(app)

        app.extensions['dynrbac'] = self

    def _validate_requirements(self, app):
        """ Checks whether the supplied app fulfills the extension/domain model requirements.
            Throws a warning if some requirement is not met."""

        if app.extensions.get('sqlalchemy') is None:
            warnings.warn('Flask-SQLAlchemy is not initialized before DynRBAC. '
                          'DynRBAC requires SQLAlchemy for role and permission data '
                          'management.', util.DynRBACInitWarning)

        if self.role_class is None:
            warnings.warn('Role class is not supplied. It is required for proper functioning of this'
                          'extension. RoleMixin is available for quicker development.', util.DynRBACInitWarning)

        if self.permission_class is None:
            warnings.warn('Permission class is not supplied. It is required for proper functioning of '
                          'this extension. PermissionMixin is available for quicker development.',
                          util.DynRBACInitWarning)

        if self.user_class is None:
            warnings.warn('User class is not supplied. It is required for proper functioning of this'
                          'extension. UserMixin is available for quicker development.', util.DynRBACInitWarning)

    def rbac(self, unit_name=None, check_hierarchy=False, error_code=None):
        """ Restricts access to a function based on a role/permission list.
            The list is retrieved from the app's database.

            :param unit_name: Optional name for a function for database storage. Defaults to func name
            :param check_hierarchy: Allows for recursive check of user roles' parent permissions.
            :param error_code: HTTP status code to return in case of permission mismatch. Defaults to
                `self.global_error_code`
            """

        def decorator(func):
            err = error_code or self.global_error_code
            unit = unit_name or '{module}_{name}'.format(module=func.__module__, name=func.__name__)

            if unit in self.registered_endpoints:
                raise KeyError('Unit {unit} is already registered in the extension. Change its name or use '
                               'a provided default (func.__module__ + "_" + func.__name__'.format(unit=unit))

            self.registered_endpoints[unit] = func

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator
