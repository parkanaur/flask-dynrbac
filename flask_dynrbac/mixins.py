from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class EntityBase(object):
    """Base class for all entities which contains useful attributes"""

    @declared_attr
    def id(self):
        """Supplies the subclass with a primary key `id` property."""
        return Column(Integer, primary_key=True)


class MixinGenerator(object):
    """Helper metaclass which generates mixins with all the necessary attributes based on supplied class names.
    Due to how SQLAlchemy works,

    :param user_class_name: User class name (defaults to 'user')
    """

    def __init__(self, user_class_name='user', role_class_name='role', permission_class_name='permission',
                 unit_class_name='unit', role_permission_class_name='role_permissions',
                 user_role_class_name='user_roles', unit_permission_class_name='unit_permissions'):
        self.user_class_name = user_class_name
        self.role_class_name = role_class_name
        self.permission_class_name = permission_class_name
        self.unit_class_name = unit_class_name
        self.role_permission_class_name = role_permission_class_name
        self.user_role_class_name = user_role_class_name
        self.unit_permission_class_name = unit_permission_class_name

        self._generate_classes()
        self._generate_relationships()

    def _generate_classes(self):
        """Generates domain model classes with necessary attributes"""

        class User(EntityBase):
            """Mixin to use on a User class"""
            __tablename__ = self.user_class_name

        self.user_class = User

        class Unit(EntityBase):
            """Mixin to use on a Unit class, which represents a source code unit (e.g. function)"""
            __tablename__ = self.unit_class_name

            #: Unit name
            name = Column(String, unique=True, nullable=False)

        self.unit_class = Unit

        class Permission(EntityBase):
            """Mixin to use on a Permission class"""
            __tablename__ = self.permission_class_name

            #: Permission name
            name = Column(String, unique=True, nullable=False)

        self.permission_class = Permission

        class Role(EntityBase):
            """Mixin to use on a Role class"""
            __tablename__ = self.role_class_name

            #: Role name
            name = Column(String, unique=True, nullable=False)

        self.role_class = Role

    def _generate_relationships(self):
        class RolePermission(object):
            """Mixin to use on a RolePermission class, which is a linking table for Role-Permission relationship"""
            role_id = Column(Integer, ForeignKey('role.id'), primary_key=True)
            permission_id = Column(Integer, ForeignKey('permission.id'), primary_key=True)

        self.role_permission_class = RolePermission

        class UserRole(object):
            """Mixin to use on a UserRole class, which is a linking table for User-Role relationship"""
            pass

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
