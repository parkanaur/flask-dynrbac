from sqlalchemy.sql.sqltypes import String as SqlString
from sqlalchemy import Column, String


def test_user_class(decl_base, mixins):
    """Should derive `User` class from mixin properly"""

    class User(decl_base, mixins.get_user_class()):
        pass

    assert hasattr(User, 'id')
    assert hasattr(User, '__tablename__')
    assert User.__tablename__ == 'user'


def test_user_mixin_id_prop_is_overridden(decl_base, mixins):
    """Should allow for pre-defined attributes to be overridden"""

    class User(decl_base, mixins.get_user_class()):
        id = Column(String, primary_key=True)

    assert hasattr(User, 'id')
    assert type(User.id.type) == String


def test_permission_class(decl_base, mixins):
    """Should derive `Permission` class from mixin properly"""

    class Permission(decl_base, mixins.get_permission_class()):
        pass

    assert hasattr(Permission, 'id')
    assert hasattr(Permission, '__tablename__')
    assert Permission.__tablename__ == 'permission'


def test_role_class(decl_base, mixins):
    """Should derive `Role` class from mixin properly"""

    class Role(decl_base, mixins.get_role_class()):
        pass

    assert hasattr(Role, 'id')
    assert hasattr(Role, '__tablename__')
    assert Role.__tablename__ == 'role'


def test_unit_class(decl_base, mixins):
    """Should derive `Unit` class from mixin properly"""

    class Unit(decl_base, mixins.get_unit_class()):
        pass

    assert hasattr(Unit, 'id')
    assert hasattr(Unit, '__tablename__')
    assert Unit.__tablename__ == 'unit'
