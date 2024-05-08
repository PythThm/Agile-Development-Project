from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import db 
from models import Product, Category
from config import photos
import secrets

products_bp = Blueprint("products", __name__)

# list products
@products_bp.route("/")
def products():
    products = Product.query.all()
    categories = Category.query.all()
    return render_template('pages/products.html', products=products, categories=categories)

@products_bp.route('/<productname>')
def product_detail(productname):
    product = db.one_or_404(db.select(Product).filter_by(name=productname))
    return render_template('pages/product_detail.html', product=product)


# Update product
@products_bp.route("/<int:product_id>", methods=["GET", "POST"])
def update_product(product_id):

    product = db.get_or_404(Product, product_id)
 
    if request.method == 'POST':
        product.name = request.form['name']
        product.price =request.form['price']
        product.available = request.form['available']
        
        db.session.commit()
        return redirect(url_for("admin.admin"))
    else:
        product = Product.to_json(product)
        return render_template('admin/product_update.html', product = product )

# Delete product
@products_bp.route("/<int:product_id>/delete")
def delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("admin.admin"))

@products_bp.route('/category/<int:id>')
def getcategory(id):
    categories = Category.query.all()
    category_items = Product.query.filter_by(category_id=id)
    return render_template('pages/products.html', categories=categories, category_items=category_items)

@products_bp.route('/product/<int:id>')
def productdetail(id):
    product = Product.query.get_or_404(id)
    categories = Category.query.all()
    return render_template('pages/product_detail.html', product=product, categories=categories)