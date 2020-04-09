def test_addition(session, dmg):
    """Should add entities to db"""
    user = dmg.User()
    session.add(user)
    session.commit()

    assert user.id == 1

    role = dmg.Role(name='test role')
    session.add(role)
    session.commit()

    assert role.id == 1


def test_autoincrement(session, dmg):
    """Should auto-increment primary key"""
    user1 = dmg.User()
    user2 = dmg.User()
    session.add(user1)
    session.add(user2)
    session.commit()

    assert user1.id == 1
    assert user2.id == 2


def test_user_role_relationship(session, dmg):
    """Should properly read/write user-role relationships"""
    user1 = dmg.User()
    user1.roles.append(dmg.Role(name='test role for user1'))

    session.add(user1)
    session.commit()

    db_user1 = session.query(dmg.User).filter(dmg.User.id == user1.id).first()
    assert db_user1 is not None
    assert db_user1.roles is not None
    assert db_user1.roles[0].name == 'test role for user1'

    role2 = dmg.Role(name='test role2')
    role2.users.append(user1)

    session.add(role2)
    session.commit()

    roles_for_user_1 = session.query(dmg.UserRole).filter(dmg.UserRole.user_id == user1.id).all()
    assert len(roles_for_user_1) == 2
    assert roles_for_user_1[0].role_id == 1 and roles_for_user_1[0].role.name == 'test role for user1'
    assert roles_for_user_1[1].role_id == 2 and roles_for_user_1[1].role.name == 'test role2'


def test_role_permission_relationship(session, dmg):
    """Should properly read/write role-permission relationships"""
    permission1 = dmg.Permission(name='can_access_p1')
    permission1.roles.append(dmg.Role(name='r1'))

    session.add(permission1)
    session.commit()

    db_permission1 = session.query(dmg.Permission).filter(dmg.Permission.id == permission1.id).first()
    assert db_permission1 is not None
    assert db_permission1.roles is not None
    assert db_permission1.roles[0].name == 'r1'

    role2 = dmg.Role(name='r2')
    role2.permissions.append(permission1)

    session.add(role2)
    session.commit()

    roles_for_perm1 = session.query(dmg.RolePermission).filter(dmg.RolePermission.permission_id == permission1.id).all()
    assert len(roles_for_perm1) == 2
    assert roles_for_perm1[0].role_id == 1 and roles_for_perm1[0].role.name == 'r1'
    assert roles_for_perm1[1].role_id == 2 and roles_for_perm1[1].role.name == 'r2'


def test_unit_permission_relationship(session, dmg):
    """Should properly read/write unit-permission relationships"""
    unit1 = dmg.Unit(name='u1')
    unit2 = dmg.Unit(name='u2')

    perm1 = dmg.Permission(name='can_access_u1_and_u2')

    perm1.units.extend((unit1, unit2))

    session.add(perm1)
    session.commit()

    db_permission1 = session.query(dmg.Permission).filter(dmg.Permission.id == perm1.id).first()
    assert db_permission1 is not None
    assert db_permission1.units is not None
    assert len(db_permission1.units) == 2


def test_full_relationships_and_deletes(session, dmg):
    """Should properly handle complex relationships, including deletes"""
    role1 = dmg.Role(name='r1')
    perm1 = dmg.Permission(name='p1')
    perm2 = dmg.Permission(name='p2')
    role1.permissions.extend((perm1, perm2))

    user1 = dmg.User(name='u1')
    user1.roles.append(role1)

    session.add(user1)
    session.commit()

    db_user1 = session.query(dmg.User).filter(dmg.User.id == user1.id).first()
    assert db_user1 is not None
    assert len(db_user1.roles) == 1
    assert len(db_user1.roles[0].permissions) == 2

