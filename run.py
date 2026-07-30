import sys, importlib
from app import create_app, config
from app.config import app_config, app_active

config = app_config[app_active]
config.APP = create_app(app_active)
app = config.APP 

'''
with app.app_context():
    # Ao importar aqui dentro, o SQLAlchemy amarra os metadados das models 
    # diretamente ao db que acabou de ser inicializado no create_app()
    from app.model import User, Product, Category, Role'''

# Roda o servidor da aplicação
if __name__ == '__main__':
    app.run(host=config.IP_HOST, port=config.PORT_HOST)
    importlib.reload(sys)