# -*- coding: utf-8 -*-
import os

# flask e app (rotas, db, etc...)
from flask import Flask, request, redirect, render_template, Response, json, abort
from sqlalchemy import inspect
from app.config import app_config, app_active
from app.extensions import db, migrate, login_manager

# login/autenticação
from flask_login import login_user, logout_user
from functools import wraps

# admin
from admin.Admin import start_views
from flask_bootstrap import Bootstrap

# controllers
from app.controller.Setup import SetupController
from app.controller.User import UserController
from app.controller.Product import ProductController

# Instância da configuração
config = app_config[app_active]


# Função que inicializa a aplicação flask com as configs
def create_app(config_name='development'):
    app = Flask(__name__, template_folder='templates')

    login_manager.init_app(app)

    app.secret_key = config.SECRET
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    caminho_absoluto = os.path.abspath(os.path.join(app.root_path, app.template_folder)) # type: ignore
    print(f"Template configurado em: {caminho_absoluto}")
    print(f"Pasta existe fisicamente? {os.path.exists(caminho_absoluto)}")
    print(f"Conteúdo da pasta: {os.listdir(caminho_absoluto) if os.path.exists(caminho_absoluto) else 'PASTA NÃO ENCONTRADA'}")
    print("----------------------------\n")
    print("Ambiente configurado: ", os.getenv('FLASK_ENV'))

    # Banco de Dados
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Bootstrap(app)
    start_views(app, db)
    db.init_app(app)
    migrate.init_app(app, db)

    # Autorização de requisições a API
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    def auth_token_required(f):
        @wraps(f)
        def verify_token(*args, **kwargs):
            user = UserController()
            try:
                print("Tentando verificar um token...")
                print(request.headers)
                result = user.verify_auth_token(request.headers['access_token'])
                if result['status'] == 200:
                    return f(*args, **kwargs)
                else:
                    abort(result['status'], result['message'])
            except KeyError as e:
                abort(401, 'Você precisa enviar um token de acesso!')

        return verify_token

    """ROTAS"""

    @app.route('/')
    def index():
        inspector = inspect(db.engine)
        setup = SetupController()

        print(inspector.get_table_names())
        if not inspector.get_table_names():
            return "Erro: O banco ainda não foi migrado. Rode o flask db upgrade", 500

        if not setup.check_admin():

            setup.create_default_roles()
            setup.create_default_admin()

        return redirect('/login')
    
    """LOGIN"""
    # Rota que acessa a página de login
    @app.route('/login/')
    def login():
        return render_template('login.html', data={'status': 200, 'msg': None, 'type': None})

    # Código de mensagens
    # type 1 - alerta de erro
    # type 2 - chamada de atenção
    # type 3 - informação
    
    # Rota que efetua o processo de login
    @app.route('/login/', methods=['POST']) # type: ignore
    def login_post():
        user = UserController()

        email = request.form['email']
        password = request.form['password']

        # Obtem o usuário associado ao email e senha fornecidos
        #print(f"Dados fornecidos - Email: {email}, Senha: {password}")
        result = user.login(email, password)

        if result:
            # Verificação do tipo de usuário que fez login

            # Caso de usuários clientes (tipo 4)
            if result.role == 4:
                return render_template('login.html', 
                                       data={'status': 401, 
                                             'msg': 'Seu usuário não tem permissão '
                                             'para acessar o admin', 
                                             'type': 2})

            # Demais tipos de usuário tem acesso a página do admin
            else:
                print("Dados validados. Efetuando login de usuário...")
                login_user(result)
                return redirect('/admin')

        # Caso de usuário inválido
        else:
            return render_template('login.html', data={'status': 401, 'msg':
        'Dados de usuário incorretos', 'type': 1})

    """RECUPERAÇÃO DE SENHA"""
    @app.route('/recovery-password/')
    def recovery_password():
        """Acessa a página de recuperação de senha"""
        return render_template('recovery.html', data={'status': 200, 'msg': None, 'type': None})
    
    @app.route('/recovery-password/', methods=['POST'])
    def send_recovery_password():
        """Envia o email para recuperação de senha"""
        user = UserController()
        result = user.recovery(request.form['email'])

        if result['status_code'] == 200 or result['status_code'] == 202:
            return render_template('recovery.html', data={'status': 200, 'msg':
            'E-mail de recuperação enviado com sucesso', 'type': 3})
        else:
            return render_template('recovery.html', data={'status': 401, 'msg':
            'Erro ao enviar e-mail de recuperação', 'type': 1})

    @app.route('/new-password/<recovery_code>')
    def new_password(recovery_code):
        """Faz a validação do código de recuperação""" 
        user = UserController()
        result = user.verify_auth_token(recovery_code)

        if result['status'] == 200:
            res = user.get_user_by_recovery(str(recovery_code))

            if res is not None:
                return render_template('new_password.html', data={'status':
                result['status'], 'msg': None, 'type': None, 'user_id': res.id})
            else:
                return render_template('recovery.html', data={'status': 400, 
                                                              'msg': 'Erro ao acessar dados do usuário. Tente novamente.', 'type': 1})
        else:
            return render_template('recovery.html', data={'status': 
                                                          result['status'], 'msg': 'Token expirado ou inválido, faça a solicitação novamente', 'type': 1})

    @app.route('/new-password/', methods=['POST'])
    def send_new_password():
        """Acessa a página de alteração de senha"""
        user = UserController()
        user_id = request.form['user_id']
        password = request.form['password']

        result = user.new_password(user_id, password)

        if result:
            return render_template('login.html', data={'status': 200, 'msg':
                                                       'Senha alterada com sucesso!', 'type': 3, 'user_id': user_id})
        else:
            return render_template('new_password.html', data={'status': 401, 
                                                              'msg': 'Erro ao alterar senha.', 'type': 1, 'user_id': user_id})

    
    """USUÁRIO"""
    @app.route('/profile/<int:id>')
    def profile(id):
        return f'O ID desse usuário é {id}'
    
    @app.route('/profile/<int:id>/action/<action>/') # type: ignore
    def profile1(id, action):
        if action == 'action1':
            return 'Ação action1 usuário de ID %d' % id
        elif action == 'action2':
            return 'Ação action2 usuário de ID %d' % id
        elif action == 'action3':
            return 'Ação action3 usuário de ID %d' % id
    
    @app.route('/profile', methods=['POST'])
    def create_profile():
        username = request.form['username']
        password = request.form['password']

        return f'Essa rota possui um método POST e criará um usuário com os dados de usuário {username} e senha {password}'
    
    @app.route('/profile/<int:id>', methods=['PUT'])
    def edit_total_profile(id):
        username = request.form['username']
        password = request.form['password']
        return f'Essa rota possui um método PUT e editará o nome do usuário para {username} e a senha para {password}'
    
    """PRODUTO"""
    # Cadastrar produto
    @app.route('/product', methods=['POST'])
    def save_products():
        product = ProductController()
        print(request.form)
        result = product.save_product(request.form)
        print(result)

        if result:
            message = 'Inserido'
        else:
            message = 'Não insere'
        
        return message

    # Editar produto
    @app.route('/product', methods=['PUT'])
    def update_products():
        product = ProductController()

        result = product.update_product(request.form)

        if result:
            message = 'Editei'
        else:
            message = 'Não foi'
        
        return message

    # Deletar produto
    @app.route('/product', methods=['DELETE'])
    def delete_products():
        product = ProductController()

        result = product.delete_product(request.form)

        if result:
            message = 'Editei'
        else:
            message = 'Não foi'
        
        return message

    @app.route('/product', methods=['GET'])    
    def get_products_test():
        product = ProductController()

        result = product.get_products(request.form)
        if result:
            message = result
        else:
            message = 'Não existe'

        return message
    
    @app.route('/products', methods=['GET'])
    @app.route('/products/<limit>', methods=['GET'])
    @auth_token_required
    def get_products(limit=None):
        header = {
            'access-token': request.headers['access-token'],
            'token-type': 'JWT'
        }
        product = ProductController()
        response = product.get_products(limit=limit)
        return Response(json.dumps(response, ensure_ascii=False), 
                        mimetype='application/json'), response['status'], header

    @app.route('/product/<product_id>', methods=['GET'])
    @auth_token_required
    def get_product(product_id):
        header = {
            'access-token': request.headers['access-token'],
            'token-type': 'JWT'
        }

        product = ProductController()
        response = product.get_product_by_id(product_id=product_id)
        return Response(json.dumps(response, ensure_ascii=False),
                        mimetype='application/json'), response['status'], header

    @app.route('/user/<user_id>', methods=['GET'])
    @auth_token_required
    def get_user_profile(user_id):
        header = {
            'access-token': request.headers['access-token'],
            'token-type': 'JWT'
        }

        user = UserController()
        response = user.get_user_by_id(user_id=user_id)

        return Response(json.dumps(response, ensure_ascii=False), 
                        mimetype='application/json'), response['status'], header
    
    ''' Sobre o Response(json, mimetype, status, header)
    Resposta do servidor ao cliente
        json: o corpo da resposta
          -> json.dumps(), converte um dado no formato JSON
        mimetype: formato do arquivo enviado
        status: codigo HTTP
        header: o cabeçalho, com conteúdo de tokens e segurança
    '''

    @app.route('/login-api/', methods=['POST'])
    def login_api():
        header = {}
        user = UserController()

        email = request.json['email']
        password = request.json['password']

        result = user.login(email, password)
        code = 401
        response = {'message': 'Usuário não autorizado', 'result': []}

        if result:
            if result.active:
                result = {
                    'id': result.id,
                    'username': result.username, 
                    'email': result.email,
                    'date_created': result.date_created,
                    'active': result.active
                }

                header = {
                    'access-token': user.generate_auth_token(result),
                    'token-type': 'JWT'
                }
                code = 200
                response['message'] = 'Login realizado com sucesso!'
                response['result'] = result
        print(header)

        return Response(json.dumps(response, ensure_ascii=False), 
                        mimetype='application/json'), code, header

    @app.route('/logout')
    def logout_send():
        print("Processando logout do usuário...")
        logout_user() # chama a função do flask-login
        return render_template('login.html', data={'status': 200, 'msg': 'Usuário deslogado com sucesso!', 'type': 3})


    # Função auxiliar do flask-login para verificar se o usuário existe no banco
    @login_manager.user_loader
    def load_user(user_id):
        print("Carregando dados do usuário...")
        user = UserController()
        return user.get_admin_login(user_id)
    
    return app