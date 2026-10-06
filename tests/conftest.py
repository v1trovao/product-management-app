import pytest, jwt
from app import create_app, config, db
from app.config import app_config, app_active
from app.controller.User import UserController
from app.controller.Setup import SetupController

config = app_config[app_active]

@pytest.fixture(scope="session")
def app():
    DATABASE_TEST_URL = "sqlite://"

    config.APP = create_app(app_active)
    app = config.APP

    app.config.update({
        "SQLALCHEMY_DATABASE_URI": DATABASE_TEST_URL
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture()
def db_session(app):
    """Limpa os dados das tabelas após cada teste individual"""
    with app.app_context():

        db.create_all()
        '''# inicia conexão
        connection = db.engine.connect()
        transaction = connection.begin()

        # estabelece sessão SQLAclhemy
        options = dict(bind=connection, binds={})
        session = db._make_scoped_session(options=options)
        db_session = session'''

        # executa setup
        setup = SetupController()
        setup.create_default_roles()
        db.session.commit()

        yield db.session

        # Depois de finalizar teste, reseta para o estado inicial do banco
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def auth_headers(app):
    with app.app_context():
        user = UserController()
        token = user.generate_auth_token({"id": 99, "username": "admin"})
        return {"Authorization": f"Bearer {token}"}
        


    


    