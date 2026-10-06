from app.model.Product import Product
from app.model.User import User
from app.model.Category import Category
from app.model.Role import Role

from app.controller.Product import ProductController
from datetime import datetime

def test_save_product_with_success(client, db_session):
    category_model = Category()
    user_model = User()

    # Arrange
    category_model.id = 99
    category_model.name = "Cereais"
    category_model.description = "Produtos do tipo cereais"
    db_session.add(category_model)
    db_session.commit()

    user_model.id = 99
    user_model.username = "admin"
    user_model.email = "Admin@gmail.com"
    user_model.password = "123"
    user_model.role = 1

    db_session.add(user_model)
    db_session.commit()

    product_valid = {
        "name": "Nescau Ball",
        "description": "Teste",
        "qtd": 2,
        "price": "50.00",
        "date_created": f"{datetime(2026, 9, 27, 19, 26, 0)}",
        "last_update": f"{datetime(2026, 9, 27, 19, 26, 0)}",
        "category": f"{category_model.id}",
        "user_created": user_model.id
    }

    # Act
    product = ProductController()
    result = product.save_product(product_valid)

    # Assert
    assert result['success'] == True

def test_save_product_without_name(client, db_session):
    
    # Arrange
    category_model = Category()
    user_model = User()

    category_model.id = 99
    category_model.name = "Cereais"
    category_model.description = "Produtos do tipo cereais"
    db_session.add(category_model)
    db_session.commit()

    user_model.id = 99
    user_model.username = "admin"
    user_model.email = "Admin@gmail.com"
    user_model.password = "123"
    user_model.role = 1
    db_session.add(user_model)
    db_session.commit()

    product_invalid = {
        "description": "Teste",
        "qtd": 2,
        "price": "50.00",
        "date_created": f"{datetime(2026, 9, 27, 19, 26, 0)}",
        "last_update": f"{datetime(2026, 9, 27, 19, 26, 0)}",
        "category": f"{category_model.id}",
        "user_created": user_model.id
    }

    # Act
    product_controller = ProductController()
    result = product_controller.save_product(product_invalid)

    # Assert
    assert result['message'] == "Field 'name' is missing..."

def test_save_product_with_existing_name(db_session):

    # Arrange
    category_model = Category()
    user_model = User()
    product_model = Product()

    category_model.id = 99
    category_model.name = "Cereais"
    category_model.description = "Produtos do tipo cereais"
    db_session.add(category_model)
    db_session.commit()

    user_model.id = 99
    user_model.username = "admin"
    user_model.email = "Admin@gmail.com"
    user_model.password = "123"
    user_model.role = 1
    db_session.add(user_model)
    db_session.commit()

    product_valid= {
        "name": "Nescau Ball",
        "description": "Teste",
        "qtd": 2,
        "price": "50.00",
        "date_created": f"{datetime(2026, 9, 27, 19, 26, 0)}",
        "last_update": f"{datetime(2026, 9, 27, 19, 26, 0)}",
        "category": f"{category_model.id}",
        "user_created": user_model.id
    }

    same_product = {
        "name": "Nescau Ball",
        "description": "Teste",
        "qtd": 2,
        "price": "50.00",
        "date_created": f"{datetime(2026, 9, 27, 19, 26, 0)}",
        "last_update": f"{datetime(2026, 9, 27, 19, 26, 0)}",
        "category": f"{category_model.id}",
        "user_created": user_model.id
    }

    first_product = ProductController()
    first_product.save_product(product_valid)

    # Act
    second_product = ProductController()
    result = second_product.save_product(same_product)

    expected = "duplicated"

    # Assert
    assert expected in result['message']