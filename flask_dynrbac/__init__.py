from . import exc
from .logic import UserLogic, UnitLogic, PermissionLogic, RoleLogic

from flask import abort

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
    :param session: SQLAlchemy session proxy. Use standard `sqlalchemy.orm.session` or Flask-SQLAlchemy's
        `SQLAlchemy().session`.
    :param user_id_provider: A callable which returns an ID of a current logged in user, e.g.
        Flask-Login's `current_user` (`lambda: return current_user.id`) or Flask's `session` directly:
        `lambda: return session['uid']`.
    :param role_class: Role entity class
    :param permission_class: Permission entity class
    :param user_class: User entity class
    :param unit_class: Unit entity class
    :param user_role_relationship: User-Role relationship class
    :param role_permission_relationship: Role-Permission relationship class
    :param unit_permission_relationship: Unit-Permission relationship class
    :param global_error_code: HTTP error code to return in case of permission mismatch. Defaults to 403 Forbidden
    :param unique_unit_names_only: If True, disallows repeating unit names during endpoint registration,
        i.e., there cannot be two functions with the same unit_name supplied to them. Setting this to True
        will require additional precautionary measures if your app has modules with repeating names (and with route
        definitions in those modules) and if you leave unit_name parameters blank (see default unit_name in
        :meth:`flask_dynrbac.DynRBAC.rbac`).
    :param create_missing_units: If True, will create missing units in the database during permission checks.
    """

    def __init__(self, app=None, session=None, user_id_provider=None, role_class=None, permission_class=None, user_class=None, unit_class=None,
                 user_role_relationship=None, role_permission_relationship=None, unit_permission_relationship=None,
                 global_error_code=403,
                 unique_unit_names_only=False, create_missing_units=True):
        """Initializes, configures and binds the extension instance to an app"""
        self.app = app
        self.global_error_code = global_error_code
        self.unique_unit_names_only = unique_unit_names_only

        self.session = session
        self.user_id_provider = user_id_provider

        self.role_class = role_class
        self.permission_class = permission_class
        self.user_class = user_class
        self.unit_class = unit_class

        self.user_role_relationship = user_role_relationship
        self.role_permission_relationship = role_permission_relationship
        self.unit_permission_relationship = unit_permission_relationship

        self.create_missing_units = create_missing_units

        #: Current endpoint collection
        self.registered_endpoints = {}

        self._user_logic = UserLogic(self.user_class, self.permission_class, self.role_class,
                                     self.unit_class, self.session)
        self._role_logic = RoleLogic(self.role_class, self.session)
        self._permission_logic = PermissionLogic(self.permission_class, self.session)
        self._unit_logic = UnitLogic(self.unit_class, self.session)

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
                          'management.', exc.DynRBACInitWarning)

        if self.session is None:
            warnings.warn('Session object is not supplied. It is required in order to make queries to'
                          'the database. Set session via `DynRBAC.session` attribute.', exc.DynRBACInitWarning)

        if self.user_id_provider is None:
            warnings.warn('User ID provider callable is not supplied. It is required in order to make queries to'
                          'the database. Set via `DynRBAC.session` attribute.', exc.DynRBACInitWarning)

        if self.role_class is None:
            warnings.warn('Role class is not supplied. It is required for proper functioning of this'
                          'extension. RoleMixin is available for quicker development.', exc.DynRBACInitWarning)

        if self.permission_class is None:
            warnings.warn('Permission class is not supplied. It is required for proper functioning of '
                          'this extension. PermissionMixin is available for quicker development.',
                          exc.DynRBACInitWarning)

        if self.user_class is None:
            warnings.warn('User class is not supplied. It is required for proper functioning of this'
                          'extension. UserMixin is available for quicker development.', exc.DynRBACInitWarning)

        if self.unit_class is None:
            warnings.warn('Unit class is not supplied. It is required for proper functioning of this'
                          'extension. UnitMixin is available for quicker development.', exc.DynRBACInitWarning)

    def rbac(self, unit_name=None, check_hierarchy=False, error_code=None):
        """ Restricts access to a function based on a role/permission list.
            The list is retrieved from the app's database.

            :param unit_name: Optional name for a function for database storage. Defaults to `func.__module__ + "_" +
                func.__name__`
            :param check_hierarchy: Allows for recursive check of user roles' parent permissions.
            :param error_code: HTTP status code to return in case of permission mismatch. Defaults to
                `self.global_error_code`
            """

        def decorator(func):
            err_code = error_code or self.global_error_code
            unit = unit_name or '{module}_{name}'.format(module=func.__module__, name=func.__name__)

            if unit in self.registered_endpoints:
                if self.unique_unit_names_only:
                    raise KeyError('Unit {unit} is already registered in the extension. Change its name or use '
                                   'a provided default (func.__module__ + "_" + func.__name__'.format(unit=unit))
            else:
                self.registered_endpoints[unit] = func
                if not self._unit_logic.is_unit_in_db(unit) and self.create_missing_units:
                    self._unit_logic.add_to_db(unit)

            if not self._user_logic.has_unit_permission(self.user_id_provider(), unit):
                return abort(err_code)

            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def get_all_roles(self):
        return self._role_logic.get_all()

    def get_all_permissions(self):
        return self._permission_logic.get_all()

    def get_all_users(self):
        return self._user_logic.get_all()

    def get_all_units(self):
        return self._unit_logic.get_all()
