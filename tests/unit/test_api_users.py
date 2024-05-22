import pytest
from unittest.mock import patch
from flask import Flask, jsonify, request
from app import create_app
from db import db
from models import User
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
        user = User(name="Test User", phone="1234567890", email="test@example.com", password="password", balance=100)
        db.session.add(user)
        db.session.commit()
        yield db

        db.session.remove()
        db.drop_all()

def test_customers_json(client, init_database):
    response = client.get("/api/users/")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Test User"

@patch.object(User, "validation", return_value=0)
@patch.object(User, "validation_name", return_value="New User")
@patch.object(User, "validation_phone", return_value="0987654321")
def test_customer_create(mock_validation_phone, mock_validation_name, mock_validation, client, init_database):
    new_user = {
        "name": "New User",
        "phone": "0987654321"
    }
    response = client.post("/api/users/", json=new_user)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data["name"] == "New User"
    assert data["phone"] == "0987654321"
    assert data["balance"] == 0

def test_customer_detail_json(client, init_database):
    response = client.get("/api/users/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["name"] == "Test User"

def test_customer_delete(client, init_database):
    response = client.delete("/api/users/1")
    assert response.status_code == 200
    assert response.data == b"deleted"
    response = client.get("/api/users/1")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data) == 0

def test_customer_update(client, init_database):
    updated_user = {
        "balance": 200
    }
    response = client.put("/api/users/1", json=updated_user)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data["balance"] == 200
