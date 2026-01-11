"""
Model Employee untuk data karyawan
"""
from datetime import datetime
from models import db

class Employee(db.Model):
    """Model untuk data karyawan"""
    __tablename__ = 'employees'
    
    id = db.Column(db.Integer, primary_key=True)
    nik = db.Column(db.String(20), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    position = db.Column(db.String(50), nullable=False)  # Jabatan
    division = db.Column(db.String(50), nullable=False)  # Divisi
    supervisor_id = db.Column(db.Integer, db.ForeignKey('employees.id'), nullable=True)  # Atasan langsung
    status = db.Column(db.String(20), default='aktif')  # aktif, nonaktif
    hire_date = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    supervisor = db.relationship('Employee', remote_side=[id], backref='subordinates')
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'nik': self.nik,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone,
            'position': self.position,
            'division': self.division,
            'supervisor_id': self.supervisor_id,
            'supervisor_name': self.supervisor.full_name if self.supervisor else None,
            'status': self.status,
            'hire_date': self.hire_date.isoformat() if self.hire_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
