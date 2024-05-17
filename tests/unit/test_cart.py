import pytest
from app import create_app, db
from models import Product, User
from unittest.mock import patch
from routes.orders import mergeDicts

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
        db.drop_all()

@pytest.fixture(scope='module')
def client(app):
    return app.test_client()

@pytest.fixture(scope='module')
def init_database(app):
    with app.app_context():
        product = Product(name='Test Product', price=10.0, photo='test.jpg')
        db.session.add(product)
        db.session.commit()

        user = User(name='Test User', email='test@test.com', password='mypassword')
        db.session.add(user)
        db.session.commit()

        yield db

def test_merge_dicts():
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'c': 3, 'd': 4}
    result = mergeDicts(dict1, dict2)
    expected = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
    assert result == expected

def test_addcart(client, init_database):
    with patch('routes.orders.Product.query.filter_by') as mock_query:
        mock_product = Product(id=1, name='Test Product', price=10.0, photo='test.jpg')
        mock_query.return_value.first.return_value = mock_product

        response = client.post('/orders/addcart', data={'product_id': 1, 'quantity': 2}, follow_redirects=True)
        assert response.status_code == 200

        with client.session_transaction() as sess:
            assert 'shoppingcart' in sess
            assert sess['shoppingcart']['1']['quantity'] == 2

def test_updatecart(client, init_database):
    with client.session_transaction() as sess:
        sess['shoppingcart'] = {'1': {'name': 'Test Product', 'price': 10.0, 'quantity': 2, 'image': 'test.jpg'}}

    response = client.post('/orders/updatecart/1', data={'quantity': 5}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Item is updated' in response.data

    with client.session_transaction() as sess:
        assert sess['shoppingcart']['1']['quantity'] == 5

def test_deletecartitem(client, init_database):
    with client.session_transaction() as sess:
        sess['shoppingcart'] = {'1': {'name': 'Test Product', 'price': 10.0, 'quantity': 2, 'image': 'test.jpg'}}

    response = client.get('/orders/delete-cart-item/1', follow_redirects=True)
    assert response.status_code == 200

    with client.session_transaction() as sess:
        assert '1' not in sess['shoppingcart']
        assert any(flash[1] == 'Item is deleted' for flash in sess['_flashes'])
