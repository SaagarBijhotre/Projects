from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from app.models import User, Trail  # Import the Trail model
from app.forms import RegistrationForm, LoginForm, TrailSubmissionForm  # Import the TrailSubmissionForm
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

# Login Route
@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')

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

# Trails Route to display all trails
@main_routes.route('/trails')
def trails():
    trails = Trail.query.all()  # Fetch all trails from the database
    return render_template('trails.html', trails=trails)  # Render trails page with all trails

# Route to submit a new trail
@main_routes.route('/submit-trail', methods=['GET', 'POST'])
@login_required
def submit_trail():
    form = TrailSubmissionForm()
    if form.validate_on_submit():
        # Convert distance to kilometers if necessary
        distance_km = form.distance.data
        if form.distance_unit.data == 'miles':
            distance_km = form.distance.data * 1.60934  # Convert miles to kilometers

        # Create a new trail object
        new_trail = Trail(
            name=form.name.data,
            location=form.location.data,
            distance=distance_km,
            scenery=form.scenery.data,
            amenities=form.amenities.data,
            creator=current_user
        )
        db.session.add(new_trail)
        db.session.commit()
        flash('Trail submitted successfully!', 'success')
        return redirect(url_for('main.trails'))
    
    return render_template('submit_trail.html', form=form)

# Route to search for trails based on scenery and amenities
@main_routes.route('/search', methods=['GET'])
def search_trails():
    scenery_query = request.args.get('scenery', '').lower()
    amenities_query = request.args.get('amenities', '').lower()

    # Filter trails based on scenery and amenities
    filtered_trails = Trail.query.filter(
        Trail.scenery.contains(scenery_query),
        Trail.amenities.contains(amenities_query)
    ).all()

    # Return filtered results as JSON
    return jsonify([{
        'name': trail.name,
        'location': trail.location,
        'distance': trail.distance,
        'scenery': trail.scenery,
        'amenities': trail.amenities,
        'latitude': trail.latitude,
        'longitude': trail.longitude
    } for trail in filtered_trails])

# Route to add a new trail manually (can also be part of the submit-trail route)
@main_routes.route('/add-trail', methods=['GET', 'POST'])
@login_required  # Only logged-in users can add trails
def add_trail():
    form = TrailSubmissionForm()
    if form.validate_on_submit():
        # Convert distance to kilometers if necessary
        distance_km = form.distance.data
        if form.distance_unit.data == 'miles':
            distance_km *= 1.60934  # Convert miles to kilometers

        # Save trail to the database
        new_trail = Trail(
            name=form.name.data,
            location=form.location.data,
            distance=distance_km,
            scenery=form.scenery.data,
            amenities=form.amenities.data,
            creator=current_user
        )
        db.session.add(new_trail)
        db.session.commit()
        flash('Trail added successfully!', 'success')
        return redirect(url_for('main.trails'))
    
    return render_template('submit_trail.html', form=form)
