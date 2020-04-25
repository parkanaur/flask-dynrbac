import flask_dynrbac as fd


def _send_request(app, url, method='get'):
    with app.test_client() as client:
        with app.app_context():
            return getattr(client, method)(url)


def test_no_restrictions(sample_filled_app):
    """Should allow requests with no rules on unit"""
    app, db, rbac, dmg = sample_filled_app

    r = _send_request(app, '/')
    assert r.status_code == 200
    assert b'Hello World!' in r.data


def test_role_1(sample_filled_app):
    """Should only allow requests from users with role 1"""
    app, db, rbac, dmg = sample_filled_app

    current_user_id = None
    rbac.user_id_provider = lambda: current_user_id

    correct_users = set(map(lambda user: user.id, rbac._role_logic.get_all_users_for_role('role1')))
    users_r1_ids = {i for i in range(1, 11) if i in correct_users}
    users_other_ids = correct_users - users_r1_ids

    for i in users_r1_ids:
        current_user_id = i
        r = _send_request(app, '/')
        assert r.status_code == 200, 'Fail for user ' + str(current_user_id)
        assert b'Hello World!' in r.data

    for i in users_other_ids:
        current_user_id = i
        r = _send_request(app, '/')
        assert r.status_code == rbac.global_error_code


def test_all_access_to_admin(sample_filled_app):
    app, db, rbac, dmg = sample_filled_app

    rbac.user_id_provider = lambda: db.session.query(dmg.User).filter(dmg.User.name == 'user_admin').first().id

    for un_name in ['unit1', 'unit2', 'unit3', 'unit4', 'unit_admin']:
        r = _send_request(app, '/' + un_name)
        assert r.status_code == 200, 'Fail + ' + un_name + ' for admin user'
        assert b'Hello World!' in r.data
