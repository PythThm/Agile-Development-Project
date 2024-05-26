import pytest
from unittest.mock import patch, MagicMock
from flask import Flask, jsonify, request
from app import create_app
from db import db
from models import Product
import json

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
def init_database(app):
    with app.app_context():
        db.create_all()
        product = Product(name="Test Product", price=10, available=100)
        db.session.add(product)
        db.session.commit()
        yield db

        db.session.remove()
        db.drop_all()

def test_products_json(client, init_database):
    response = client.get("/api/products/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Test Product"


def test_product_detail_json(client, init_database):
    response = client.get("/api/products/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Test Product"

def test_product_delete(client, init_database):
    response = client.delete("/api/products/1")
    assert response.status_code == 200
    assert response.data == b"deleted"
    response = client.get("/api/products/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 0

def test_product_update(client, init_database):
    updated_product = {
        "name": "Updated Product",
        "price": 30,
        "available": 70
    }
    response = client.put("/api/products/1", json=updated_product)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["name"] == "Updated Product"
    assert data["price"] == 30
    assert data["available"] == 70