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

from routes.html import html_bp
app.register_blueprint(html_bp, url_prefix="/")


app.instance_path = Path("data").resolve()
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{ app.instance_path }/store.sqlite'
db.init_app(app)

# @app.route('/')
# def home_page():
#     name = 'John'
#     return render_template('home.html', name=name, my_list=[1, 2, 3, 4, 5])

# @app.route('/home')
# def home():
#     name = 'John'
#     return render_template('home.html', name=name, my_list=[1, 2, 3, 4, 5])

# @app.route('/customers')
# def customers():
#     customers_data = []
#     with open('data/customers.csv', 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             customers_data.append(row)
#     print(customers_data)
#     return render_template('customers.html', customers=customers_data)

# @app.route('/products')
# def prouducts():
#     products_data = []
#     with open('data/products.csv', 'r') as file:
#         reader = csv.DictReader(file)
#         for row in reader:
#             products_data.append(row)
#     print(products_data)
#     return render_template('products.html', products=products_data)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home_page():
    return render_template('home.html', name='philip')

@app.route('/customers')
def customer():
    customers = Customer.query.all()
    return render_template('customers.html', customers=customers)

@app.route('/products')
def product():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/customers/<int:customer_id>')
def customer_detail(customer_id):
    customer = Customer.query.get_or_404(customer_id)
    return render_template('customer_detail.html', customer=customer)

@app.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('order.html', orders=orders)

@app.route('/orders/<int:order_id>')
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_detail.html', order=order)

@app.route("/orders/<int:order_id>/delete", methods=["POST"])
def order_delete(order_id):
    order = db.get_or_404(Order, order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("orders"))

@app.route("/orders/<int:order_id>/process", methods=["POST"])
def order_process_web(order_id):
    order = db.get_or_404(Order, order_id)
    success, message = order.process()
    if not success:
        return message, 400
    db.session.commit()
    return redirect(url_for("orders"))


# Customer API
'''
@app.route("/api/customers")
def customers_json():
    statement = db.select(Customer).order_by(Customer.name)
    results = db.session.execute(statement)
    customers = [] 
    for customer in results.scalars():
        customers.append(customer.to_json())
    return jsonify(customers)

@app.route("/api/customers", methods=["POST"])
def customer_create():
    data = request.json
    customer = Customer(name=data["name"], phone=data["phone"])
    db.session.add(customer)
    db.session.commit()
    return jsonify(customer.to_json()), 201

# Cuctomer IDs API
@app.route("/api/customers/<int:customer_id>")
def customer_detail_json(customer_id):
    statement = db.select(Customer).where(Customer.id == customer_id)
    results = db.session.execute(statement)
    customers = [] 
    for customer in results.scalars():
        customers.append(customer.to_json())
    return jsonify(customers)

@app.route("/api/customers/<int:customer_id>", methods=["DELETE"])
def customer_delete(customer_id):
    customer = db.session.execute(db.select(Customer).where(Customer.id == customer_id))
    customer = customer.scalar_one()
    db.session.delete(customer)
    db.session.commit()
    return "deleted"

@app.route("/api/customers/<int:customer_id>", methods=["PUT"])
def customer_update(customer_id):
    data = request.json
    customer = db.session.execute(db.select(Customer).where(Customer.id == customer_id))
    customer = customer.scalar_one()
    customer.balance = data["balance"]
    db.session.commit()
    return jsonify(customer.to_json())
'''

# Product API
'''
@app.route("/api/products")
def products_json():
    statement = db.select(Product).order_by(Product.name)
    results = db.session.execute(statement)
    products = [] 
    for product in results.scalars():
        products.append(product.to_json())
    return jsonify(products)

@app.route("/api/products", methods=["POST"])
def product_create():
    data = request.json
    product = Product(name=data["name"], price=data["price"])
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_json()), 201

# Product IDs API
@app.route("/api/products/<int:product_id>")
def product_detail_json(product_id):
    statement = db.select(Product).where(Product.id == product_id)
    results = db.session.execute(statement)
    products = [] 
    for product in results.scalars():
        products.append(product.to_json())
    return jsonify(products)

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def product_delete(product_id):
    product = db.session.execute(db.select(Product).where(Product.id == product_id))
    product = product.scalar_one()
    db.session.delete(product)
    db.session.commit()
    return "deleted"

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def product_update(product_id):
    data = request.json
    product = db.session.execute(db.select(Product).where(Product.id == product_id))
    product = product.scalar_one()
    product.name = data["name"]
    product.price = data["price"]
    product.available = data["available"]
    db.session.commit()
    return jsonify(product.to_json())
'''

# Order AP
''''
@app.route("/api/orders")
def orders_json():
    statement = db.select(Order).order_by(Order.id)
    results = db.session.execute(statement)
    orders = [] 
    for order in results.scalars():
        orders.append(order.to_json())
    return jsonify(orders)

@app.route("/api/orders", methods=["POST"])
def order_create():
    data = request.json
    order = Order(customer_id=data["customer_id"])
    db.session.add(order)
    db.session.commit()
    return jsonify(order.to_json()), 201

# Order IDs API
@app.route("/api/orders/<int:order_id>")
def order_detail_json(order_id):
    statement = db.select(Order).where(Order.id == order_id)
    results = db.session.execute(statement)
    orders = [] 
    for order in results.scalars():
        orders.append(order.to_json())
    return jsonify(orders)
'''

# Order delete thing 


'''
@app.route("/api/orders/<int:order_id>", methods=["PUT"])
def order_process(order_id):
    order = db.get_or_404(Order, order_id)
    data = request.get_json()

    if not data or "processed" not in data:
        return "Not available", 400

    process = data["processed"]
    if "strategy" in data:
        strategy = data["strategy"]
    else:
        strategy = "adjust"

    success, message = order.process(strategy)
    if not success:
        return message, 400
    else:
        #db.session.commit()
        return jsonify(order.to_json()), 200
    
    db.session.commit()
    return jsonify(order.to_json()), 200
'''




if __name__ == '__main__':
    app.run(debug=True, port=8888)
    print(app.url_map)

