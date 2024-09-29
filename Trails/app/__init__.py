from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'main.login'
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__,
                static_folder='../static',  # Point to the static folder outside app
                template_folder='../templates')  # Point to the templates folder outside app

    class Config:
        SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost/db_name'
        SQLALCHEMY_TRACK_MODIFICATIONS = False


    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.routes import main_routes
    app.register_blueprint(main_routes)

    # Create database tables if not exist
    with app.app_context():
        from app.models import User
        db.create_all()

    return app

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))
