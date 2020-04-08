from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.associationproxy import association_proxy


class DomainModelGenerator:
    def __init__(self, base):
        self.base = base

        class User(self.base):
            __tablename__ = 'users'

            id = Column(Integer, primary_key=True)
            name = Column(String)

            roles = relationship('Role', secondary='user_roles', backref='users')

            def __repr__(self):
                return "<User: " + str(self.id) + " " + self.name + ">"

        class Unit(self.base):
            __tablename__ = 'units'

            id = Column(Integer, primary_key=True)
            name = Column(String, unique=True, nullable=False)

            permissions = relationship('Permission', secondary='unit_permissions', backref='units')

            def __repr__(self):
                return "<User: " + str(self.id) + " " + self.name + ">"

        class Permission(self.base):
            __tablename__ = 'permissions'

            id = Column(Integer, primary_key=True)
            name = Column(String, unique=True, nullable=False)

            def __repr__(self):
                return "<User: " + str(self.id) + " " + self.name + ">"

        class Role(self.base):
            __tablename__ = 'roles'

            id = Column(Integer, primary_key=True)
            name = Column(String, unique=True, nullable=False)

            permissions = relationship('Permission', secondary='role_permissions', backref='roles')

            def __repr__(self):
                return "<User: " + str(self.id) + " " + self.name + ">"

        class UserRole(self.base):
            __tablename__ = 'user_roles'

            user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
            user = relationship('User', backref=backref('user_roles', passive_deletes='all'))

            role_id = Column(Integer, ForeignKey(Role.id), primary_key=True)
            role = relationship('Role', backref=backref('user_roles', passive_deletes='all'))

        class UnitPermission(self.base):
            __tablename__ = 'unit_permissions'

            unit_id = Column(Integer, ForeignKey(Unit.id), primary_key=True)
            unit = relationship('Unit', backref=backref('unit_permissions', passive_deletes='all'))

            permission_id = Column(Integer, ForeignKey(Permission.id), primary_key=True)
            permission = relationship('Permission', backref=backref('unit_permissions', passive_deletes='all'))

        class RolePermission(self.base):
            __tablename__ = 'role_permissions'

            role_id = Column(Integer, ForeignKey(Role.id), primary_key=True)
            role = relationship('Role', backref=backref('role_permissions', passive_deletes='all'))

            permission_id = Column(Integer, ForeignKey(Permission.id), primary_key=True)
            permission = relationship('Permission', backref=backref('role_permissions', passive_deletes='all'))

        self.User = User
        self.Role = Role
        self.Permission = Permission
        self.Unit = Unit
        self.UnitPermission = UnitPermission
        self.UserRole = UserRole
        self.RolePermission = RolePermission
