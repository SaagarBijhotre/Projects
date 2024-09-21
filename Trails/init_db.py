# init_db.py
from app import create_app, db
from flask import Flask

# Create the app instance
app = create_app()

# Create all the tables
with app.app_context():
    db.create_all()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)

    print(app.jinja_loader.searchpath)  # Print the template search paths

    with app.app_context():
        db.create_all()

    return app
