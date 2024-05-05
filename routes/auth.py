from flask import Blueprint, render_template, redirect, url_for, request, flash
from db import db
from models import User, Order, Product, ProductOrder
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("html", __name__)

# Login
@auth.route('/login')
def login():
    return render_template('login.html')

# Signup
@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth_blueprint.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth_blueprint.login'))


# Logout
@auth.route('/logout')
def logout():
    return render_template('logout.html')
