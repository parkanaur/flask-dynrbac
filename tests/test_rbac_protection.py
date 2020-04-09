import flask_dynrbac as fd


def _send_request(app, url, method='get'):
    with app.test_client() as client:
        with app.app_context():
            return getattr(client, method)(url)


def test_no_restrictions(sample_filled_app):
    """Should allow requests with no rules on unit"""
    app, db, rbac, dmg = sample_filled_app

    @app.route('/')
    @rbac.rbac(unit_name='test1')
    def hello_world():
        return 'Hello World!'

    r = _send_request(app, '/')
    assert r.status_code == 200
    assert b'Hello World!' in r.data


def test_role_1(sample_filled_app):
    """Should only allow requests from users with role 1"""
    app, db, rbac, dmg = sample_filled_app

    current_user_id = None
    rbac.user_id_provider = lambda: current_user_id
    users_r1_ids = [1, 2, 4, 8]
    users_other_ids = [3, 5, 6, 7, 9, 10]

    @app.route('/')
    @rbac.rbac(unit_name='test1')
    def hello_world():
        return 'Hello World!'

    for i in users_r1_ids:
        current_user_id = i
        r = _send_request(app, '/')
        assert r.status_code == 200
        assert b'Hello World!' in r.data

    for i in users_other_ids:
        current_user_id = i
        r = _send_request(app, '/')
        assert r.status_code == rbac.global_error_code
