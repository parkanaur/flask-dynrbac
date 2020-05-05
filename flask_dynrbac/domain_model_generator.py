from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
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
            __tablename__ = 'user'

            id = Column(Integer, primary_key=True)
            name = Column(String)

            roles = relationship('Role', secondary='user_role', backref='users')

            def __repr__(self):
                return "<User: " + str(self.id) + " " + self.name + ">"

            def __hash__(self):
                return hash(self.id)

            def __eq__(self, other):
                return isinstance(other, User) and self.id == other.id

            def to_dict(self):
                return {'id': self.id,
                        'name': self.name,
                        'roles': [{'id': role.id, 'name': role.name} for role in self.roles]}

        class Unit(self.base):
            __tablename__ = 'unit'

            id = Column(Integer, primary_key=True)
            name = Column(String, unique=True, nullable=False)

            perms_all_required = Column(Boolean, nullable=False, default=False)

            permissions = relationship('Permission', secondary='unit_permission', backref='units')

            def __repr__(self):
                return "<Unit: " + str(self.id) + " " + self.name + ">"

            def __hash__(self):
                return hash(self.id)

            def __eq__(self, other):
                return isinstance(other, Unit) and self.id == other.id

            def to_dict(self):
                return {'id': self.id,
                        'name': self.name,
                        'perms_all_required': self.perms_all_required,
                        'permissions': [{'id': perm.id, 'name': perm.name} for perm in self.permissions]}

        class Permission(self.base):
            __tablename__ = 'permission'

            id = Column(Integer, primary_key=True)
            name = Column(String, unique=True, nullable=False)

            def __repr__(self):
                return "<Permission: " + str(self.id) + " " + self.name + ">"

            def __hash__(self):
                return hash(self.id)

            def __eq__(self, other):
                return isinstance(other, Permission) and self.id == other.id

            def to_dict(self):
                return {'id': self.id,
                        'name': self.name,
                        'roles': [{'id': role.id, 'name': role.name} for role in self.roles],
                        'units': [{'id': unit.id, 'name': unit.name} for unit in self.units]}

        class Role(self.base):
            __tablename__ = 'role'

            id = Column(Integer, primary_key=True)
            name = Column(String, unique=True, nullable=False)

            permissions = relationship('Permission', secondary='role_permission', backref='roles')

            parents = relationship('Role', secondary='role_role_hierarchy',
                                   primaryjoin='Role.id == RoleHierarchy.child_id',
                                   secondaryjoin='Role.id == RoleHierarchy.parent_id',
                                   backref='children')

            incompatible_roles = relationship('Role', secondary='role_role_restriction',
                                              primaryjoin='Role.id == RoleRestriction.incompat_role_id',
                                              secondaryjoin='Role.id == RoleRestriction.role_id',
                                              backref='roles_restricted_by_this_role')

            def __repr__(self):
                return "<Role: " + str(self.id) + " " + self.name + ">"

            def __hash__(self):
                return hash(self.id)

            def __eq__(self, other):
                return isinstance(other, Role) and self.id == other.id

            def to_dict(self):
                return {'id': self.id,
                        'name': self.name,
                        'permissions': [{'id': perm.id, 'name': perm.name} for perm in self.permissions],
                        'users': [{'id': user.id, 'name': user.name} for user in self.users],
                        'parents': [{'id': role.id, 'name': role.name} for role in self.parents],
                        'children': [{'id': role.id, 'name': role.name} for role in self.children],
                        'incompatible_roles': [{'id': role.id, 'name': role.name} for role in set().union(
                            self.incompatible_roles, self.roles_restricted_by_this_role
                        )]}

        class RoleHierarchy(self.base):
            __tablename__ = 'role_role_hierarchy'

            parent_id = Column(Integer, ForeignKey(Role.id), primary_key=True)

            child_id = Column(Integer, ForeignKey(Role.id), primary_key=True)

        class RoleRestriction(self.base):
            __tablename__ = 'role_role_restriction'

            role_id = Column(Integer, ForeignKey(Role.id), primary_key=True)

            incompat_role_id = Column(Integer, ForeignKey(Role.id), primary_key=True)

        class UserRole(self.base):
            __tablename__ = 'user_role'

            user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
            user = relationship('User', backref=backref('user_role', passive_deletes='all'))

            role_id = Column(Integer, ForeignKey(Role.id), primary_key=True)
            role = relationship('Role', backref=backref('user_role', passive_deletes='all'))

        class UnitPermission(self.base):
            __tablename__ = 'unit_permission'

            unit_id = Column(Integer, ForeignKey(Unit.id), primary_key=True)
            unit = relationship('Unit', backref=backref('unit_permission', passive_deletes='all'))

            permission_id = Column(Integer, ForeignKey(Permission.id), primary_key=True)
            permission = relationship('Permission', backref=backref('unit_permission', passive_deletes='all'))

        class RolePermission(self.base):
            __tablename__ = 'role_permission'

            role_id = Column(Integer, ForeignKey(Role.id), primary_key=True)
            role = relationship('Role', backref=backref('role_permission', passive_deletes='all'))

            permission_id = Column(Integer, ForeignKey(Permission.id), primary_key=True)
            permission = relationship('Permission', backref=backref('role_permission', passive_deletes='all'))

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
        #: Role-Role many-to-many hierarchy relationship class (association object)
        self.RoleHierarchy = RoleHierarchy
        #: Role-Role incompatible roles relationship class (association object)
        self.RoleRestriction = RoleRestriction
