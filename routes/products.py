from flask import Blueprint, render_template
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

