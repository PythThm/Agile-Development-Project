from flask import Blueprint, redirect, url_for, render_template, request, session, flash
from db import db 
from models import Order, Product, User, OrderHistory, OrderProduct
from flask_login import current_user
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
    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return redirect(url_for("orders.orders"))

@orders_bp.route("/<int:order_id>/process", methods=["POST"])
def order_process_web(order_id):
    order = Order.query.get_or_404(order_id)
    success, message = order.process()
    if not success:
        return message, 400
    db.session.commit()
    return redirect(url_for("orders.orders"))

# Cart Functionality
# Checkout
@orders_bp.route('/checkout', methods = ['POST', 'GET'])
def checkout():
    if request.method == 'POST':
        
        creditcard = request.form['ccn']
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()

        if not user:
            user = email
        else:
            user = user.email

        subtotal = 0
        total = 0

        for key, product in session['shoppingcart'].items():
            quantity = product['quantity']
            subtotal += float(product['price'] * int(product['quantity']))
            total = float("%.2f" % (1.06 * subtotal))


        order = OrderHistory(user_email=user, total=total)
            
        if creditcard == '4444 4444 4444 4444':
            return redirect(url_for('orders.failure'))
        

        for key, product in session['shoppingcart'].items():
            quantity = product['quantity']
            product_name = product['name']
            product = Product.query.filter_by(name=product_name).first()

            new_order = OrderProduct( order=order, product=product, quantity=quantity) 
            db.session.add(new_order) 
            db.session.commit()

        return redirect(url_for('orders.success'))
    return render_template('pages/checkout.html', user=current_user)

@orders_bp.route('/success')
def success():
    session.pop('shoppingcart', None)
    return render_template('pages/success.html')

@orders_bp.route('/failure')
def failure():
    return render_template('pages/failure.html')

# Add items to shopping cart
# Get and calculate items in cart
@orders_bp.route('/cart')
def getcart():
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    estimated = 0
    for key, product in session['shoppingcart'].items():
        subtotal += float(product['price'] * int(product['quantity']))
        tax = ("%.2f" % (0.06 * float(subtotal)))
        estimated = float("%.2f" % (1.06 * subtotal))

    return render_template('pages/cart.html', tax = tax, estimated = estimated, subtotal = subtotal)

# function to combine items with items in session
def mergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    else:
        False

# add items to cart
@orders_bp.route("/addcart", methods=['GET', 'POST'])
def addcart():

    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity'))

    product = Product.query.filter_by(id=product_id).first()

    if product_id and quantity and request.method == "POST":
        cartItems = {product_id:{'name': product.name, 'price': product.price, 'quantity':quantity, 'image':product.photo}} 

        if 'shoppingcart' in session:
            print(session['shoppingcart'])

            if product_id in session['shoppingcart']:
                for key, item in session['shoppingcart'].items():
                    if int(key) == int(product_id):
                        session.modified = True
                        item['quantity'] += quantity
                        flash("Item is Added to Cart Successfully")           
            else:
                session['shoppingcart'] = mergeDicts(session['shoppingcart'], cartItems)
                flash("Item is Added to Cart Successfully")
                #  request.referrer : the URL of the previous web page from which a link was followed     
                return redirect(request.referrer)

        else:
            session['shoppingcart'] = cartItems
            flash("Item is Added to Cart Successfully")
            return redirect(request.referrer)


    return redirect(request.referrer)

# Update Cart
@orders_bp.route('/updatecart/<int:code>', methods=['POST'])
def updatecart(code):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('home'))
    if request.method == "POST":
        quantity = request.form.get('quantity')
        session.modified = True
        for key, item in session['shoppingcart'].items():
            if int(key) == code:
                item['quantity'] = quantity
                flash("Item is updated")
                return redirect(url_for('orders.getcart'))

# Clear all items
@orders_bp.route('/clearcart')
def clearcart():
    session.pop('shoppingcart', None)
    return redirect(url_for('home')) 

# Clear one item
@orders_bp.route('/delete-cart-item/<int:id>')
def deletecartitem(id):
    if 'shoppingcart' not in session or len(session['shoppingcart']) <= 0:
        return redirect(url_for('product.product'))

    session.modified = True
    for key, item in session['shoppingcart'].items():
        if int(key) == id:
            session['shoppingcart'].pop(key, None)
            flash(" Item is deleted ")
            return redirect(url_for('orders.getcart'))
        
@orders_bp.route('/order-history/<int:id>')
def orderdetails(id):
    orders = OrderProduct.query.filter_by(order_id=id)
    return render_template("pages/order_detail.html", orders=orders)
