import pytest
from app import create_app, db
from models import Product, User, Order
from werkzeug.security import generate_password_hash


@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    with app.test_client() as test_client:
        with app.app_context():
            yield test_client

@pytest.fixture(scope='module')
def init_database_auth():
    db.create_all()
    yield db
    db.drop_all()

@pytest.fixture(scope='module')
def add_user(init_database_auth):
    hashed_password = generate_password_hash('mypassword', method='pbkdf2:sha256')
    user = User(name='test1', email='test@test.com', password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture(scope='module')
def add_admin(init_database_auth):
    hashed_password = generate_password_hash('adminpassword', method='pbkdf2:sha256')
    admin = User(name='admin', email='admin@test.com', password=hashed_password, is_admin=True)
    db.session.add(admin)
    db.session.commit()
    return admin


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
def init_database_func_cart(app):
    with app.app_context():
        product = Product(name='Test Product', price=10.0, photo='test.jpg')
        db.session.add(product)
        db.session.commit()
        user = User(name='Test User', email='test@test.com', password=generate_password_hash('mypassword'))
        db.session.add(user)
        db.session.commit()
        yield db

@pytest.fixture
def init_database_cart(app):
    with app.app_context():
        product = Product(name='Test Product', price=10.0, photo='test.jpg')
        db.session.add(product)
        db.session.commit()

        user = User(name='Test User', email='test@test.com', password='mypassword')
        db.session.add(user)
        db.session.commit()

        yield db

@pytest.fixture
def init_database_model(app):
    with app.app_context():
        db.create_all()
        user = User(email='test@example.com', name='testuser', password=generate_password_hash('password', method='pbkdf2:sha256'), balance=100)
        db.session.add(user)
        db.session.commit()

        yield db

        db.session.remove()
        db.drop_all()
        