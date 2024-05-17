import pytest
from app import create_app, db
from models import Product, User, Order
from werkzeug.security import generate_password_hash



def test_add_to_cart(client, init_database_func_cart):
    response = client.post('/orders/addcart', data={'product_id': 1, 'quantity': 2}, follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert 'shoppingcart' in sess
        assert sess['shoppingcart']['1']['quantity'] == 2

def test_update_cart(client, init_database_func_cart):
    with client.session_transaction() as sess:
        sess['shoppingcart'] = {'1': {'name': 'Test Product', 'price': 10.0, 'quantity': 2, 'image': 'test.jpg'}}
    response = client.post('/orders/updatecart/1', data={'quantity': 5}, follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert sess['shoppingcart']['1']['quantity'] == 5

def test_delete_from_cart(client, init_database_func_cart):
    with client.session_transaction() as sess:
        sess['shoppingcart'] = {'1': {'name': 'Test Product', 'price': 10.0, 'quantity': 2, 'image': 'test.jpg'}}
    response = client.get('/orders/delete-cart-item/1', follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert '1' not in sess['shoppingcart']

def test_checkout_success(client, init_database_func_cart):
    with client.session_transaction() as sess:
        sess['shoppingcart'] = {'1': {'name': 'Test Product', 'price': 10.0, 'quantity': 2, 'image': 'test.jpg'}}
    response = client.post('/orders/checkout', data={'ccn': '1234 5678 8765 4321'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Payment Confirmed!' in response.data

def test_checkout_failure(client, init_database_func_cart):
    with client.session_transaction() as sess:
        sess['shoppingcart'] = {'1': {'name': 'Test Product', 'price': 10.0, 'quantity': 2, 'image': 'test.jpg'}}
    response = client.post('/orders/checkout', data={'ccn': '4444 4444 4444 4444'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'An issue was found with your credit card' in response.data
