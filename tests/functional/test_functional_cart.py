import pytest
from app import create_app, db
from models import Product, User
from unittest.mock import patch
from routes.orders import mergeDicts

@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
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
def init_database_cart(app):
    with app.app_context():
        db.create_all()
        product = Product(id=1, name="Test Product", price=10.0, photo="test.jpg")
        user = User(name="Test User", email="test@example.com", password="password")
        db.session.add(product)
        db.session.add(user)
        db.session.commit()
        yield db

        db.session.remove()
        db.drop_all()


def test_getcart_with_items(client, init_database_cart):
    with client.session_transaction() as sess:
        sess["shoppingcart"] = {
            "1": {
                "name": "Test Product",
                "price": 10.0,
                "quantity": 2,
                "image": "test.jpg"
            }
        }

    response = client.get("/orders/cart", follow_redirects=True)
    assert response.status_code == 200
    assert b"Shopping Cart" in response.data
    assert b"Test Product" in response.data

def test_clearcart(client, init_database_cart):
    with client.session_transaction() as sess:
        sess["shoppingcart"] = {
            "1": {
                "name": "Test Product",
                "price": 10.0,
                "quantity": 2,
                "image": "test.jpg"
            }
        }

    response = client.get("/orders/clearcart", follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert "shoppingcart" not in sess

def test_deletecartitem(client, init_database_cart):
    with client.session_transaction() as sess:
        sess["shoppingcart"] = {
            "1": {
                "name": "Test Product",
                "price": 10.0,
                "quantity": 2,
                "image": "test.jpg"
            }
        }

    response = client.get("/orders/delete-cart-item/1", follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert "1" not in sess["shoppingcart"]
        assert any(flash[1] == " Item is deleted " for flash in sess["_flashes"])

def test_updatecart(client, init_database_cart):
    with client.session_transaction() as sess:
        sess["shoppingcart"] = {"1": {"name": "Test Product", "price": 10.0, "quantity": 2, "image": "test.jpg"}}

    response = client.post("/orders/updatecart/1", data={"quantity": 5}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Item is updated" in response.data

    with client.session_transaction() as sess:
        assert int(sess["shoppingcart"]["1"]["quantity"]) == 5
