from helpers import send_and_assert, send_request


def test_get_list(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    roles = send_request(app, api_url + '/roles').get_json()
    assert len(roles) == 5
    for role in roles:
        assert 'name' in role
        assert 'id' in role
        assert len(role['permissions']) >= 1
        assert len(role['children']) >= 0
        assert len(role['parents']) >= 0
        assert len(role['incompatible_roles']) >= 0
        assert len(role['users']) >= 1


def test_get_role(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/roles/1')
    assert r.status_code == 200, 'GOT ' + str(r.status_code)
    role = r.get_json()
    assert 'name' in role
    assert 'id' in role
    assert role['id'] == 1
    assert len(role['permissions']) >= 1
    assert len(role['children']) >= 0
    assert len(role['parents']) >= 0
    assert len(role['incompatible_roles']) >= 0
    assert len(role['users']) >= 1


def test_put_role(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/roles/1', method='put', json={
        'name': 'role_new_1',
        'update_permissions': True,
        'permission_ids': [1, 2, 3, 4],
        'update_users': True,
        'user_ids': [1, 2],
        'update_parents': True,
        'parent_ids': [2, 3],
        'update_children': True,
        'child_ids': [4],
        'update_incompatible': True,
        'incompatible_ids': [5]
    })
    assert r.status_code == 204, 'GOT ' + str(r.status_code) + ' ' + r.data

    # Test general
    r = send_request(app, api_url + '/roles/1')
    assert r.status_code == 200, 'GOT ' + str(r.status_code)
    role = r.get_json()
    assert role['name'] == 'role_new_1'
    assert role['id'] == 1
    assert len(role['users']) == 2
    for user in role['users']:
        assert user['id'] in [1, 2]
    assert len(role['permissions']) == 4
    for perm in role['permissions']:
        assert perm['id'] in [1, 2, 3, 4]
    assert len(role['parents']) == 2
    for r in role['parents']:
        assert r['id'] in [2, 3]
    assert len(role['children']) == 1 and role['children'][0]['id'] == 4
    assert len(role['incompatible_roles']) == 1 and role['incompatible_roles'][0]['id'] == 5

    # Test incompatible roles
    incompat_role = send_request(app, api_url + '/roles/5').get_json()
    assert incompat_role['incompatible_roles'][0]['id'] == 1

    # Test parent roles
    r2 = send_request(app, api_url + '/roles/2').get_json()
    assert r2['children'][0]['id'] == 1
    r3 = send_request(app, api_url + '/roles/3').get_json()
    assert r3['children'][0]['id'] == 1

    # Test child roles
    r4 = send_request(app, api_url + '/roles/4').get_json()
    assert r4['parents'][0]['id'] == 1


def test_create_role(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/roles', method='post', json={
        'name': 'new_role_create',
        'permission_ids': [1, 2, 3, 4],
        'parent_ids': [1, 2],
        'child_ids': [3, 4],
        'incompatible_ids': [5],
        'user_ids': [1, 3, 4]
    })
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    rid = r.get_json()['id']

    r = send_request(app, api_url + '/roles/' + str(rid))
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    role = r.get_json()
    assert role['name'] == 'new_role_create'
    assert role['id'] == rid
    assert len(role['permissions']) == 4
    assert len(role['users']) == 3
    assert len(role['parents']) == 2
    assert len(role['children']) == 2
    assert len(role['incompatible_roles']) == 1

    # Test incompatible roles
    incompat_role = send_request(app, api_url + '/roles/5').get_json()
    assert incompat_role['incompatible_roles'][0]['id'] == rid

    # Test parent roles
    r1 = send_request(app, api_url + '/roles/1').get_json()
    assert r1['children'][0]['id'] == rid
    r2 = send_request(app, api_url + '/roles/2').get_json()
    assert r2['children'][0]['id'] == rid

    # Test child roles
    r4 = send_request(app, api_url + '/roles/4').get_json()
    assert r4['parents'][0]['id'] == rid
    r3 = send_request(app, api_url + '/roles/3').get_json()
    assert r3['parents'][0]['id'] == rid


def test_create_empty_role(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/roles', method='post', json={
        'name': 'new_role_create_empty'
    })
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    rid = r.get_json()['id']

    r = send_request(app, api_url + '/roles/' + str(rid))
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    role = r.get_json()
    assert role['name'] == 'new_role_create_empty'
    assert role['id'] == rid
