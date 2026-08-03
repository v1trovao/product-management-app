import os
from dotenv import load_dotenv
import random, string 

load_dotenv()

class Config(object):

    # Habilita criptografia
    CSRF_ENABLED = os.getenv('CSRF_ENABLED')
    SECRET = os.getenv('SECRET')
    
    # Diretórios 
    TEMPLATE_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    
    # Instâncias
    APP = None
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

# Subclasses
# Testing: habilita testes, warnings e erros visíveis
# Debug: Habilita o log exibido no terminal
# Ip Host: IP da máquina
# Port Host: A porta executando
# URL_Main: IP+Porta

class DevelopmentConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = 'localhost'
    PORT_HOST = 8000
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    IP_HOST = 'localhost' # Aqui geralmente é um IP de um servidor na nuvem e não o endereço da máquina local
    PORT_HOST = 5000
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)


class ProductionConfig(Config):
    TESTING = False
    DEBUG = False
    IP_HOST = 'localhost' # Aqui geralmente é um IP de um servidor na nuvem e não o endereço da máquina local
    PORT_HOST = 8080
    URL_MAIN = 'http://%s:%s/' % (IP_HOST, PORT_HOST)

# Dicionário dos ambientes disponíveis
app_config = {
'development': DevelopmentConfig(),
'testing': TestingConfig(),
'production': ProductionConfig()
}

# Recebe a variável de ambiente para definir a config.
app_active = os.getenv('FLASK_ENV', 'development') 

# Dados pré-definidos no contexto do app
default_roles = ['Admin', 'Gerente', 'Lojista', 'Cliente']
default_admin = {
    'username': 'admin',
    'email': 'admin@gmail.com',
    'password': '123'
}
