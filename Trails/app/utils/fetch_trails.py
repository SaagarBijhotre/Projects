import sys
import os
import requests
import math
import subprocess
import json  # To handle GeoJSON data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from app import create_app, db
from app.models import Trail
from shapely.geometry import LineString, Point, mapping
from shapely.ops import split

def find_intersections(trails):
    """
    Identify intersections between trails and split them into segments.
    :param trails: List of LineStrings representing trails
    :return: List of trail segments
    """
    trail_segments = []
    for i, trail_a in enumerate(trails):
        for j, trail_b in enumerate(trails):
            if i != j:
                # Find the intersection points
                if trail_a.intersects(trail_b):
                    intersection_point = trail_a.intersection(trail_b)
                    if isinstance(intersection_point, Point):
                        # Split trails at the intersection
                        split_trail = split(trail_a, intersection_point)
                        trail_segments.extend(split_trail)
                    else:
                        trail_segments.append(trail_a)
    return trail_segments

def calculate_distance(trail_segment):
    """
    Calculate the total distance of a trail segment.
    :param trail_segment: A LineString representing the trail segment.
    :return: The distance in kilometers.
    """
    return trail_segment.length * 100  # Convert to kilometers

def process_trails(geojson_data):
    """
    Process the GeoJSON data and extract trails, segment them, and calculate distances.
    :param geojson_data: GeoJSON data of trails
    :return: List of trail segments with distances
    """
    trails = []
    
    # Convert GeoJSON trails to LineStrings
    for feature in geojson_data['features']:
        if feature['geometry']['type'] == 'LineString':
            coordinates = feature['geometry']['coordinates']
            line = LineString(coordinates)
            trails.append(line)
    
    # Find and segment trails at intersections
    trail_segments = find_intersections(trails)
    
    # Calculate distance for each segment
    trail_data = []
    for segment in trail_segments:
        distance = calculate_distance(segment)
        trail_data.append({
            'segment': mapping(segment),
            'distance': distance
        })
    
    return trail_data

def store_segments_in_db(trail_data):
    """
    Store the trail segments with distances in the database.
    :param trail_data: List of trail segments with distance.
    """
    for trail_segment in trail_data:
        new_trail = Trail(
            name="Segmented Trail",
            location="Dallas",
            distance=trail_segment['distance'],
            latitude=trail_segment['segment']['coordinates'][0][1],  # Start latitude
            longitude=trail_segment['segment']['coordinates'][0][0],  # Start longitude
            user_id=1  # Default user
        )
        db.session.add(new_trail)
    db.session.commit()
    print("Trail segments stored in the database.")

def load_geojson(filepath):
    """
    Load the GeoJSON file from disk.
    :param filepath: Path to the GeoJSON file.
    :return: Parsed GeoJSON data.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def fetch_trails_from_osm_tile(lng, lat, tile_dim=2):
    """
    Fetch hiking trails from OpenStreetMap's Overpass API within a 2x2 degree tile.
    
    :param lng: Longitude of the tile's lower-left corner.
    :param lat: Latitude of the tile's lower-left corner.
    :param tile_dim: Dimension of the tile (default 2 degrees).
    :return: OSM data in .osm format.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    bbox = f"{lat},{lng},{lat + tile_dim},{lng + tile_dim}"  # Adjust bbox format (lat, lon, lat_max, lon_max)

    overpass_query = f"""
    [out:xml][timeout:25];
    (
      way["highway"="path"]({bbox});
      way["highway"="track"]({bbox});
      way["highway"="footway"]({bbox});
      way["route"="hiking"]({bbox});
    );
    out body;
    """

    response = requests.get(overpass_url, params={'data': overpass_query})
    
    if response.status_code == 200:
        return response.text  # Return .osm data in text format
    else:
        print(f"Error fetching data for tile {lng}, {lat}: {response.status_code}")
        return None


def save_osm_data(osm_data, lng, lat):
    """
    Save the fetched OSM data to a .osm file.
    
    :param osm_data: OSM data as text.
    :param lng: Longitude of the tile's lower-left corner (used in the filename).
    :param lat: Latitude of the tile's lower-left corner (used in the filename).
    """
    filename = f"osm_tile_{lat}_{lng}.osm"
    filepath = os.path.join("osm_data", filename)
    
    if not os.path.exists("osm_data"):
        os.makedirs("osm_data")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(osm_data)
    
    print(f"Saved OSM data to {filepath}")
    return filepath  # Return the file path to be used for conversion

def convert_to_geojson(osm_filepath, lng, lat):
    """
    Convert .osm file to .geojson format using the osmtogeojson CLI.
    
    :param osm_filepath: Path to the .osm file.
    :param lng: Longitude of the tile's lower-left corner (used in the filename).
    :param lat: Latitude of the tile's lower-left corner (used in the filename).
    """
    geojson_filename = f"geojson_tile_{lat}_{lng}.geojson"
    geojson_filepath = os.path.join("geojson_data", geojson_filename)

    if not os.path.exists("geojson_data"):
        os.makedirs("geojson_data")

    try:
        subprocess.run(f"osmtogeojson {osm_filepath} > {geojson_filepath}", shell=True, check=True)
        print(f"Converted and saved GeoJSON to {geojson_filepath}")
    except subprocess.CalledProcessError:
        print("Error: Could not process the .osm data with osmtogeojson CLI.")
    
    return geojson_filepath

def main():
    app = create_app()
    with app.app_context():
        # Define the latitude and longitude range (in 2x2 degree tiles)
        lat_min, lat_max = 32.6, 33.1  # Dallas area latitude range
        lng_min, lng_max = -97.0, -96.4  # Dallas area longitude range
        tile_dim = 2  # Tile dimension (2x2 degree)
        
        # Loop through the bounding box in 2x2 degree tiles
        for lat in range(math.floor(lat_min), math.ceil(lat_max), tile_dim):
            for lng in range(math.floor(lng_min), math.ceil(lng_max), tile_dim):
                # Fetch OSM data for the current tile
                osm_data = fetch_trails_from_osm_tile(lng, lat, tile_dim)
                
                if osm_data:
                    # Save the fetched OSM data to a file
                    osm_filepath = save_osm_data(osm_data, lng, lat)
                    
                    # Convert the .osm file to .geojson using the CLI tool
                    geojson_filepath = convert_to_geojson(osm_filepath, lng, lat)

                    # Load the generated GeoJSON file
                    geojson_data = load_geojson(geojson_filepath)

                    # Process the GeoJSON trails and extract trail segments
                    trail_data = process_trails(geojson_data)

                    # Store the trail segments in the database
                    store_segments_in_db(trail_data)

if __name__ == "__main__":
    main()
