from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_user, current_user, login_required, logout_user
from app.forms import LoginForm, RegistrationForm
from app.models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash

# Define auth blueprint
auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():
    # if current_user.is_authenticated:
    #     flash('You are already logged in!', 'success')
    #     return redirect(url_for('main.dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists. Please use a different email address.', 'error')
            return redirect(url_for('auth.register'))

        if User.query.filter_by(user_name=form.user_name.data).first():
            flash('Username already exists. Please use a different username.', 'error')
            return redirect(url_for('auth.register'))
        
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(email=form.email.data, user_name=form.user_name.data, password=hashed_password,
                        role=form.role.data,
            department=form.department.data,
            institution=form.institution.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('register.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    # if current_user.is_authenticated:
    #     flash('You are already logged in!', 'success')
    #     return redirect(url_for('main.dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.email == form.email_or_username.data) |
                                 (User.user_name == form.email_or_username.data)).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.dashboard'))
        flash('Login failed. Please check your email/username and password.', 'error')
    
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.home'))
