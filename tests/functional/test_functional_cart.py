import pytest
from app import create_app, db
from models import Product, User, Order
from werkzeug.security import generate_password_hash

@pytest.fixture
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
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    with app.app_context():
        product = Product(name='Test Product', price=10.0, photo='test.jpg')
        db.session.add(product)
        db.session.commit()
        user = User(name='Test User', email='test@test.com', password=generate_password_hash('mypassword'))
        db.session.add(user)
        db.session.commit()
        yield db

def test_add_to_cart(client, init_database):
    response = client.post('/orders/addcart', data={'product_id': 1, 'quantity': 2}, follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert 'shoppingcart' in sess
        assert sess['shoppingcart']['1']['quantity'] == 2

def test_update_cart(client, init_database):
    with client.session_transaction() as sess:
        sess['shoppingcart'] = {'1': {'name': 'Test Product', 'price': 10.0, 'quantity': 2, 'image': 'test.jpg'}}
    response = client.post('/orders/updatecart/1', data={'quantity': 5}, follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess['shoppingcart']['1']['quantity'] == 5

def test_delete_from_cart(client, init_database):
    with client.session_transaction() as sess:
        sess['shoppingcart'] = {'1': {'name': 'Test Product', 'price': 10.0, 'quantity': 2, 'image': 'test.jpg'}}
    response = client.get('/orders/delete-cart-item/1', follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert '1' not in sess['shoppingcart']

def test_checkout_success(client, init_database):
    with client.session_transaction() as sess:
        sess['shoppingcart'] = {'1': {'name': 'Test Product', 'price': 10.0, 'quantity': 2, 'image': 'test.jpg'}}
    response = client.post('/orders/checkout', data={'ccn': '1234 5678 8765 4321'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Payment Confirmed!' in response.data

def test_checkout_failure(client, init_database):
    with client.session_transaction() as sess:
        sess['shoppingcart'] = {'1': {'name': 'Test Product', 'price': 10.0, 'quantity': 2, 'image': 'test.jpg'}}
    response = client.post('/orders/checkout', data={'ccn': '4444 4444 4444 4444'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'An issue was found with your credit card' in response.data
