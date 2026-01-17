"""
Model Office untuk data lokasi kantor
"""
from datetime import datetime
from models import db

class Office(db.Model):
    """Model untuk data lokasi kantor"""
    __tablename__ = 'offices'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # Nama kantor
    address = db.Column(db.String(255), nullable=True)  # Alamat lengkap
    latitude = db.Column(db.Float, nullable=False)  # Koordinat latitude
    longitude = db.Column(db.Float, nullable=False)  # Koordinat longitude
    radius_meters = db.Column(db.Integer, nullable=False, default=100)  # Radius dalam meter
    is_active = db.Column(db.Boolean, default=True)  # Status aktif/nonaktif
    description = db.Column(db.Text, nullable=True)  # Deskripsi kantor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'radius_meters': self.radius_meters,
            'is_active': self.is_active,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Office {self.name}>'
