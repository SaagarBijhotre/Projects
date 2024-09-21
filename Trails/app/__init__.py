# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Initialize extensions without importing models yet
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    # Register blueprints before importing models
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    # Import models after db and app are fully initialized
    with app.app_context():
        from app.models import User  # Import here to avoid circular import
        db.create_all()  # Create database tables

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User  # Import User here to avoid circular import
    return User.query.get(int(user_id))
