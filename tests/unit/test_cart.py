import pytest
from app import create_app, db
from models import Product
from unittest.mock import patch
from routes.orders import mergeDicts

@pytest.fixture(scope="module")
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
def init_database_cart(app):
    with app.app_context():
        db.create_all()
        product = Product(id=1, name="Test Product", price=10.0, photo="test.jpg")
        db.session.add(product)
        db.session.commit()
        yield db
        db.drop_all()

def test_updatecart(client, init_database_cart):
    with client.session_transaction() as sess:
        sess["shoppingcart"] = {"1": {"name": "Test Product", "price": 10.0, "quantity": 2, "image": "test.jpg"}}
    response = client.post("/orders/updatecart/1", data={"quantity": 5}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Item is updated" in response.data
    with client.session_transaction() as sess:
        assert int(sess["shoppingcart"]["1"]["quantity"]) == 5

def test_deletecartitem(client, init_database_cart):
    with client.session_transaction() as sess:
        sess["shoppingcart"] = {"1": {"name": "Test Product", "price": 10.0, "quantity": 2, "image": "test.jpg"}}
    response = client.get("/orders/delete-cart-item/1", follow_redirects=True)
    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert "1" not in sess["shoppingcart"]
        flashes = list(sess["_flashes"])
        assert any(flash[1] == " Item is deleted " for flash in flashes)
