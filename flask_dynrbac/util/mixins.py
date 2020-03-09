from flask_sqlalchemy import SQLAlchemy


class UserMixin(SQLAlchemy.Model):
    """Mixin to use on a User class"""
    pass


class PermissionMixin:
    """Mixin to use on a Permission class"""
    pass


class RoleMixin:
    """Mixin to use on a Role class"""
    pass


class RolePermissionMixin:
    """Mixin to use on a RolePermission class, which is a linking table for Role-Permission relationship"""
    pass


class UserRoleMixin:
    """Mixin to use on a UserRole class, which is a linking table for User-Role relationship"""
    pass
