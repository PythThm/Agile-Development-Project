from flask import Blueprint, render_template
from db import db 
from models import User

users_bp = Blueprint("users", __name__)

@users_bp.route('/')
def users():
    customers = User.query.all()
    return render_template('pages/customers.html', customers=customers)

@users_bp.route('/customers/<int:customer_id>')
def customer_detail(customer_id):
    user = User.query.get_or_404(customer_id)
    return render_template('pages/customer_detail.html', user=user)

@users_bp.route('/profile')
def profile():
    return render_template('pages/profile.html')

# Image testing
@users_bp.route('/imagetesting')
def upload():
    return render_template('imagetesting.html')