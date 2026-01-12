"""
Konfigurasi aplikasi
"""
import os
from datetime import timedelta

class Config:
    """Konfigurasi dasar aplikasi"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Demo Mode (untuk melihat tampilan tanpa database)
    DEMO_MODE = os.environ.get('DEMO_MODE', 'false').lower() in ['true', '1', 'yes']
    
    # SQL Server Database
    # Membuat DATABASE_URL dari environment variables jika tidak ada
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if not DATABASE_URL:
        SQL_SERVER = os.environ.get('SQL_SERVER', 'localhost')
        DATABASE_NAME = os.environ.get('DATABASE_NAME', 'AbsensiDB')
        SQL_USERNAME = os.environ.get('SQL_USERNAME', 'sa')
        SQL_PASSWORD = os.environ.get('SQL_PASSWORD', '')
        USE_WINDOWS_AUTH = os.environ.get('USE_WINDOWS_AUTH', 'true').lower() in ['true', '1', 'yes']
        
        if USE_WINDOWS_AUTH:
            # Windows Authentication
            DATABASE_URL = f'mssql+pyodbc://{SQL_SERVER}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server&trusted_connection=yes'
        else:
            # SQL Server Authentication
            DATABASE_URL = f'mssql+pyodbc://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_SERVER}/{DATABASE_NAME}?driver=ODBC+Driver+17+for+SQL+Server'
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(hours=8)
    
    # Presensi Settings
    CHECK_IN_START = '07:00'  # Jam mulai check-in
    CHECK_IN_END = '09:00'    # Jam akhir check-in
    CHECK_OUT_START = '16:00' # Jam mulai check-out
    CHECK_OUT_END = '18:00'   # Jam akhir check-out
    
    # Geolocation Settings
    OFFICE_LATITUDE = -6.2088  # Contoh koordinat Jakarta
    OFFICE_LONGITUDE = 106.8456
    GEO_RADIUS_METERS = 100  # Radius dalam meter
    
    # Upload Settings
    UPLOAD_FOLDER = 'uploads'
    MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'}
    
    # Email Settings (opsional)
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
