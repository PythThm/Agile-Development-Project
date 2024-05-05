from flask import Flask, render_template
from pathlib import Path
from db import db

from routes import api_users_bp, api_products_bp, api_orders_bp, api_images_bp
from routes import users_bp, products_bp, orders_bp, auth_bp 

from flask_login import LoginManager

login_manager = LoginManager()

app = Flask(__name__)

app.instance_path = Path("data").resolve()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///store.db"
app.config["SECRET_KEY"] = "secretkey"
app.config['UPLOAD_FOLDER'] = "static"

db.init_app(app)

# home
@app.route("/")
def home():
    return render_template('index.html')

# API
app.register_blueprint(api_users_bp, url_prefix="/api/users")
app.register_blueprint(api_products_bp, url_prefix="/api/products")
app.register_blueprint(api_orders_bp, url_prefix="/api/orders")
app.register_blueprint(api_images_bp, url_prefix="/api/images")

# View
app.register_blueprint(auth_bp, url_prefix="/auth")
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(products_bp, url_prefix="/products")
app.register_blueprint(orders_bp, url_prefix="/orders")

if __name__ == '__main__':
    app.run(debug=True, port=8888)

