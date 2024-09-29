from app import create_app, db
from app.models import Trail

def view_trails():
    app = create_app()
    with app.app_context():
        # Query all trails
        trails = Trail.query.all()

        # Print each trail
        if trails:
            for trail in trails:
                print(f"Name: {trail.name}, Location: {trail.location}, Distance: {trail.distance} km, "
                      f"Scenery: {trail.scenery}, Amenities: {trail.amenities}, "
                      f"Latitude: {trail.latitude}, Longitude: {trail.longitude}")
        else:
            print("No trails found in the database.")

if __name__ == '__main__':
    view_trails()
