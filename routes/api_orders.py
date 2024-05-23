from flask import Blueprint, jsonify, request
import datetime
from db import db
from models import Order, ProductOrder, Product, User
from sqlalchemy import func

api_orders_bp = Blueprint("api_orders", __name__)

@api_orders_bp.route("/")
def orders_json():
    statement = db.select(Order).order_by(Order.id)
    results = db.session.execute(statement)
    orders = [] 
    for order in results.scalars():
        orders.append(order.to_json())
    return jsonify(orders)

@api_orders_bp.route("/", methods=["POST"])
def order_create():
    data = request.json
    order = Order(user_id=data["user_id"])
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_json()), 201

# Order IDs API
@api_orders_bp.route("/<int:order_id>")
def order_detail_json(order_id):
    statement = db.select(Order).where(Order.id == order_id)
    results = db.session.execute(statement)
    orders = [] 
    for order in results.scalars():
        orders.append(order.to_json())
    return jsonify(orders)

@api_orders_bp.route("/<int:order_id>", methods=["PUT"])
def order_process(order_id):
    order = db.get_or_404(Order, order_id)
    data = request.get_json()

    if not data or "processed" not in data:
        return "Not available", 400
    
    customer = User.query.get(order.user_id)

    if customer.balance < 0:
        return "Customer has insufficient balance", 400
    
    if "strategy" in data:
        strategy = data["strategy"]
    else:
        strategy = "adjust"
    if strategy == "reject": # We want to reject the order and not process it, setting everything to 0
        order.total = 0
        order.items = [{}]
        order.processed = datetime.datetime.now()
    elif strategy == "ignore": # The order is ignored and order quantity is set to 0
        order.processed = datetime.datetime.now()
        order.total = 0
        for item in order.item:
            item.quantity = 0
    else: # Adjust the order quantity based on the available stock, and if there isn't enough stock we set the order quantity to the available stock
        # Check if there is enough stock
        for item in order.item:
            if item.quantity > item.product.available:
                item.quantity = item.product.available
            item.product.available -= item.quantity
            order.total += item.product.price * item.quantity
        order.processed = datetime.datetime.now()
    order.strategy = strategy
    db.session.commit()
    success, message = order.process(strategy)
    if not success:
        return message, 400
    else:
        return jsonify(order.to_json()), 200
    
@api_orders_bp.route("/dailysales")
def daily():
    today = datetime.datetime.now().date()
    results = db.session.query(func.sum(Order.total).label('dailysales')).filter(Order.created.like(f'%{today}%'))
    sumoftodaysales = db.session.execute(results).scalar()
    if sumoftodaysales == None:
        sumoftodaysales = 0
    else:
        sumoftodaysales = round(float(sumoftodaysales), 2)
    return jsonify(dailysales=sumoftodaysales)
    
    
@api_orders_bp.route("/totalsales")
def total():
    result = Order.query.with_entities(func.sum(Order.total).label("totalsales"))
    totalsales = round(float(db.session.execute(result).scalar()), 2)
    return jsonify(totalsales=totalsales)
    
@api_orders_bp.route("/yearlysales")
def yearly():
    yearnow = datetime.datetime.now().year
    results = db.session.query(func.sum(Order.total).label('yearsales')).filter(Order.created.like(f'%{yearnow}%'))
    sumofyear = db.session.execute(results).scalar()
    if sumofyear == None:
        sumofyear = 0
    else:
        sumofyear = round(float(sumofyear), 2)
    return jsonify(yearlysales=sumofyear)
    
@api_orders_bp.route("/monthlysales")
def monthly():
    current_month = datetime.datetime.now().strftime("%m")
    results= db.session.query(func.sum(Order.total).label('yearsales')).filter(Order.created.like(f'%{current_month}%'))
    sumofmonth = db.session.execute(results).scalar()
    if sumofmonth == None:
        sumofmonth = 0
    else:
        sumofmonth = round(sumofmonth, 2)
    return jsonify(monthlysales=sumofmonth)