#test test test
from flask import Flask, render_template
from flask_login import LoginManager
from pathlib import Path
from db import db
from models import User
# image upload 
from config import configure_uploads_app

app = Flask(__name__)
app.instance_path = Path("data").resolve()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SECRET_KEY"] = "secretkey"
app.config['UPLOAD_FOLDER'] = "static"
# image upload 
configure_uploads_app(app)

db.init_app(app)

def create_app():

    from routes import api_users_bp, api_products_bp, api_orders_bp, api_images_bp
    from routes import users_bp, products_bp, orders_bp, auth_bp, supports_bp, admin_bp

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # Set up database

    # Define user loader function
    @login_manager.user_loader
    def load_user(user_id):
        # Load the user from the database based on the user ID
        return User.query.get(int(user_id))

    # API blueprints
    app.register_blueprint(api_users_bp, url_prefix="/api/users")
    app.register_blueprint(api_products_bp, url_prefix="/api/products")
    app.register_blueprint(api_orders_bp, url_prefix="/api/orders")
    app.register_blueprint(api_images_bp, url_prefix="/api/images")

    # Web blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(users_bp, url_prefix="/users")
    app.register_blueprint(products_bp, url_prefix="/products")
    app.register_blueprint(orders_bp, url_prefix="/orders")
    app.register_blueprint(supports_bp, url_prefix="/supports")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # Home route
    @app.route("/")
    def home():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8888)
