import flask_dynrbac as fd
from flask_dynrbac.util.mixins import *


def test_user_class(decl_base):
    """Should derive `User` class from mixin properly"""

    class User(decl_base, UserMixin):
        pass

    assert hasattr(User, 'id')
    assert hasattr(User, '__tablename__')
    assert User.__tablename__ == 'user'


def test_permission_class(decl_base):
    """Should derive `Permission` class from mixin properly"""

    class Permission(decl_base, PermissionMixin):
        pass

    assert hasattr(Permission, 'id')
    assert hasattr(Permission, '__tablename__')
    assert Permission.__tablename__ == 'permission'


def test_role_class(decl_base):
    """Should derive `Role` class from mixin properly"""

    class Role(decl_base, UserMixin):
        pass

    assert hasattr(Role, 'id')
    assert hasattr(Role, '__tablename__')
    assert Role.__tablename__ == 'role'


def test_unit_class(decl_base):
    """Should derive `Unit` class from mixin properly"""

    class Unit(decl_base, UserMixin):
        pass

    assert hasattr(Unit, 'id')
    assert hasattr(Unit, '__tablename__')
    assert Unit.__tablename__ == 'unit'
