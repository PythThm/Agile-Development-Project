from flask import Blueprint, render_template
from routes import api_orders
from models import Category

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

