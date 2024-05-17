import pytest
from flask import url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash
from app import create_app, db
from models import User


# Fixtures
@pytest.fixture(scope='session')
def test_client():
    app = create_app()
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client

@pytest.fixture(scope='session')
def init_database():
    db.create_all()
    yield db
    db.drop_all()

@pytest.fixture(scope='session')
def add_user(init_database):
    hashed_password = generate_password_hash('mypassword', method='pbkdf2:sha256')
    user = User(name='test1', email='test@test.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope='session')
def add_admin(init_database):
    hashed_password = generate_password_hash('adminpassword', method='pbkdf2:sha256')
    admin = User(name='admin', email='admin@test.com', password=hashed_password, is_admin=True)
    db.session.add(admin)
    db.session.commit()
    return admin

# Login Tests
def test_login(test_client, add_user):
    response = test_client.post('/auth/login', data=dict(email='test@test.com', password='mypassword'), follow_redirects=True)
    assert response.status_code == 200
    with test_client.session_transaction() as session:
        assert session['_user_id'] == str(add_user.id)

def test_login_get(test_client):
    response = test_client.get('/auth/login')
    assert response.status_code == 200

def test_login_post_valid(test_client, add_user):
    response = test_client.post('/auth/login', data=dict(email='test@test.com', password='mypassword'), follow_redirects=True)
    assert response.status_code == 200
    assert current_user.is_authenticated

def test_login_post_invalid_email(test_client, init_database):
    response = test_client.post('/auth/login', data=dict(email='wrong@test.com', password='mypassword'), follow_redirects=True)
    assert response.status_code == 200
    assert not current_user.is_authenticated

def test_login_post_invalid_password(test_client, add_user):
    response = test_client.post('/auth/login', data=dict(email='test@test.com', password='wrongpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert not current_user.is_authenticated

def test_login_post_admin(test_client, add_admin):
    response = test_client.post('/auth/login', data=dict(email='admin@test.com', password='adminpassword'), follow_redirects=True)
    assert response.status_code == 200
    assert current_user.is_authenticated
    assert current_user.is_admin


# Signup Tests
def test_signup_post_valid(test_client, init_database):
    response = test_client.post('/auth/signup', data=dict(name='newuser', email='newuser@test.com', password='mypassword'), follow_redirects=True)
    assert response.status_code == 200
    assert current_user.is_authenticated
    new_user = User.query.filter_by(email='newuser@test.com').first()
    assert new_user is not None

def test_signup_post_email_in_use(test_client, init_database):
    existing_user = User(name='existinguser', email='existinguser@test.com', password='mypassword')
    db.session.add(existing_user)
    db.session.commit()
    response = test_client.post('/auth/signup', data=dict(name='newuser', email='existinguser@test.com', password='mypassword'), follow_redirects=True)
    assert response.status_code == 200
    assert not current_user.is_authenticated
    new_user = User.query.filter_by(email='newuser@test.com').first()
    assert new_user is None