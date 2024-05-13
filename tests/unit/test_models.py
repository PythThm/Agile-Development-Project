import pytest
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash
from app import create_app
from db import db
from models import User, Order, Product, ProductOrder, Category

@pytest.fixture(scope='module')
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test_secret_key"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        db.create_all()
        user = User(email='test@example.com', name='testuser', password=generate_password_hash('password', method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()

def test_user_validation_name(init_database):
    user = User(name=" ")
    with pytest.raises(ValueError):
        user.validation_name()

def test_user_validation_phone(init_database):
    user = User(phone=" ")
    with pytest.raises(ValueError):
        user.validation_phone()

def test_order_total_calc(init_database):
    user = User(email='test2@example.com', name='testuser2', password=generate_password_hash('password', method='pbkdf2:sha256'))
    product = Product(name="Test Product", price=10, available=100)
    order = Order(user=user)
    product_order = ProductOrder(order=order, product=product, quantity=3)

    db.session.add(user)
    db.session.add(product)
    db.session.add(order)
    db.session.add(product_order)
    db.session.commit()

    assert order.total_calc() == 30