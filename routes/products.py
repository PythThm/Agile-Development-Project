from flask import Blueprint, render_template,request, redirect, url_for
from db import db 
from models import Product

products_bp = Blueprint("products", __name__)

# list products
@products_bp.route("/")
def products():
    products = Product.query.all()
    return render_template('pages/products.html', products=products)

@products_bp.route('/<productname>')
def product_detail(productname):
    product = db.one_or_404(db.select(Product).filter_by(name=productname))
    return render_template('pages/product_detail.html', product=product)

# create product
@products_bp.route("/", methods=['GET', 'POST'])
def products_list():
    if request.method == 'POST':

        name = request.form['name']
        price =request.form['price']
        new_product = Product(name=name, price=price)

        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for("products.products_list"))
    
    else:
        statement = db.select(Product).order_by(Product.id)
        results = db.session.execute(statement)
        products = []
        for product in results.scalars():
            json_record = Product.to_json(product)
            products.append(json_record)

        return render_template("products.html", products = products)

# Update product
@products_bp.route("/<int:product_id>", methods=["GET", "POST"])
def update_product(product_id):

    product = db.get_or_404(Product, product_id)
 
    if request.method == 'POST':
        product.name = request.form['name']
        product.price =request.form['price']
        product.available = request.form['available']
        
        db.session.commit()
        return redirect(url_for("products.products_list"))
    else:
        product = Product.to_json(product)
        return render_template('pages/product_update.html', product = product )

# Delete product
@products_bp.route("/<int:product_id>/delete")
def delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("products.products"))
