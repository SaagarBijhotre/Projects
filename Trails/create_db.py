from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    # Query all users
    users = User.query.all()

    if users:
        print("Users in the database:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}")
    else:
        print("No users found.")
