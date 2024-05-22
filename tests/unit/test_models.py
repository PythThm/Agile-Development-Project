import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from app import create_app
from db import db
from models import User, Order, Product, ProductOrder, Category

def test_user_validation_name(init_database_model):
    user = User(name=" ")
    with pytest.raises(ValueError):
        user.validation_name()

def test_user_validation_phone(init_database_model):
    user = User(phone=" ")
    with pytest.raises(ValueError):
        user.validation_phone()

def test_order_total_calc(init_database_model):
    user = User(email="test2@example.com", name="testuser2", password=generate_password_hash("password", method="pbkdf2:sha256"))
    product = Product(name="Test Product", price=10, available=100)
    order = Order(user=user)
    product_order = ProductOrder(order=order, product=product, quantity=3)
    db.session.add(user)
    db.session.add(product)
    db.session.add(order)
    db.session.add(product_order)
    db.session.commit()

    assert order.total_calc() == 30

def test_order_process(init_database_model):
    user = User(email="test3@example.com", name="testuser3", password=generate_password_hash("password", method="pbkdf2:sha256"), balance=100)
    product = Product(name="Test Product 2", price=20, available=5)
    order = Order(user=user)
    product_order = ProductOrder(order=order, product=product, quantity=3)
    db.session.add(user)
    db.session.add(product)
    db.session.add(order)
    db.session.add(product_order)
    db.session.commit()

    success, message = order.process(strategy="adjust")
    assert success == True
    assert message == "Order processed"
    assert product.available == 2
    assert user.balance == 40
    assert order.processed is not None

def test_order_validation_total():
    order = Order(total=-1)
    assert order.total_calc() == 0

def test_product_validation_name():
    product = Product(name=" ")
    with pytest.raises(ValueError):
        product.validation_name()

def test_product_validation_price():
    product = Product(price=-1)
    assert product.validation_price() == 0

def test_product_validation_available():
    product = Product(available=-1)
    assert product.validation_available() == 0

def test_category_validation_name():
    category = Category(name=" ")
    with pytest.raises(ValueError):
        category.validation_name()