from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager
from pathlib import Path
from db import db
from models import User
from config import configure_uploads_app  # Image upload

def create_app():
    app = Flask(__name__)
    app.instance_path = Path("data").resolve()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
    app.config["SECRET_KEY"] = "secretkey"
    app.config['UPLOAD_FOLDER'] = "static"
    configure_uploads_app(app)  # Image upload

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Import and register blueprints
    from routes.api_users import api_users_bp
    from routes.api_products import api_products_bp
    from routes.api_orders import api_orders_bp
    from routes.api_images import api_images_bp
    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.products import products_bp
    from routes.orders import orders_bp
    from routes.supports import supports_bp
    from routes.admin import admin_bp

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

    @app.route("/")
    def home():
        return redirect(url_for('products.products'))
    
    @app.route("/help")
    def help():
        return "No support page yet xd"
    
    @app.route("/login")
    def login():
        return "No login yet xd"

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8888)
