from flask import Blueprint, render_template, redirect, url_for, request, flash
from db import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = True if request.form.get('remember') else False

        # Retrieve the user based on the provided email
        user = User.query.filter_by(email=email).first()

        # Check if a user with the provided email exists
        if not user:
            logout_user()
            flash('User with this email does not exist.')
            return redirect(url_for('auth.login'))

        # Check if the password is correct
        if not check_password_hash(user.password, password) or user is None:
            logout_user()
            flash('Please check your login details and try again.')
            return redirect(url_for('auth.login'))

        # Check if the user is an admin
        if user.is_admin:
            # Log in the admin user
            login_user(user, remember=remember)
            return redirect(url_for('admin.admin'))

        # Log in the regular user
        login_user(user, remember=remember)
        return redirect(url_for('home'))

    return render_template('auth/login.html')

# Signup
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')
        print(email)
        user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

        if user is not None: # if a user is found, we want to redirect back to signup page so user can try again
            logout_user()
            flash('Email address already exists')
            return redirect(url_for('auth.signup'))

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

        # add the new user to the database
        db.session.add(new_user)
        
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('auth.login'))
    
    return render_template('auth/signup.html')


# Logout
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template('index.html')
