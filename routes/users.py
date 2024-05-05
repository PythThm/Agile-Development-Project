from flask import Blueprint, render_template, request, redirect, url_for
from db import db 
from models import User

users_bp = Blueprint("users", __name__)

# List users
@users_bp.route('/')
def users():
    users = User.query.all()
    return render_template('pages/customers.html', users=users)

# List user
@users_bp.route('/<int:user_id>')
def user_detail(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('pages/customer_detail.html', user=user)

@users_bp.route('/profile')
def profile():
    return render_template('pages/profile.html')

# Update user
@users_bp.route("/<int:user_id>/update", methods=["GET", "POST"])
def update_user(user_id):

    user = db.get_or_404(User, user_id)
 
    if request.method == 'POST':
        user.name = request.form['name']
        user.phone = request.form['phone']
        user.email = request.form['email']
        user.password = request.form['password']

        db.session.commit()
        return redirect(url_for("users.users"))
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