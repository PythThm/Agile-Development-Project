from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import current_user, login_required
from db import db 
from models import User, OrderHistory

users_bp = Blueprint("users", __name__)

# List users
@users_bp.route('/')
def users():
    users = User.query.all()
    return render_template('admin/customers.html', users=users)

# List a user
@users_bp.route('/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('pages/customer_detail.html', user=user)

# Update user
@users_bp.route("/update/<int:user_id>", methods=["GET", "POST"])
def update_user(user_id):

    user = db.get_or_404(User, user_id)
 
    if request.method == 'POST':
        user.name = request.form['name']
        user.phone = request.form['phone']
        user.email = request.form['email']
        user.password = request.form['password']

        db.session.commit()

        return redirect(url_for("users.profile"))
    
    else:
        return render_template('pages/profile_update.html', user = user)

# Delete Customer
@users_bp.route("/<int:user_id>/delete")
def user_delete(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("users.users"))

# Image testing
# http://localhost:8888/users/imagetesting
@users_bp.route('/imagetesting')
def upload():
    return render_template('imagetesting.html')

# Profile
@users_bp.route('/profile')
@login_required
def profile():

    histories = OrderHistory.query.filter_by(user_email=current_user.email)
    return render_template('pages/profile.html', user=current_user, histories=histories)