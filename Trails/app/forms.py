from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectMultipleField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo

# Choices for scenery and nearby amenities
SCENERY_CHOICES = [
    ('forest', 'Forest'),
    ('lake', 'Lake'),
    ('mountain', 'Mountain'),
    ('urban', 'Urban'),
    ('river', 'River'),
]

AMENITIES_CHOICES = [
    ('restrooms', 'Restrooms'),
    ('water_stations', 'Water Stations'),
    ('parking', 'Parking'),
    ('benches', 'Benches'),
]

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class TrailSubmissionForm(FlaskForm):
    name = StringField('Trail Name', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    distance = FloatField('Distance', validators=[DataRequired()])
    distance_unit = SelectField('Unit', choices=[('km', 'Kilometers'), ('miles', 'Miles')], validators=[DataRequired()])
    scenery = SelectMultipleField('Scenery', choices=[('mountains', 'Mountains'), ('forest', 'Forest'), ('lake', 'Lake'), ('city', 'City')])
    amenities = SelectMultipleField('Nearby Amenities', choices=[('restrooms', 'Restrooms'), ('water', 'Water fountains'), ('parking', 'Parking'), ('cafe', 'Café')])
    submit = SubmitField('Submit Trail')