from helpers import send_and_assert, send_request


def test_get_list(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    permissions = send_request(app, api_url + '/permissions').get_json()
    assert len(permissions) == 5
    for perm in permissions:
        assert 'name' in perm
        assert 'id' in perm
        assert 'roles' in perm
        assert 'units' in perm
        assert len(perm['roles']) >= 1
        assert len(perm['units']) >= 1


def test_get_permission(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/permissions/1')
    assert r.status_code == 200, 'GOT ' + str(r.status_code)
    perm = r.get_json()
    assert 'name' in perm
    assert 'id' in perm
    assert perm['id'] == 1
    assert len(perm['roles']) >= 1
    assert len(perm['units']) >= 1


def test_put_permission(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/permissions/1', method='put', json={
        'name': 'permission_new_1',
        'update_roles': True,
        'role_ids': [1, 2, 3, 4]
    })
    assert r.status_code == 204, 'GOT ' + str(r.status_code) + ' ' + r.data

    r = send_request(app, api_url + '/permissions/1')
    assert r.status_code == 200, 'GOT ' + str(r.status_code)
    perm = r.get_json()
    assert perm['name'] == 'permission_new_1'
    assert len(perm['roles']) == 4
    for role in perm['roles']:
        assert role['id'] in [1, 2, 3, 4]

    r = send_request(app, api_url + '/roles/1')
    role = r.get_json()
    assert any(perm['id'] == 1 for perm in role['permissions'])


def test_delete_permission(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/permissions/1', method='delete')
    assert r.status_code == 204, 'GOT ' + str(r.status_code) + ' ' + r.data

    r = send_request(app, api_url + '/permissions/1')
    assert r.status_code == 404, 'GOT ' + str(r.status_code) + ' ' + r.data


def test_create_permission(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/permissions', method='post', json={
        'name': 'new_permission_create',
        'role_ids': [1, 2, 3],
        'unit_ids': [1, 2]
    })

    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    pid = r.get_json()['id']

    r = send_request(app, api_url + '/permissions/' + str(pid))
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    perm = r.get_json()
    assert perm['name'] == 'new_permission_create'
    assert perm['id'] == pid
    assert len(perm['roles']) == 3
    assert len(perm['units']) == 2


def test_create_empty_permission(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/permissions', method='post', json={
        'name': 'new_permission_create_empty'
    })
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    pid = r.get_json()['id']

    r = send_request(app, api_url + '/permissions/' + str(pid))
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    perm = r.get_json()
    assert perm['name'] == 'new_permission_create_empty'
    assert perm['id'] == pid
    assert len(perm['roles']) == 0
    assert len(perm['units']) == 0
