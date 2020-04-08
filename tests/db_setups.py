import pytest


@pytest.fixture
def sample_filled_app(app, db, rbac, dmg):

    roles = [
        dmg.Role(name='role1'),
        dmg.Role(name='role2'),
        dmg.Role(name='role3'),
        dmg.Role(name='role4'),
        dmg.Role(name='admin')
    ]
    users = [
        dmg.User(name='user1_role1'),
        dmg.User(name='user2_role1'),
        dmg.User(name='user1_role2'),
        dmg.User(name='user1_roles12'),
        dmg.User(name='user1_role3'),
        dmg.User(name='user2_role3'),
        dmg.User(name='user3_role3'),
        dmg.User(name='user1_roles123'),
        dmg.User(name='user1_role4'),
        dmg.User(name='user1_admin')
    ]
    permissions = [
        dmg.Permission(name='can_r1'),
        dmg.Permission(name='can_r2'),
        dmg.Permission(name='can_r3'),
        dmg.Permission(name='can_r4'),
        dmg.Permission(name='can_admin')
    ]

    roles[0].users.extend((users[0], users[1], users[3], users[4], users[-3]))
    roles[0].permissions.append(permissions[0])
    roles[1].users.extend((users[2], users[3], users[-3]))
    roles[1].permissions.append(permissions[1])
    roles[2].users.extend(users[4:8])
    roles[2].permissions.append(permissions[2])
    roles[3].users.append(users[-2])
    roles[3].permissions.append(permissions[3])
    roles[4].users.append(users[-1])
    roles[4].permissions.append(permissions[4])

    db.session.add(roles[0])
    db.session.add(roles[1])
    db.session.add(roles[2])
    db.session.add(roles[3])
    db.session.add(roles[4])

    db.session.commit()

    return app, db, rbac



