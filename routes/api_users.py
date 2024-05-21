from flask import Blueprint, jsonify, request
from models import User
from db import db

api_users_bp = Blueprint("api_users", __name__)

@api_users_bp.route("/")
def customers_json():
    statement = db.select(User).order_by(User.name)
    results = db.session.execute(statement)
    customers = [] 
    for customer in results.scalars():
        customers.append(customer.to_json())
    return jsonify(customers)

@api_users_bp.route("/", methods=["POST"])
def customer_create():
    data = request.json
    customer = User(name=data["name"], phone=data["phone"])
    customer.balance = customer.validation()
    customer.name = customer.validation_name()
    customer.phone = customer.validation_phone()
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_json()), 201

# Customer IDs API
@api_users_bp.route("/<int:customer_id>")
def customer_detail_json(customer_id):
    statement = db.select(User).where(User.id == customer_id)
    results = db.session.execute(statement)
    customers = [] 
    for customer in results.scalars():
        customers.append(customer.to_json())
    return jsonify(customers)

@api_users_bp.route("/<int:customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    customer = db.session.execute(db.select(User).where(User.id == customer_id))
    customer = customer.scalar_one()
    db.session.delete(customer)
    db.session.commit()
    return "deleted"

@api_users_bp.route("/<int:customer_id>", methods=["PUT"])
def customer_update(customer_id):
    data = request.json
    customer = db.session.execute(db.select(User).where(User.id == customer_id))
    customer = customer.scalar_one()
    customer.balance = data["balance"]
    db.session.commit()
    return jsonify(customer.to_json())

