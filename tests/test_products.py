from app.model.Product import Product
from app.model.User import User
from app.model.Category import Category

from app.controller.Product import ProductController

from decimal import Decimal
import pytest

def _set_category(db_session, id=99, name="Cereais", desc="Produtos do Tipo Cereais"):
    category_model = Category()

    category_model.id = id
    category_model.name = name
    category_model.description = desc

    db_session.add(category_model)
    db_session.commit()

    return category_model.id;

def _get_category(db_session, id=99):
    category_model = Category()
    category_model.id = id
    category = db_session.get(Category, category_model.id)

    return category.id

def _get_user(id=1):
    user_model = User()
    user_model.id = id
    user_model.get_user_by_id()

    return user_model.id

def _save(now, category, user_id, qtd=None, name="Nescau Ball", desc="Teste", price="50.00"):
    '''Chama a função de criar novo produto esperado'''
    product_valid = {
            "name": name,
            "description": desc,
            "qtd": 0 if qtd == None else qtd,
            "price": Decimal(price),
            "date_created": now,
            "last_update": now,
            "category": category,
            "user_created": user_id
        }
    
    product_controller = ProductController()
    result = product_controller.save_product(product_valid)

    return result

CASOS_CARACTERES = [
    pytest.param("Nescau-ball", id="product-name-valid"),
    pytest.param("", id="product-without-name"),
    pytest.param("Nescau Ball Nescau B", id="product-name-with-20-characters"),
    pytest.param("Nescau Ball Nescau Ba", id="product-name-with-21-characters"),
]

def test_save_product_with_success(now, client, db_session):
    # Act
    result = _save(now, _set_category(db_session), _get_user(), name="Nescau Ball")

    # Assert
    assert result['status'] == 200

def test_save_product_without_name(now, client, db_session):
    # Act
    result = _save(now, _set_category(db_session), _get_user(), name="")

    # Assert
    assert result['message'] == "Field 'name' is missing..."

def test_save_product_with_existing_name(now, db_session):

    # Arange
    _save(now, _set_category(db_session), _get_user(), name="Nescau Ball")

    # Act
    result = _save(now, _get_category(db_session), _get_user(), name="Nescau Ball")
    expected = "duplicated"

    # Assert
    assert expected in result['message']

def test_save_product_with_name_length_20_characters(now, db_session):
    name = "Nescau Ball Nescau B"
    print(len(name))
    result = _save(now, _set_category(db_session), _get_user(), name=name)

    assert result['status'] == 200

def test_not_save_product_with_name_21_characters(now, db_session):
    name = "Nescau Ball Nescau Ba"
    result = _save(now, _set_category(db_session), _get_user(), name=name)

    assert result['status'] == 400

def test_not_save_product_with_quantity_negative(now, db_session):
    result = _save(now, _set_category(db_session), _get_user(), qtd=-1)
    assert result['status'] == 400

def test_save_product_with_quantity_zero(now, db_session):
    result = _save(now, _set_category(db_session), _get_user(), qtd=0)
    assert result['status'] == 200

def test_not_save_product_with_quantity_decimal(now, db_session):
    result = _save(now, _set_category(db_session), _get_user(), qtd=0.5)
    assert result['status'] == 400

def test_save_product_with_value_zero(now, db_session):
    result = _save(now, _set_category(db_session), _get_user(), price="0.00")
    assert result['status'] == 400

def test_save_product_with_negative_value(now, db_session):
    result = _save(now, _set_category(db_session), _get_user(), price="-1.00")
    assert result['status'] == 400

def test_save_product_without_date_created(now, db_session):
    result = _save("", _set_category(db_session), _get_user())
    assert result['status'] == 400

def test_save_product_without_last_update(db_session):
    result = _save("", _set_category(db_session), _get_user())
    assert result['status'] == 400