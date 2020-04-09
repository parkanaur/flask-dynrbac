from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.associationproxy import association_proxy


class DomainModelGenerator:
    """A class which will generate domain model classes which can be used directly
       or expanded upon.

       Alternatively, the source code of domain model classes can be copied
       and pasted into the project's existing codebase.

       :param base: base SQLAlchemy class for entities (e.g. `declarative_base` or
           `db.Model` for flask-sqlalchemy)
       """
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

        #: User domain model class
        self.User = User
        #: Role domain model class
        self.Role = Role
        #: Permission domain model class
        self.Permission = Permission
        #: Unit domain model class
        self.Unit = Unit
        #: Unit-Permission relationship class (association object)
        self.UnitPermission = UnitPermission
        #: User-Role relationship class (association object)
        self.UserRole = UserRole
        #: Role-Permission relationship class (association object)
        self.RolePermission = RolePermission
