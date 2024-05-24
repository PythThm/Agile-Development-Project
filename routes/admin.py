from flask import Blueprint, render_template, redirect, url_for, request
from routes import api_orders
from models import Category, Issue, User, Product
from db import db

admin_bp = Blueprint("admin", __name__)

#function to get stats
def get_stats(route, timeframe):
    response = route()
    data = response.get_json()
    return data[timeframe]

@admin_bp.route('/')
def admin():
    users = User.query.order_by(User.id.desc()).limit(3).all()
    products = Product.query.order_by(Product.id.desc()).limit(3).all()
    issues = Issue.query.order_by(Issue.id.desc()).limit(3).all()

    daily = get_stats(api_orders.daily, 'dailysales')
    yearly = get_stats(api_orders.yearly, 'yearlysales')
    total = get_stats(api_orders.total, 'totalsales')
    monthly = get_stats(api_orders.monthly, 'monthlysales')
    
    return render_template('admin/dashboard.html', users=users, products=products, issues=issues, daily=daily, yearly=yearly, total=total, monthly=monthly)

@admin_bp.route('/stats')
def stats():
    # def get_stats(route, timeframe):
    #     response = route()
    #     data = response.get_json()
    #     return data[timeframe]
    
    daily = get_stats(api_orders.daily, 'dailysales')
    yearly = get_stats(api_orders.yearly, 'yearlysales')
    total = get_stats(api_orders.total, 'totalsales')
    monthly = get_stats(api_orders.monthly, 'monthlysales')
    return render_template('admin/stats.html', daily=daily, yearly=yearly, total=total, monthly=monthly)

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

# admin support pages

@admin_bp.route('/view_issues')
# @login_required
def view_issues():
    issues = Issue.query.all()
    return render_template('admin/customer_issues.html', issues=issues)

@admin_bp.route('/<int:issue_id>')
def issue_detail(issue_id):
    issue = db.one_or_404(db.select(Issue).filter_by(id=issue_id))
    return render_template('admin/issue_details.html', issue=issue)

@admin_bp.route("/<int:issue_id>/delete")
def delete_product(issue_id):
    issue = db.get_or_404(Issue, issue_id)
    db.session.delete(issue)
    db.session.commit()
    return redirect(url_for("admin.view_issues"))