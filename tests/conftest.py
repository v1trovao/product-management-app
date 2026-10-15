import pytest, jwt
from datetime import datetime

from app import create_app, db
from app.config import app_config, app_active
from app.controller.User import UserController
from app.controller.Setup import SetupController

config = app_config["testing"]

NOW = datetime(2026, 9, 27, 19, 26, 0)

@pytest.fixture(scope="session")
def app():
    DATABASE_TEST_URL = "sqlite://"

    config.SQLALCHEMY_DATABASE_URI = DATABASE_TEST_URL
    config.APP = create_app("testing", config)
    app = config.APP

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture()
def db_session(app):
    """Limpa os dados das tabelas após cada teste individual"""
    with app.app_context():

        db.create_all()

        # executa setup
        setup = SetupController()
        setup.create_default_roles()
        setup.create_default_admin()
        db.session.commit()

        yield db.session

        # Depois de finalizar teste, reseta para o estado inicial do banco
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def now():
    return NOW;

def auth_headers(app):
    with app.app_context():
        user = UserController()
        token = user.generate_auth_token({"id": 99, "username": "admin"})
        return {"Authorization": f"Bearer {token}"}
        