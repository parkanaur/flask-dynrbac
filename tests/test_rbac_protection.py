import flask_dynrbac as fd


def test_no_restrictions(inited_app):
    app, db, rbac = inited_app

    @app.route('/')
    @rbac.rbac(unit_name='test1')
    def hello_world():
        return 'Hello World!'


