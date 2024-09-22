from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User
from app.forms import RegistrationForm, LoginForm
from app import db, bcrypt

# Create a blueprint for the routes
main_routes = Blueprint('main', __name__)

# Home Route
@main_routes.route('/')
def home():
    return render_template('home.html')  # Home page

# Signup Route
@main_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('main.login'))

    return render_template('signup.html', form=form)

# Login Route with Debugging
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()

    # Debugging statements to trace the login flow
    if form.validate_on_submit():
        print("Form validated successfully.")
        user = User.query.filter_by(email=form.email.data).first()
        print(f"User found: {user}")
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            print("Password matched.")
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
            print("Login failed. Incorrect credentials.")
    
    # Print form errors if there are any
    if form.errors:
        print(f"Form errors: {form.errors}")

    return render_template('login.html', form=form)

# Logout Route
@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('main.home'))

# Profile Route
@main_routes.route('/profile')
@login_required  # Ensure only logged-in users can access this
def profile():
    return render_template('profile.html')  # Render profile page

# Trails Route
@main_routes.route('/trails')
def trails():
    return render_template('trails.html')  # Render trails page

# Route to search for trails (placeholder)
@main_routes.route('/search', methods=['GET'])
def search_trails():
    query = request.args.get('query', '').lower()
    results = [
        {'name': 'Sunny Trail', 'difficulty': 'Easy'},
        {'name': 'Mountain Path', 'difficulty': 'Moderate'},
        {'name': 'Forest Walk', 'difficulty': 'Hard'}
    ]
    matching_results = [trail for trail in results if query in trail['name'].lower()]
    return jsonify(matching_results)
