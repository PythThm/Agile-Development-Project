from flask import Blueprint, render_template, session, redirect, url_for, request, current_app
from models import Product, Category
from db import db
from pathlib import Path
import secrets
from config import photos

admin_bp = Blueprint("admin", __name__)


# @admin_bp.route('/')
# def admin():
#         products = Product.query.all()
#         return render_template('admin/products.html', products = products)

@admin_bp.route('/admin')
def admin():
        products = Product.query.all()
        return render_template('admin/products.html', products = products)
    
@admin_bp.route('/category')
def category():
        categories = Category.query.all()
        return render_template('admin/category.html', categories = categories)

# @admin_bp.route('/addcategory', methods=['GET', 'POST'])
# def addcategory():
#     if 'email' not in session:
        
#         return redirect(url_for('login'))
    
#     if request.method=='POST':
#         getCategory = request.form.get('category')
#         category = Category(name=getCategory)
#         db.session.add(category)
#         db.session.commit()
       
#         return redirect(url_for('addcategory'))
    
#     return render_template('admin/additem.html')

# create product
@admin_bp.route('/additem', methods=['GET', 'POST'])
def additem():
    if request.method=='POST':

        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']
        description = request.form['description']
        category_id = request.form['category']
        photo = photos.save(request.files['item-photo'], name=secrets.token_hex(10) + ".")

        item = Product(name=name, price=float(price), available=quantity, description=description, category_id=category_id, photo=photo)     

        db.session.add(item)
        db.session.commit()
  
        return redirect(url_for('admin.additem'))
    
    categories = Category.query.all()
    return render_template('admin/additem.html', items='items', categories=categories)    

# Create Category
@admin_bp.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if request.method=='POST':
        getCategory = request.form.get('category')
        category = Category(name=getCategory)
        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.addcategory'))
    
    return render_template('admin/additem.html')


@admin_bp.route('/update/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
    if 'email' not in session:
       
        return redirect(url_for('login'))
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')
    if request.method == 'POST':
        updatecategory.name = category
        db.session.commit()
        return redirect(url_for('category'))
    return render_template('admin/updatecat.html', updatecategory=updatecategory)


@admin_bp.route('/deletecat/<int:id>')
def deletecategory(id):

    category = Category.query.get_or_404(id)

    db.session.delete(category)
    db.session.commit()
   
    return redirect(url_for('admin.category'))
    

@admin_bp.route('/updateitem/<int:id>', methods=['GET', 'POST'])
def updateitem(id):
    
    categories = Category.query.all()
    product = Product.query.get_or_404(id)
    
    name = request.form.get('name')
    price = request.form.get('price')
    quantity =request.form.get('quantity')
    description = request.form.get('description')
    category_id = request.form.get('category')
    photo = request.files.get('item-photo')

    if request.method == 'POST':
        product.name = name
        product.price = price
        product.quantity = quantity
        product.description = description
        product.category_id = category_id
        if photo :
            try:
                Path(current_app.root_path, "static", "img", product.photo).unlink()
                product.photo = photos.save(request.files.get('item-photo'), name=secrets.token_hex(10) + ".")
            except:
                product.photo = photos.save(request.files.get('item-photo'), name=secrets.token_hex(10) + ".")

        db.session.commit()

        return redirect(url_for('admin'))
        
    return render_template('admin/updateitem.html', categories=categories, product=product)
    


@admin_bp.route('/deleteitem/<int:id>')
def deleteitem(id):

    item = Product.query.get_or_404(id)

    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('admin'))