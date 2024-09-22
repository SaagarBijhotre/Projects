# query_users.py
from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Query all users
    users = User.query.all()
    
    # Print each user's information
    for user in users:
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Bio: {user.bio}")
