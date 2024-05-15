from flask import Blueprint, render_template, redirect, url_for, request
from routes import api_orders
from models import Category
from db import db

admin_bp = Blueprint("admin", __name__)

@admin_bp.route('/')
def admin():
    return render_template('admin/dashboard.html')

@admin_bp.route('/stats')
def stats():
    def get_stats(route, timeframe):
        response = route()
        data = response.get_json()
        return data[timeframe]
    
    daily = get_stats(api_orders.daily, 'dailysales')
    yearly = get_stats(api_orders.yearly, 'yearlysales')
    total = get_stats(api_orders.total, 'totalsales')
    return render_template('admin/stats.html', daily=daily, yearly=yearly, total=total)

# Get All Categories
@admin_bp.route('/category')
def category():
        categories = Category.query.all()

        return render_template('admin/category.html', categories = categories)


# Create Category
@admin_bp.route('/addcategory', methods=['GET', 'POST'])
def addcategory():
    if request.method=='POST':
        getCategory = request.form.get('category')
        category = Category(name=getCategory)
        db.session.add(category)
        db.session.commit()

        return redirect(url_for('admin.addcategory'))
    
    return redirect(url_for('admin.category'))



# Update Category
@admin_bp.route('/update-category/<int:id>', methods=['GET', 'POST'])
def updatecategory(id):
 
    updatecategory = Category.query.get_or_404(id)
    category = request.form.get('category')

    if request.method == 'POST':
        updatecategory.name = category
        db.session.commit()
        return redirect(url_for('admin.category'))
    
    return render_template('admin/updatecat.html', updatecategory=updatecategory)


# Delete Category

@admin_bp.route('/delete-category/<int:id>')
def deletecategory(id):

    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
   
    return redirect(url_for('admin.category'))