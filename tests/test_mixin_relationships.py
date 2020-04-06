# def test_user_role_relationship(decl_base, mixins):
#     """Should work with user-role relationship properly"""
#
#     class User(mixins.get_user_class()):
#         pass
#
#     class Role(mixins.get_role_class()):
#         pass
#
#     class UserRole(mixins.get_user_role_class()):
#         pass
#
#     assert hasattr(UserRole, 'role_id')
#     assert hasattr(UserRole, 'user_id')
#     assert hasattr(UserRole, 'user')
#     assert hasattr(UserRole, 'role')
#     assert hasattr(UserRole, '__tablename__')
#     assert UserRole.__tablename__ == 'user_roles'
#
#     assert hasattr(User, 'roles')
#     assert hasattr(Role, 'users')
