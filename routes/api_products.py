from flask import Blueprint, jsonify, request

from db import db
from models import Product

api_products_bp = Blueprint("api_products", __name__)

@api_products_bp.route("/")
def products_json():
    statement = db.select(Product).order_by(Product.name)
    results = db.session.execute(statement)
    products = [] 
    for product in results.scalars():
        products.append(product.to_json())
    return jsonify(products)

@api_products_bp.route("/", methods=["POST"])
def product_create():
    data = request.json
    product = Product(name=data["name"], price=data["price"], available=data["available"])
    product.price = product.validation()
    product.available = product.validation_available()
    product.name = product.validation_name()
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json()), 201

# Product IDs API
@api_products_bp.route("/<int:product_id>")
def product_detail_json(product_id):
    statement = db.select(Product).where(Product.id == product_id)
    results = db.session.execute(statement)
    products = [] 
    for product in results.scalars():
        products.append(product.to_json())
    return jsonify(products)

@api_products_bp.route("/<int:product_id>", methods=["DELETE"])
def product_delete(product_id):
    product = db.session.execute(db.select(Product).where(Product.id == product_id))
    product = product.scalar_one()
    db.session.delete(product)
    db.session.commit()
    return "deleted"

@api_products_bp.route("/<int:product_id>", methods=["PUT"])
def product_update(product_id):
    data = request.json
    product = db.session.execute(db.select(Product).where(Product.id == product_id))
    product = product.scalar_one()
    product.name = data["name"]
    product.price = data["price"]
    product.available = data["available"]
    db.session.commit()
    return jsonify(product.to_json())

