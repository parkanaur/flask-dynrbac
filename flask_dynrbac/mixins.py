from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.associationproxy import association_proxy


class MixinGenerator(object):
    """Helper metaclass which generates mixins with all the necessary attributes based on supplied class names.
    Due to how SQLAlchemy works,

    :param user_table_name: User table name (defaults to 'users')
    :param role_table_name: Role table name (defaults to 'roles')
    :param permission_table_name: Permission table name (defaults to 'permissions')
    :param unit_table_name: Unit table name (defaults to 'units')
    :param role_permission_table_name: Role-Permission table name (defaults to 'role_permissions')
    :param user_role_table_name: User-Role table name (defaults to 'user_roles')
    :param unit_permission_table_name: Unit-Permission table name (defaults to 'unit_permissions')
    """

    def __init__(self, decl_base,
                 user_table_name='users', role_table_name='roles', permission_table_name='permissions',
                 unit_table_name='units', role_permission_table_name='role_permissions',
                 user_role_table_name='user_roles', unit_permission_table_name='unit_permissions',
                 ):
        self.user_table_name = user_table_name
        self.role_table_name = role_table_name
        self.permission_table_name = permission_table_name
        self.unit_table_name = unit_table_name
        self.role_permission_table_name = role_permission_table_name
        self.user_role_table_name = user_role_table_name
        self.unit_permission_table_name = unit_permission_table_name

        self.base = decl_base

        self._generate_classes()
        self._generate_relationships()



    def _generate_classes(self):
        """Generates domain model classes with necessary attributes"""

        class User(self.base):
            """Mixin to use on a User class"""
            __tablename__ = self.user_table_name
            __table_args__ = {'extend_existing': True}

            id = Column(Integer, primary_key=True)

            roles = association_proxy('user_roles', 'role')

        self.user_class = User

        class Unit(self.base):
            """Mixin to use on a Unit class, which represents a source code unit (e.g. function)"""
            __tablename__ = self.unit_table_name
            id = Column(Integer, primary_key=True)

            #: Unit name
            name = Column(String, unique=True, nullable=False)

        self.unit_class = Unit

        class Permission(self.base):
            """Mixin to use on a Permission class"""
            __tablename__ = self.permission_table_name
            id = Column(Integer, primary_key=True)

            #: Permission name
            name = Column(String, unique=True, nullable=False)

        self.permission_class = Permission

        class Role(self.base):
            """Mixin to use on a Role class"""
            __tablename__ = self.role_table_name
            id = Column(Integer, primary_key=True)

            #: Role name
            name = Column(String, unique=True, nullable=False)

            users = association_proxy('role_users', 'user')

        self.role_class = Role

    def _generate_relationships(self):
        class RolePermission(object):
            """Mixin to use on a RolePermission class, which is a linking table for Role-Permission relationship"""
            __tablename__ = self.role_permission_table_name

            @declared_attr
            def role_id(self):
                return Column(Integer, ForeignKey('role.id'), primary_key=True)

            @declared_attr
            def permission_id(self):
                return Column(Integer, ForeignKey('permission.id'), primary_key=True)

        self.role_permission_class = RolePermission

        class UserRole(self.base):
            """Mixin to use on a UserRole class, which is a linking table for User-Role relationship"""
            __tablename__ = self.user_role_table_name

            _user_cls = self.user_class
            _role_cls = self.role_class

            @declared_attr
            def user_id(self):
                return Column(Integer, ForeignKey(self._user_cls.id), primary_key=True)

            @declared_attr
            def user(self):
                return relationship(self._user_cls, backref=backref('user_roles'))

            @declared_attr
            def role_id(self):
                return Column(Integer, ForeignKey(self._role_cls.id), primary_key=True)

            @declared_attr
            def role(self):
                return relationship(self._role_cls, backref=backref('role_users'))

        self.user_role_class = UserRole

        class UnitPermission(object):
            """Mixin to use on a UnitPermission class, which is a linking table for Unit-Permission relationship"""
            pass

        self.unit_permission_class = UnitPermission

    def get_user_class(self):
        return self.user_class

    def get_permission_class(self):
        return self.permission_class

    def get_role_class(self):
        return self.role_class

    def get_unit_class(self):
        return self.unit_class

    def get_user_role_class(self):
        return self.user_role_class

    def get_role_permission_class(self):
        return self.role_permission_class

    def get_unit_permission_class(self):
        return self.unit_permission_class


if __name__ == '__main__':
    m = MixinGenerator()
    print(m.user_class.roles)
    class G(declarative_base(), m.get_user_class()):
        pass
    print(G.roles)
