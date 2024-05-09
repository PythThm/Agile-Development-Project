from flask import Blueprint, redirect, url_for, render_template, request, session
from db import db 
from models import Order, Product, Category
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
    return render_template('/pages/success.html')

@orders_bp.route('/failure')
def failure():
    return render_template('/pages/failure.html')


# Add items to shopping cart
# reference
# https://youtu.be/nBAxuxM9tpw?si=jMr1qwNgsC7-9l4Q

def mergeDicts(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    else:
        False

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
                print("Already in your Cart")
            else:
                session['shoppingcart'] = mergeDicts(session['shoppingcart'], cartItems)
                return redirect(request.referrer)
        
        else:
            session['shoppingcart'] = cartItems
            return redirect(request.referrer)
        

    return redirect(request.referrer)


@orders_bp.route('/cart')
def getcart():
    if 'shoppingcart' not in session:
        return redirect(request.referrer)
    subtotal = 0
    estimated = 0
    for key, product in session['shoppingcart'].items():
        subtotal += float(product['price'] * int(product['quantity']))
        tax = ("%.2f" % (0.06 * float(subtotal)))
        estimated = float("%.2f" % (1.06 * subtotal))

    return render_template('pages/cart.html', tax = tax, estimated = estimated)


@orders_bp.route('/category/<int:id>')
def getcategory(id):
    categories = Category.query.all()
    category_items = Product.query.filter_by(category_id=id)
    return render_template('pages/products.html', categories=categories, category_items=category_items)


@orders_bp.route('/addcategory', methods=['GET', 'POST'])
def addcategory():

    if request.method=='POST':
        getCategory = request.form.get('category')
        category = Category(name=getCategory)
        db.session.add(category)
        db.session.commit()
    
        return redirect(url_for('admin.addcategory'))
    
    return render_template('admin/additem.html')

@orders_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):

    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecategory.name = category
        db.session.commit()
        return redirect(url_for('admin.category'))
    return render_template('admin/updatecat.html', updatecategory=updatecategory)


@orders_bp.route('/deletecat/<int:id>')
def deletecategory(id):

    category = Category.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()

    return redirect(url_for('admin.category'))