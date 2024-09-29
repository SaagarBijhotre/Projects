from app import create_app, db
from app.models import User,Trail

app = create_app()

def initialize_database():

    with app.app_context():
        db.create_all()
        print("database initialized")

if __name__ =='__main__':
    initialize_database()

