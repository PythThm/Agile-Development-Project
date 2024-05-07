from flask import Flask, render_template, jsonify, request, redirect, url_for, Blueprint
from pathlib import Path
from db import db
from models import Customer, Product, Order, ProductOrder

app = Flask(__name__)

from routes.api_customers import api_customers_bp
app.register_blueprint(api_customers_bp, url_prefix="/api/customers")

from routes.api_products import api_products_bp
app.register_blueprint(api_products_bp, url_prefix="/api/products")

from routes.api_orders import api_orders_bp
app.register_blueprint(api_orders_bp, url_prefix="/api/orders")

# from routes.html import html_bp
# app.register_blueprint(html_bp, url_prefix="/")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/help")
def help():
    #return render_template("help.html")
    return "Haven't built a support page yet xd"

@app.route("/login")
def login():
    return "No login yet xd"

app.instance_path = Path("data").resolve()
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{ app.instance_path }/store.sqlite'
db.init_app(app)




if __name__ == '__main__':
    app.run(debug=True, port=8888)

