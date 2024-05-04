from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from pathlib import Path
from db import db
from models import User, Product, Order, ProductOrder
from flask_login import LoginManager, login_user, login_required, current_user, logout_user

login_manager = LoginManager()

app = Flask(__name__)



from routes.api_customers import api_customers_bp
app.register_blueprint(api_customers_bp, url_prefix="/api/customers")

from routes.api_products import api_products_bp
app.register_blueprint(api_products_bp, url_prefix="/api/products")

from routes.api_orders import api_orders_bp
app.register_blueprint(api_orders_bp, url_prefix="/api/orders")

from routes.html import html_bp
app.register_blueprint(html_bp, url_prefix="/")


app.instance_path = Path("data").resolve()
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{ app.instance_path }/store.sqlite'
app.config["SECRET_KEY"] = "secretkey"
db.init_app(app)




if __name__ == '__main__':
    app.run(debug=True, port=8888)

