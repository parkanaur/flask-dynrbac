import flask_dynrbac as fd


def test_no_restrictions(inited_app):
    """Should allow requests with no rules on unit"""
    app, db, rbac = inited_app

    @app.route('/')
    @rbac.rbac(unit_name='test1')
    def hello_world():
        return 'Hello World!'

    with app.test_client() as client:
        with app.app_context():
            a = client.get('/')
            assert b'Hello World!' in a.data


