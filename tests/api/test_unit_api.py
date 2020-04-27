from helpers import send_and_assert, send_request


def test_get_list(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    units = send_request(app, api_url + '/units').get_json()
    assert len(units) == 5
    for unit in units:
        assert 'name' in unit
        assert 'id' in unit
        assert 'permissions' in unit
        assert len(unit['permissions']) >= 1


def test_get_unit(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/units/1')
    assert r.status_code == 200, 'GOT ' + str(r.status_code)
    unit = r.get_json()
    assert 'name' in unit
    assert 'id' in unit
    assert unit['id'] == 1
    assert 'permissions' in unit
    assert len(unit['permissions']) >= 1


def test_put_unit(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/units/1', method='put', json={
        'name': 'unit_new_1',
        'update_permissions': True,
        'permission_ids': [1, 2, 3, 4],
        'perms_all_required': True
    })
    assert r.status_code == 204, 'GOT ' + str(r.status_code) + ' ' + r.data

    r = send_request(app, api_url + '/units/1')
    assert r.status_code == 200, 'GOT ' + str(r.status_code)
    unit = r.get_json()
    assert unit['name'] == 'unit_new_1'
    assert unit['perms_all_required'] == True
    for perm in unit['permissions']:
        assert perm['id'] in [1, 2, 3, 4]

    r = send_request(app, api_url + '/units/1', method='put', json={
        'permission_ids': [1]
    })

    r = send_request(app, api_url + '/units/1')
    unit = r.get_json()
    assert unit['name'] == 'unit_new_1'
    assert unit['perms_all_required'] == True
    assert len(unit['permissions']) == 4
    for perm in unit['permissions']:
        assert perm['id'] in [1, 2, 3, 4]

    r = send_request(app, api_url + '/units/1', method='put', json={
        'update_permissions': True,
        'permission_ids': [1, 4],
        'perms_all_required': False
    })

    r = send_request(app, api_url + '/units/1')
    unit = r.get_json()
    assert len(unit['permissions']) == 2
    assert unit['perms_all_required'] == False
    for perm in unit['permissions']:
        assert perm['id'] in [1, 4]


def test_delete_unit(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/units/1', method='delete')
    assert r.status_code == 204, 'GOT ' + str(r.status_code) + ' ' + r.data

    r = send_request(app, api_url + '/units/1')
    assert r.status_code == 404, 'GOT ' + str(r.status_code) + ' ' + r.data


def test_create_unit(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/units', method='post', json={
        'name': 'new_unit_create',
        'permission_ids': [1, 2, 3]
    })
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    uid = r.get_json()['id']

    r = send_request(app, api_url + '/units/' + str(uid))
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    unit = r.get_json()
    assert unit['name'] == 'new_unit_create'
    assert unit['id'] == uid
    assert len(unit['permissions']) == 3


def test_create_unit_empty_permissions(sample_filled_app, api_url):
    app, db, rbac, dmg = sample_filled_app

    r = send_request(app, api_url + '/units', method='post', json={
        'name': 'new_unit_create_empty'
    })
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    uid = r.get_json()['id']

    r = send_request(app, api_url + '/units/' + str(uid))
    assert r.status_code == 200, 'GOT ' + str(r.status_code) + ' ' + r.data
    unit = r.get_json()
    assert unit['name'] == 'new_unit_create_empty'
    assert unit['id'] == uid
    assert len(unit['permissions']) == 0
