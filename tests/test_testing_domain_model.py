import flask_dynrbac as fd
from flask_dynrbac.testing_domain_model import *


def test_init_with_testing_models(app):
    """Should init with testing domain model properly"""

    rbac = fd.DynRBAC(app, role_class=Role, permission_class=Permission,
                      user_class=User, unit_class=Unit)
    rbac.init_app(app)

    assert rbac is not None
