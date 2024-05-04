from flask import Blueprint, render_template, redirect, url_for, request
from db import db
from models import User, Order, Product, ProductOrder

html_bp = Blueprint("html", __name__)

@html_bp.route('/')
def home():
    return render_template('home.html')

@html_bp.route('/home')
def home_page():
    return render_template('home.html', name='welcome to the Green Basket')

@html_bp.route('/customers')
def user():
    customers = User.query.all()
    return render_template('customers.html', customers=customers)

@html_bp.route('/products')
def product():
    products = Product.query.all()
    return render_template('products.html', products=products)

@html_bp.route('/products/<name>')
def product_detail(name):
    product = db.one_or_404(db.select(Product).filter_by(name=name))
    return render_template('product_detail.html', product=product)

@html_bp.route('/customers/<int:customer_id>')
def customer_detail(customer_id):
    user = User.query.get_or_404(customer_id)
    return render_template('customer_detail.html', user=user)

@html_bp.route('/orders')
def orders():
    orders = Order.query.all()
    return render_template('order.html', orders=orders)

@html_bp.route('/orders/<int:order_id>')
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('order_detail.html', order=order)

@html_bp.route("/orders/<int:order_id>/delete", methods=["POST"])
def order_delete(order_id):
    order = db.get_or_404(Order, order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("html.orders"))

@html_bp.route("/orders/<int:order_id>/process", methods=["POST"])
def order_process_web(order_id):
    order = db.get_or_404(Order, order_id)
    success, message = order.process()
    if not success:
        return message, 400
    db.session.commit()
    return redirect(url_for("html.orders"))


# Authentication and Authorization
@html_bp.route('/login')
def login():
    return render_template('login.html')

@html_bp.route('/signup')
def signup():
    return render_template('signup.html')

@html_bp.route('/logout')
def logout():
    return render_template('logout.html')

@html_bp.route('/profile')
def profile():
    return render_template('profile.html')
