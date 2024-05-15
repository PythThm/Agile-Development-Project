import pytest
from flask import url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash
from app import create_app, db
from models import User

@pytest.fixture
def test_client():
    app = create_app()
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client

@pytest.fixture
def init_database():
    db.create_all()
    hashed_password = generate_password_hash('mypassword', method='pbkdf2:sha256')
    user = User(name='test1', email='test@test.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()

    yield db

    db.drop_all()

def test_login(test_client, init_database):
    response = test_client.post('/login', data=dict(email='test@test.com', password='mypassword'), follow_redirects=True)
    assert response.status_code == 200
    assert b'You were logged in' in response.data
    assert current_user.is_authenticated

