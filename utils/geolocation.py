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

def validate_location(latitude, longitude, office_id=None):
    """
    Validasi apakah lokasi berada dalam radius yang diizinkan
    Mendukung multiple kantor dari database, fallback ke config jika tidak ada kantor di database
    
    Args:
        latitude: Latitude lokasi user
        longitude: Longitude lokasi user
        office_id: ID kantor spesifik (optional), jika None akan cek semua kantor aktif
    
    Returns: (is_valid, distance_in_meters, office_name)
    """
    try:
        # Coba ambil dari database dulu
        from models.office import Office
        
        if office_id:
            # Validasi untuk kantor spesifik
            office = Office.query.filter_by(id=office_id, is_active=True).first()
            if office:
                distance = calculate_distance(
                    office.latitude,
                    office.longitude,
                    latitude,
                    longitude
                )
                is_valid = distance <= office.radius_meters
                return is_valid, distance, office.name
        
        # Cek semua kantor aktif
        offices = Office.query.filter_by(is_active=True).all()
        
        if offices:
            # Cek setiap kantor, return yang terdekat
            min_distance = float('inf')
            nearest_office = None
            
            for office in offices:
                distance = calculate_distance(
                    office.latitude,
                    office.longitude,
                    latitude,
                    longitude
                )
                
                if distance <= office.radius_meters:
                    # Lokasi valid untuk kantor ini
                    return True, distance, office.name
                
                # Simpan kantor terdekat
                if distance < min_distance:
                    min_distance = distance
                    nearest_office = office
            
            # Tidak ada kantor yang valid, return kantor terdekat
            if nearest_office:
                return False, min_distance, nearest_office.name
            else:
                return False, min_distance, None
        
    except Exception:
        # Jika ada error (misalnya tabel belum ada), fallback ke config
        pass
    
    # Fallback ke config lama (backward compatibility)
    distance = calculate_distance(
        Config.OFFICE_LATITUDE,
        Config.OFFICE_LONGITUDE,
        latitude,
        longitude
    )
    
    is_valid = distance <= Config.GEO_RADIUS_METERS
    return is_valid, distance, "Kantor Utama"
