import pytest
from app import create_app, db
from models import Order, Product, User, ProductOrder
from werkzeug.security import generate_password_hash
import datetime

@pytest.fixture(scope="function", autouse=True)
def reset_database(app):
    with app.app_context():
        db.session.rollback()
        db.drop_all()
        db.create_all()
        product = Product(name="Test Product", price=10.0, available=100, photo="test.jpg")
        db.session.add(product)
        user = User(name="Test User", email="test@test.com", password=generate_password_hash("mypassword"), balance=100.0)
        db.session.add(user)
        db.session.commit()

@pytest.fixture
def add_order(reset_database):
    user = User.query.filter_by(email="test@test.com").first()
    product = Product.query.filter_by(name="Test Product").first()
    order = Order(user_id=user.id, total=20.0)
    order_item = ProductOrder(product_id=product.id, quantity=2)
    order.item.append(order_item)
    db.session.add(order)
    db.session.commit()
    return order

def test_get_orders(client):
    response = client.get("/api/orders/")
    assert response.status_code == 200

def test_create_order(client):
    user = User.query.filter_by(email="test@test.com").first()
    data = {"user_id": user.id}
    response = client.post("/api/orders/", json=data)
    assert response.status_code == 201

def test_get_order_detail(client, add_order):
    order = add_order
    response = client.get(f"/api/orders/{order.id}")
    assert response.status_code == 200

def test_process_order(client, add_order):
    order = add_order
    data = {"processed": True, "strategy": "adjust"}
    response = client.put(f"/api/orders/{order.id}", json=data)
    assert response.status_code == 200

def test_process_order_insufficient_balance(client):
    user = User(name="Test User 2", email="test2@test.com", password=generate_password_hash("mypassword"), balance=-10.0)
    db.session.add(user)
    db.session.commit()
    product = Product.query.filter_by(name="Test Product").first()
    order = Order(user_id=user.id)
    order_item = ProductOrder(product_id=product.id, quantity=2)
    order.item.append(order_item)
    order.total = product.price * order_item.quantity
    db.session.add(order)
    db.session.commit()
    data = {"processed": True, "strategy": "adjust"}
    response = client.put(f"/api/orders/{order.id}", json=data)
    assert response.status_code == 400
    assert b"Customer has insufficient balance" in response.data

def test_daily_sales(client, add_order):
    order = add_order
    order.created = datetime.datetime.now().replace(microsecond=0)
    db.session.commit()
    response = client.get("/api/orders/dailysales")
    assert response.status_code == 200
    assert response.json["dailysales"] == round(float(order.total), 2)

def test_total_sales(client, add_order):
    response = client.get("/api/orders/totalsales")
    assert response.status_code == 200
    assert response.json["totalsales"] == round(float(add_order.total), 2)

def test_yearly_sales(client, add_order):
    order = add_order
    order.created = datetime.datetime.now().replace(microsecond=0)
    db.session.commit()
    response = client.get("/api/orders/yearlysales")
    assert response.status_code == 200
    assert response.json["yearlysales"] == round(float(order.total), 2)
