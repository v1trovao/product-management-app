from app.model.User import User
from app.model.Role import Role
from app.model.Product import Product
from app.model.Category import Category

from app.controller.Product import ProductController
from app.controller.User import UserController

from faker import Faker
from datetime import datetime

import random, json

from app.config import default_roles

fake = Faker('pt-Br')
NOW = datetime.now()

role_model = Role()
user_model = User()
product_model = Product()
category_model = Category()

_users = [
    {
        "username": "João Vitor Cunha",
        "email": "nicolas80@outlook.com",
        "password": "123",
        "role": 1
    },
    {
        "username": "Heloisa Andrade",
        "email": "emilly98@hotmail.com",
        "password": "123",
        "role": 1
    },
    {
        "username": "Benício Souza",
        "email": "pereiraluiza@live.com",
        "password": "123",
        "role": 1
    },
    {
        "username": "Renato Aragão",
        "email": "fernando92@gmail.com",
        "password": "123",
        "role": 1
    }
]

_categories = [
    {
        "name": "Eletrônicos", 
        "description": "Celulares, notebooks e acessórios"
    },
    {
        "name": "Bebidas",
        "description": "Todo líquido industrializado ou natural para consumo"
    },
    {
        "name": "Limpeza",
        "description": "Produtos destinados a limpeza em residências e ambiente no geral"
    }
]

images_sample = "https://picsum.photos"

def run_seed():

    # Creating categories
    for data in _categories:
        category_model.name = data['name']

        category_exist = category_model.get_category_by_name()

        if not category_exist:
            # print(f"Adicionando {category_model.name}...")

            new_category = Category()
            new_category.name = data['name']
            new_category.description = data['description']

            new_category.save()

        # Verificar as categorias existentes no banco
        # categories = category_model.get_all_categories()
        # print(categories)

    # Creating Users
    for user in _users:
        # user = fake.profile()
        user_model.username = user['username']
        user_exist = user_model.get_user_by_name()

        if not user_exist:
            user_data = {   
                            #"username": user['name'],
                            "username": user['username'],
                            #"email": user['mail'],
                            "email": user['email'],
                            "password": user['password'],
                            "role": role_model.get_role_id_by_name(random.choice(default_roles))
                        }
            
            new_user = UserController()
            new_user.save_user(user_data)
            _users.append(user_data)  

    # Creating Products
    for _ in range(5):
        product_model.name = str.join(" ", fake.words(nb=2))
        
        product_exist = product_model.get_product_by_name()

        if not product_exist:
            user_model.username = random.choice(_users)['username']
            category_model.name = random.choice(_categories)['name']

            new_product = ProductController()

            product_data = {
                "name": product_model.name,
                "description": fake.paragraph(nb_sentences=2),
                "qtd": random.randint(0, 50),
                "image": f"{images_sample}/id/{random.randint(1, 500)}/200",
                "price": round(random.uniform(5.0, 500.0), 2),
                "date_created": NOW,
                "last_update": NOW,
                "category": category_model.get_category_by_name().id,
                "user_created": user_model.get_user_by_name().id,
            }

            new_product.save_product(product_data)