# from sqlalchemy import Column, String
#
#
# def test_user_class(decl_base, mixins):
#     """Should derive `User` class from mixin properly"""
#
#     class User(mixins.get_user_class()):
#         pass
#
#     assert hasattr(User, 'id')
#     assert hasattr(User, '__tablename__')
#     assert User.__tablename__ == 'users'
#
#
# def test_user_mixin_id_prop_is_overridden(decl_base, mixins):
#     """Should allow for pre-defined attributes to be overridden"""
#
#     class User(mixins.get_user_class()):
#         id = Column(String, primary_key=True)
#
#     assert hasattr(User, 'id')
#     assert type(User.id.type) == String
#
#
# def test_permission_class(decl_base, mixins):
#     """Should derive `Permission` class from mixin properly"""
#
#     class Permission(mixins.get_permission_class()):
#         pass
#
#     assert hasattr(Permission, 'id')
#     assert hasattr(Permission, '__tablename__')
#     assert Permission.__tablename__ == 'permissions'
#
#
# def test_role_class(decl_base, mixins):
#     """Should derive `Role` class from mixin properly"""
#
#     class Role(mixins.get_role_class()):
#         pass
#
#     assert hasattr(Role, 'id')
#     assert hasattr(Role, '__tablename__')
#     assert Role.__tablename__ == 'roles'
#
#
# def test_unit_class(decl_base, mixins):
#     """Should derive `Unit` class from mixin properly"""
#
#     class Unit(mixins.get_unit_class()):
#         pass
#
#     assert hasattr(Unit, 'id')
#     assert hasattr(Unit, '__tablename__')
#     assert Unit.__tablename__ == 'units'
