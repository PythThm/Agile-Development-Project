import pytest
from app import create_app, db
from models import Product, Category
from flask import url_for
from io import BytesIO
from unittest.mock import patch
import secrets

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test_secret_key",
        "SERVER_NAME": "localhost"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()

        product = Product(name='Test Product', price=10.0, photo='test.jpg', category_id=category.id)
        db.session.add(product)
        db.session.commit()

        yield db

def test_products_list(client, init_database):
    response = client.get(url_for('products.products'))
    assert response.status_code == 200
    assert b'Test Product' in response.data

def test_product_detail(client, init_database):
    product_name = 'Test Product'
    response = client.get(url_for('products.product_detail', productname=product_name))
    assert response.status_code == 200
    assert b'Test Product' in response.data

def test_additem_get(client, init_database):
    response = client.get(url_for('products.additem'))
    assert response.status_code == 200
    assert b'Add Item' in response.data

def test_additem_post(client, init_database):
    with client.application.app_context():
        category = Category(name='New Category')
        db.session.add(category)
        db.session.commit()

        data = {
            'name': 'New Product',
            'price': '20.0',
            'quantity': '100',
            'description': 'A new product',
            'category': str(category.id),
            'item-photo': (BytesIO(b'my file contents'), 'test.jpg')
        }

        with patch('secrets.token_hex', return_value='12345'):
            with patch('config.photos.save', return_value='12345.jpg'):
                response = client.post(url_for('products.additem'), data=data, content_type='multipart/form-data', follow_redirects=True)
                assert response.status_code == 200
                with client.application.app_context():
                    product = Product.query.filter_by(name='New Product').first()
                    assert product is not None
                    assert product.photo == '12345.jpg'

def test_delete_product(client, init_database):
    product = Product.query.first()
    response = client.get(url_for('products.delete_product', product_id=product.id), follow_redirects=True)
    assert response.status_code == 200
    with client.application.app_context():
        deleted_product = Product.query.get(product.id)
        assert deleted_product is None
