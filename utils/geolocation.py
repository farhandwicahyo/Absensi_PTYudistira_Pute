"""
Utility untuk validasi geolocation
"""
from math import radians, cos, sin, asin, sqrt
from config import Config

def calculate_distance(lat1, lon1, lat2, lon2):
    """
    Menghitung jarak antara dua koordinat menggunakan formula Haversine
    Returns: jarak dalam meter
    """
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000  # Radius bumi dalam meter
    
    return c * r

def validate_location(latitude, longitude):
    """
    Validasi apakah lokasi berada dalam radius yang diizinkan
    Returns: (is_valid, distance_in_meters)
    """
    distance = calculate_distance(
        Config.OFFICE_LATITUDE,
        Config.OFFICE_LONGITUDE,
        latitude,
        longitude
    )
    
    is_valid = distance <= Config.GEO_RADIUS_METERS
    return is_valid, distance
