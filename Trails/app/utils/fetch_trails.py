import sys
import os
import requests
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import create_app, db
from app.models import Trail


def fetch_trails_from_osm(bbox):
    """
    Fetch trails from OpenStreetMap's Overpass API within the given bounding box.

    :param bbox: A tuple containing (south, west, north, east) latitude and longitude values.
    :return: A list of trails with their coordinates and properties.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    
    # Overpass API query to fetch hiking trails and related amenities
    overpass_query = f"""
    [out:json][timeout:25];
    (
      way["highway"="path"]["route"="hiking"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      node["amenity"="parking"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      node["amenity"="toilets"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
      node["amenity"="drinking_water"]({bbox[0]},{bbox[1]},{bbox[2]},{bbox[3]});
    );
    out body;
    >;
    out skel qt;
    """
    
    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        return response.json()  # Return JSON data with OSM features
    else:
        print(f"Error fetching data: {response.status_code}")
        return None

def parse_trails(osm_data):
    """
    Parse OSM data to extract trails and their coordinates.

    :param osm_data: JSON data returned by Overpass API.
    :return: A list of trails with names, coordinates, and other properties.
    """
    elements = osm_data.get('elements', [])
    nodes = {el['id']: el for el in elements if el['type'] == 'node'}
    
    trails = []
    
    for element in elements:
        if element['type'] == 'way' and 'tags' in element and element['tags'].get('highway') == 'path':
            trail_name = element['tags'].get('name', 'Unnamed Trail')
            trail_location = element['tags'].get('location', 'Unknown Location')
            trail_distance = element['tags'].get('distance', 0.0)  # You may need to calculate this
            trail_scenery = element['tags'].get('scenery', 'Various')
            trail_amenities = element['tags'].get('amenities', 'None')
            
            # Extract coordinates
            trail_coords = [(nodes[node_id]['lat'], nodes[node_id]['lon']) for node_id in element['nodes'] if node_id in nodes]
            
            # Calculate the center of the trail for map placement (average of coordinates)
            if trail_coords:
                avg_lat = sum(coord[0] for coord in trail_coords) / len(trail_coords)
                avg_lon = sum(coord[1] for coord in trail_coords) / len(trail_coords)
            else:
                avg_lat, avg_lon = 0.0, 0.0  # Default values if no coordinates
            
            trails.append({
                'name': trail_name,
                'location': trail_location,
                'distance': trail_distance,
                'scenery': trail_scenery,
                'amenities': trail_amenities,
                'latitude': avg_lat,
                'longitude': avg_lon,
                'coordinates': trail_coords
            })
    
    return trails

def store_trails(trails):
    """
    Store the fetched trails into the database.

    :param trails: A list of trail dictionaries.
    """
    for trail in trails:
        # Check if the trail already exists to prevent duplicates
        existing_trail = Trail.query.filter_by(name=trail['name'], location=trail['location']).first()
        if not existing_trail:
            new_trail = Trail(
                name=trail['name'],
                location=trail['location'],
                distance=trail['distance'],
                scenery=trail['scenery'],
                amenities=trail['amenities'],
                latitude=trail['latitude'],
                longitude=trail['longitude'],
                user_id=1  # Assign to a default user or handle appropriately
            )
            db.session.add(new_trail)
    db.session.commit()
    print("Trails have been added to the database.")

def main():
    app = create_app()
    with app.app_context():
        # Define your bounding box (south, west, north, east)
        # Example: Bounding box for London
        bbox_london = (51.28, -0.489, 51.686, 0.236)
        
        # Fetch trails data from OSM
        osm_data = fetch_trails_from_osm(bbox_london)
        
        if osm_data:
            # Parse the trails
            trails = parse_trails(osm_data)
            print(f"Fetched {len(trails)} trails from OSM.")
            
            # Store trails in the database
            store_trails(trails)

if __name__ == "__main__":
    main()
