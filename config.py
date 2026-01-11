"""
Konfigurasi aplikasi
"""
import os
from datetime import timedelta

class Config:
    """Konfigurasi dasar aplikasi"""
    # Flask
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # SQL Server Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mssql+pyodbc://username:password@localhost/dbname?driver=ODBC+Driver+17+for+SQL+Server'
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
