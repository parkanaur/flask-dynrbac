from flask_dynrbac.testing_domain_model import *


def test_addition(session):
    """Should add entities to db"""
    user = User()
    session.add(user)
    session.commit()

    print(user.id)
