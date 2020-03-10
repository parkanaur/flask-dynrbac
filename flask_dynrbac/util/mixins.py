from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base, declared_attr


class EntityBase(object):
    """Base class for all entities which contains useful attributes"""

    @declared_attr
    def id(self):
        """Supplies the subclass with a primary key `id` property."""
        return Column(Integer, primary_key=True)

    @declared_attr
    def __tablename__(self):
        """Supplies the subclass with a `tablename` attribute."""
        return self.__name__.lower()


class UnitMixin(EntityBase):
    """Mixin to use on a Unit class, which represents a source code unit (e.g. function)"""

    #: Unit name
    name = Column(String, unique=True, nullable=False)


class UserMixin(EntityBase):
    """Mixin to use on a User class"""
    pass


class PermissionMixin(EntityBase):
    """Mixin to use on a Permission class"""

    #: Permission name
    name = Column(String, unique=True, nullable=False)


class RoleMixin(EntityBase):
    """Mixin to use on a Role class"""

    #: Role name
    name = Column(String, unique=True, nullable=False)


class RolePermissionMixin(object):
    """Mixin to use on a RolePermission class, which is a linking table for Role-Permission relationship"""
    pass


class UserRoleMixin(object):
    """Mixin to use on a UserRole class, which is a linking table for User-Role relationship"""
    pass


class UnitPermissionMixin(object):
    """Mixin to use on a UnitPermission class, which is a linking table for Unit-Permission relationship"""
    pass
