import flask_dynrbac as fd
from flask_dynrbac.testing_domain_model import *


def test_init_with_testing_models(flask_app_with_db):
    """Should init with testing domain model properly"""
    app, db = flask_app_with_db

    rbac = fd.DynRBAC(session=db.session, user_id_provider=lambda: 1,
                      role_class=Role, permission_class=Permission,
                      user_class=User, unit_class=Unit)
    rbac.init_app(app)

    assert rbac is not None
