from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.associationproxy import association_proxy


test_base = declarative_base()


class User(test_base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    roles = relationship('Role', secondary='user_roles', backref='users')


class Unit(test_base):
    __tablename__ = 'units'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    permissions = relationship('Permission', secondary='unit_permissions', backref='units')


class Permission(test_base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)


class Role(test_base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    permissions = relationship('Permission', secondary='role_permissions', backref='roles')


class UserRole(test_base):
    __tablename__ = 'user_roles'

    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    user = relationship('User', backref=backref('user_roles', passive_deletes='all'))

    role_id = Column(Integer, ForeignKey(Role.id), primary_key=True)
    role = relationship('Role', backref=backref('user_roles', passive_deletes='all'))


class UnitPermission(test_base):
    __tablename__ = 'unit_permissions'

    unit_id = Column(Integer, ForeignKey(Unit.id), primary_key=True)
    unit = relationship('Unit', backref=backref('unit_permissions', passive_deletes='all'))

    permission_id = Column(Integer, ForeignKey(Permission.id), primary_key=True)
    permission = relationship('Permission', backref=backref('unit_permissions', passive_deletes='all'))


class RolePermission(test_base):
    __tablename__ = 'role_permissions'

    role_id = Column(Integer, ForeignKey(Role.id), primary_key=True)
    role = relationship('Role', backref=backref('role_permissions', passive_deletes='all'))

    permission_id = Column(Integer, ForeignKey(Permission.id), primary_key=True)
    permission = relationship('Permission', backref=backref('role_permissions', passive_deletes='all'))

