# -*- coding: utf-8 -*-
import os
from typing import Any

from markupsafe import Markup

from flask import redirect

# Visão do admin
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from app.config import app_config, app_active


from app.model.User import User
from app.model.Category import Category
from app.model.Product import Product
from app.model.Role import Role
from flask_login import current_user

config = app_config[app_active]

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'app', 'templates')

class HomeView(AdminIndexView):

    extra_css = [config.URL_MAIN + 'static/css/home.css', 
                 'https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css']
   
    @expose('/')
    def index(self):
        print("Carregando /admin...")
        # Instanciando os modelos para cada tabela
        user_model = User()
        category_model = Category()
        product_model = Product()

        # Obtendo o total de cada tabela a partir dos métodos
        users = user_model.get_total_users()
        categories = category_model.get_total_category()
        products = product_model.get_total_product()
        last_products = product_model.get_last_products()

        #print(users)
        #print(last_products)
        #print("Testando carregando da view base")
        
        # Passando o argumento report, como um dicionário contendo os valores de cada tabela
        return self.render('home_admin.html', data={
            'username': current_user.username,
        }, report={
            'users': 0 if not users else users[0],
            'categories': 0 if not categories else categories[0],
            'products': 0 if not products else products[0]
        }, last_products=last_products)

    # Função que verifica o nível de acesso do usuário
    def is_accessible(self):
        #print("Verificando se user tem acesso (Admin)")
        #print(current_user.is_authenticated)
        return current_user.is_authenticated

    # Função que trata acessos não autorizados
    def inaccessible_callback(self, name, **kwargs) -> Any:
        print("Callback de error")
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')


        


class UserView(ModelView):
    column_exclude_list = ['password', 'recovery_code']
    form_excluded_columns = ['last_update', 'recovery_code']
    form_widget_args = {
        'password': {
        'type': 'password'
        }
    }
    
    can_set_page_size = True
    can_view_details = True
    column_searchable_list = ['username', 'email']
    column_filters = ['username', 'email', 'funcao']
    '''column_editable_list = ['username', 'funcao', 'email', 'active']'''
    create_modal = True
    
    edit_modal = True
    can_export = True
    
    column_sortable_list = ['username']
    column_default_sort = ('username', True)
    column_details_exclude_list = ['password', 'recovery_code']
    column_export_exclude_list = ['password', 'recovery_code']

    # Só funciona CSV
    export_types = ['json', 'yaml', 'csv', 'xls', 'df']

    column_labels = {
        'funcao': 'Função',
        'username': 'Nome de usuário',
        'email': 'E-mail',
        'date_created': 'Data de criação',
        'last_update': 'Última atualização',
        'active': 'Ativo',
        'password': 'Senha',
    }

    column_descriptions = {
        'funcao': 'Função no painel administrativo',
        'username': 'Nome de usuário no sistema',
        'email': 'E-mail do usuário no sistema',
        'date_created': 'Data de criação do usuário no sistema',
        'last_update': 'Última atualização desse usuário no sistema',
        'active': 'Estado ativo ou inativo no sistema',
        'password': 'Senha do usuário no sistema',
    }
    
    def on_model_change(self, form, User, is_created):
        print("Mudou...")
        if 'password' in form:
            if form.password.data is not None:
                User.set_password(form.password.data)
        else:
            del form.password

    def is_accessible(self):
        print("Verificando se usuário tem acesso (Página de Users)")

        if current_user.is_authenticated:
            role = current_user.role
            print("Papel do user: ", role)
            print(current_user.funcao)
            if role == 1:
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        print("Acessando o callback...")
        if current_user.is_authenticated:
            print("Liberando acesso...")
            return redirect('/admin')
        else:
            print("Acho que não...")
            return redirect('/login')

def image_formatter(view, context, model, name):
        url_image = getattr(model, name)
        if url_image:
            return Markup(f'<img src="{url_image}" width="80">')
        return 'Image'

class ProductView(ModelView):
    
    column_formatters = {
        'image': image_formatter
    }

class RoleView(ModelView):
    def is_accessible(self):
        print("Verificando se usuário tem acesso (Página de Roles)")

        if current_user.is_authenticated:
            role = current_user.role

            if role == 1:
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                return current_user.is_authenticated
            
    def inaccessible_callback(self, name: Any, **kwargs: Any) -> Any:
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')

class CategoryView(ModelView):
    def is_accessible(self):
        print("Verificando se usuário tem acesso (Página de Categories)")
        if current_user.is_authenticated:
            role = current_user.role

            if role == 1:
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                return current_user.is_authenticated
            """PAREI AQUI"""

    
    def inaccessible_callback(self, name: Any, **kwargs: Any) -> Any:
        if current_user.is_authenticated:
            return redirect('/admin')
        else:
            return redirect('/login')

