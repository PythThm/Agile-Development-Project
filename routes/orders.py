from flask import Blueprint, redirect, url_for, render_template, request
from db import db 
from models import Order
from time import sleep

orders_bp = Blueprint("orders", __name__)

@orders_bp.route('/')
def orders():
    orders = Order.query.all()
    return render_template('admin/orders.html', orders=orders)

@orders_bp.route('/<int:order_id>')
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    return render_template('pages/order_detail.html', order=order)

@orders_bp.route("/<int:order_id>/delete", methods=["GET", "POST"])
def order_delete(order_id):
    order = db.get_or_404(Order, order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("orders.orders"))

@orders_bp.route("/<int:order_id>/process", methods=["POST"])
def order_process_web(order_id):
    order = db.get_or_404(Order, order_id)
    success, message = order.process()
    if not success:
        return message, 400
    db.session.commit()
    return redirect(url_for("orders.orders"))

@orders_bp.route('/cart')
def cart():
    return render_template('pages/cart.html')

@orders_bp.route('/checkout', methods = ['POST', 'GET'])
def checkout():
    if request.method == 'POST':
        creditcard = request.form['ccn']
        if creditcard == '4444 4444 4444 4444':
            return redirect(url_for('orders.failure'))
        return redirect(url_for('orders.success'))
    return render_template('pages/checkout.html')

@orders_bp.route('/success')
def success():
    render_template('pages/success.html')
    sleep(3)
    return redirect(url_for('home'))

@orders_bp.route('/failure')
def failure():
    render_template('pages/failure.html')
    sleep(3)
    return redirect(url_for('orders.checkout'))
